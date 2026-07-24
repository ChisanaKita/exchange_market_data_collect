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
2. **Unified Symbols & Output**: Translates exchange-specific symbols (e.g., `BTC_USDT`, `BTC-USDT-PERP`, `BTCUSDT`) into a standard unified scheme (`BTCUSDT-PERPETUAL`) for storage, ensuring downstream consumers get identical data shapes regardless of the source exchange.
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
    ├── hashkey/
    │   ├── BTCUSDT-PERPETUAL/
    │   │   └── futures/
    │   │       ├── kline_1m.jsonl
    │   │       ├── trades.jsonl
    │   │       ├── depth.jsonl
    │   │       ├── bbo.jsonl
    │   │       └── orderbook_rest.jsonl
    │   └── ...
    ├── bullish/
    │   ├── BTCUSDT-PERPETUAL/
    │   │   └── futures/
    │   │       └── ...
    │   └── ...
    ├── bitget/
    │   ├── BTCUSDT-PERPETUAL/
    │   │   └── futures/
    │   │       └── ...
    │   └── ...
    └── gate/
        ├── BTCUSDT-PERPETUAL/
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
  "exchange": "hashkey", // or "bullish", "bitget", "gate"
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

---

## 🛠️ Configuration (.env)

Adjust parameters by copying `.env.example` to `.env` or setting system environment variables.

| Key | Description | Default |
|---|---|---|
| `S3_BUCKET_NAME` | S3 bucket where zipped archives will be uploaded | `your-market-data-bucket` |
| `S3_REGION` | AWS Region of S3 bucket | `ap-east-1` |
| `S3_PREFIX` | S3 folder prefix where day packages are stored | `crypto-market-data/` |
| `LOCAL_DATA_DIR` | Directory on disk where raw data is temporarily cached | `./local_cache` |
| `UPLOAD_DELAY_MINUTES` | Wait minutes after UTC midnight before archiving the past day | `5` |
| `HASHKEY_REST_POLL_INTERVAL_MS` | Frequency of Hashkey REST depth requests in milliseconds | `200` |
| `HASHKEY_REST_RATE_LIMIT_RPS` | Global safety cap of requests per second for Hashkey REST queries | `1.5` |
| `BULLISH_REST_POLL_INTERVAL_MS` | Frequency of Bullish REST depth requests in milliseconds | `200` |
| `BULLISH_REST_RATE_LIMIT_RPS` | Global safety cap of requests per second for Bullish REST queries | `2.0` |
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
