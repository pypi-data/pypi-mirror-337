"""
ETF configuration system using dictionary-based configuration.
Integrates with Django settings.py through a clean ETF_CONFIG dictionary approach.
"""
import os
from datetime import datetime, timedelta
from typing import Dict, Any
from django.conf import settings

class ETFConfig:
    """Configuration manager for ETF data fetching"""
    # Default configuration values
    DEFAULTS = {
        # Core settings
        "etf_files_dir": "data/management/commands/utils/ETF_list",
        "start_date": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
        "end_date": datetime.now().strftime("%Y-%m-%d"),
        
        # Performance settings
        "max_threads": 8,
        "batch_size": 50,
        "db_batch_size": 500,
        "pause_seconds": 15,
        "retry_attempts": 3,
        "retry_backoff": 2,
        "max_price_age_days": 90,
        "connection_timeout": 30,
        
        # Default provider mapping
        "provider_map": {
            "Allianz.csv": "Allianz",
            "AmericanCentury.csv": "American Century",
            "ARK.csv": "ARK",
            "CapitalGroup.csv": "Capital Group",
            "DigitalCurrencyGroup.csv": "Digital Currency Group",
            "Dimensional.csv": "Dimensional",
            "Direxion.csv": "Direxion",
            "ExchangeTradedConcepts.csv": "Exchange Traded Concepts",
            "Fidelity.csv": "Fidelity",
            "Franklin.csv": "Franklin Templeton",
            "GraniteShares.csv": "GraniteShares",
            "Innovator.csv": "Innovator",
            "Invesco.csv": "Invesco",
            "iShares.csv": "iShares",
            "JanusHenderson.csv": "Janus Henderson",
            "JPMorgan.csv": "JPMorgan",
            "Mirae.csv": "Mirae Asset",
            "MorganStanley.csv": "Morgan Stanley",
            "NewYorkLife.csv": "New York Life",
            "ProShares.csv": "ProShares",
            "Rafferty.csv": "Rafferty",
            "Schwab.csv": "Schwab",
            "SPDR.csv": "SPDR",
            "SS&C.csv": "SS&C",
            "Toroso.csv": "Toroso",
            "VanEck.csv": "VanEck",
            "Vanguard.csv": "Vanguard",
            "WisdomTree.csv": "WisdomTree",
            "Xtrackers.csv": "Xtrackers",
            "YieldMax.csv": "YieldMax",
        }
    }
    
    def __init__(self):
        """Initialize config from settings.py ETF_CONFIG and environment variables"""
        # Start with defaults
        self._config = self.DEFAULTS.copy()
        
        # Override with Django settings if available
        if hasattr(settings, 'ETF_CONFIG') and isinstance(settings.ETF_CONFIG, dict):
            self._config.update(settings.ETF_CONFIG)
            
        # Environment variables take precedence (with ETF_ prefix)
        for key in self._config:
            env_key = f"ETF_{key.upper()}"
            if env_key in os.environ:
                # Convert value types based on default value type
                default_val = self.DEFAULTS[key]
                env_val = os.environ[env_key]
                
                if isinstance(default_val, int):
                    self._config[key] = int(env_val)
                elif isinstance(default_val, float):
                    self._config[key] = float(env_val)
                elif isinstance(default_val, bool):
                    self._config[key] = env_val.lower() in ('true', 'yes', '1')
                else:
                    self._config[key] = env_val
    
    def __getitem__(self, key):
        """Enable dictionary-like access"""
        return self._config[key]
    
    def get(self, key, default=None):
        """Get config value with optional default"""
        return self._config.get(key, default)


# Create singleton instance
etf_config = ETFConfig()

# Export legacy-compatible variables
ETF_FILES_DIR = etf_config["etf_files_dir"]
DEFAULT_START_DATE = etf_config["start_date"]
DEFAULT_END_DATE = etf_config["end_date"]
PROVIDER_MAP = etf_config["provider_map"]
CONFIG = {
    "max_threads": etf_config["max_threads"],
    "batch_size": etf_config["batch_size"],
    "db_batch_size": etf_config["db_batch_size"],
    "pause_seconds": etf_config["pause_seconds"],
    "retry_attempts": etf_config["retry_attempts"],
    "retry_backoff": etf_config["retry_backoff"],
    "max_price_age_days": etf_config["max_price_age_days"],
    "connection_timeout": etf_config["connection_timeout"],
}