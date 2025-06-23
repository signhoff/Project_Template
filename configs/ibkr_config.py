# config/ibkr_config.py
import logging

# No need for local logger setup anymore
logger = logging.getLogger(__name__)

# --- IBKR Connection Parameters ---
HOST = '127.0.0.1'
PORT = 7497 # 7497 for TWS Paper Trading, 7496 for TWS Live, 4002 for Gateway Paper, 4001 for Gateway Live

# --- API Call Delays & Timeouts ---
IBKR_API_DELAY_SECONDS = 0.05
IBKR_CONNECTION_TIMEOUT_SECONDS = 15
IBKR_REQUEST_TIMEOUT_SECONDS = 45

# --- Logging Configuration ---
LOG_LEVEL = 'INFO'