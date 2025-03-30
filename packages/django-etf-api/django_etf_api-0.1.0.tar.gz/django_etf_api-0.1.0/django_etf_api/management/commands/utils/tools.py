import time
import psutil
from dataclasses import dataclass, asdict, fields
from typing import Dict, Any

@dataclass
class ImportStats:
    """Data class to track import statistics"""
    # Time tracking
    start_time: float = 0
    end_time: float = 0
    
    # ETF counts
    total_etfs: int = 0
    processed_etfs: int = 0
    updated_etfs: int = 0
    skipped_etfs: int = 0
    failed_etfs: int = 0
    
    # Price data
    total_prices: int = 0
    prices_updated: int = 0
    
    # API metrics
    api_calls: int = 0
    api_failures: int = 0
    
    # Additional data metrics
    updated_holdings: int = 0
    holdings_attempted: int = 0
    updated_sectors: int = 0
    sectors_attempted: int = 0
    updated_allocations: int = 0
    allocations_attempted: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary with calculated values""" 
        result = asdict(self)
        
        # Time calculations
        if self.end_time and self.start_time:
            result["execution_time_seconds"] = round(self.end_time - self.start_time, 2)
            result["execution_time_formatted"] = f"{result['execution_time_seconds'] // 60}m {result['execution_time_seconds'] % 60:.1f}s"
        
        # Success rates
        if self.total_etfs:
            result["etf_success_rate"] = round((self.updated_etfs / self.total_etfs) * 100, 2)
        
        if self.api_calls:
            result["api_success_rate"] = round(((self.api_calls - self.api_failures) / self.api_calls) * 100, 2)
        
        # Per-data-type success rates
        if self.holdings_attempted:
            result["holdings_success_rate"] = round((self.updated_holdings / self.holdings_attempted) * 100, 2)
        
        if self.sectors_attempted:
            result["sectors_success_rate"] = round((self.updated_sectors / self.sectors_attempted) * 100, 2)
            
        if self.allocations_attempted:
            result["allocations_success_rate"] = round((self.updated_allocations / self.allocations_attempted) * 100, 2)
        
        # Performance metrics
        if result.get("execution_time_seconds", 0) > 0:
            result["etfs_per_second"] = round(self.processed_etfs / result["execution_time_seconds"], 2)
        
        return result

def retry_on_exception(max_retries=3, backoff_factor=1, 
                     allowed_exceptions=(Exception,)):
    """Retry decorator with exponential backoff for API functions"""
    def decorator(func):
        from functools import wraps
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            stats = getattr(args[0], 'stats', None)
            logger = getattr(args[0], 'logger', None)
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    if stats:
                        stats.api_failures += 1
                    
                    # Last attempt failed - re-raise exception
                    if attempt == max_retries:
                        if logger:
                            logger.error(f"Failed after {max_retries} attempts: {str(e)}")
                        raise
                    
                    # Calculate backoff time
                    wait_time = backoff_factor * (2 ** attempt)
                    if logger:
                        logger.warning(f"Attempt {attempt+1} failed: {str(e)}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
        return wrapper
    return decorator