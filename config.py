import os
import json
import logging
from pathlib import Path
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Load JSON config
CONFIG = {}
try:
    with open("config.json", "r") as f:
        CONFIG = json.load(f)
        logger.info("Loaded config.json")
except FileNotFoundError:
    logger.warning("config.json not found, using defaults.")
except json.JSONDecodeError as e:
    logger.error(f"Error parsing config.json: {e}, using defaults.")
except PermissionError as e:
    logger.error(f"Permission denied reading config.json: {e}")
    raise

# Settings
USE_LOCAL = CONFIG.get("use_local_model", False)
LOCAL_MODEL = CONFIG.get("local_model_name", "tinyllama")

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    key_file = Path.home() / ".openai_key"
    try:
        with open(key_file, "r") as f:
            for line in f:
                if line.strip().startswith("OPENAI_API_KEY="):
                    OPENAI_API_KEY = line.strip().split("=", 1)[1]
                    break
    except Exception:
        logger.warning(f"Failed to read API key from {key_file}")

if not OPENAI_API_KEY:
    logger.error("No OpenAI API key found. Set OPENAI_API_KEY or add to ~/.openai_key.")
    raise ValueError("OpenAI API key missing")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)
