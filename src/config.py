# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

# Directory to store temporary files
DATA_DIR = '/app/data'

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)