import os
import time
import pandas as pd
import yfinance as yf
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.db import transaction
from django.core.management.base import CommandError
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime, date

# Import custom modules
from .utils.base_command import PortfolioBaseCommand
from .utils.tools import ImportStats, retry_on_exception

# Import settings
from .utils.etf_config import ETF_FILES_DIR, DEFAULT_START_DATE, DEFAULT_END_DATE, PROVIDER_MAP, CONFIG
from ...models import ETFDetails, ETFPrice, ETFAssetAllocation, ETFTopHolding, ETFSectorWeighting


class Command(PortfolioBaseCommand):
    """Django command to populate ETF details and update ETF prices"""
    help = "Populate ETF details and update ETF prices from CSV files and Yahoo Finance"

    def __init__(self, *args, **kwargs):
        super().__init__('fetch_etfs_data', *args, **kwargs)
        self.stats = ImportStats()
        self.session = self._setup_http_session()
        
    def _setup_http_session(self) -> requests.Session:
        """Create a configured HTTP session with retry mechanism"""
        session = requests.Session()
        retry_strategy = Retry(
            total=CONFIG["retry_attempts"],
            backoff_factor=CONFIG["retry_backoff"],
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(
            pool_connections=CONFIG["max_threads"],
            pool_maxsize=CONFIG["max_threads"],
            max_retries=retry_strategy
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def add_arguments(self, parser):
        """Add command-line arguments"""
        # Core operation flags
        parser.add_argument("--etfs-only", action="store_true", 
                           help="Only import ETF information without updating prices")
        parser.add_argument("--prices-only", action="store_true", 
                           help="Only update ETF prices without importing ETF information")
        
        # Additional data operations
        parser.add_argument('--additional-only', action='store_true', 
                           help='Only update additional ETF data (holdings, sectors, allocations)')
        parser.add_argument('--update-holdings', action='store_true', 
                           help='Update ETF holdings')
        parser.add_argument('--update-sectors', action='store_true',
                           help='Update ETF sector weightings')
        parser.add_argument('--update-allocations', action='store_true', 
                           help='Update ETF asset allocations')
        
        # Processing parameters
        parser.add_argument("--symbols", type=str,
                           help="Comma-separated list of ETF symbols to process (e.g. SPY,QQQ,VOO)")
        parser.add_argument("--threads", type=int,
                           help=f"Number of threads to use (default: {CONFIG['max_threads']})")

    def handle(self, *args, **options):
        """Main command handler"""
        try:
            self.stats.start_time = time.time()
            self.success("Starting ETF population process")
            
            # Process command options
            CONFIG["max_threads"] = options.get("threads") or CONFIG["max_threads"]
            symbols = self._parse_symbols(options.get("symbols"))
            operations = self._determine_operations(options)
            
            # Execute operations based on flags
            if operations["import_etfs"]:
                self._import_etfs_from_files(symbols)
            
            if operations["update_prices"]:
                self.success("Updating ETF prices...")
                self.update_etf_prices(symbols)
            
            # Handle additional data operations
            additional_ops = [operations[k] for k in ["update_holdings", "update_sectors", "update_allocations"]]
            if any(additional_ops):
                self._update_additional_data(symbols=symbols, operations=operations)
            else:
                self.success("Skipping additional ETF data update")
            
            # Log final statistics
            self.stats.end_time = time.time()
            self.log_stats(self.stats.to_dict(), "FETCH ETF PERFORMANCE STATS")
            self.success("ETF population complete!")
            
        except Exception as e:
            self.error(f"Command failed: {str(e)}")
            raise CommandError(str(e))

    def _parse_symbols(self, symbols_str: Optional[str]) -> Optional[List[str]]:
        """Parse comma-separated symbols into a list"""
        if not symbols_str:
            return None
            
        symbols = [s.strip() for s in symbols_str.split(",")]
        self.success(f"Processing only these symbols: {', '.join(symbols)}")
        return symbols

    def _determine_operations(self, options: Dict) -> Dict[str, bool]:
        """Determine which operations to perform based on command options"""
        # Default operations
        operations = {
            "import_etfs": not options.get("prices_only"),
            "update_prices": not options.get("etfs_only"),
            "update_holdings": options.get("update_holdings", False),
            "update_sectors": options.get("update_sectors", False),
            "update_allocations": options.get("update_allocations", False)
        }
        
        # Override for additional-only mode
        if options.get("additional_only"):
            self.success("Running in additional-data-only mode")
            operations.update({
                "import_etfs": False,
                "update_prices": False,
                "update_holdings": True,
                "update_sectors": True,
                "update_allocations": True
            })
            
        return operations

    def _import_etfs_from_files(self, symbols: Optional[List[str]]) -> None:
        """Process all ETF files and import data"""
        if not os.path.exists(ETF_FILES_DIR):
            self.error(f"Directory not found: {ETF_FILES_DIR}")
            return
        
        files = [f for f in os.listdir(ETF_FILES_DIR) if f.endswith(".csv")]
        self.success(f"Found {len(files)} CSV files to process")
        
        for file in files:
            self.import_etfs_from_file(os.path.join(ETF_FILES_DIR, file), symbols)

    def import_etfs_from_file(self, file_path: str, symbols: Optional[List[str]] = None) -> None:
        """Import ETFs from a CSV file and update the database"""
        try:
            filename = os.path.basename(file_path)
            self.success(f"Processing file: {filename}")
            
            # Read and filter CSV data
            df = pd.read_csv(file_path)
            if symbols:
                df = df[df["Symbol"].isin(symbols)]
                if df.empty:
                    self.warning(f"No matching symbols found in {filename}")
                    return
            
            provider = PROVIDER_MAP.get(filename, "Unknown")
            processed, created, updated = 0, 0, 0
            
            # Process ETFs in a transaction
            with transaction.atomic():
                for _, row in df.iterrows():
                    # Prepare ETF data with base fields
                    etf_data = {
                        "name": row["ETF Name"],
                        "provider": provider,
                    }
                    
                    # Add optional fields if present
                    optional_fields = {
                        "asset_class": "Asset Class",
                        "total_assets": "Total Assets ",
                        "inception": "Inception",
                        "ter": "ER",
                        "pe_ratio": "P/E Ratio", 
                        "beta": "Beta"
                    }
                    
                    for field, csv_field in optional_fields.items():
                        if csv_field in row and pd.notna(row[csv_field]):
                            etf_data[field] = row[csv_field]
                    
                    # Create or update ETF
                    etf, was_created = ETFDetails.objects.update_or_create(
                        symbol=row["Symbol"],
                        defaults=etf_data
                    )
                    
                    processed += 1
                    if was_created:
                        created += 1
                    else:
                        updated += 1
            
            # Log results and update stats
            self.success(
                f"File {filename}: Processed {processed} ETFs "
                f"({created} created, {updated} updated)"
            )
            self.stats.processed_etfs += processed

        except Exception as e:
            self.error(f"Error processing {file_path}: {str(e)}")
            raise

    def validate_price_data(self, df: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Validate price data from Yahoo Finance to filter out bad values"""
        if df.empty:
            return df
            
        validated_df = df.copy()
        rows_before = len(validated_df)
        
        # Apply validation filters
        validated_df = (validated_df.dropna()
                       .query("Open >= 0 and High >= 0 and Low >= 0 and Close >= 0 and Volume >= 0")
                       .query("High >= Low"))
        
        # Check for extreme price deviations
        max_deviation = 0.5  # 50% deviation threshold
        validated_df = validated_df[
            (validated_df["High"] <= validated_df["Close"] * (1 + max_deviation)) &
            (validated_df["Low"] >= validated_df["Close"] * (1 - max_deviation))
        ]
        
        # Log if rows were filtered out
        rows_dropped = rows_before - len(validated_df)
        if rows_dropped > 0:
            self.warning(f"Removed {rows_dropped} problematic rows from {symbol} data")
            
        return validated_df

    @retry_on_exception(
        max_retries=CONFIG["retry_attempts"],
        backoff_factor=CONFIG["retry_backoff"],
        allowed_exceptions=(
            requests.exceptions.RequestException,
            ValueError,
            IOError
        )
    )
    def fetch_etf_prices(self, etf: ETFDetails) -> Tuple[List[ETFPrice], str]:
        """Fetch historical ETF price data from Yahoo Finance"""
        symbol = etf.symbol
        self.stats.api_calls += 1
        
        # Determine start date based on last price date
        start_date = DEFAULT_START_DATE
        if etf.last_price_date:  # Use last_price_date instead of last_updated
            if isinstance(etf.last_price_date, (datetime, date)):
                start_date = etf.last_price_date.strftime("%Y-%m-%d") 
            else:
                start_date = etf.last_price_date
        
        try:
            # Fetch data using the yfinance API
            ticker = yf.Ticker(symbol, session=self.session)
            df = ticker.history(
                start=start_date, 
                end=DEFAULT_END_DATE, 
                interval="1d", 
                timeout=CONFIG["connection_timeout"]
            )
            
            if df.empty:
                return [], symbol
            
            # Validate the data
            df = self.validate_price_data(df, symbol)
            if df.empty:
                self.warning(f"All price data for {symbol} was invalid")
                return [], symbol
            
            # Create price objects
            price_objects = [
                ETFPrice(
                    etf=etf,
                    date=idx.date(),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=int(row["Volume"]),
                )
                for idx, row in df.iterrows()
            ]
            
            # Update the last_price_date field
            if price_objects:
                etf.last_price_date = price_objects[-1].date
                etf.save(update_fields=["last_price_date"])  # Only update this field
            
            return price_objects, symbol
            
        except Exception as e:
            self.stats.api_failures += 1
            self.error(f"Error fetching data for {symbol}: {str(e)}")
            raise

    def update_etf_prices(self, symbols: Optional[List[str]] = None) -> None:
        """Update ETF prices from Yahoo Finance using multithreading"""
        # Get ETFs to process
        etfs = ETFDetails.objects.all()
        if symbols:
            etfs = etfs.filter(symbol__in=symbols)
        
        total_etfs = etfs.count()
        self.stats.total_etfs = total_etfs
        
        if total_etfs == 0:
            self.warning("No ETFs found to update")
            return
            
        self.success(f"Updating prices for {total_etfs} ETFs using {CONFIG['max_threads']} threads")
        
        # Process in batches
        batch_size = CONFIG["batch_size"]
        for i in range(0, total_etfs, batch_size):
            batch = etfs[i:i + batch_size]
            self.success(f"Processing batch {i//batch_size + 1}/{(total_etfs-1)//batch_size + 1}")
            
            self._process_price_batch(batch)
            
            # Pause between batches if not the last one
            if i + batch_size < total_etfs:
                pause_seconds = CONFIG["pause_seconds"]
                self.success(f"Pausing for {pause_seconds}s to avoid rate limits...")
                time.sleep(pause_seconds)

    def _process_price_batch(self, batch):
        """Process a batch of ETFs for price updates using multithreading"""
        all_price_objects = []
        batch_updated = batch_failed = 0
        
        # Process batch in parallel
        with ThreadPoolExecutor(max_workers=CONFIG["max_threads"]) as executor:
            future_to_etf = {executor.submit(self.fetch_etf_prices, etf): etf for etf in batch}
            
            for future in as_completed(future_to_etf):
                try:
                    price_objects, symbol = future.result()
                    if price_objects:
                        all_price_objects.extend(price_objects)
                        self.stats.updated_etfs += 1
                        batch_updated += 1
                        self.success(f"Updated {symbol} with {len(price_objects)} price records")
                    else:
                        self.stats.skipped_etfs += 1
                except Exception as e:
                    etf = future_to_etf[future]
                    self.stats.failed_etfs += 1
                    batch_failed += 1
                    self.error(f"Failed to update {etf.symbol}: {str(e)}")
        
        # Bulk save price data
        if all_price_objects:
            self._bulk_save_objects(ETFPrice, all_price_objects)
            self.stats.total_prices += len(all_price_objects)
        
        self.success(
            f"Batch results: {batch_updated} updated, {batch_failed} failed, "
            f"{len(batch) - batch_updated - batch_failed} skipped"
        )

    def _bulk_save_objects(self, model_class, objects):
        """Save objects in bulk with batching to manage memory usage"""
        with transaction.atomic():
            db_batch_size = CONFIG["db_batch_size"]
            for j in range(0, len(objects), db_batch_size):
                sub_batch = objects[j:j+db_batch_size]
                model_class.objects.bulk_create(sub_batch, ignore_conflicts=True)

    def _update_additional_data(self, symbols: Optional[List[str]] = None, operations: Dict[str, bool] = None) -> None:
        """Update additional ETF data (holdings, sectors, allocations)"""
        # Default empty operations dict
        operations = operations or {}
        
        # Get ETFs to process
        etfs = ETFDetails.objects.all()
        if symbols:
            etfs = etfs.filter(symbol__in=symbols)
        
        total_etfs = etfs.count()
        self.stats.total_etfs = total_etfs
        
        if total_etfs == 0:
            self.warning("No ETFs found to update")
            return
            
        # Log the data types being updated
        data_types = [op.replace("update_", "") for op, enabled in operations.items() 
                      if op.startswith("update_") and enabled]
        self.success(
            f"Updating {', '.join(data_types)} for {total_etfs} ETFs "
            f"using {CONFIG['max_threads']} threads"
        )
        
        # Process in batches
        batch_size = CONFIG["batch_size"]
        for i in range(0, total_etfs, batch_size):
            batch = etfs[i:i + batch_size]
            self.success(f"Processing batch {i//batch_size + 1}/{(total_etfs-1)//batch_size + 1}")
            
            self._process_additional_data_batch(batch, operations)
            
            # Pause between batches if not the last one
            if i + batch_size < total_etfs:
                pause_seconds = CONFIG["pause_seconds"]
                self.success(f"Pausing for {pause_seconds}s to avoid rate limits...")
                time.sleep(pause_seconds)

    def _process_additional_data_batch(self, batch, operations):
        """Process a batch of ETFs for additional data updates"""
        batch_results = {
            "holdings": 0,
            "sectors": 0,
            "allocations": 0,
            "failed": 0
        }
        
        # Process batch in parallel
        with ThreadPoolExecutor(max_workers=CONFIG["max_threads"]) as executor:
            # Build the task list based on enabled operations
            futures = {}
            for etf in batch:
                futures[executor.submit(
                    self._fetch_all_etf_data, 
                    etf, 
                    operations.get("update_holdings", False),
                    operations.get("update_sectors", False),
                    operations.get("update_allocations", False)
                )] = etf
            
            # Process results as they complete
            for future in as_completed(futures):
                etf = futures[future]
                try:
                    results = future.result()
                    
                    # Process each data type if requested and update counters
                    for data_type, (objects, success) in results.items():
                        if success and objects:
                            # Save the data
                            model_map = {
                                "holdings": ETFTopHolding,
                                "sectors": ETFSectorWeighting,
                                "allocation": ETFAssetAllocation
                            }
                            
                            # First clear existing data
                            model_map[data_type].objects.filter(etf=etf).delete()
                            
                            # Then bulk create new data
                            self._bulk_save_objects(model_map[data_type], objects)
                            
                            # Update counters
                            result_type = data_type if data_type != "allocation" else "allocations"
                            batch_results[result_type] += 1
                            
                            # Update stats attribute
                            stat_attr = f"updated_{result_type}"
                            if hasattr(self.stats, stat_attr):
                                setattr(self.stats, stat_attr, getattr(self.stats, stat_attr) + 1)
                            
                            self.success(
                                f"Updated {etf.symbol} with {len(objects)} {data_type}"
                            )
                except Exception as e:
                    batch_results["failed"] += 1
                    self.stats.failed_etfs += 1
                    self.error(f"Failed to update {etf.symbol} data: {str(e)}")
        
        # Log batch results
        update_results = [f"{count} {data_type}" for data_type, count in batch_results.items() 
                         if data_type != "failed" and count > 0]
        
        self.success(
            f"Batch results: {', '.join(update_results)}, {batch_results['failed']} failed"
        )

    @retry_on_exception(
        max_retries=CONFIG["retry_attempts"],
        backoff_factor=CONFIG["retry_backoff"],
        allowed_exceptions=(
            requests.exceptions.RequestException,
            ValueError,
            IOError,
            AttributeError
        )
    )
    def _fetch_all_etf_data(self, etf: ETFDetails, fetch_holdings: bool, 
                           fetch_sectors: bool, fetch_allocations: bool) -> dict:
        """Fetch all ETF data types in a single API call"""
        symbol = etf.symbol
        self.stats.api_calls += 1
        
        results = {
            "holdings": ([], False),
            "sectors": ([], False),
            "allocation": ([], False)
        }
        
        try:
            # Make a single API call to fetch all data
            ticker = yf.Ticker(symbol, session=self.session).funds_data
            
            # Process holdings if requested
            if fetch_holdings and ticker.top_holdings is not None and not ticker.top_holdings.empty:
                top_holdings = []
                for idx, row in ticker.top_holdings.iterrows():
                    # Safely extract values with fallbacks
                    symbol_val = idx if idx != '' else 'N/A'
                    name_val = row.iloc[0] if not pd.isna(row.iloc[0]) else 'N/A'
                    percent_val = float(row.iloc[1]) * 100 if len(row) > 1 and not pd.isna(row.iloc[1]) else 0.0
                    
                    top_holdings.append(
                        ETFTopHolding(
                            etf=etf,
                            symbol=symbol_val,
                            name=name_val,
                            holding_percent=percent_val
                        )
                    )
                
                results["holdings"] = (top_holdings, True)
            
            # Process sectors if requested
            if fetch_sectors and ticker.sector_weightings is not None:
                sector_weightings = [
                    ETFSectorWeighting(
                        etf=etf,
                        sector=sector,
                        weighting_percent=float(weight) * 100
                    )
                    for sector, weight in ticker.sector_weightings.items()
                    if isinstance(weight, (int, float)) and weight > 0
                ]
                
                results["sectors"] = (sector_weightings, True)

            # Process allocation if requested
            if fetch_allocations and ticker.asset_classes is not None:
                asset_allocations = [
                    ETFAssetAllocation(
                        etf=etf,
                        allocation=allocation,
                        allocation_percent=float(weight) * 100
                    )
                    for allocation, weight in ticker.asset_classes.items()
                    if isinstance(weight, (int, float)) and weight > 0
                ]
                
                results["allocation"] = (asset_allocations, True)
            
            return results
            
        except Exception as e:
            self.stats.api_failures += 1
            self.error(f"Error fetching data for {symbol}: {str(e)}")
            raise