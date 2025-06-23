# config/polygon_config.py
import os
import logging
from dotenv import load_dotenv

# Logger for this module - will now inherit the central configuration
logger = logging.getLogger(__name__)

# --- Load Environment Variables ---
# Construct the path to the .env file which is in the project root (one level up from 'configs')
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
    logger.info(".env file found and loaded.")
else:
    logger.warning(".env file not found at expected path. API keys must be set as system environment variables.")

# --- Polygon API Configuration ---
# Securely get the API key from the environment variable. It will be None if not found.
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

if not POLYGON_API_KEY:
    logger.error("POLYGON_API_KEY not found in environment. The Polygon handler will not be able to connect.")
elif "YOUR_KEY" in POLYGON_API_KEY or "_placeholder" in POLYGON_API_KEY:
     logger.warning("The POLYGON_API_KEY appears to be a placeholder. Please update it in your .env file.")

# This value can remain as it's not a secret
POLYGON_API_DELAY_SECONDS = 12.50  # Adjust as needed based on your API plan. Free tier allows 5 calls a minute

# You can add other Polygon-specific settings here if needed, for example:
# POLYGON_BASE_URL = "https://api.polygon.io"