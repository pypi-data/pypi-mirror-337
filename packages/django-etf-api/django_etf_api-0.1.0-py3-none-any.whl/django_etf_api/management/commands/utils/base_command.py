import logging
import os
from typing import Dict, Any, Optional, Callable
from django.core.management.base import BaseCommand

class PortfolioBaseCommand(BaseCommand):
    """Base command class for all portfolio analyzer commands with unified logging"""
    
    def __init__(self, command_name: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_name = command_name or self.__class__.__module__.split('.')[-1]
        self.logger = self._configure_logging()
        
    def _configure_logging(self):
        """Configure logging with file output"""
        logger = logging.getLogger(self.command_name)
        if not logger.handlers:  # Only add handlers if none exist
            logger.setLevel(logging.INFO)
            # Create logs directory
            log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.dirname(__file__)))), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            # Add file handler
            file_handler = logging.FileHandler(os.path.join(log_dir, f'{self.command_name}.log'))
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        return logger
        
    def log(self, message: str, level: str = 'info', style_func: Optional[Callable] = None):
        """Log message to both console and file"""
        # Map level to logging function
        log_funcs = {
            'info': self.logger.info,
            'warning': self.logger.warning,
            'error': self.logger.error,
            'debug': self.logger.debug,
            'success': self.logger.info
        }
        
        # Log to file (with SUCCESS prefix for success level)
        log_func = log_funcs.get(level, self.logger.info)
        log_message = f"SUCCESS: {message}" if level == 'success' else message
        log_func(log_message)
        
        # Log to console with appropriate styling
        if level == 'success' and hasattr(self.style, 'SUCCESS'):
            self.stdout.write(self.style.SUCCESS(message))
        elif level == 'warning' and hasattr(self.style, 'WARNING'):
            self.stdout.write(self.style.WARNING(message))
        elif level == 'error' and hasattr(self.style, 'ERROR'):
            self.stdout.write(self.style.ERROR(message))
        elif style_func:
            self.stdout.write(style_func(message))
        else:
            self.stdout.write(message)
    
    # Alias for backward compatibility
    log_message = log
            
    # Convenience methods
    def info(self, message: str): self.log(message, 'info')
    def success(self, message: str): self.log(message, 'success')
    def warning(self, message: str): self.log(message, 'warning')
    def error(self, message: str): self.log(message, 'error')
    def debug(self, message: str): self.log(message, 'debug')
    
    def log_stats(self, stats_dict: Dict[str, Any], title: str = "STATISTICS"):
        """Log statistics with pretty formatting"""
        self.success("=" * 50)
        self.success(title)
        self.success("=" * 50)
        for key, value in {k: v for k, v in stats_dict.items() 
                           if k not in ["start_time", "end_time"]}.items():
            self.success(f"{key.replace('_', ' ').title()}: {value}")
        self.success("=" * 50)