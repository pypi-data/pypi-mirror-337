import pyarrow.dataset as ds
from pyarrow.fs import S3FileSystem
import pyarrow as pa
import pandas as pd
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from sovai.tools.authentication import authentication
import os
import datetime
import s3fs
import logging
from tqdm import tqdm

# -------------------------------
# Cached Filesystem Accessors
# -------------------------------

@lru_cache(maxsize=2)
def get_cached_s3_filesystem(storage_provider):
    return authentication.get_s3_filesystem_pickle(storage_provider, verbose=True)

@lru_cache(maxsize=2)
def get_cached_s3fs_filesystem(storage_provider):
    return authentication.get_s3fs_filesystem_json(storage_provider, verbose=True)

# -------------------------------
# Logging Configuration
# -------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_operations.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# -------------------------------
# Helper Functions
# -------------------------------

def construct_s3_path(bucket, type_name, provider, partition_type, ticker=None, publish_date=None, year=None, all_dates_after=False, has_year_subdir=True):
    """
    Construct the S3 path based on the partitioning scheme.
    
    Parameters:
      - bucket (str): Bucket name/path prefix.
      - type_name (str): Type of data (e.g., 'applications')
      - provider (str): Storage provider (e.g., 'wasabi' or 'digitalocean')
      - partition_type (str): 'date' or 'ticker'
      - ticker (str, optional): Ticker symbol (required for ticker partitioning)
      - publish_date (str, optional): Publish date in 'YYYY-MM-DD' format (required for date partitioning)
      - year (int, optional): Year (required for ticker partitioning when has_year_subdir is True)
      - all_dates_after (bool, optional): If True, returns the parent directory for scanning all date partitions
      - has_year_subdir (bool, optional): Indicates whether the ticker partition includes a year subdirectory.
      
    Returns:
      - str: Constructed S3 path.
    """
    if partition_type == "date":
        if all_dates_after:
            path = f"{type_name}/date/"
        else:
            if not publish_date:
                raise ValueError("publish_date must be provided for date partitioning.")
            path = f"{type_name}/date/date/date_partitioned={publish_date}/"
    elif partition_type == "ticker":
        if not ticker:
            raise ValueError("Ticker must be provided for ticker partitioning.")
        if has_year_subdir:
            if not year:
                raise ValueError("Year must be provided when has_year_subdir is True for ticker partitioning.")
            path = f"{type_name}/ticker/ticker/ticker_partitioned={ticker}/year={year}/"
        else:
            path = f"{type_name}/ticker/ticker/ticker_partitioned={ticker}/"
    else:
        raise ValueError("Invalid partition_type. Choose 'date' or 'ticker'.")
    
    return f"{bucket}/{path}"


def list_ticker_years(provider, bucket, type_name, ticker, has_year_subdir=True):
    """
    List actual year subfolders for a given ticker in the S3 partition scheme.
    
    If has_year_subdir is False, simply returns a single tuple with None as the year.
    
    Returns:
      - list of tuples: [(year, path), ...] where year is an integer if available, or None.
    """
    ticker_base_path = f"{bucket}/{type_name}/ticker/ticker/ticker_partitioned={ticker}/"
    if not has_year_subdir:
        return [(None, ticker_base_path)]
    
    fs = get_cached_s3fs_filesystem(provider)
    try:
        subdirs = fs.ls(ticker_base_path)
    except Exception as e:
        logger.error(f"Error listing subfolders in {ticker_base_path} ({provider}): {e}")
        return []
    
    year_paths = []
    for subdir in subdirs:
        basename = os.path.basename(subdir.rstrip('/'))
        if basename.startswith('year='):
            year_str = basename.split('=')[1]
            try:
                year_int = int(year_str)
                year_paths.append((year_int, subdir))
            except ValueError:
                logger.warning(f"Could not parse year from folder name: {basename}")
    return year_paths


def list_date_partitions(provider, bucket, type_name):
    """
    List date partitions in the S3 bucket.
    
    Returns:
      - list of tuples: [(date_obj, partition_path), ...]
    """
    s3_path = construct_s3_path(bucket, type_name, provider, partition_type="date", all_dates_after=True)
    fs = get_cached_s3fs_filesystem(provider)
    try:
        partitions = fs.ls(s3_path)
        dates = []
        for partition in partitions:
            basename = os.path.basename(partition.rstrip('/'))
            if basename.startswith('date_partitioned='):
                date_str = basename.split('=')[1]
                try:
                    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    dates.append((date_obj, partition))
                except ValueError:
                    logger.warning(f"Unable to parse date from partition {partition}")
        return dates
    except Exception as e:
        logger.error(f"Error listing date partitions in {s3_path} ({provider}): {e}")
        return []


def load_parquet_from_s3(s3_path, provider, columns=None, start_date=None, end_date=None):
    """
    Load a Parquet file from S3 into a pandas DataFrame with optional date filtering.
    
    Now supports filtering on both start_date and end_date.
    """
    fs = get_cached_s3_filesystem(provider)
    try:
        dataset = ds.dataset(s3_path, filesystem=fs, format='parquet')
        
        # Build filter expression if start_date and/or end_date are provided.
        filter_expr = None
        if start_date:
            min_date_pa = pa.scalar(pd.to_datetime(start_date).date(), type=pa.date32())
            filter_expr = ds.field('date') >= min_date_pa
        if end_date:
            max_date_pa = pa.scalar(pd.to_datetime(end_date).date(), type=pa.date32())
            if filter_expr is not None:
                filter_expr = filter_expr & (ds.field('date') <= max_date_pa)
            else:
                filter_expr = ds.field('date') <= max_date_pa
        if filter_expr is not None:
            dataset = dataset.filter(filter_expr)
        
        table = dataset.to_table(columns=columns, use_threads=True)
        logger.info(f"Schema for {s3_path} ({provider}): {table.schema}")
        df = table.to_pandas()
        
        # Optionally, reorder columns if partition columns exist
        partition_cols = ['ticker', 'date']
        existing_cols = [col for col in partition_cols if col in df.columns]
        other_cols = [col for col in df.columns if col not in partition_cols]
        df = df[existing_cols + other_cols]
        return df
    except Exception as e:
        logger.error(f"Error loading data from {s3_path} ({provider}): {e}")
        return pd.DataFrame()


# -------------------------------
# Loading Functions
# -------------------------------

def load_data_by_ticker(
    type_name,
    buckets,  # Dictionary mapping provider -> bucket value.
    providers=['wasabi', 'digitalocean'],
    tickers=None,
    start_date=None,
    end_date=None,
    columns=None,
    max_workers=4,
    has_year_subdir=True
):
    """
    Load data for specified tickers and/or dates from S3 storage providers.
    """
    date_tasks = []
    ticker_tasks = []
    results = []

    # Normalize tickers to a list (if provided)
    if tickers and isinstance(tickers, str):
        tickers = [tickers]
    if not tickers:
        tickers = []
    
    # Case 1: Tickers and a start_date provided.
    if tickers and start_date:
        try:
            min_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            logger.info(f"Minimum date provided: {min_date_obj}")
        except ValueError:
            logger.error(f"Invalid start_date format: {start_date}. Expected 'YYYY-MM-DD'.")
            return pd.DataFrame()

        # If end_date is provided, determine the maximum year to scan.
        if end_date:
            try:
                max_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
                logger.info(f"End date provided: {max_date_obj}")
            except ValueError:
                logger.error(f"Invalid end_date format: {end_date}. Expected 'YYYY-MM-DD'.")
                return pd.DataFrame()
        else:
            max_date_obj = None

        for provider in providers:
            for ticker in tickers:
                if has_year_subdir:
                    # Determine the upper bound for years
                    current_year = datetime.datetime.now().year
                    max_year = max_date_obj.year if max_date_obj else current_year
                    # Create a task for each year from the minimum year up to the max_year.
                    for year in range(min_date_obj.year, max_year + 1):
                        s3_path = construct_s3_path(
                            bucket=buckets[provider],
                            type_name=type_name,
                            provider=provider,
                            partition_type="ticker",
                            ticker=ticker,
                            year=year,
                            has_year_subdir=True
                        )
                        ticker_tasks.append((s3_path, provider, columns, None))
                else:
                    s3_path = construct_s3_path(
                        bucket=buckets[provider],
                        type_name=type_name,
                        provider=provider,
                        partition_type="ticker",
                        ticker=ticker,
                        has_year_subdir=False
                    )
                    ticker_tasks.append((s3_path, provider, columns, None))

    # Case 2: Only dates provided (no tickers), with both start and end dates.
    elif start_date and end_date and not tickers:
        try:
            min_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            max_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            logger.info(f"Date range provided: {min_date_obj} to {max_date_obj}")
        except ValueError as e:
            logger.error(f"Invalid date format. Expected 'YYYY-MM-DD': {e}")
            return pd.DataFrame()

        for provider in providers:
            date_partitions = list_date_partitions(provider, buckets[provider], type_name)
            for date_obj, partition_path in date_partitions:
                if min_date_obj <= date_obj <= max_date_obj:
                    date_tasks.append((partition_path, provider, columns, None))
    
    # Case 3: Only start_date provided (no tickers)
    elif start_date and not tickers:
        try:
            min_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            logger.info(f"Minimum date provided: {min_date_obj}")
        except ValueError:
            logger.error(f"Invalid start_date format: {start_date}. Expected 'YYYY-MM-DD'.")
            return pd.DataFrame()

        for provider in providers:
            date_partitions = list_date_partitions(provider, buckets[provider], type_name)
            for date_obj, partition_path in date_partitions:
                if date_obj >= min_date_obj:
                    date_tasks.append((partition_path, provider, columns, None))

    # Case 4: Only tickers provided.
    elif tickers and not start_date:
        for provider in providers:
            for ticker in tickers:
                print(f"DEBUG: Looking for ticker {ticker} in {buckets[provider]}/{type_name}")
                ticker_years = list_ticker_years(provider, buckets[provider], type_name, ticker, has_year_subdir=has_year_subdir)
                print(f"DEBUG: Found ticker years: {ticker_years}")
                for year_val, path in ticker_years:
                    print(f"DEBUG: Adding task for path: {path}")
                    ticker_tasks.append((path, provider, columns, None))
    else:
        logger.warning("No tickers or start_date provided. Please provide at least one.")
        return pd.DataFrame()

    # Combine tasks from ticker and date sources.
    all_tasks = ticker_tasks + date_tasks
    if not all_tasks:
        logger.warning("No tasks to process. Exiting.")
        return pd.DataFrame()

    def load_task(task):
        s3_path, provider, columns, ticker_filter = task
        # Pass both start_date and end_date to the loading function.
        df = load_parquet_from_s3(s3_path, provider, columns, start_date=start_date, end_date=end_date)
        if not df.empty and ticker_filter:
            if 'ticker' in df.columns:
                df = df[df['ticker'].isin(ticker_filter)]
            else:
                logger.warning(f"'ticker' column not found in data from {s3_path} ({provider}). Skipping ticker filter.")
        return df

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {executor.submit(load_task, task): task for task in all_tasks}
        for future in tqdm(as_completed(future_to_task), total=len(all_tasks), desc="Loading data"):
            df = future.result()
            if not df.empty:
                results.append(df)

    if results:
        final_df = pd.concat(results, ignore_index=True)
        logger.info(f"Successfully loaded data with {len(final_df)} records.")
    else:
        final_df = pd.DataFrame()
        logger.warning("No data found.")

    return final_df


# -------------------------------
# Example Usage
# -------------------------------

# Try to import CustomDataFrame; if unavailable, fall back to pandas.DataFrame.
try:
    from sovai.extensions.pandas_extensions import CustomDataFrame
    HAS_CUSTOM_DATAFRAME = True
except ImportError:
    HAS_CUSTOM_DATAFRAME = False
    CustomDataFrame = pd.DataFrame

def load_frame_s3_partitioned_high(endpoint, tickers=None, columns=None, start_date=None, end_date=None):
    """
    Load data for a given endpoint using the S3 partitioned scheme.
    
    The endpoint configuration now contains the bucket mapping, data type, and a new parameter
    'has_year_subdir' that indicates whether the ticker partition includes a year subdirectory.
    """
    print(f"DEBUG: load_frame_s3_partitioned_high called with endpoint={endpoint}, tickers={tickers}")
    endpoint_config = {
        "patents/applications": {
            "bucket": {
                "digitalocean": "sovai/sovai-patents-bulk",  # Use the "bulk" bucket for ticker partitions
                "wasabi": "sovai-patents-export"
            },
            "type": "applications",
            "has_year_subdir": True
        },
        "patents/grants": {
            "bucket": {
                "digitalocean": "sovai/sovai-patents-bulk",
                "wasabi": "sovai-patents-export"
            },
            "type": "grants",
            "has_year_subdir": True
        },
        "clinical_trials": {
            "bucket": {
                "digitalocean": "sovai/sovai-clinical-trials-export",
                "wasabi": "sovai-clinical-trials-export"  # Adjust as needed
            },
            "type": "partitioned",
            "has_year_subdir": False
        },
        "clinical_trials": {
            "bucket": {
                "digitalocean": "sovai/sovai-clinical-trials-export",
                "wasabi": "sovai-clinical-trials-export"  # Adjust as needed
            },
            "type": "partitioned",
            "has_year_subdir": False
        },
        "spending/awards": {
            "bucket": {
                "digitalocean": "sovai/sovai-spending-export",
                "wasabi": "sovai-spending-export"  # Adjust as needed
            },
            "type": "partitioned/awards",
            "has_year_subdir": False
        }
    }
    
    if endpoint not in endpoint_config:
        raise ValueError(f"Invalid endpoint: {endpoint}")
    
    config = endpoint_config[endpoint]

    loaded_df_both = load_data_by_ticker(
        type_name=config["type"],
        buckets=config["bucket"],
        providers=['digitalocean'],
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        columns=columns,
        max_workers=8,  # Adjust based on your system's capabilities
        has_year_subdir=config.get("has_year_subdir", True)
    )
    
    # Sort the dataframe if the required columns exist
    sort_columns = []
    if 'ticker' in loaded_df_both.columns:
        sort_columns.append('ticker')
    if 'date' in loaded_df_both.columns:
        sort_columns.append('date')
    
    if sort_columns:
        loaded_df_both = loaded_df_both.sort_values(sort_columns)

    if HAS_CUSTOM_DATAFRAME:
        return CustomDataFrame(loaded_df_both)
    else:
        return loaded_df_both
