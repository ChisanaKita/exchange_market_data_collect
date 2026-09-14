import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# --- AWS & S3 Settings ---
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "your-market-data-bucket")
S3_REGION = os.getenv("S3_REGION", "ap-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)

# Path prefix in the S3 bucket
S3_PREFIX = os.getenv("S3_PREFIX", "crypto-market-data/")

# --- Storage Settings ---
LOCAL_DATA_DIR = os.getenv("LOCAL_DATA_DIR", "./local_cache")

# Time (in minutes) to wait after midnight UTC before zipping and uploading the previous day's data
UPLOAD_DELAY_MINUTES = int(os.getenv("UPLOAD_DELAY_MINUTES", "5"))

# --- Target Symbols ---
TARGET_SYMBOLS = [
    "BTCUSDT-PERPETUAL",
    "ETHUSDT-PERPETUAL",
    "BTCUSD-PERPETUAL",
    "BTCUSDC",
    "USDTUSDC"
]

# Hashkey MENA (UAE) lists tokenised equity/ETF perpetuals not available elsewhere,
# so it gets its own target list. Only the MENA collector receives these.
HASHKEY_MENA_TARGET_SYMBOLS = TARGET_SYMBOLS + [
    "SKHYNIXUSDT-PERPETUAL",
    "QQQUSDT-PERPETUAL",
    "SPCXUSDT-PERPETUAL",
    "SOXLUSDT-PERPETUAL"
]

# --- Connection Settings ---

# 1. Hashkey Settings
HASHKEY_WS_URL = os.getenv("HASHKEY_WS_URL", "wss://stream-glb.hashkey.com/quote/ws/v2")
HASHKEY_REST_URL = os.getenv("HASHKEY_REST_URL", "https://api-glb.hashkey.com")
HASHKEY_REST_POLL_INTERVAL_MS = int(os.getenv("HASHKEY_REST_POLL_INTERVAL_MS", "200"))
HASHKEY_REST_RATE_LIMIT_RPS = float(os.getenv("HASHKEY_REST_RATE_LIMIT_RPS", "1.5"))

# 1b. Hashkey MENA (UAE) Settings — served from the HK platform hosts with site=MENA
HASHKEY_MENA_WS_URL = os.getenv("HASHKEY_MENA_WS_URL", "wss://stream-pro.hashkey.com/quote/ws/v2")
HASHKEY_MENA_REST_URL = os.getenv("HASHKEY_MENA_REST_URL", "https://api-pro.hashkey.com")
HASHKEY_MENA_REST_POLL_INTERVAL_MS = int(os.getenv("HASHKEY_MENA_REST_POLL_INTERVAL_MS", "200"))
HASHKEY_MENA_REST_RATE_LIMIT_RPS = float(os.getenv("HASHKEY_MENA_REST_RATE_LIMIT_RPS", "1.5"))
# Delay between consecutive (sequential) funding rate queries
HASHKEY_MENA_FUNDING_RATE_DELAY_MS = int(os.getenv("HASHKEY_MENA_FUNDING_RATE_DELAY_MS", "500"))

# 2. Bitget Settings
BITGET_WS_URL = os.getenv("BITGET_WS_URL", "wss://ws.bitget.com/v2/ws/public")
BITGET_REST_URL = os.getenv("BITGET_REST_URL", "https://api.bitget.com")
BITGET_REST_POLL_INTERVAL_MS = int(os.getenv("BITGET_REST_POLL_INTERVAL_MS", "200"))
BITGET_REST_RATE_LIMIT_RPS = float(os.getenv("BITGET_REST_RATE_LIMIT_RPS", "2.0"))

# 4. Gate.io Settings
GATE_USDT_WS_URL = os.getenv("GATE_USDT_WS_URL", "wss://fx-ws.gateio.ws/v4/ws/usdt")
GATE_BTC_WS_URL = os.getenv("GATE_BTC_WS_URL", "wss://fx-ws.gateio.ws/v4/ws/btc")
GATE_REST_URL = os.getenv("GATE_REST_URL", "https://fx-api.gateio.ws/api/v4")
GATE_REST_POLL_INTERVAL_MS = int(os.getenv("GATE_REST_POLL_INTERVAL_MS", "200"))
GATE_REST_RATE_LIMIT_RPS = float(os.getenv("GATE_REST_RATE_LIMIT_RPS", "2.0"))

# 5. OSL Settings
OSL_API_KEY = os.getenv("OSL_API_KEY", "")
OSL_API_SECRET = os.getenv("OSL_API_SECRET", "")
OSL_REST_URL = os.getenv("OSL_REST_URL", "https://api.osl.com")
OSL_WS_URL = os.getenv("OSL_WS_URL", "wss://stream-api.osl.com/openapi/v1/ws")
OSL_REST_POLL_INTERVAL_MS = int(os.getenv("OSL_REST_POLL_INTERVAL_MS", "200"))
OSL_REST_RATE_LIMIT_RPS = float(os.getenv("OSL_REST_RATE_LIMIT_RPS", "2.0"))


