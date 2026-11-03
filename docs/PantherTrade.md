PantherTrade | REST API_V1.0
1. Introduction
PantherTrade (Hong Kong) Limited is a virtual asset trading platform licensed by the Securities and Futures Commission ("SFC") of Hong Kong, which conducts Type 1 (Dealing in Securities) and Type 7 (Providing Automated Trading Services) regulated activities under the Securities and Futures Ordinance (SFO).

The PantherTrade REST API enables developers to programmatically access market data, execute trades, and manage account information on the PantherTrade platform. It uses standard HTTP methods, response codes, and JSON for data formatting.
With this API, you can:
- Access market data
- Execute trades and manage orders
- Process deposits and withdrawals
- Retrieve account information and transaction history

Note: Access to certain API features may be contingent upon your account type and permissions. If you encounter any issues, please contact your PantherTrade implementation manager or PantherTrade support.

2. Getting Started
After opening real accounts, you can get started with your API.
This section covers the essential information you need to start using the PantherTrade REST API, including environments, authentication, request structure, and rate limits.

2.1 General Introduction
2.1.1 Environments
PantherTrade provides two types of client portal: 
- Web portal: Manage accounts, trade, users, and API keys.
- Rest API: Get quotes, trade, deposit, and withdraw.
Each client portal has two separate environments: 
- UAT environment: The UAT environment is designed for testing purposes. You can develop and test without affecting your real accounts. The UAT environment requires separate API credentials from the production environment. To gain access to UAT resources, please contact your account manager. 
- Production environment: The production environment is designed for live trading with real assets. 
Note: Before engaging in actual trading, ensure you are familiar with the platform's functionality and have conducted sufficient testing in the UAT environment.

| . | Web Portal Address | Rest API Base URL |
| --- | --- | --- |
| UAT Environment | web-portal-uat.panthertrade.com | web-api-uat.panthertrade.com |
| Production Environment | web-portal.panthertrade.com | web-api.panthertrade.com |


2.1.2 HTTP Method
PantherTrade Rest API supports the following HTTP methods:

| Method | Description | 
| --- | --- |
| GET | Retrieve resources |
| POST | Create resources or perform actions|
| DELETE | Remove resources |

2.2 Authentication
PantherTrade uses API keys and a signature mechanism for request authentication.

2.2.1 Obtaining API Keys
<Skipped>

2.2.2 Creating a Signature

To authenticate your requests, you need to create a signature for each API call:
1. Construct the string to sign:
```
var message = timestamp + method + requestPath + body
//GET: "1739429329GET/v1/accounts/111"
//POST: "1739429329POST/v1/accounts{}"
```
  - timestamp is a Unix timestamp in seconds.
  - method is the HTTP method in uppercase.
  - requestPath is the path of the API endpoint.
  - body is the request body (omit if there's no body).

2. Generate the signature using HMAC-SHA256:
```
var crypto = require("crypto"); // Node.js
var message = timestamp + method + requestPath + body 
var hmac = crypto.createHmac("sha256", secret_key)
var signature = hmac.update(message).digest("base64")
```

2.2.3 Sending Requests

1. Prepare headers for your API requests. The headers must include:
  - PT-ACCESS-KEY: Your API Access Key.
  - PT-SIGNATURE: The generated signature.
  - PT-TIMESTAMP: Request timestamp (in seconds).
  - PT-Passphrase: Your API Passphrase.
2. Send a GET request to the URL {base-url}/{endpoint}?{query-parameters} with headers.
  - {base-url}: Refer to 2.1 Environments.
  - {endpoint}: Refer to 2.3 API Endpoints Overview (e.g., /v1/accounts/{account_id}/orders).
  - {query-parameters}: Optional parameters, preceded by ? and separated by &.
3. Send a POST/DELETE request to the URL {base-url}/{endpoint} with headers and body.
  - {base-url}: Refer to 2.1 Environments.
  - {endpoint}: Refer to 2.3 API Endpoints Overview (e.g., /v1/accounts/{account_id}/orders).
  - body: Refer to the body parameters of each API. For POST/DELETE requests, parameters must be included in the request body instead of appending them at the end of the URL.

2.3 API Endpoints Overview
API Category
API Name
Method
Endpoint
Description
Permission
Rate Limit

### Products & Quotes
List Trading Pairs
GET
/v1/products
Get all tradable trading pairs
View
2 rps/IP

Get Trading Pair
GET
/v1/products/{product_symbol}
Get specific trading pair information
View
2 rps/IP

Get Order Book
GET
/v1/products/{product_symbol}/orderbook
Get an order book for a specific trading pair
View
2 rps/IP

Get Product OHLC Data
GET
/v1/products/{product_symbol}/ohlc
Get OHLC data for a specific trading pair
View
2 rps/IP

List Currencies
GET
/v1/currencies
Retrieves a list of all supported currencies and info.
View
2 rps/IP

Get Currency
GET
/v1/currencies/{currency_symbol}
Retrieves information for a specific currency.
View
2 rps/IP

### Accounts
List Accounts
GET
/v1/accounts
Get a list of accounts
View
2 rps/IP

Get Account
GET
/v1/accounts/{account_id}
Get specific account information
View
2 rps/IP

Create Account
POST
/v1/accounts
Create a new account
Manage
2 rps/IP

Get Account Balances
GET
/v1/accounts/{account_id}/balances
Get balances for a specific account
View
2 rps/IP

Get EOD Balances
GET
/v1/accounts/{account_id}/balances/eod
Get EOD balances for a specific account
View
2 rps/IP

Get Account Transactions
GET
/v1/accounts/{account_id}/transactions
Get detailed fund information for a specific account
View
2 rps/IP

### Orders
Create Order
POST
/v1/accounts/{account_id}/orders
Create a new order for a specific account
Trade
10 rps/IP

List Orders
GET
/v1/accounts/{account_id}/orders
Get an order list for a specific account
View
2 rps/IP

Get Order
GET
/v1/accounts/{account_id}/orders/{order_id}
Get specific order information for an account
View
2 rps/IP

Cancel Order
DELETE
/v1/accounts/{account_id}/orders/{order_id}
Cancel a specific unfilled order for an account
Trade
10 rps/IP

List Fills
GET
/v1/accounts/{account_id}/fills
Get trade execution records for a specific account
View
2 rps/IP

### Internal Transfers
Create Internal Transfer
POST
/v1/accounts/{source_account_id}/internal_transfer/{destination_account_id}
Initiates an internal fund transfer between two accounts owned by the same entity
Transfer
2 rps/IP

### Crypto Transfers
Get Crypto Deposit Info
GET
/v1/accounts/{account_id}/deposits/crypto/info
Get deposit information for a specific account
View
2 rps/IP

Withdraw Crypto
POST
/v1/accounts/{account_id}/withdrawals/crypto
Initiate crypto withdrawal for a specific account
Transfer
2 rps/IP

Get Whitelisted Addresses
GET
/v1/accounts/{account_id}/whitelisted_addresses
Get whitelisted addresses for a specific account
View
2 rps/IP

### Fiat Transfers
List Fiat Funding Channels
GET
/v1/entities/funding_channels
Retrieves a list of entity's funding channels
View
2 rps/IP

Withdraw Fiat
POST
/v1/accounts/{account_id}/withdrawals/fiat
Initiate a fiat withdrawal
Transfer
2 rps/IP

Get Fiat Withdrawal

GET
/v1/accounts/{account_id}/withdrawals/fiat/{fiat_withdrawal_id}
Retrieve details for a single fiat withdrawal order
View
2 rps/IP

### Users
List Users
GET
/v1/entities/users
Get the current entity's permission role information
View
2 rps/IP

List Account Users
GET
/v1/accounts/{account_id}/users
Get permission role information for a specific account
View
2 rps/IP

> PantherTrade implements IP-based rate limiting. rps/IP means the maximum request times per second per IP.

3. Products & Quotes
3.1 List Trading Pairs
Description
Retrieves a list of all available trading pairs and their information.
Request
Endpoint
/v1/products
Method
GET
Response Parameters

Parameter Name
Type
Required
Example
Description
Response Body
object[]

product_symbol
string
R
BTC-USD
The unique identifier for the trading pair

type
string
R
spot
The type of trading pair (e.g., spot, futures)

market_status

string

R
active
Current market status of the trading pair:
- active: Normal trading
- cooling-off: Temporary restrictions on orders significantly deviating from market price
- paused: Trading temporarily suspended due to maintenance or abnormal activity

base_currency
string
R
BTC
The base currency of the trading pair

quote_currency
string
R
USD
The quote currency of the trading pair

base_increment

string
R
0.00001
The smallest allowed increment for the base currency quantity

quote_increment
string
R
0.00001
The smallest allowed increment for the quote currency amount

hk_pi_permission
boolean

R

false
Indicates if the currency is restricted to Hong Kong Professional Investors (PI) only. 
trueonly HK PI can trade
falseall investors can trade

base_min_size
string
R
0.01
The minimum order quantity for an order. 

base_max_size_limit
string
R
32
The maximum order quantity for a limit order. 

base_max_size_market
string
R
32
The maximum order quantity for a market order. 

3.2 Get Trading Pair
Description
Retrieves information for a specific trading pair.
Request
Endpoint
/v1/products/{product_symbol}
Method
GET
Request Parameters

Parameter Name
Type
Required
Example
Description
Path params
product_symbol
string
R
BTC-USD
The unique identifier for the trading pair
Response Parameters

Parameter Name
Type
Required
Example
Description
Response Body

product_symbol
string
R
BTC-USD
The unique identifier for the trading pair

type
string
R
spot
The type of trading pair (e.g., spot, futures)

market_status
string

R
active

Current market status of the trading pair:
- active: Normal trading
- cooling-off: Temporary restrictions on orders significantly deviating from market price
- paused: Trading temporarily suspended due to maintenance or abnormal activity

base_currency
string
R
BTC
The base currency of the trading pair

quote_currency
string
R
USD
The quote currency of the trading pair

base_increment
string
R
0.00001
The smallest allowed increment for the base currency quantity

quote_increment
string
R
0.00001
The smallest allowed increment for the quote currency amount

hk_pi_permission
boolean
R
false
Indicates if the currency is restricted to Hong Kong Professional Investors (PI) only. 
trueonly HK PI can trade
falseall investors can trade

base_min_size
string
R
0.01
The minimum order quantity for an order. 

base_max_size_limit
string
R
32
The maximum order quantity for a limit order. 

base_max_size_market
string
R
32
The maximum order quantity for a market order. 

3.3 Get Order Book
Description
Retrieves order book information for a specific trading pair. PantherTrade offers 20 levels of aggregated order book data (Orders at the same price are combined.). 
HTTP interface calling should be under frequency limits. For more real-time market data, please use the WebSocket Feed.
Request
Endpoint
/v1/products/{product_symbol}/orderbook
Method
GET
Request Parameters

Parameter Name
Type
Required
Example
Description
Path Params
product_symbol
string
R
BTC-USD
The unique identifier for the trading pair
Query Params
depth

int

O
1
Order book depth (1-20 level)
If no order book depth is specified, the API returns only the best bid and best ask prices.
Response Parameters

Parameter Name

Type
Required
Example
Description
Response Body

product_symbol

string
R
BTC-USD
The unique identifier for the trading pair

bids
object[]
price
string
R
96999.98
Bid price


size
string
R
12.429
Bid quantity

asks
object[]
price
string
R
96999.99
Ask price


size
string
R
0.123
Ask quantity

sequence

string
R
1344
Order book sequence number
A monotonically increasing integer  that identifies each update of the order book.

time

timestampms
R
1739519298323
Generation time of the current order book data

3.4 Get OHLC Data
Retrieves OHLC (Open, High, Low, Close) data for a specific trading pair.
Request
Endpoint
/v1/products/{product_symbol}/ohlc
Method
GET
Request Parameters

Parameter Name
Type
Required
Example
Description
Path Params
product_symbol
string
R
BTC-USD
The unique identifier for the trading pair
Query Params
interval

string
O
1m

OHLC data time interval
Must be one of the following values: 
1m,5m,15m,30m,1H,4H,8H,12H,1d,1w,1M

start_time

timestampms

O
1739519238323
Start time of the data range (timestamp in milliseconds)
- If start and end times are specified, the response includes OHLC data points within the specified range,  including the start and end times.
- If start and end times are not specified, the API ignores these parameters and returns the most recent candlestick's data.

end_time
timestampms
O
1739519258323
End time of the data range (timestamp in milliseconds)
Response Parameters

Parameter Name
Type
Required
Example
Description
Response Body
object[]
low
string
R
96699.98
Lowest price in the interval

high
string
R
96999.98
Highest price in the interval

open
string
R
96889.98
Opening price of the interval

close
string
R
96999.98
Closing price of the interval

volume
string
R
789.123
Trading volume in the interval

open_time
timestampms
R
1739519220000
Open time of the candlestick

close_time
timestampms
R
1739519280000
Close time of the candlestick

Note:
- The candlestick data is arranged in chronological order.
- A single request can return a maximum of 300 OHLC data points. If you want more than 300 data points, you can make multiple requests.  In subsequent requests, set the start_time parameter to the end_time of the last data point from the previous response.
- Historical data may be incomplete, with some periods missing data due to lack of trading activity.


11. Websocket
PantherTrade provides Websocket API for you to get stream data. 2 steps to use the websocket api:
1. Create connections with the PantherTrade server.
2. Subscribe or unsubscribe to the data you want.
Rate Limits
Phase
Limit
Pre-Connection (during wss:// handshake)
3 requests/second/IP
Post-Connection
20 requests/second/IP
Additional Constraints:
- Maximum 50 active connections per Entity.
Automatic Disconnection
- Pre-Authentication:
  - Connections that fail to complete the login process within 10 seconds after establishment will be terminated automatically.
- Post-Authentication:
  - Connections with no data interaction (e.g., no heartbeats or messages) for 60 seconds will be terminated automatically.

11.1 Connect and Maintain 
11.1.1 Create a connection
- UAT environment: wss://ws-api-uat.panthertrade.com/v1
- Production environment: wss://ws-api.panthertrade.com/v1
```
timestamp = int(time.time() * 1000)
message = f"{timestamp}GET/login"

def sign_message(message: str, api_secret: str) -> str:
    import hmac
    import hashlib
    import base64

    hmac_obj = hmac.new(api_secret.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(hmac_obj.digest()).decode()
```

```python ws_demo.py
import json
import time
import websocket
import threading

def sign_message(message: str, api_secret: str) -> str:
    import hmac
    import hashlib
    import base64

    hmac_obj = hmac.new(api_secret.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(hmac_obj.digest()).decode()

class WebSocket:
    def __init__(self, url: str, api_key: str, api_secret: str, passphrase: str, message_handler=None, ping_interval: int = 45):
        self.url = url
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.message_handler = message_handler
        self.ping_interval = ping_interval
        self.ws = None
        self.ws_thread = None
        self.is_connected = False
        self.stop_ping = False
        self.connected_event = threading.Event()
        self.login_event = threading.Event()

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def _on_message(self, ws, message):
        if self.message_handler:
            try:
                msg = json.loads(message)
                if not self.login_event.is_set() and msg.get('method') == 'login_ack' and msg.get('data', {}).get('status') == 'success':
                    self.login_event.set()
                self.message_handler(message)
            except Exception as e:
                print(f"\033[31mError handling message: {e}\033[0m")

    def _on_error(self, ws, error):
        print(f"\033[31mWebSocket error: {error}\033[0m")
        self.is_connected = False

    def _on_close(self, ws, close_status_code, close_msg):
        print("\033[31mWebSocket connection closed\033[0m")
        self.is_connected = False
        self.stop_ping = True

    def _on_open(self, ws):
        print("\033[32mWebSocket connection established\033[0m")
        self.is_connected = True
        self.connected_event.set()  # 设置连接就绪事件
        threading.Thread(target=self._ping_thread).start()

    def send_login(self):
        timestamp = int(time.time() * 1000)
        message = f"{timestamp}GET/login"
        signature = sign_message(message, self.api_secret)

        login_data = {
            "method": "login",
            "params": {
                "api_key": self.api_key,
                "timestamp": timestamp,
                "signature": signature,
                "passphrase": self.passphrase
            },
            "timestamp": timestamp
        }
        print(f"\033[32mLogin msg: {login_data['params']}\033[0m")
        self.ws.send(json.dumps(login_data))

    def send_subscription(self, channel: str, params: dict):
        sub_message = {
            "method": "subscribe",
            "channel": channel,
            "params": params,
            "timestamp": int(time.time() * 1000)
        }
        print(f"\033[32mSubscribe msg: {params}\033[0m")
        self.ws.send(json.dumps(sub_message))

    def _ping_thread(self):
        # 等待登录完成
        if not self.login_event.wait(timeout=5):
            print("\033[31mLogin timeout\033[0m")
            return

        while not self.stop_ping:
            if self.is_connected:
                try:
                    current_time = int(time.time() * 1000)
                    ping_message = {"method": "heartbeat", "timestamp": current_time}
                    self.ws.send(json.dumps(ping_message))
                    print(f"\033[32mPing sent with UTC time: {current_time}\033[0m")
                except Exception as e:
                    print(f"\033[31mFailed to send ping: {e}\033[0m")
                    break
            time.sleep(self.ping_interval)

    def disconnect(self):
        self.stop_ping = True
        if self.ws:
            self.ws.close()

def main():
    url = "WebSocketURL"  # todo 替换为实际的WebSocket URL

    # 认证信息
    api_key = "YourAPIKey"  # todo 替换为实际的API Key
    api_secret = "YourAPISecret"  # todo 替换为实际的API Secret
    passphrase = "YourPassphrase"  # todo 替换为实际的Passphrase

    def message_handler(message):
        print(f"\033[34mReceived message: {message}\033[0m")

    # 创建并使用WebSocket
    ws = WebSocket(url, api_key, api_secret, passphrase, message_handler)

    try:
        ws.connect()
        ws.connected_event.wait(timeout=5)
        ws.send_login()

        # 订阅行情数据
        ws.send_subscription("book", {
            "product_symbol": ["BTC-USD", "ETH-USD"],
            "depth": 5
        })

        # 订阅账户数据
        ws.send_subscription("order", {
            "account_id": ["YourAccountID"],  # todo 替换为实际的账户ID
            "product_symbol": ["BTC-USD"]
        })

        # 保持程序运行
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\033[32mClosing WebSocket connection...\033[0m")
    except Exception as e:
        print(f"\033[31mError occurred: {e}\033[0m")
    finally:
        ws.disconnect()

if __name__ == "__main__":
    main()
```

11.1.2 Authentication for Connection
- Session Authentication: Clients complete identity verification by sending a login request (login) to establish a trusted session. Must be completed within 10 seconds after connection establishment, otherwise the connection will be forcibly terminated.
- Access Control: In unauthenticated state, if the client sends any non-login requests (e.g., heartbeat, ticker subscription), the connection will be forcibly terminated.
Request Parameters
Parameter Name

Type
Required
Example
Description
method

string
R
login
Fixed value: login
params

api_key
string
R

API Access Key

signature
string
R


timestamp

timestampms
R

Request initiation time (milliseconds). Server verifies timestamp deviation ≤30 seconds.
Response Parameters
Parameter Name

Type
Required
Description
method

string
R
login_ack (Fixed response identifier)
data
status
string
R
Authentication result: success

eid
string
R
Entity ID associated with the current API Key

conn_limit
string
R
Remaining WebSocket connection quota for the current Entity
timestamp

timestampms
R
Echo of the timestamp value sent in client requests.

Demo
```
def sign_message(message: str, api_secret: str) -> str:
    import hmac
    import hashlib
    import base64

    hmac_obj = hmac.new(api_secret.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(hmac_obj.digest()).decode()
```

``` json login
{
    "method": "login",
    "params": {
        "api_key": "YourApiKey",
        "timestamp": 1747377779383,
        "signature": "YourSignature",
        "passphrase": "YourPassphrase"
    },
    "timestamp": 1747377779383
}
{
    "method": "login_ack",
    "data": {
        "status": "success",
        "eid": "I289111950",
        "conn_limit": 4
    },
    "timestamp": 1747377779383
}
```

11.1.3 Connection Maintenance
- Connection Persistence: Maintains WebSocket connection liveness to prevent closure due to prolonged inactivity.
- Active Heartbeat Mechanism: Allows clients to initiate heartbeat requests (suggested interval: 30-45 seconds). 
- Server Time Synchronization: Provides server timestamp in milliseconds for precise time alignment.
- Retry Strategy: Implements exponential backoff (2s → 4s) for up to 2 retries. If all retries fail, the connection terminates automatically.
Request Parameters
Parameter Name
Type
Required
Example
Description
id
string
R
req_12345
Unique client-generated request ID for response matching
method
string
R
heartbeat
Fixed value: heartbeat
timestamp
timestampms
R

Request timestamp (milliseconds). Server checks for ≤30s deviation.
Response Parameters
Parameter Name

Type
Required
Description
method

string
R
heartbeat_ack (Fixed response identifier)
data
server_time
timestampms
R
Current server timestamp in milliseconds (UTC timezone) when generating the response.
timestamp

timestampms
R
Echo of the timestamp value sent in client requests.

Demo
```json
{
    "method": "heartbeat",
    "timestamp": 1747377799385
}
{
    "method": "heartbeat_ack",
    "data": {
        "server_time": 1747377799411
    },
    "timestamp": 1747377799385
}
```

11.2 Subscribe
11.2.1 Subscribe
11.2.1.1 Subscription Request
Clients must send a subscribe message to initiate data stream subscriptions.
Key Rules:
1. Single-channel restriction: Each request can only subscribe to one channel
2. Parameter handling varies by channel type:
  - Ticker Channel: Union of trading pairs
  - Book Channel: Independent subscriptions per trading pair+depth
  - Balance Channel: Independent per account+currency combination
  - Order Channel: Independent per account+product combination
Request Parameters
Parameter Name

Type
Required
Example
Description
id

string
O
req_12345
Unique client-generated request ID for response matching
method

string
R
subscribe
subscribe (fixed value)
channel

string
R
orderbook
Target channel name (e.g., ticker)
params

others parameters

R
product_symbol
Channel-specific parameters (e.g., depth for order book channels)
timestamp

timestamp
R
1730096420000
Request timestamp (milliseconds). Server checks for ≤30s deviation.
Request Demo
``` json
{
  "method": "subscribe",
  "channel": "<channel_name>",
  "params": {
    // Channel-specific parameters (e.g., product_symbol, depth, account_id)
  },
  "timestamp": 1730096420000
}
```

11.2.1.2 Subscription acknowledgment.
The server returns a confirmation after processing the request.
Response Parameters
Parameter Name

Type
Required
Example
Description
id

string
O
req_12345
Unique client-generated request ID for response matching
method

string
R
subscription_ack
subscribe
channel

string
R
ticker
Subscribe to the ticker variation push.
data
ticker_subscribed
object[]
R

Channel-specific parameters
timestamp

timestamp
R
1730096420000
Echo of the timestamp value sent in client requests.
Success Response:
``` json
{
  "method": "subscription_ack",
  "channel": "<channel_name>",
  "data": {
    "subscribed": [
      // List of successfully subscribed parameters
    ]
  },
  "timestamp": 1730096420000  // Echoes client's timestamp
}
```

Error Response:
``` json
{
  "method": "error",
  "code": -100001,
  "message": "Error description",
  "channel": "<channel_name>",
  "data": {
    // Request parameters that caused the error
  },
  "timestamp": 1730096420000  // Echoes client's timestamp
}
```

11.2.2 Unsubscribe
11.2.2.1 Unsubscription Request
Clients must send an unsubscribe message to cancel a subscription.
Key Rules:
1. Precision Required: Parameters must exactly match the active subscription to succeed.
2. Single-Channel Per Request: Each request can unsubscribe from one channel only.

Request Parameters
Parameter Name

Type
Required
Example
Description
id

string
O
req_12345
Unique client-generated request ID for response matching
method

string
R
subscribe
subscribe (fixed value)
channel

string
R
orderbook
Target channel name (e.g., ticker)
params

others parameters

R
product_symbol
Channel-specific parameters (e.g., depth for order book channels)
timestamp

timestamp
R

Request timestamp (milliseconds). Server checks for ≤30s deviation.
Request Demo
```json
{
  "method": "unsubscribe",
  "channel": "<channel_name>",
  "params": {
    // Exact parameters used in the original subscription
  },
  "timestamp": 1730096420000
}
```

11.2.2.2 UnSubscription acknowledgment.
The server returns a confirmation after processing the request.
Response Parameters
Parameter Name

Type
Required
Example
Description
id

string
O
req_12345
Unique client-generated request ID for response matching
method

string
R
subscription_ack
subscribe
channel

string
R
ticker
Subscribe to the ticker variation push.
data
unsubscribed
object[]
R



remaining
object[]
R


timestamp

timestamp
R

Echo of the timestamp value sent in client requests.
Success Response:
```json
{
  "method": "unsubscription_ack",
  "channel": "<channel_name>",
  "data": {
    "unsubscribed": [
      // List of unsubscribed parameters
    ],
    "remaining": [
      // Remaining active subscriptions for the channel
    ]
  },
  "timestamp": 1730096420000  // Echoes client's timestamp
}
```

Error Response:
```json
{
  "method": "error",
  "code": -100002,
  "message": "Unsubscribe failed: No matching subscription",
  "channel": "<channel_name>",
  "data": {
    "request_params": {
      // Parameters sent in the unsubscribe request
    },
    "active_subscriptions": [
      // List of active subscriptions for the channel
    ]
  },
  "timestamp": 1730096420000  // Echoes client's timestamp
}
```

11.3 Channels
11.3.1 Trade
Update frequency
Real-time push
Request Parameters
Parameter Name

Type
Required
Example
Description
method

string
R
subscribe
Subscription action.
channel

string
R
trade
Fixed value, identifies the subscription channel type.
params

product_symbol
string[]
R

['BTC-USD','ETH-USD']

The unique identifier for the trading pair. You can obtain trading pair identifiers via REST. Format: base currency - quote currency (e.g.,ETH-USD)
timestamp

timestamp
R

Request timestamp (milliseconds). Server checks for ≤30s deviation.
Response Parameters of data.trades_subscribed
Parameter Name
Type
Required
Example
Description
product_symbol
string[]
R
['BTC-USD','ETH-USD']
Subscribed trading pair(s). 
Example (Request & Response)
Request Demo
```json
{
    "method":"subscribe",
    "channel":"trade",
    "params":{
        "product_symbol":["BTC-USD","BTC-HKD"]
    },
    "timestamp": 1730096420000
}
```

Response Demo
```json
{
    "method":"subscription_ack",
    "channel":"trade",
    "data":{
        "ticker_subscribed":[
            {"product_symbol":["BTC-USD","BTC-HKD"]}
        ],
    },
    "timestamp": 1730096420000
}
```

WS Push Content
Parameter Name

Type
Description
channel

string
trade
product_symbol

string
The unique identifier for the trading pair. 
type

string
update
data

price
string
Executed price

quantity
string
Executed quantity

taker_side
string
Side (buy or sell) of the taker (i.e., the aggressor) in the trade.

public_trade_id
string
A public, monotonically increasing numeric identifier. It is non-aggregated and unique per match, representing a single trade between exactly one taker and one maker. 

time
timestampms
Executed time
WS Push Demo
```json
{
    "channel": "trades",
    "product_symbol": "BTC-USD",
    "type": "update",
    "data": {
        "price": "88.1",
        "quantity": "0.1",
        "taker_side": "buy",
        "public_trade_id": "497385",
        "time": 1747188696494
    }
}
```

11.3.2 New Ticker
Update frequency
50 ms push once.
Request Parameters
Parameter Name

Type
Required
Example
Description
method

string
R
subscribe
Subscription action.
channel

string
R
ticker
Fixed value, identifies the subscription channel type.
params

product_symbol
string[]
R

['BTC-USD','ETH-USD']
The unique identifier for the trading pair. You can obtain trading pair identifiers via REST. Format: base currency - quote currency (e.g.,ETH-USD)
timestamp

timestamp
R

Request timestamp (milliseconds). Server checks for ≤30s deviation.
Response Parameters of data.ticker_subscribed
Parameter Name
Type
Required
Example
Description
product_symbol
string[]
R
['BTC-USD','ETH-USD']
Subscribed trading pair(s). 
Example (Request & Response)
Request Demo
```json
{
    "method":"subscribe",
    "channel":"ticker",
    "params":{
        "product_symbol":["BTC-USD","BTC-HKD"]
    },
    "timestamp": 1730096420000
}
```

Response Demo
```json
{
    "method":"subscription_ack",
    "channel":"ticker",
    "data":{
        "ticker_subscribed":[
            {"product_symbol":["BTC-USD","BTC-HKD"]}
        ],
    },
    "timestamp": 1730096420000
}
```

WS Push Content
Parameter Name

Type
Description
channel

string
ticker
product_symbol

string
The unique identifier for the trading pair. 
type

string
update
data
best_ask_price
string
Price of the best (lowest) ask level.

best_ask_quantity
string
Aggregate quantity available at the best ask price.

best_bid_price
string
Price of the best (highest) bid level.

best_bid_quantity
string
Aggregate quantity available at the best bid price.

last_trade_price
string
Price of the most recent trade.

last_trade_quantity
string
Quantity of the most recent trade, denominated in base currency.

last_taker_side
string
Side of the taker in the most recent trade:"buy"or"sell".

last_public_trade_id
string
A public, monotonically increasing numeric identifier. It is non-aggregated and unique per match, representing a single trade between exactly one taker and one maker. 

last_trade_time
timestamp (ms)
Unix timestamp (in milliseconds) of the most recent trade.

open_24h
string
Price of the first trade in the past 24 hours (rolling window)."NA"if no trades occurred.

high_24h
string
Highest trade price in the past 24 hours."NA"if no trades occurred.

low_24h
string
Lowest trade price in the past 24 hours."NA"if no trades occurred.

volume_24h
string
Total traded volume in base currency over the past 24 hours."0"if no trades occurred.
WS Push Demo
```json
{
  "channel": "ticker",
  "product_symbol": "BTC-USD",
  "type": "update",
  "data": {
    "best_ask_price": "67250.3",
    "best_ask_quantity": "2.45",
    "best_bid_price": "67249.8",
    "best_bid_quantity": "1.89",
    "last_price": "67250.0",
    "last_size": "0.12",
    "last_taker_side": "buy",
    "last_public_trade_id": "497385",
    "last_trade_time": 1730123456789,
    "open_24h": "66800.5",
    "high_24h": "67500.0",
    "low_24h": "66200.1",
    "volume_24h": "1245.67"
  }
}
```

11.3.3 Reference Price
Update frequency
Push on reference price change.
Request Parameters
Parameter Name

Type
Required
Example
Default
Description
method

string
R
subscribe
-
Subscription action.
channel

string
R
reference_price
-
Fixed value, identifies the subscription channel type.
params
product_symbol
object[]
R
Trading pair list
-
The unique identifier for the trading pair. 
timestamp

timestampms
R


Request initiation time (milliseconds). Server checks timestamp deviation ≤30 seconds.
Response Parameters of data.reference_price_subscribed
Parameter Name

Type
Required
Example
Default
Description
method

string
R
subscription_ack
-
Subscription acknowledgment.
channel

string
R
reference_price
-
Fixed value, identifies the subscription channel type.
data

reference_price_subscribed
object[]
R
Trading pair list

Subscribed trading pair(s). You can obtain trading pair identifiers via REST.
timestamp

timestampms
R


Request initiation time (milliseconds).
Example (Request & Response)
Request Demo
```json
{
    "method": "subscribe",
    "channel": "reference_price",
    "params": {
        "product_symbol": ["CAMFU-HKD", "CAMFF-USD"]
    },
    "timestamp": 1778551133947
}
```

Response Demo
```json
{
    "id": "1778551133947177000",
    "method": "subscription_ack",
    "channel": "reference_price",
    "data": {
        "reference_price_subscribed": [
            {
                "product_symbol": "CAMFF-HKD"
            },
            {
                "product_symbol": "CAMFU-USD"
            }
        ]
    },
    "timestamp": 1778551133947
}
```

WS Push Content
Parameter Name

Type
Required
Description
channel

string
R
Fixed value, identifies the subscription channel type.
product_symbol

string
R
The unique identifier for the trading pair. You can obtain trading pair identifiers via REST.
data

price_type
string
R
Price type identifier. Current enum values: NAV (post-market NAV), iNAV (real-time estimated NAV).

price
string
R
Reference price value. String, preserving full precision.

quote_currency
string
R
Quote/settlement currency (e.g., USD, USDT, EUR, CNY). RWA is typically pegged to fiat or stablecoins.

market_type
string
R
Market/source identifier. Current enum values: PRIMARY (primary market, subscription/redemption basis). 

asset_category
string
R
RWA asset category identifier. Enum values: money_fund. 

price_timestamp
timestampms
O
The actual generation/calculation timestamp of the price (milliseconds).

price_date
string
O
Valuation/NAV belonging date. Format YYYY-MM-DD. Strongly correlated with fund NAV; empty for other categories.

price_status

int
R
Price status. These statuses apply specifically to iNAV messages:
0 = normal (regular price update period). 
1 = maintenance_routine (routine maintenance period, CET Mon–Sat 23:45–23:50, Sun 23:30–23:35). 
2 = maintenance_special (special maintenance period notified by Solactive, occurring on Saturday).
WS Push Demo
Normal price update
```json
{
    "channel": "reference_price",
    "product_symbol": "CAMFF-HKD",
    "data": {
        "price_type": "iNAV",
        "price": "1.023456",
        "quote_currency": "HKD",
        "market_type": "PRIMARY",
        "asset_category": "money_fund",
        "price_timestamp": 1730096412000,
        "price_date": "2024-10-28",
        "price_status": 0
    }
}
```
Routine maintenance start
```json
{
    "channel": "reference_price",
    "product_symbol": "CAMFF-HKD",
    "data": {
        "price_type": "iNAV",
        "price": "1.023456",
        "quote_currency": "HKD",
        "market_type": "PRIMARY",
        "asset_category": "money_fund",
        "price_timestamp": 1730096412000,
        "price_date": "2024-10-28",
        "price_status": 1
    }
}
```
Special maintenance start
```json
{
    "channel": "reference_price",
    "product_symbol": "CAMFF-HKD",
    "data": {
        "price_type": "iNAV",
        "price": "1.023456",
        "quote_currency": "HKD",
        "market_type": "PRIMARY",
        "asset_category": "money_fund",
        "price_timestamp": 1730096412000,
        "price_date": "2024-10-28",
        "price_status": 2
    }
}
```

Error Message
Code

Message
Scenario


Parameter validation failed: product_symbol contains non-RWA currencies.
Subscription request includes non-RWA trading pairs.

11.3.4 Order Book
Update frequency
50 ms push once.
Request Parameters
Parameter Name

Type
Required
Example
Description
method

string
R
subscribe
Subscription action.
channel

string
R
book
Fixed value, identifies the subscription channel type.
params

product_symbol
string[]
R
['BTC-USD','ETH-USD']
The unique identifier for the trading pair. 

depth

int
O
10

Order book depth (1-20 level)
If no order book depth is specified, it returns only the best bid and best ask prices.
timestamp

timestamp
R
1730096420000
Request timestamp (milliseconds). Server checks for ≤30s deviation.
Response parameters of data.book_subscribed
Parameter Name
Type
Required
Example
Description
product_symbol
string[]
R
['BTC-USD','ETH-USD']
Subscribed trading pair(s).
depth

int
O
10
Subscribed trading pair(s) depth.

Example (Request & Response)
Request Demo
```json
{
    "method":"subscribe",
    "channel":"book",
    "params":{
        "product_symbol":["BTC-USD","BTC-HKD"],
        "depth":5
    },
    "timestamp": 1730096420000
}
```

Response Demo
```json
{
    "method":"subscription_ack",
    "channel":"book",
    "data":{
        "book_subscribed":[
            {"product_symbol":["BTC-USD","BTC-HKD"],"depth":5},
            {"product_symbol":["ETH-HKD"],"depth":10}
        ],
    },
    "timestamp": 1730096420000
}
```

WS Push Content
Parameter Name


Type
Description
channel


string
book
product_symbol


string
The unique identifier for the trading pair
type


string
snapshot update
- For type=update, only price levels with changed quantities or newly added/removed levels are included.
data

bids
[]
price
string
Bid price


quantity
string
Latest quantity at this price (overrides previous value).

asks
[]
price
string
Ask price


quantity
string
Latest quantity at this price (overrides previous value).

time

timestampms
Order book update timestamp (milliseconds).

prev_seq_id

int
Previous sequence ID for this product_symbol within the current WebSocket connection. Use this to detect message gaps:
- If prev_seq_id ≠ last received seq_id, messages may have been lost.

seq_id

int
Sequence ID for this update. Globally unique and monotonically increasing per product_symbol, but may appear non-consecutive if subscribing to partial order book depths.

WS Push Demo
snapshot
```json
{
    "channel": "book",
    "product_symbol": "BTC-HKD",
    "type": "snapshot",
    "data": {
        "bids": [
            {
                "price": "108.001",
                "qty": "9.292581"
            },
            {
                "price": "105",
                "qty": "0.1"
            },
            {
                "price": "100",
                "qty": "191.86184"
            },
            {
                "price": "88.001",
                "qty": "0.2"
            },
            {
                "price": "0.0001",
                "qty": "0.1"
            }
        ],
        "asks": [
            {
                "price": "109.001",
                "qty": "0.09"
            },
            {
                "price": "110",
                "qty": "139.079699"
            },
            {
                "price": "110.001",
                "qty": "0.100031"
            },
            {
                "price": "656083",
                "qty": "0.1"
            },
            {
                "price": "656496",
                "qty": "0.11"
            }
        ],
        "time": 1747330286713,
        "pre_seq_id": 0,
        "seq_id": 29307
    }
}
```

update
```json
{
    "channel": "book",
    "product_symbol": "BTC-HKD",
    "type": "update",
    "data": {
        "bids": [
            {
                "price": "108.001",
                "qty": "9.302581"
            }
        ],
        "asks": [],
        "time": 1747364110299,
        "pre_seq_id": 29307,
        "seq_id": 29308
    }
}
{
    "channel": "book",
    "product_symbol": "BTC-HKD",
    "type": "update",
    "data": {
        "bids": [
            {
                "price": "108.001",
                "qty": "9.292581"
            }
        ],
        "asks": [],
        "time": 1747364194947,
        "pre_seq_id": 29308,
        "seq_id": 29309
    }
}
{
    "channel": "book",
    "product_symbol": "BTC-HKD",
    "type": "update",
    "data": {
        "bids": [],
        "asks": [
            {
                "price": "109.001",
                "qty": "0.11"
            }
        ],
        "time": 1747364237917,
        "pre_seq_id": 29309,
        "seq_id": 29310
    }
}
```

11.4 WebSocket Error Code
status_code
error_code
error_message
Description
Request Format Errors

-100001
The input parameter of '%s' is invalid


-100105
Unknown input parameter of '%s'


-100001
The input parameter of '%s' is out of range. 
The parameter depth is out of range. 

-804010
Unsubscribe failed: no active subscription matches the provided parameters


-804011
Channel '%s' not subscribed

Authentication Errors
-803002
Incorrect signature
Failed to verify your signature. Please check if your signature is correct.

-803004
Invalid access key
Failed to verify your access key.  Please check your access key permission.

-803005
The access key expired
The access key has expired. Please log in to Web Portal and renew it.

-803006
Invalid passphrase
Failed to verify your passphrase. Please check your passphrase.

-803007
The timestamp you set in the request headers should be within 30 seconds from now
The server only accepts the request within the 60 seconds, from 30 seconds before to 30 seconds later.

-803008
Invalid IP
The Request Source IP doesn't match the IP whitelist for this access key. Please login to the Web Portal and add it to the IP whitelist.

-100002
No permission


-804001
Unauthorized: Login required


-804002
Connection already authorized

Connection Errors
-804101
Connection error


-804102
Connection closed due to inactivity


-804103
Connections limit exceeded (current: %d/%d)
Exceed the rate limit for each configuration. Please manage your requested quantity.