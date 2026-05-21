import os
from urllib.parse import urlparse

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False

    raise ValueError(f"{name} must be a boolean value")


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default

    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc


def _normalize_mode(value: str) -> str:
    mode = value.strip().lower()
    if mode not in {"polling", "webhook"}:
        raise ValueError("BOT_MODE must be either 'polling' or 'webhook'")
    return mode


def _webhook_url_path(webhook_url: str) -> str:
    parsed = urlparse(webhook_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("WEBHOOK_URL must be a full HTTPS URL, for example https://example.com/telegram-webhook")

    return parsed.path.lstrip("/")


# Bot configuration
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

BOT_MODE = _normalize_mode(os.getenv("BOT_MODE", "webhook"))

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
WEBHOOK_LISTEN = os.getenv("WEBHOOK_LISTEN", "0.0.0.0").strip()
WEBHOOK_PORT = _get_int("WEBHOOK_PORT", 8443)
WEBHOOK_CERT = os.getenv("WEBHOOK_CERT") or None
WEBHOOK_KEY = os.getenv("WEBHOOK_KEY") or None
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN") or None
WEBHOOK_DROP_PENDING_UPDATES = _get_bool("WEBHOOK_DROP_PENDING_UPDATES", False)
WEBHOOK_URL_PATH = _webhook_url_path(WEBHOOK_URL) if WEBHOOK_URL else ""

if BOT_MODE == "webhook" and not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL is required when BOT_MODE=webhook")

if bool(WEBHOOK_CERT) != bool(WEBHOOK_KEY):
    raise ValueError("WEBHOOK_CERT and WEBHOOK_KEY must be configured together")

# Directory to store temporary files
DATA_DIR = os.getenv('DATA_DIR', 'data')

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)
