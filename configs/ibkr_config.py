# config/ibkr_config.py
import logging
import sys

# Logger for config file sanity checks (if any)
logger = logging.getLogger(__name__)
if not logger.hasHandlers():  # Avoid duplicate handlers
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s (IBKR_Config) - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)

# --- IBKR Connection Parameters ---
HOST = '127.0.0.1'
PORT = 7497  # 7497 for TWS Paper Trading, 7496 for TWS Live, 4002 for Gateway Paper, 4001 for Gateway Live

# --- API Call Delays & Timeouts ---
IBKR_API_DELAY_SECONDS = 0.05
IBKR_CONNECTION_TIMEOUT_SECONDS = 15
IBKR_REQUEST_TIMEOUT_SECONDS = 45

# --- Logging Configuration ---
LOG_LEVEL = 'INFO'