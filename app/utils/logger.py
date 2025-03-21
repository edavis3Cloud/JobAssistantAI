import os
import logging
from pathlib import Path
import datetime

class Logger:
    """Logging utility for the application."""
    
    def __init__(self, config):
        """
        Initialize the logger.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """
        Set up the logger.
        
        Returns:
            logging.Logger: The configured logger
        """
        # Create logger
        logger = logging.getLogger('job_assistant')
        logger.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Create file handler
        log_dir = Path(__file__).parent.parent.parent / 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        log_file = log_dir / f'job_assistant_{today}.log'
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def get_logger(self):
        """
        Get the logger.
        
        Returns:
            logging.Logger: The logger
        """
        return self.logger
    
    def info(self, message):
        """Log an info message."""
        self.logger.info(message)
    
    def error(self, message):
        """Log an error message."""
        self.logger.error(message)
    
    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
    
    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)
    
    def exception(self, message):
        """Log an exception message."""
        self.logger.exception(message)
