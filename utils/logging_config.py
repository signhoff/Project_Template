# utils/logging_config.py
import logging
import sys
from configs import ibkr_config

def setup_logging():
    """
    Configures the root logger for the entire application.

    This function sets the logging level and format for all modules.
    It should be called once at the very beginning of the main application
    entry point.
    """
    log_level = getattr(logging, ibkr_config.LOG_LEVEL.upper(), logging.INFO)
    
    # Use a format that includes the module name for clarity
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Clear any existing handlers to avoid duplicates if this is called more than once
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    # Add a stream handler to output to console
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(handler)
    
    # Set the level on the root logger
    root_logger.setLevel(log_level)
    
    logging.info(f"Root logger configured with level: {ibkr_config.LOG_LEVEL}")