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


def _parse_symbol_list(env_var_name: str, default: list) -> list:
    raw = os.getenv(env_var_name)
    if raw:
        return [s.strip() for s in raw.split(",") if s.strip()]
    return list(default)


# General target symbol baseline (used as default fallback)
TARGET_SYMBOLS = [
    "BTCUSDT-PERPETUAL",
    "ETHUSDT-PERPETUAL",
    "BTCUSD-PERPETUAL",
    "BTCUSDC",
    "USDTUSDC",
]

# Per-exchange fine-grained target symbol lists
# 1a. Hashkey Global
HASHKEY_GLOBAL_TARGET_SYMBOLS = _parse_symbol_list(
    "HASHKEY_GLOBAL_TARGET_SYMBOLS",
    _parse_symbol_list(
        "HASHKEY_TARGET_SYMBOLS",
        ["BTCUSDT-PERPETUAL", "ETHUSDT-PERPETUAL", "BTCUSD-PERPETUAL"],
    ),
)
HASHKEY_TARGET_SYMBOLS = (
    HASHKEY_GLOBAL_TARGET_SYMBOLS  # Alias for backward compatibility
)

# 1b. Hashkey HK
HASHKEY_HK_TARGET_SYMBOLS = _parse_symbol_list(
    "HASHKEY_HK_TARGET_SYMBOLS",
    [
        "BTCUSDT-PERPETUAL",
        "ETHUSDT-PERPETUAL",
        "BTCUSD-PERPETUAL",
        "BTCUSD",
        "BTCUSDT",
        "ETHUSD",
        "ETHUSDT",
        "SOLUSD",
        "AVAXUSD",
        "XRPUSD",
        "LINKUSD",
        "ARBUSD",
    ],
)

# 1c. Hashkey MENA (UAE)
HASHKEY_MENA_TARGET_SYMBOLS = _parse_symbol_list(
    "HASHKEY_MENA_TARGET_SYMBOLS",
    [
        "BTCUSDT-PERPETUAL",
        "ETHUSDT-PERPETUAL",
        "SKHYNIXUSDT-PERPETUAL",
        "QQQUSDT-PERPETUAL",
        "SPCXUSDT-PERPETUAL",
        "SOXLUSDT-PERPETUAL",
        "USDTUSDC",
    ],
)

# 2. Bitget
BITGET_TARGET_SYMBOLS = _parse_symbol_list(
    "BITGET_TARGET_SYMBOLS",
    ["BTCUSDT-PERPETUAL", "ETHUSDT-PERPETUAL", "BTCUSD-PERPETUAL"],
)

# 3. Gate.io
GATE_TARGET_SYMBOLS = _parse_symbol_list(
    "GATE_TARGET_SYMBOLS",
    ["BTCUSDT-PERPETUAL", "ETHUSDT-PERPETUAL", "BTCUSD-PERPETUAL"],
)

# 4. OSL
OSL_TARGET_SYMBOLS = _parse_symbol_list("OSL_TARGET_SYMBOLS", ["BTCUSDC", "USDTUSD"])

# Registry dictionary mapping exchange keys to target symbol lists
EXCHANGE_TARGET_SYMBOLS = {
    "hashkey_global": HASHKEY_GLOBAL_TARGET_SYMBOLS,
    "hashkey_hk": HASHKEY_HK_TARGET_SYMBOLS,
    "hashkey_mena": HASHKEY_MENA_TARGET_SYMBOLS,
    "bitget": BITGET_TARGET_SYMBOLS,
    "gate": GATE_TARGET_SYMBOLS,
    "osl": OSL_TARGET_SYMBOLS,
}

# --- Connection Settings ---

# 1a. Hashkey Global Settings
HASHKEY_GLOBAL_WS_URL = os.getenv(
    "HASHKEY_GLOBAL_WS_URL",
    os.getenv("HASHKEY_WS_URL", "wss://stream-glb.hashkey.com/quote/ws/v2"),
)
HASHKEY_GLOBAL_REST_URL = os.getenv(
    "HASHKEY_GLOBAL_REST_URL",
    os.getenv("HASHKEY_REST_URL", "https://api-glb.hashkey.com"),
)
HASHKEY_GLOBAL_REST_POLL_INTERVAL_MS = int(
    os.getenv(
        "HASHKEY_GLOBAL_REST_POLL_INTERVAL_MS",
        os.getenv("HASHKEY_REST_POLL_INTERVAL_MS", "200"),
    )
)
HASHKEY_GLOBAL_REST_RATE_LIMIT_RPS = float(
    os.getenv(
        "HASHKEY_GLOBAL_REST_RATE_LIMIT_RPS",
        os.getenv("HASHKEY_REST_RATE_LIMIT_RPS", "1.5"),
    )
)

# Backward compatibility aliases
HASHKEY_WS_URL = HASHKEY_GLOBAL_WS_URL
HASHKEY_REST_URL = HASHKEY_GLOBAL_REST_URL
HASHKEY_REST_POLL_INTERVAL_MS = HASHKEY_GLOBAL_REST_POLL_INTERVAL_MS
HASHKEY_REST_RATE_LIMIT_RPS = HASHKEY_GLOBAL_REST_RATE_LIMIT_RPS

# 1b. Hashkey HK Settings — served from the HK platform hosts with site=HK
HASHKEY_HK_WS_URL = os.getenv(
    "HASHKEY_HK_WS_URL", "wss://stream-pro.hashkey.com/quote/ws/v2"
)
HASHKEY_HK_REST_URL = os.getenv("HASHKEY_HK_REST_URL", "https://api-pro.hashkey.com")
HASHKEY_HK_REST_POLL_INTERVAL_MS = int(
    os.getenv("HASHKEY_HK_REST_POLL_INTERVAL_MS", "200")
)
HASHKEY_HK_REST_RATE_LIMIT_RPS = float(
    os.getenv("HASHKEY_HK_REST_RATE_LIMIT_RPS", "1.5")
)

# 1c. Hashkey MENA (UAE) Settings — served from the HK platform hosts with site=MENA
HASHKEY_MENA_WS_URL = os.getenv(
    "HASHKEY_MENA_WS_URL", "wss://stream-pro.hashkey.com/quote/ws/v2"
)
HASHKEY_MENA_REST_URL = os.getenv(
    "HASHKEY_MENA_REST_URL", "https://api-pro.hashkey.com"
)
HASHKEY_MENA_REST_POLL_INTERVAL_MS = int(
    os.getenv("HASHKEY_MENA_REST_POLL_INTERVAL_MS", "200")
)
HASHKEY_MENA_REST_RATE_LIMIT_RPS = float(
    os.getenv("HASHKEY_MENA_REST_RATE_LIMIT_RPS", "1.5")
)
# Delay between consecutive (sequential) funding rate queries
HASHKEY_MENA_FUNDING_RATE_DELAY_MS = int(
    os.getenv("HASHKEY_MENA_FUNDING_RATE_DELAY_MS", "500")
)

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
