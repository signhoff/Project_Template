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

# Client IDs for main application components (e.g., GUI)
# Ensure these are unique for each concurrent connection to IBKR.
CLIENT_ID_GUI_STOCK = 101
CLIENT_ID_GUI_OPTION = 102
CLIENT_ID_GUI_GENERAL = 103  # If GUI needs another general purpose connection

# --- Logging Configuration ---
LOG_LEVEL = 'INFO'
