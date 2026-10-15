# Multi-Exchange Perpetual Futures Market Data Collector

A high-performance, asynchronous, containerized market data collector designed to capture and archive full-fidelity, real-time perpetual futures market data from **HashKey Global**, **Bullish**, **Bitget**, and **Gate.io**. Built in Python using `asyncio`, `websockets`, and `aiohttp`, this application gathers, normalizes, and segments market data into program-friendly JSON Lines (`.jsonl`) files.

At the end of each UTC calendar day, the program compresses the full 24-hour directory into a `.zip` archive, uploads it to AWS S3, and purges the local cache to maintain a flat disk signature on the host.

This system is engineered specifically for **downstream back-testing engines and virtual exchanges**.

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Co-Routines (asyncio)
        HK_COL[Hashkey Collector]
        BL_COL[Bullish Collector]
        BG_COL[Bitget Collector]
        GT_COL[Gate Collector]
    end

    subgraph Data Flow
        HK_COL -->|Unified Records| Writer[MarketDataWriter]
        BL_COL -->|Unified Records| Writer
        BG_COL -->|Unified Records| Writer
        GT_COL -->|Unified Records| Writer
        
        Writer -->|Line-buffered write| Cache[(Local Disk Cache)]
    end

    subgraph Chron Job / Archive
        Uploader[MarketDataUploader] -->|Polls hourly for past days| Cache
        Uploader -->|Zips past day| Zip[Temp .zip]
        Zip -->|Uploads to S3| S3[(AWS S3 Bucket)]
        S3 -->|Success| Clean[Purge local cache & temp zip]
    end
    
    style S3 fill:#FF9900,stroke:#fff,stroke-width:2px,color:#000
    style Cache fill:#118888,stroke:#fff,stroke-width:2px,color:#fff
```

### Key Design Pillars:
1. **Abstracted Collector Core**: Uses a modular, inherited design (`BaseExchangeCollector`) that implements generalized WebSocket handling, connection recovery with exponential backoff, and REST polling.
2. **Config as the Single Symbol Source**: Each exchange's target symbols are listed in `config.py` / env vars using that exchange's *native* names (e.g. Bitget `BTCUSDT`, Gate.io `BTC_USDT`, HashKey `BTCUSDT-PERPETUAL`). They are used verbatim for subscriptions, REST polling and the output folder names; collectors perform no symbol translation.
3. **Fault Tolerance & Self-Healing**: Connections use robust reconnection loops with exponential backoff.
4. **Rate Limit & IP Block Protection**: Incorporates an `AsyncRateLimiter` to keep REST queries under the official API limits for each exchange. It also detects HTTP 429 errors and automatically enforces a global 60-second backoff across polling coroutines.
5. **Data Integrity**: File writes are **line-buffered** (`buffering=1`). In the event of a system or container crash, data is already committed to disk and will not be lost.
6. **Dynamic Day Transitions**: At exactly `00:00:00 UTC`, the writer closes active file handles for the completed day and opens handles for the new day, avoiding race conditions.
7. **Zero-Maintenance Disk Signature**: Completed days are zipped, uploaded to S3, and deleted locally. If the container goes offline, it automatically retroactively zips and uploads any missed days once it restarts.

---

## 📂 Directory & Zip Structure

The zipped file uploaded to S3 contains the following program-friendly nested hierarchy:

```text
20260618.zip (1 calendar day, UTC)
└── 20260618/
    ├── hashkey/            # HashKey Hong Kong (site=HK)
    │   ├── BTCUSDT-PERPETUAL/
    │   │   └── futures/
    │   │       ├── kline_1m.jsonl
    │   │       ├── trades.jsonl
    │   │       ├── depth.jsonl
    │   │       ├── bbo.jsonl
    │   │       └── orderbook_rest.jsonl
    │   └── ...
    ├── hashkey_global/     # HashKey Global (same layout)
    ├── hashkey_mena/       # HashKey MENA / UAE (same layout, plus funding_rate.jsonl)
    ├── bullish/
    │   ├── BTCUSDT-PERPETUAL/
    │   │   └── futures/
    │   │       └── ...
    │   └── ...
    ├── bitget/
    │   ├── BTCUSDT/
    │   │   └── futures/
    │   │       └── ...
    │   └── ...
    └── gate/
        ├── BTC_USDT/
        │   └── futures/
        │       └── ...
        └── ...
```

---

## 📊 Collected Streams & Normalized Schemas

Every line in the `.jsonl` file is a valid self-contained JSON object. All files share a **unified metadata header**, standard **normalized fields** at the top level, and the unmodified raw payload under the `"raw"` key.

### Common Header Fields (Unified):
```json
{
  "timestamp": 1781568000000,
  "datetime": "2026-06-18T16:00:00.000000Z",
  "exchange": "hashkey", // HK; or "hashkey_global", "hashkey_mena", "bitget", "gate", "osl"
  "symbol": "BTCUSDT-PERPETUAL",
  "market_type": "futures",
  "category": "<stream_category>"
}
```

### 1. WS Kline (`category: "kline_1m"`)
Real-time 1-minute candlestick bar updates.
```json
{
  "timestamp": 1781774280000,
  "datetime": "2026-06-18T17:18:00.000000Z",
  "exchange": "hashkey",
  "symbol": "BTCUSDT-PERPETUAL",
  "market_type": "futures",
  "category": "kline_1m",
  "open_time": 1781774280000,
  "close_time": 1781774339999,
  "open": 64405.3,
  "high": 64405.3,
  "low": 64405.3,
  "close": 64405.3,
  "volume": 0.0,
  "raw": { ... }
}
```

### 2. WS Trade (`category: "trades"`)
Full tick execution stream of every trade matching on the order book.
```json
{
  "timestamp": 1781774280000,
  "datetime": "2026-06-18T17:18:00.000000Z",
  "exchange": "hashkey",
  "symbol": "BTCUSDT-PERPETUAL",
  "market_type": "futures",
  "category": "trades",
  "price": 64405.3,
  "quantity": 0.015,
  "side": "sell",
  "trade_id": "12345678",
  "raw": { ... }
}
```

### 3. WS Depth (`category: "depth"`)
Real-time order book level changes.
```json
{
  "timestamp": 1781773472970,
  "datetime": "2026-06-18T17:04:32.970000Z",
  "exchange": "hashkey",
  "symbol": "BTCUSDT-PERPETUAL",
  "market_type": "futures",
  "category": "depth",
  "bids": [[64335.9, 1.0], [64335.5, 2.0]],
  "asks": [[64349.2, 2.0]],
  "version": "29161378_1",
  "raw": { ... }
}
```

### 4. WS BBO (`category: "bbo"`)
Top of order book Best Bid / Offer (level 1 depth) updates.
```json
{
  "timestamp": 1781773496239,
  "datetime": "2026-06-18T17:04:56.239000Z",
  "exchange": "hashkey",
  "symbol": "BTCUSDT-PERPETUAL",
  "market_type": "futures",
  "category": "bbo",
  "bid_price": 64335.5,
  "bid_quantity": 2.0,
  "ask_price": 64369.3,
  "ask_quantity": 746.0,
  "version": "29161416_18",
  "raw": { ... }
}
```

### 5. REST Order Book (`category: "orderbook_rest"`)
High-frequency order book snapshot fetched via REST API (by default every 200 ms).
```json
{
  "timestamp": 1781772441368,
  "datetime": "2026-06-18T16:47:21.368000Z",
  "exchange": "hashkey",
  "symbol": "BTCUSDT-PERPETUAL",
  "market_type": "futures",
  "category": "orderbook_rest",
  "bids": [[64483.6, 2.0], [64482.6, 1.0]],
  "asks": [[64483.8, 2.0]],
  "raw": { ... }
}
```

### 6. REST Funding Rate (`category: "funding_rate"`, Hashkey MENA only)
Current funding rate per perpetual, polled sequentially via `GET /api/v2/futures/fundingRate` with a 500 ms delay between symbols. `timestamp` is the query time.
```json
{
  "timestamp": 1789365000000,
  "datetime": "2026-09-14T05:50:00.000000Z",
  "exchange": "hashkey_mena",
  "symbol": "BTCUSDT-PERPETUAL",
  "market_type": "futures",
  "category": "funding_rate",
  "rate": 0.0001,
  "next_funding_time": 1789372800000,
  "raw": { ... }
}
```

---

### OSL (API v5)

OSL is collected from the v5 public API (IP limit: 1800 weight/min at 1 weight per call, so the default `OSL_REST_RATE_LIMIT_RPS=2.0` is well inside it): WS `ticker` -> `bbo`, `books15` -> `depth`, `trade` -> `trades`,
and REST `/kline` -> `kline_1m_rest`. All OSL data is `spot`. See [ADR 0003](docs/adr/0003-osl-v5-collector.md).

---

## 🛠️ Configuration (.env)

Adjust parameters by copying `.env.example` to `.env` or setting system environment variables.

Symbols are exchange-native and used verbatim ([ADR 0002](docs/adr/0002-config-is-the-single-symbol-source.md)); the HashKey site naming is in [ADR 0001](docs/adr/0001-per-exchange-symbols-and-hashkey-site-naming.md).

| Key | Description | Default |
|---|---|---|
| `S3_BUCKET_NAME` | S3 bucket where zipped archives will be uploaded | `your-market-data-bucket` |
| `S3_REGION` | AWS Region of S3 bucket | `ap-east-1` |
| `S3_PREFIX` | S3 folder prefix where day packages are stored | `crypto-market-data/` |
| `LOCAL_DATA_DIR` | Directory on disk where raw data is temporarily cached | `./local_cache` |
| `UPLOAD_DELAY_MINUTES` | Wait minutes after UTC midnight before archiving the past day | `5` |
| `HASHKEY_GLOBAL_TARGET_SYMBOLS` | Comma-separated target symbols for Hashkey Global (`hashkey_global`). | `BTCUSDT-PERPETUAL,ETHUSDT-PERPETUAL` |
| `HASHKEY_HK_TARGET_SYMBOLS` | Comma-separated HashKey-native target symbols for Hashkey HK (`hashkey`) | `BTCUSD,BTCUSDT,ETHUSD,ETHUSDT,SOLUSD,AVAXUSD,XRPUSD,LINKUSD,ARBUSD,USDTUSD,USDTHKD` |
| `HASHKEY_MENA_TARGET_SYMBOLS` | Comma-separated HashKey-native target symbols for Hashkey MENA (`hashkey_mena`) | `BTCUSDT-PERPETUAL,ETHUSDT-PERPETUAL,SKHYNIXUSDT-PERPETUAL,QQQUSDT-PERPETUAL,SPCXUSDT-PERPETUAL,SOXLUSDT-PERPETUAL,USDTUSDC,USDTAED` |
| `BITGET_TARGET_SYMBOLS` | Comma-separated Bitget instIds (`BTCUSD` is routed to COIN-FUTURES, everything else to USDT-FUTURES) | `BTCUSDT,ETHUSDT` |
| `GATE_TARGET_SYMBOLS` | Comma-separated Gate.io contract names (`BTC_USD` uses the btc settle endpoint, others usdt) | `BTC_USDT,ETH_USDT,BTC_USD` |
| `OSL_TARGET_SYMBOLS` | Comma-separated OSL v5 spot symbols (`BTCUSDC` does not exist on v5). Unknown symbols produce no WS data and REST kline errors | `BTCUSD,USDTUSD` |
| `OSL_WS_URL` / `OSL_REST_URL` | OSL v5 public WebSocket and REST base URL (REST polling reads `/kline`) | `wss://stream-hk.osl.com/ws/v5/public` / `https://trade-hk.osl.com/api/v5` |
| `HASHKEY_GLOBAL_WS_URL` / `HASHKEY_GLOBAL_REST_URL` | Hashkey Global endpoints. Fall back to legacy `HASHKEY_WS_URL` / `HASHKEY_REST_URL` | `wss://stream-glb.hashkey.com/quote/ws/v2` / `https://api-glb.hashkey.com` |
| `HASHKEY_GLOBAL_REST_POLL_INTERVAL_MS` | Frequency of Hashkey Global REST depth requests in milliseconds. Falls back to legacy `HASHKEY_REST_POLL_INTERVAL_MS` | `200` |
| `HASHKEY_GLOBAL_REST_RATE_LIMIT_RPS` | Global safety cap of requests per second for Hashkey Global REST queries. Falls back to legacy `HASHKEY_REST_RATE_LIMIT_RPS` | `1.5` |
| `HASHKEY_HK_WS_URL` | Hashkey HK WebSocket URL (HK platform host; `site=HK` is sent on every subscription) | `wss://stream-pro.hashkey.com/quote/ws/v2` |
| `HASHKEY_HK_REST_URL` | Hashkey HK REST base URL (`site=HK` is sent on every request) | `https://api-pro.hashkey.com` |
| `HASHKEY_HK_REST_POLL_INTERVAL_MS` | Frequency of Hashkey HK REST depth requests in milliseconds | `200` |
| `HASHKEY_HK_REST_RATE_LIMIT_RPS` | Global safety cap of requests per second for Hashkey HK REST queries. HK and MENA share one host/IP, so budget `HK + MENA` against the documented 5 rps query limit | `1.5` |
| `HASHKEY_MENA_WS_URL` | Hashkey MENA (UAE) WebSocket URL (HK platform host; `site=MENA` is sent on every subscription) | `wss://stream-pro.hashkey.com/quote/ws/v2` |
| `HASHKEY_MENA_REST_URL` | Hashkey MENA (UAE) REST base URL (HK platform host; `site=MENA` is sent on every request) | `https://api-pro.hashkey.com` |
| `HASHKEY_MENA_REST_POLL_INTERVAL_MS` | Frequency of Hashkey MENA REST depth requests in milliseconds | `200` |
| `HASHKEY_MENA_REST_RATE_LIMIT_RPS` | Global safety cap of requests per second for Hashkey MENA REST queries | `1.5` |
| `HASHKEY_MENA_FUNDING_RATE_DELAY_MS` | Delay between sequential Hashkey MENA funding rate queries (one perpetual per query) | `500` |
| `BITGET_REST_POLL_INTERVAL_MS` | Frequency of Bitget REST depth requests in milliseconds | `200` |
| `BITGET_REST_RATE_LIMIT_RPS` | Global safety cap of requests per second for Bitget REST queries | `2.0` |
| `GATE_REST_POLL_INTERVAL_MS` | Frequency of Gate.io REST depth requests in milliseconds | `200` |
| `GATE_REST_RATE_LIMIT_RPS` | Global safety cap of requests per second for Gate.io REST queries | `2.0` |

---

## 🚀 Running Locally & via Docker

### Running Locally

1. Create and source virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Launch application:
   ```bash
   python main.py
   ```

### Running with Docker Compose

Build and run the background data collector container:
```bash
docker-compose up -d --build
```

View real-time logs:
```bash
docker-compose logs -f
```

Stop the container safely (flushes active file buffers):
```bash
docker-compose down
```
