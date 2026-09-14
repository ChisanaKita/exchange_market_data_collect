# OVERVIEW

## Introduction

**Welcome to HashKey MENA Exchange API Documentation!**

**Rest API**

Our REST API offers a simple and secure way to manage orders and monitor your digital asset portfolios. The REST API can be publicly access endpoints via market data endpoints and private authenticated endpoints for trading, funding and account data which require requests to be signed.

**Websocket API**

Use an asynchronous method (pub/sub) approach to efficiently deliver push notifications for orders, transactions, market and other pertinent information. By subscribing to specific topics of interest, users can receive real-time updates without the need for constant polling.

## Test our sandbox

Please direct any questions or feedback to [ [[email protected]](/cdn-cgi/l/email-protection#81e6edeee3e0edace0f1e8c1e9e0f2e9eae4f8afe2eeec) ] to obtain sandbox account.

📘 All 2FA/SMS/Email verification code is defaulted to "123456" in Sandbox environment for ease of use

**1. Go to our sandbox website page:**

📘 [https://global.sim.hashkeydev.com/ae/en-AE](https://global.sim.hashkeydev.com/ae/en-AE)

**2. Go to Settings -&gt; API Management -&gt; Create API**

**3. Enter API Key name, select API permission and setup IP Access Restriction**

**4. Choose authentication mode** * **HMAC (system-generated)** : the system issues an Access key and Secret key. * **Ed25519 (self-generated)** : generate an Ed25519 key pair locally, create an API Key with **Self-generated** , and upload the full PEM public key ( `-----BEGIN PUBLIC KEY-----` ... `-----END PUBLIC KEY-----` ). After creation, the page shows **Access Key** (use as `X-APIKEY` ) and **Public Key** . Keep the private key yourself - HashKey never receives it.

## Technical Support

**General Inquiry**

Operating hours: Monday to Friday, 9:00 AM to 6:00 PM HKT

Preferred method of contact： [[email protected]](/cdn-cgi/l/email-protection#8aede6e5e8ebe6a7ebfae3cae2ebf9e2e1eff3a4e9e5e7)

Please provide your inquiry in the following format:

Subject:

Environment: Production / Sandbox Inquiry

Identity: UID / Email

Request Body:

Question:

**Emergency Production Trading issue**

Operating hours: 7 * 24

For urgent matters during non-office hours, please log in to hashkey.com and contact our online Customer Support team via instant message widget.

## Announcement

### MENA Service Migration

**Effective: 2026.06.16**

To unify and strengthen our infrastructure, the MENA (UAE) service is being merged into the HashKey HK platform. The MENA API documentation remains separate; only the underlying services are consolidated. Please coordinate with your technical team to make the following adjustments.

**1. Domain Change** (REST &amp; WebSocket)

The MENA API domains are switching from `api-glb` / `stream-glb` to `api-pro` / `stream-pro` , aligning with the HK platform.

| Environment   | Type      | Old Domain                      | New Domain                      |
|---------------|-----------|---------------------------------|---------------------------------|
| Sandbox       | REST      | `api-glb.sim.hashkeydev.com`    | `api-pro.sim.hashkeydev.com`    |
| Sandbox       | WebSocket | `stream-glb.sim.hashkeydev.com` | `stream-pro.sim.hashkeydev.com` |
| Production    | REST      | `api-glb.hashkey.com`           | `api-pro.hashkey.com`           |
| Production    | WebSocket | `stream-glb.hashkey.com`        | `stream-pro.hashkey.com`        |

**2. Spot Order Endpoint Change**

The unified spot order endpoints (consistent with the HK platform) are now recommended:

- Create Order: `/api/v1.1/spot/order`
- Create Multiple Orders: `/api/v1.1/spot/batchOrders`

The previous MENA-specific endpoints `/api/v1/spot/new/order` and `/api/v1/spot/batch-orders` remain functional for MENA accounts, but are no longer documented. We recommend migrating to the unified endpoints above.

**3. MarketPlace Public Stream Topic Change**

For the MarketPlace public stream, the subscription `topic` values have been renamed:

- `rfqs` → `rfqs-mena`
- `quotes` → `quotes-mena`

Please update your subscription requests accordingly.

**4. Market Data** **`site`** **Parameter**

To support querying market data across sites after the merger, an optional `site` parameter is added to market data interfaces:

- **REST requests:** An optional `site` parameter (enum: `MENA` , `HK` ; defaults to `HK` if not specified) is supported on all market data endpoints. In addition, the `/api/v1/exchangeInfo` response now returns a `site` field (enum: `hk` , `mena` ).
- **WebSocket (V1 &amp; V2):** An optional `site` parameter (enum: `MENA` , `HK` ; defaults to `HK` if not specified) can be included when subscribing to public market data streams, and every pushed message now includes a `site` field (enum: `hk` , `mena` ).

This parameter is optional and fully backward compatible; existing requests that omit it will continue to work as before.

We are committed to providing a superior and more secure service. Thank you for your understanding and cooperation. If you have any questions, please do not hesitate to contact our technical support team.

### API Parameter Rules Update

**Effective Apr 30, 2026**

To further enhance the stability and security of our API services, we are updating the parameter rules for all signed endpoints (such as order creation, cancellation, etc.) on **Apr 30, 2026** .

Please forward this notice to your technical team to make the necessary adjustments to your implementation.

**1.** **`timestamp`** **Parameter Change**

- **Now Mandatory:** All requests sent to signed endpoints must now include the `timestamp` parameter.
- **Format Requirement:** The `timestamp` must be a **13-digit, millisecond-level Unix timestamp** . Any requests missing this parameter or with an incorrect format will be rejected.

**2.** **`recvWindow`** **Parameter Change**

- **Validation Added:** The system will now validate the `recvWindow` parameter.
- **Default Value:** If you do not send the `recvWindow` parameter, the system will automatically default to **5000** (5 seconds).
- **Maximum Value:** The value of `recvWindow` must not exceed **8000** (8 seconds). Any requests exceeding this limit will be rejected.

**Recommended Actions**

We recommend that you:

1. Immediately review and update your API request logic to ensure the correct transmission of the `timestamp` parameter.
2. Review your use of `recvWindow` to ensure its value is within 8 seconds for optimal system performance and security.

We are committed to providing a superior and more secure service. Thank you for your understanding and cooperation.

If you have any questions, please do not hesitate to contact our technical support team.

# AGENT SKILLS

## Agent Skills Overview

Hashkey Skills is an agent skill pack for HashKey API that helps teams launch trading automation with a **SIM sandbox-first** workflow, explicit execution guardrails, and multi-site compatibility.

## Why Hashkey Skills

API docs describe endpoints. Skills describe goal-oriented execution.

- Faster onboarding: map user intent directly to stable workflows instead of re-reading endpoint docs every time.
- Safer execution: shared runtime rules enforce draft -&gt; confirmation -&gt; execute-once flow for write actions.
- Multi-site aware: explicit behavior for `glb` / `hk` / `sg` / `uae` , including endpoint and header differences.
- Production-minded defaults: sandbox-first, redaction rules, 2FA handling, and least-privilege guidance.

## What Is Included

- `hashkey-public-market` : read-only market data queries.
- `hashkey-spot-trading` : spot order workflows with pre-check and confirmation.
- `hashkey-futures-trading` : GLB-first futures order, position, leverage, and trading-stop workflows.
- `hashkey-account` : account, trade history, and internal transfer flows.
- `hashkey-wallet` : deposit/withdraw/allowlist workflows with strict safety controls.
- `hashkey-otc-trading` : OTC MarketPlace RFQ/quote workflows for supported sites.
- `hashkey-skills-installer` : one-click installer for local skill directories and credentials template.
- `hashkey-runtime-rules.md` : shared runtime policy imported by all skills.
- `hashkey-site-profiles.md` : multi-site compatibility matrix (GLB/HK/SG/UAE).
- Site-level feature availability (including OTC) follows `hashkey-site-profiles.md` and `SITE_COMPATIBILITY.md` .

## Repository Layout

- `skills/hashkey-*/SKILL.md` : intent-driven domain skills.
- `skills/hashkey-runtime-rules.md` : machine-loaded security and execution policy.
- `skills/hashkey-site-profiles.md` : machine-loaded site/environment compatibility facts.
- `skills/hashkey-skills-installer/scripts/install.sh` : local installation helper.
- `SECURITY.md` : threat model and operational controls.
- `SITE_COMPATIBILITY.md` : human-readable multi-site overview.

## Repository Download

Download the full package directly:

- [Download](../../hashkey-skills.zip) [`hashkey-skills.zip`](../../hashkey-skills.zip)

## Install: Choose Your Agent Target

```
# Run from repository root.
# Cursor only bash skills/hashkey-skills-installer/scripts/install.sh --target cursor # Codex only bash skills/hashkey-skills-installer/scripts/install.sh --target codex # Agent CLI style directory bash skills/hashkey-skills-installer/scripts/install.sh --target agent # Custom directory used by your IDE/runtime bash skills/hashkey-skills-installer/scripts/install.sh --target-dir " $HOME /.agent/skills"
# If `--target` is not provided, installer keeps backward compatibility by defaulting to `both` (`codex` + `cursor`) and prints a selection tip.
```

The installer supports multiple target directories. Pick only what you need.

- Cursor: `~/.cursor/skills`
- Codex: `~/.codex/skills`
- Agent CLI style: `~/.agent/skills`
- Custom IDE path: any folder via `--target-dir`

## SIM Sandbox First (Recommended)

Start in HashKey sim sandbox before any production usage:

- `glb` sandbox REST: `https://api-glb.sim.hashkeydev.com`
- `hk` / `sg` / `uae` sandbox REST: `https://api-pro.sim.hashkeydev.com`

For futures workflows in this package, use `site=glb` with the GLB sandbox endpoint first.

```
bash skills/hashkey-skills-installer/scripts/install.sh --target agent --setup-credentials --site hk
```

With credential setup:

Credentials are stored in a local secure profile with restricted permissions. Runtime output must never disclose the exact credential file location.

## Runtime Modes

### Mode A: Direct AK/SK (default)

- Credentials from env vars or local secure credential profile.
- No dedicated middle layer is required.

## Manual Credentials JSON (User Config)

If you prefer manual configuration, use the sample file:

- credentials.sample.json

Steps:

1. Copy it to your local secure location (do not commit real secrets).
2. Fill `environment` , `site` , `api_key` , `secret_key` manually.
3. Keep file permissions restricted to your local user only.
4. Never paste full keys into chat or logs.

## Risk Notice

- Hashkey Skills is a support and tooling layer only and does not constitute advice, solicitation or a recommendation to transact.
- Users remain solely responsible for reviewing outputs, verifying draft actions and making and authorizing their own decisions.
- Any action-related functionality is subject to applicable permissions, controls, approvals and platform rules.
- Digital assets are high risk and highly volatile; losses may be substantial, and leveraged or derivative transactions may result in rapid liquidation and losses exceeding expectations.
- Test in sandbox first where available, use least-privilege API credentials, and verify all live actions carefully before confirmation.
- AI-generated outputs may be inaccurate or outdated and should not be solely relied upon.
- The feature is subject to HashKey's applicable terms of use, risk disclosure statements and other applicable disclosures.

See `SECURITY.md` for full controls and operational policy.

## Disclaimer

Hashkey Skills is a user support and interface feature. It may provide information, summaries and other support outputs and, where applicable, may facilitate the submission of user-authorized instructions, in each case subject to applicable permissions, controls, approvals and platform rules. Hashkey Skills and any outputs made available through it are provided to you on an "as is" and "as available" basis, without representation or warranty of any kind. It does not constitute investment, financial, legal, tax, trading or any other form of advice, and does not constitute or represent any solicitation, invitation, endorsement or recommendation to buy, sell or hold any assets or to enter into any transaction; nor does it guarantee the accuracy, timeliness, completeness, reliability or fitness for purpose of any data, content, analysis, summary or other output presented through the feature. Your use of Hashkey Skills and any information or output provided in connection with this feature is at your own risk, and you are solely responsible for reviewing and evaluating any information or output provided through HashKey Skills and for all decisions, instructions, transactions and other actions made or taken by you or on your behalf. Hashkey Skills does not provide portfolio management, discretionary account management, robo-advisory or algorithmic trading services, and does not independently determine whether, when, how or on what terms you should transact. Where functionality is made available to facilitate the submission or processing of user instructions, such functionality is limited to user-authorized actions and remains subject to applicable permissions, controls, approvals, restrictions and platform rules. Hashkey does not endorse or guarantee any AI-generated information, output, summary or analysis. Any AI-generated information, output, summary or analysis should not be solely relied on for decision making. AI-generated content may include or reflect information, views and opinions of third parties, and may be incomplete, inaccurate, delayed, biased or outdated. To the fullest extent permitted by applicable law, Hashkey is not responsible or liable for any losses, damages, costs or expenses incurred as a result of or in connection with your use of, inability to use, or reliance on the Hashkey Skills feature or any output made available through it. Hashkey may modify, suspend or discontinue the Hashkey Skills feature at its discretion, and availability or functionality may vary by jurisdiction, region, user type, account status or user profile. Digital asset prices are subject to high market risk and price volatility. The value of your investment may go down or up, and you may lose some or all of the amount invested. You are solely responsible for your investment and trading decisions and Hashkey is not liable for any losses you may incur subject to applicable law. Past performance is not a reliable predictor of future performance. You should only invest in products you are familiar with and where you understand the risks. You should carefully consider your investment experience, financial situation, investment objectives and risk tolerance and consult an independent professional adviser prior to making any investment or trading decision. Your use of Hashkey Skills is subject to this feature-specific disclaimer and to Hashkey's applicable terms of use, client agreements, risk disclosures, product disclosures and other applicable terms, conditions and warnings, each as amended from time to time. These documents should be read together. Nothing in this disclaimer or in the Hashkey Skills feature limits or overrides any mandatory legal or regulatory protections that cannot lawfully be excluded. This material should not be construed as advice.

# REST API

## Get Started

Python [POST] Order Submit sample

```
import time
import base64
import requests
import hashlib
import hmac
import json
from urllib.parse import urlencode
from cryptography.hazmat.primitives import serialization
"""
####################################################################################################################################
# Test REST API
#
# Copyright: Hashkey Trading 2025 All rights reserved.
# Please note the API code is provided "As Is" basis, without warranty of any kind, either express or implied, including
# without limitation, warranties that the API code is free of defects, merchantable, non-infringing or fit for a particular purpose
####################################################################################################################################
"""
class RestAPIClient : def __init__ ( self , base_url , user_key , sign_type = "HMAC" , user_secret = None , private_key_pem = None , private_key_passphrase = None ): """
        Initialize the RestAPIClient.

        Args:
            base_url (str): The base URL of the API.
            user_key (str): Access Key (sent as X-APIKEY).
            sign_type (str): "HMAC" (default) or "ED25519".
            user_secret (str): HMAC secret key. Required when sign_type="HMAC".
            private_key_pem (bytes|str): Ed25519 PKCS#8 PEM private key.
                Required when sign_type="ED25519".
            private_key_passphrase (bytes|str): Passphrase for an encrypted private key.
                Use None if the private key is unencrypted.
        """ self . base_url = base_url self . user_key = user_key self . sign_type = sign_type . upper () self . user_secret = user_secret self . private_key = None self . headers = { 'X-APIKEY' : user_key , 'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8' , } if self . sign_type == "ED25519" : if private_key_pem is None : raise ValueError ( "private_key_pem is required when sign_type=ED25519" ) if isinstance ( private_key_pem , str ): private_key_pem = private_key_pem . encode ( "utf-8" ) if isinstance ( private_key_passphrase , str ): private_key_passphrase = private_key_passphrase . encode ( "utf-8" ) self . private_key = serialization . load_pem_private_key ( private_key_pem , password = private_key_passphrase ) elif self . sign_type == "HMAC" : if not user_secret : raise ValueError ( "user_secret is required when sign_type=HMAC" ) else : raise ValueError ( "sign_type must be HMAC or ED25519" ) def get_timestamp ( self ): """
        Get the current timestamp in milliseconds.

        Returns:
            int: The current timestamp.
        """ return int ( time . time () * 1000 ) def create_signature ( self , content ): """
        Create request signature.

        Args:
            content (str): totalParams to be signed.

        Returns:
            str: HMAC hex digest, or Ed25519 Base64 signature.
        """ content_bytes = content . encode ( 'utf-8' ) if self . sign_type == "ED25519" : signature = self . private_key . sign ( content_bytes ) return base64 . b64encode ( signature ). decode ( "ascii" ) return hmac . new ( self . user_secret . encode ( 'utf-8' ), content_bytes , hashlib . sha256 ). hexdigest () def place_order ( self , symbol , side , order_type , quantity , price = None ): """
        Place an order.

        Args:
            symbol (str): The trading pair symbol (e.g., BTCUSDT).
            side (str): The order side (BUY or SELL).
            order_type (str): The order type (LIMIT or MARKET).
            quantity (str): The order quantity.
            price (str, optional): The order price (required for LIMIT orders).

        Returns:
            dict or None: The JSON response if successful, None otherwise.
        """ timestamp = self . get_timestamp () data = { "symbol" : symbol , "side" : side , "type" : order_type , "price" : price , "quantity" : quantity , "timestamp" : timestamp } if order_type == 'MARKET' : del data [ 'price' ] data_string = urlencode ( data ) signature = self . create_signature ( data_string ) data [ 'signature' ] = signature response = requests . post ( f " { self . base_url } /api/v1.1/spot/order" , headers = self . headers , data = data ) if response . status_code == 200 : response_json = response . json () print ( "Response:" ) print ( json . dumps ( response_json , indent = 4 )) # Print formatted JSON response return response_json else : try : error_json = response . json () print ( "Error:" ) print ( json . dumps ( error_json , indent = 4 )) # Print formatted error response except json . JSONDecodeError : print ( f "Error: { response . status_code } - { response . text } " ) return None
if __name__ == '__main__' : # For Production account please change base_url to https://api-pro.hashkey.com # Set use_ed25519 = True to sign with Ed25519 instead of HMAC use_ed25519 = True if use_ed25519 : with open ( "ed25519_private.pem" , "rb" ) as f : private_key_pem = f . read () api_client = RestAPIClient ( base_url = "https://api-pro.sim.hashkeydev.com" , user_key = "your_access_key" , sign_type = "ED25519" , private_key_pem = private_key_pem , private_key_passphrase = "your_passphrase" # or None if unencrypted ) else : api_client = RestAPIClient ( base_url = "https://api-pro.sim.hashkeydev.com" , user_key = "your_access_key" , sign_type = "HMAC" , user_secret = "your_secret_key" ) # Place an order with the desired parameters api_client . place_order ( "BTCUSDT" , "BUY" , "LIMIT" , "0.01" , "85000" )
```

Python [GET] Account balance sample

```
import time
import base64
import requests
import hashlib
import hmac
import json
from cryptography.hazmat.primitives import serialization
"""
####################################################################################################################################
# Test REST API
#
# Copyright: Hashkey Trading 2025 All rights reserved.
# Please note the API code is provided "As Is" basis, without warranty of any kind, either express or implied, including
# without limitation, warranties that the API code is free of defects, merchantable, non-infringing or fit for a particular purpose
####################################################################################################################################
"""
class RestAPIClient : def __init__ ( self , base_url , user_key , sign_type = "HMAC" , user_secret = None , private_key_pem = None , private_key_passphrase = None ): """
        Initialize the RestAPIClient.

        Args:
            base_url (str): The base URL of the API.
            user_key (str): Access Key (sent as X-APIKEY).
            sign_type (str): "HMAC" (default) or "ED25519".
            user_secret (str): HMAC secret key. Required when sign_type="HMAC".
            private_key_pem (bytes|str): Ed25519 PKCS#8 PEM private key.
                Required when sign_type="ED25519".
            private_key_passphrase (bytes|str): Passphrase for an encrypted private key.
                Use None if the private key is unencrypted.
        """ self . base_url = base_url self . user_key = user_key self . sign_type = sign_type . upper () self . user_secret = user_secret self . private_key = None self . headers = { 'X-APIKEY' : user_key , 'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8' , } if self . sign_type == "ED25519" : if private_key_pem is None : raise ValueError ( "private_key_pem is required when sign_type=ED25519" ) if isinstance ( private_key_pem , str ): private_key_pem = private_key_pem . encode ( "utf-8" ) if isinstance ( private_key_passphrase , str ): private_key_passphrase = private_key_passphrase . encode ( "utf-8" ) self . private_key = serialization . load_pem_private_key ( private_key_pem , password = private_key_passphrase ) elif self . sign_type == "HMAC" : if not user_secret : raise ValueError ( "user_secret is required when sign_type=HMAC" ) else : raise ValueError ( "sign_type must be HMAC or ED25519" ) def get_timestamp ( self ): """
        Get the current timestamp in milliseconds.

        Returns:
            int: The current timestamp.
        """ return int ( time . time () * 1000 ) def create_signature ( self , content ): """
        Create request signature.

        Args:
            content (str): totalParams to be signed.

        Returns:
            str: HMAC hex digest, or Ed25519 Base64 signature.
        """ content_bytes = content . encode ( 'utf-8' ) if self . sign_type == "ED25519" : signature = self . private_key . sign ( content_bytes ) return base64 . b64encode ( signature ). decode ( "ascii" ) return hmac . new ( self . user_secret . encode ( 'utf-8' ), content_bytes , hashlib . sha256 ). hexdigest () def get_account_info ( self ): """
        Get account information.

        Returns:
            dict or None: The JSON response if successful, None otherwise.
        """ timestamp = self . get_timestamp () data = { "timestamp" : timestamp } query_string = '&' . join ([ f " { key } = { value } " for key , value in data . items ()]) signature = self . create_signature ( query_string ) response = requests . get ( f " { self . base_url } /api/v1/account? { query_string } &signature= { signature } " , headers = self . headers ) if response . status_code == 200 : response_json = response . json () print ( "Response:" ) print ( json . dumps ( response_json , indent = 4 )) # Print formatted JSON response return response_json else : try : error_json = response . json () print ( "Error:" ) print ( json . dumps ( error_json , indent = 4 )) # Print formatted error response except json . JSONDecodeError : print ( f "Error: { response . status_code } - { response . text } " ) return None
if __name__ == '__main__' : # For Production account please change base_url to https://api-pro.hashkey.com # Set use_ed25519 = True to sign with Ed25519 instead of HMAC use_ed25519 = True if use_ed25519 : with open ( "ed25519_private.pem" , "rb" ) as f : private_key_pem = f . read () api_client = RestAPIClient ( base_url = "https://api-pro.sim.hashkeydev.com" , user_key = "your_access_key" , sign_type = "ED25519" , private_key_pem = private_key_pem , private_key_passphrase = "your_passphrase" # or None if unencrypted ) else : api_client = RestAPIClient ( base_url = "https://api-pro.sim.hashkeydev.com" , user_key = "your_access_key" , sign_type = "HMAC" , user_secret = "your_secret_key" ) # Get account information api_client . get_account_info ()
```

**Sandbox Environment**

- Restful URL: `https://api-pro.sim.hashkeydev.com`
- WebSocket: `wss://stream-pro.sim.hashkeydev.com`
- Website: [https://global.sim.hashkeydev.com/ae](https://global.sim.hashkeydev.com/ae/en-AE)

**Production Environment**

- Restful URL: `https://api-pro.hashkey.com`
- WebSocket: `wss://stream-pro.hashkey.com`
- Website: [https://global.hashkey.com/ae](https://global.hashkey.com/ae)

**General API Information**

- All **responses** will return a JSON object or array.
- Data is returned in **ascending** order with the earlier data displayed first and subsequent updates appearing later
- All time or timestamp-related variables are measured in milliseconds (ms)
- `HTTP 4XX` error code indicate that the request content is invalid. This typically originates from the client's end.
- `HTTP 429` error code indicates that the request rate limit has been exceeded.
- `HTTP 418` error code when our server have detected the IP address continues to send subsequent requests after receiving `429` error code and is automatically blocked
- `HTTP 5XX` indicates an internal system error. This signifies that the issue originates within the trading system. When addressing this error, it's important not to immediately categorise it as a failed task. The execution status is uncertain, it could potentially be either successful or unsuccessful.
- For **GET** endpoints, parameters must be sent as query strings.
- For **POST** , **PUT** , and **DELETE** endpoints, unless explicitly stated otherwise, parameters must be sent as query strings or in the request body with the content type set to `application/x-www-form-urlencoded` .
- Request Parameters can be sent in any order.
- If there are parameters in both query string and request body, only the parameters of query string will be used.

**Access Restrictions**

- If any rate limit is violated, a `429` error code will be returned
- Each API endpoint has an associated with a specific weight, and certain endpoints may possess varying weights based on different parameters. Endpoints that consume more resources will have a higher weight assigned to them.
- Upon receiving `429` error code, please take precautionary steps to cease sending requests. API abuse is strictly prohibited
- It is recommended to use Websocket API to obtain corresponding real-time data as much as possible to reduce the traffic of access restrictions caused by frequent API requests.

**Order Rate Limiting**

- Unless explicitly stated otherwise, each API Key has a default rate limit of 5 requests per second for query-related endpoints, while order-related endpoints allow 20 requests per second.
- When the number of orders exceeds the set limit, a response with an HTTP CODE 429 will be received. Please wait 1 minute for the suspended period to expire.

**Endpoint Security Types**

- Each endpoint is assigned a security type that determines how you interact with it.
- The API-KEY must be passed in the REST API header as **X-APIKEY** .
- API-KEY is case-sensitive. For HMAC keys, SECRET-KEY is also case-sensitive.
- By default, API-KEY have access to all secure endpoints.

**API-KEY Management**

- Users have to log in the exchange website and apply for an API-KEY. Two authentication modes are supported:
    - **HMAC (system-generated)**
        - **Access key** : API access key
        - **Secret key** : System-generated key used for HMAC SHA256 signature (visible only at creation time)
    - **Ed25519 (self-generated)**
        - Generate an Ed25519 key pair locally, then create an API Key on the Web portal with **Self-generated** and upload the full PEM public key (see [Authentication](#Ed25519-Signature) ).
        - After creation, the page shows **Access Key** (use as `X-APIKEY` ) and **Public Key** (the uploaded public key).
        - Keep the private key securely on your side. HashKey never receives or stores the private key.
        - Use your private key to produce the Ed25519 `signature` ( **Base64** recommended; Hex also accepted).
- Users have to assign permissions to API-KEY. There are two kinds of permissions,
    - **READ-ONLY PERMISSION** : read permission is used for data query interfaces such as order query, transaction query, etc.
    - **READ/WRITE PERMISSION** : read-write permission is used for order placing, order cancelling, including transfer permission whereby user can transfer between subaccounts under the same main trading account.
- **API key validity period** : The validity period of an API key is **90** days. To reduce the security threat posed by idle credentials, any API key that remains unused for 90 consecutive days will be automatically deactivated by the system. Each time an API key is used to make a request, its validity period is reset to 90 days. Please regularly review your keys to ensure critical ones remain active.
- Both private REST and WebSocket modes require users to authenticate the transaction through the API-KEY passed in the API header. Refer to the following Authentication chapter for the signature algorithm of the API-KEY.

## Authentication

### Endpoint security type

API requests are likely to be tampered during transmission through the internet. To ensure that the request remains unchanged, all private interfaces other than public interfaces (basic information, market data) must be verified by signature authentication via API-KEY to make sure the parameters or configurations are unchanged during transmission.

Each created API-KEY need to be assigned with appropriate permissions in order to access the corresponding interface. Before using the interface, users is required to check the permission type for each interface and confirm there is appropriate permissions.

| Authentication Type   | Description                                              |
|-----------------------|----------------------------------------------------------|
| NONE                  | Endpoints are freely accessible                          |
| TRADE                 | Endpoints requires sending a valid API-KEY and signature |
| USER_DATA             | Endpoints requires sending a valid API-KEY and signature |
| USER_STREAM           | The endpoints requires sending a valid API-KEY           |
| MARKET_DATA           | The endpoints requires sending a valid API-KEY           |

### Signature Authentication

#### Signature

TRADE &amp; USER\_DATA

- The SIGNED (signature required) endpoint needs to send a parameter, `signature` , in the **query string** or **request body** .
- `totalParams` refers to the concatenation of the query string and the request body. Both signing methods below use the same `totalParams` payload.
- Two signature methods are supported. Use the method that matches how the API Key was created:

| Method          | Key material                                                                 | Signature encoding                          | Notes                                    |
|-----------------|------------------------------------------------------------------------------|---------------------------------------------|------------------------------------------|
| **HMAC SHA256** | System-generated                                                             | Hex string                                  | Existing method; remains fully supported |
| **Ed25519**     | Client-generated private key (public key uploaded when creating the API Key) | **Base64** (recommended); Hex also accepted | Self-generated mode                      |

All signed HTTP requests to API endpoints require authentication and authorization.

The following headers should be added to all signed HTTP requests:

| Key      | Value      | Type   | Description                        |
|----------|------------|--------|------------------------------------|
| X-APIKEY | Access Key | string | The API Access Key you applied for |

The following parameters should be added to all signed HTTP requests:

| Key       | Value                            | Type   | Description                                                                                                                                                                          |
|-----------|----------------------------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| timestamp | Millisecond-level Unix timestamp | string | Must be a 13-digit, millisecond-level Unix timestamp. Any requests missing this parameter or with an incorrect format will be rejected.                                              |
| signature | Signature string                 | string | HMAC: hex digest of HMAC SHA256( `secretKey` , `totalParams` ). Ed25519: encode the Ed25519 signature over the UTF-8 bytes of `totalParams` as **Base64** (recommended) or **Hex** . |

When placing an Ed25519 Base64 `signature` in the query string, percent-encode `+` , `/` , and `=` (e.g. `+` → `%2B` ). Otherwise `+` may be decoded as a space and signature verification will fail.

##### HMAC SHA256

- Use your `secretKey` as the HMAC key and `totalParams` as the value. The result is a **hex** string.
- HMAC signature is not case sensitive.

***Example 1: In queryString***

- queryString:

```
symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000
```

- HMAC SHA256 signature:

```
echo -n "symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000" | openssl dgst -sha256 -hmac "lH3ELTNiFxCQTmi9pPcWWikhsjO04Yoqw3euoHUuOLC3GYBW64ZqzQsiOEHXQS76"
```

Shell standard output:

```
5f2750ad7589d1d40757a55342e621a44037dad23b5128cc70e18ec1d1c3f4c6
```

- curl command:

```
curl -H "X-APIKEY: tAQfOrPIZAhym0qHISRt8EFvxPemdBm5j5WMlkm3Ke9aFp0EGWC2CGM8GHV4kCYW" -X POST 'https://$HOST/api/v1/spot/order?symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000&signature=5f2750ad7589d1d40757a55342e621a44037dad23b5128cc70e18ec1d1c3f4c6'
```

***Example 2: In the request body***

- requestBody:

```
symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000
```

- HMAC SHA256 signature:

```
echo -n "symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000" | openssl dgst -sha256 -hmac "lH3ELTNiFxCQTmi9pPcWWikhsjO04Yoqw3euoHUuOLC3GYBW64ZqzQsiOEHXQS76"
```

Shell standard output:

```
5f2750ad7589d1d40757a55342e621a44037dad23b5128cc70e18ec1d1c3f4c6
```

- curl command:

```
curl -H "X-APIKEY: tAQfOrPIZAhym0qHISRt8EFvxPemdBm5j5WMlkm3Ke9aFp0EGWC2CGM8GHV4kCYW" -X POST 'https://$HOST/api/v1/spot/order' -d 'symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000&signature=5f2750ad7589d1d40757a55342e621a44037dad23b5128cc70e18ec1d1c3f4c6'
```

***Example 3: mixing queryString and request body***

- queryString:

```
symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC
```

- requestBody:

```
quantity=1&price=0.1&recvWindow=5000×tamp=1538323200000
```

- HMAC SHA256 signature:

```
echo -n "symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTCquantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000" | openssl dgst -sha256 -hmac "lH3ELTNiFxCQTmi9pPcWWikhsjO04Yoqw3euoHUuOLC3GYBW64ZqzQsiOEHXQS76"
```

Shell standard output:

```
885c9e3dd89ccd13408b25e6d54c2330703759d7494bea6dd5a3d1fd16ba3afa
```

- curl command:

```
curl -H "X-APIKEY: tAQfOrPIZAhym0qHISRt8EFvxPemdBm5j5WMlkm3Ke9aFp0EGWC2CGM8GHV4kCYW" -X POST 'https://$HOST/openapi/v1/order?symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC' -d 'quantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000&signature=885c9e3dd89ccd13408b25e6d54c2330703759d7494bea6dd5a3d1fd16ba3afa'
```

Note the difference in Example 3, where there is no &amp; between "GTC" and "quantity = 1".

##### Ed25519

**Setup steps**

1. Generate an Ed25519 key pair locally (private key + public key). Keep the private key securely on your side.
2. On the Web portal, go to **API Management** → **Create API** , and choose **Self-generated** (Ed25519).
3. Paste your **full PEM public key** into the form. The public key **must** include the header and footer lines: `-----BEGIN PUBLIC KEY-----` and `-----END PUBLIC KEY-----` .
4. After the API Key is created successfully, the page displays:
    - **Access Key** - this is your API Key. Send it in the request header as `X-APIKEY` .
    - **Public Key** - the public key you uploaded (for reference).
5. Verification flow: the client signs `totalParams` with the **private key** to produce `signature` ; HashKey verifies the signature with the stored **public key** . If verification succeeds, the request is authenticated.
6. HashKey never receives or stores your private key. Only the public key is uploaded and kept on HashKey's side.

**Signing rules**

- Sign the UTF-8 bytes of `totalParams` with your Ed25519 private key (PKCS#8 PEM).
- Encode the raw signature bytes as **Base64** (recommended) or **Hex** , then send it as the `signature` parameter.
- Ed25519 Base64 signatures are case sensitive.

**Generate key pair (OpenSSL)**

Recommended method to generate Ed25519 key pair. For security, protect the private key with a passphrase ( `-aes-256-cbc` ).

```
# 1. Generate private key (encrypted with passphrase; OpenSSL will prompt for it) openssl genpkey -algorithm ed25519 -aes-256-cbc -out ed25519_private.pem # Optional: pass the passphrase non-interactively (avoid this in shared shells / CI logs)
# openssl genpkey -algorithm ed25519 -aes-256-cbc -pass pass:YOUR_PASSPHRASE -out ed25519_private.pem
# 2. Export public key (will prompt for the private-key passphrase) openssl pkey -in ed25519_private.pem -pubout -out ed25519_public.pem # Optional: export public key non-interactively
# openssl pkey -in ed25519_private.pem -passin pass:YOUR_PASSPHRASE -pubout -out ed25519_public.pem
```

Keep the passphrase secure. HashKey never receives your private key or passphrase. When signing API requests, load the private key with the same passphrase.

Example public key format to upload:

-----BEGIN PUBLIC KEY-----  
MCowBQYDK2VwAyEA...  
-----END PUBLIC KEY-----

Python example (Ed25519)

```
import base64
from cryptography.hazmat.primitives import serialization
def create_ed25519_signature ( total_params : str , private_key_pem : bytes , passphrase : bytes = None ) -> str : # passphrase: bytes of the private-key passphrase, or None if the key is unencrypted private_key = serialization . load_pem_private_key ( private_key_pem , password = passphrase ) signature = private_key . sign ( total_params . encode ( "utf-8" )) return base64 . b64encode ( signature ). decode ( "ascii" )
```

***Example: Ed25519 signature (queryString)***

- queryString / totalParams:

```
symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000
```

- curl command (percent-encode the Base64 `signature` in the URL):

```
curl -H "X-APIKEY: <your_access_key>" -X POST 'https://$HOST/api/v1/spot/order?symbol=ETHBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1538323200000&signature=<base64_signature>'
```

#### Time-base security

📘 If your timestamp is ahead of serverTime it needs to be within 1 second + serverTime

The logic of this parameter is as follows:

```
if ( timestamp < ( serverTime + 1000 ) && ( serverTime - timestamp ) <= recvWindow ) // process request } else { // reject request }
```

📘 A relatively small recvWindow (5000 or less) is recommended!

- For a SIGNED endpoint, an additional parameter "timestamp" needs to be included in the request. This timestamp is in milliseconds and reflect the time when the request was initiated.
- An optional parameter (not mandatory) `recvWindow` can be used to specify the validity period of the request in milliseconds. If recvWindow is not sent as part of the request, the default value is **5000** and the max value is **8000**
- Trading and timeliness are closely interconnected. Network can sometimes be unstable or unreliable, which can lead to inconsistent times when requests are sent to the server.
- With recvWindow, you can specify how many milliseconds the request is valid, otherwise it will be rejected by the server.

## Spot Trading

**Order Status**

- PENDING\_NEW - Pending order to be NEW
- NEW - New order, pending to be filled
- PARTIALLY\_FILLED - Partially filled
- PARTIALLY\_CANCELED - Partially filled and Partially cancelled
- FILLED - Completed filled
- CANCELED - Order cancelled
- REJECTED - Order refers to the rejection of an order during the order matching process.

**Order Types**

- LIMIT - Limit order
- MARKET - Market order
- LIMIT\_MAKER - Maker limit order

**Order Direction**

- BUY - Buy order
- SELL - Sell Order

**TimeInForce**

- GTC（Currently only supports limit and limit\_maker orders)
- IOC（Currently supports limit and market orders)

### Create Order v1.1

**POST** `/api/v1.1/spot/order`

📘 Note: Supports specifying both the cash amount and the quantity for market orders, regardless of whether it's a buy or sell order

Certain parameters are mandatory depending on the order `type` :

| Type        | Mandatory parameters   |
|-------------|------------------------|
| LIMIT       | quantity, price        |
| MARKET      | quantity or amount     |
| LIMIT_MAKER | quantity, price        |

**Weight: 1**

**Request Parameters**

| **PARAMETER**    | **TYPE**   | Req'd   | **DESCRIPTION**                                                                                                                                                                                                                                                                                                                                                               |
|------------------|------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol           | STRING     | Y       | Name of instrument   e.g. "BTCUSD", "ETHUSD"                                                                                                                                                                                                                                                                                                                                  |
| side             | ENUM       | Y       | BUY or SELL                                                                                                                                                                                                                                                                                                                                                                   |
| type             | ENUM       | Y       | Currently offer 3 order types:  - LIMIT - Limit order   - MARKET - Market order   - LIMIT\_MAKER - Maker Limit order                                                                                                                                                                                                                                                          |
| quantity         | DECIMAL    | C       | Order quantity in units of the instrument  - Limit order: Represents the amount of the base asset you want to buy or sell.   For example: BTC/USD pair, if quantity is 0.5, you're ordering 0.5 BTC  - Market order: Represents the amount of the base asset to buy or sell   For example: BTC/USDT pair, if quantity is 0.5, you're buying 0.5 BTC worth at the market price |
| amount           | DECIMAL    | C       | Cash amount in the units of quote asset. Market order only  - Market order: Represents the amount of the quote asset you want to use for the trade   For example: For BTC/USD pair, if amount = 1000, you are placing a MARKET buy order to purchase BTC using 1000 USD at the current market price.                                                                          |
| price            | DECIMAL    | C       | Required for LIMIT and LIMIT_MAKER order                                                                                                                                                                                                                                                                                                                                      |
| newClientOrderId | STRING     |         | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request. (up to 255 characters)                                                                                                                                                                                                                                        |
| timeInForce      | ENUM       |         | **"GTC"** for Limit order &amp; Limit maker order **"IOC"** for Limit order &amp; Market order **"FOK"** for Limit order                                                                                                                                                                                                                                                      |
| stpMode          | ENUM       | C       | Self Trade Prevention Mode.   Enum: EXPIRE\_TAKER, EXPIRE\_MAKER   Default EXPIRE\_TAKER if not specified.                                                                                                                                                                                                                                                                    |
| recvWindow       | LONG       |         | Recv Window. Default 5000                                                                                                                                                                                                                                                                                                                                                     |
| timestamp        | LONG       | Y       | Timestamp                                                                                                                                                                                                                                                                                                                                                                     |

**Response Content**

```
{ "accountId" : "1471090223379184384" , "symbol" : "BTCUSD" , "symbolName" : "BTCUSD" , "clientOrderId" : "1768459741532390" , "orderId" : "2128389008024406016" , "transactTime" : "1768459741535" , "price" : "98001" , "origQty" : "0.01" , "executedQty" : "0" , "status" : "PENDING_NEW" , "timeInForce" : "GTC" , "type" : "LIMIT" , "side" : "BUY" , "reqAmount" : "0" , "concentration" : "" , "alert" : ""
}
```

| **PARAMETER**   | **TYPE**   | Example values      | **DESCRIPTION**                                                                                                |
|-----------------|------------|---------------------|----------------------------------------------------------------------------------------------------------------|
| accountId       | LONG       | 1467298646903017216 | Account number                                                                                                 |
| symbol          | STRING     | BTCUSD              | Trading pair                                                                                                   |
| symbolName      | STRING     | BTCUSD              | Trading pair name                                                                                              |
| clientOrderId   | STRING     | 1690084460710352    | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| orderId         | LONG       | 1470929500342690304 | System-generated order ID (up to 20 characters)                                                                |
| transactTime    | LONG       | 1690084460716       | Timestamp in milliseconds                                                                                      |
| price           | DECIMAL    | 28000               | Price                                                                                                          |
| origQty         | DECIMAL    | 0.01                | Quantity                                                                                                       |
| executedQty     | DECIMAL    | 0                   | Traded Volume                                                                                                  |
| status          | ENUM       | NEW                 | Order status (see enumeration definition for more details)                                                     |
| timeInForce     | ENUM       | GTC                 | Duration of the order before expiring                                                                          |
| type            | ENUM       | LIMIT               | Order type (see enumeration definition for more details)                                                       |
| side            | ENUM       | BUY                 | BUY or SELL                                                                                                    |
| reqAmount       | STRING     | 0                   | Requested Cash amount                                                                                          |
| concentration   | STRING     |                     | Concentration reminder message                                                                                 |
| alert           | STRING     |                     | STO only                                                                                                       |

### Create Multiple orders by Symbol v1.1

**POST** `/api/v1.1/spot/batchOrders`

Create orders in batches up to 20 orders at a time. Currently only support for same symbol.

**Weight: 1**

**Upper Limit: 20 orders/batch**

**Request Parameters**

```
curl --request POST \ --url '/api/v1.1/spot/batchOrders?timestamp=1707492562526&signature=f19400b8b39964fd596280bbf03b37d39ff858d97e522a82d4994ecddd961e71' \ --header 'X-APIKEY: NuVdtBcogpRjyQ6sMMlC6KEB0xuXZbng9zXDPyT0TOWHp64UEkyIJ287bBhaW4vy' \ --header 'accept: application/json' \ --header 'content-type: application/json' \ --data '
        [
          {
            "symbol": "BTCUSD",
            "side": "SELL",
            "type": "LIMIT",
            "price": "52000",
            "quantity": "0.01",
            "newClientOrderId": "123456789"
          },
          {
            "symbol": "BTCUSD",
            "side": "BUY",
            "type": "LIMIT",
            "price": "43000",
            "quantity": "0.01",
            "newClientOrderId": "123456790"
          }
        ]
     '
```

| **PARAMETER**    | **TYPE**   | Req'd   | **DESCRIPTION**                                                                                                                                                                                                                                                                                                                                                               |
|------------------|------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol           | STRING     | Y       | Name of instrument   e.g. "BTCUSD", "ETHUSD"                                                                                                                                                                                                                                                                                                                                  |
| side             | ENUM       | Y       | BUY or SELL                                                                                                                                                                                                                                                                                                                                                                   |
| type             | ENUM       | Y       | Currently offer 3 order types:  - LIMIT - Limit order   - MARKET - Market order   - LIMIT\_MAKER - Maker Limit order                                                                                                                                                                                                                                                          |
| quantity         | DECIMAL    | C       | Order quantity in units of the instrument  - Limit order: Represents the amount of the base asset you want to buy or sell.   For example: BTC/USD pair, if quantity is 0.5, you're ordering 0.5 BTC  - Market order: Represents the amount of the base asset to buy or sell   For example: BTC/USDT pair, if quantity is 0.5, you're buying 0.5 BTC worth at the market price |
| amount           | DECIMAL    | C       | Cash amount in the units of quote asset. Market order only  - Market order: Represents the amount of the quote asset you want to use for the trade   For example: For BTC/USD pair, if amount = 1000, you are placing a MARKET buy order to purchase BTC using 1000 USD at the current market price.                                                                          |
| price            | DECIMAL    | C       | Required for LIMIT and LIMIT_MAKER order                                                                                                                                                                                                                                                                                                                                      |
| newClientOrderId | STRING     |         | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request. (up to 255 characters)                                                                                                                                                                                                                                        |
| timeInForce      | ENUM       |         | **"GTC"** for Limit order &amp; Limit maker order **"IOC"** for Limit order &amp; Market order **"FOK"** for Limit order                                                                                                                                                                                                                                                      |
| stpMode          | ENUM       | C       | Self Trade Prevention Mode.   Enum: EXPIRE\_TAKER, EXPIRE\_MAKER   Default EXPIRE\_TAKER if not specified.                                                                                                                                                                                                                                                                    |
| recvWindow       | LONG       |         | Recv Window. Default 5000                                                                                                                                                                                                                                                                                                                                                     |
| timestamp        | LONG       | Y       | Timestamp                                                                                                                                                                                                                                                                                                                                                                     |

**Response Content**

```
{ "code" : 0 , "result" : [ { "code" : "0000" , "order" : { "accountId" : "1471090223379184384" , "symbol" : "BTCUSD" , "symbolName" : "BTCUSD" , "clientOrderId" : "01151450" , "orderId" : "2128390066566072320" , "transactTime" : "1768459867723" , "price" : "98003" , "origQty" : "0.01" , "executedQty" : "0" , "status" : "PENDING_NEW" , "timeInForce" : "GTC" , "type" : "LIMIT" , "side" : "BUY" , "reqAmount" : "0" , "alert" : "" } }, { "code" : "0000" , "order" : { "accountId" : "1471090223379184384" , "symbol" : "BTCUSD" , "symbolName" : "BTCUSD" , "clientOrderId" : "01151451" , "orderId" : "2128390066574460928" , "transactTime" : "1768459867723" , "price" : "98004" , "origQty" : "0.01" , "executedQty" : "0" , "status" : "PENDING_NEW" , "timeInForce" : "GTC" , "type" : "LIMIT" , "side" : "BUY" , "reqAmount" : "0" , "alert" : "" } } ], "concentration" : ""
}
```

| **PARAMETER**       | **TYPE**     | Example values        | **DESCRIPTION**                                                                                                |
|---------------------|--------------|-----------------------|----------------------------------------------------------------------------------------------------------------|
| code                | INTEGER      | 0                     | Error code                                                                                                     |
| result              | Object Array |                       | Batch order result                                                                                             |
| -code               | STRING       | 0000                  | Error code of an order                                                                                         |
| -msg                | STRING       | "Create order failed" | Error message                                                                                                  |
| -order              | Object Array |                       | Order response data                                                                                            |
| order.accountId     | LONG         | 1467298646903017216   | Account number                                                                                                 |
| order.symbol        | STRING       | BTCUSD                | Trading pair                                                                                                   |
| order.symbolName    | STRING       | BTCUSD                | Trading pair name                                                                                              |
| order.clientOrderId | STRING       | 1690084460710352      | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| order.orderId       | LONG         | 1470929500342690304   | System-generated order ID (up to 20 characters)                                                                |
| order.transactTime  | LONG         | 1690084460716         | Timestamp in milliseconds                                                                                      |
| order.price         | DECIMAL      | 28000                 | Price                                                                                                          |
| order.origQty       | DECIMAL      | 0.01                  | Quantity                                                                                                       |
| order.executedQty   | DECIMAL      | 0                     | Traded Volume                                                                                                  |
| order.status        | ENUM         | NEW                   | Order status (see enumeration definition for more details)                                                     |
| order.timeInForce   | ENUM         | GTC                   | Duration of the order before expiring                                                                          |
| order.type          | ENUM         | LIMIT                 | Order type (see enumeration definition for more details)                                                       |
| order.side          | ENUM         | BUY                   | BUY or SELL                                                                                                    |
| order.reqAmount     | STRING       | 0                     | Requested Cash amount                                                                                          |
| order.alert         | STRING       |                       | STO only                                                                                                       |
| concentration       | STRING       |                       | Concentration reminder message                                                                                 |

### Cancel Order

**DELETE** `/api/v1/spot/order`

Cancel an existing order. Either orderId or clientOrderId must be sent.

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | **DESCRIPTION**                           |
|-----------------|------------|---------|-------------------------------------------|
| orderId         | STRING     | C       | Order ID                                  |
| clientOrderId   | STRING     | C       | An ID defined by the client for the order |
| recvWindow      | LONG       |         | Recv Window. Default 5000                 |
| timestamp       | LONG       | Y       | Timestamp                                 |

**Response Content**

```
{ "accountId" : "1464567707961719552" , "symbol" : "ETHUSD" , "clientOrderId" : "99999888912" , "orderId" : "1563291927536863744" , "transactTime" : "1701094920045" , "price" : "1900" , "origQty" : "1" , "executedQty" : "0" , "status" : "NEW" , "timeInForce" : "GTC" , "type" : "LIMIT" , "side" : "BUY"
}
```

| **PARAMETER**   | **TYPE**   | Example values      | **DESCRIPTION**                                                                                                |
|-----------------|------------|---------------------|----------------------------------------------------------------------------------------------------------------|
| accountId       | LONG       | 1467298646903017216 | Account number                                                                                                 |
| symbol          | STRING     | BTCUSD              | Trading pair                                                                                                   |
| clientOrderId   | STRING     | 1690084460710352    | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| orderId         | LONG       | 1470929500342690304 | System-generated order ID (up to 20 characters)                                                                |
| transactTime    | LONG       | 1690084460716       | Timestamp in milliseconds                                                                                      |
| price           | DECIMAL    | 28000               | Price                                                                                                          |
| origQty         | DECIMAL    | 0.01                | Quantity                                                                                                       |
| executedQty     | DECIMAL    | 0                   | Traded Volume                                                                                                  |
| status          | ENUM       | NEW                 | Order status (see enumeration definition for more details)                                                     |
| timeInForce     | ENUM       | GTC                 | Duration of the order before expiring                                                                          |
| type            | ENUM       | LIMIT               | Order type (see enumeration definition for more details)                                                       |
| side            | ENUM       | BUY                 | BUY or SELL                                                                                                    |

### Cancel All Open Orders by Symbol

**DELETE** `/api/v1/spot/openOrders`

Cancel all open orders (Same symbol only)

**Weight: 1**

**Upper Limit: 200 orders/batch**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values   | **DESCRIPTION**           |
|-----------------|------------|---------|------------------|---------------------------|
| symbol          | STRING     | Y       | BTCUSDT          | Currency pair name        |
| side            | STRING     |         | BUY              | BUY or SELL               |
| recvWindow      | LONG       |         |                  | Recv Window. Default 5000 |
| timestamp       | LONG       | Y       | 1714311403031    | Timestamp                 |

**Response Content**

```
{ "success" : true
}
```

| **PARAMETER**   | **TYPE**   | Example values   | **DESCRIPTION**    |
|-----------------|------------|------------------|--------------------|
| success         | BOOLEAN    | TRUE             | Whether successful |

### Cancel All Open Spot Orders

**DELETE** `/api/v1/spot/cancelAllOpenOrders`

Cancel all open orders (Max 200 orders per request). If requesting via main trading account API Key, only orders from main trading account will be canceled, but not the ones from sub trading account.

**Weight: 1**

**Upper Limit: 200 orders/batch**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values      | **DESCRIPTION**                                                                              |
|-----------------|------------|---------|---------------------|----------------------------------------------------------------------------------------------|
| symbol          | STRING     |         | BTCUSDT             | Currency pair name. **Return results for all Symbols if not specified.**                     |
| side            | STRING     |         | BUY                 | BUY or SELL                                                                                  |
| fromOrderId     | STRING     |         | 1470930457684189696 | From Order ID, from which order Id will the results be generated.                            |
| limit           | INTERGER   |         | 20                  | Default 100, Max 200. Will only return 200 results even if limit being set greater than 200. |
| recvWindow      | LONG       |         |                     | Recv Window. Default 5000                                                                    |
| timestamp       | LONG       | Y       | 1714311403031       | Timestamp                                                                                    |

**Response Content**

```
{ "code" : "0000" , "message" : "success" , "timestamp" : 1714406315538 , "lastOrderId" : 1470930457684189700
}
```

| **PARAMETER**   | **TYPE**   | Example values      | **DESCRIPTION**                                                                                                                                        |
|-----------------|------------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| code            | STRING     | 0000                | Return code of cancellation request.                                                                                                                   |
| message         | STRING     | success             | Return message of cancellation request. Reflecting whether the request is successfully accepted (does not indicate the task is successfully completed) |
| timestamp       | LONG       | 1714406315538       | Timestamp when returning                                                                                                                               |
| lastOrderId     | LONG       | 1470930457684189700 | Last Order ID to be canceled                                                                                                                           |

### Cancel Multiple Orders By OrderId

**DELETE** `/api/v1/spot/cancelOrderByIds`

Cancel orders in batches according to order IDs (Maximum of 100 orders in a single batch)

📘 Note: A return code of 0 from the code indicates that the cancel order request has been executed. To determine if it was successful, you need to check the results in the result field. If the result is null, it means all were successful. If it is non empty, the orderId represents the ID of the order that failed to cancel, and code represents the reason for the cancellation failure.

**Weight: 1**

**Upper Limit: 100 orders/batch**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values                        | **DESCRIPTION**                |
|-----------------|------------|---------|---------------------------------------|--------------------------------|
| ids             | STRING     | Y       | 202212231234567895,202212231234567896 | Order id (multiple, separated) |
| recvWindow      | LONG       |         |                                       | Recv Window. Default 5000      |
| timestamp       | LONG       | Y       | 1714311403031                         | Timestamp                      |

**Response Content**

Success

```
{ "code" : "0000" , "result" : []
}
```

Certain error happened

```
{ "code" : "0000" , "result" : [ { "orderId" : "1507155386372816640" , "code" : "0211" }, { "orderId" : "1507155487740667904" , "code" : "0211" } ]
}
```

| **PARAMETER**   | **TYPE**     |    Example values | **DESCRIPTION**                                           |
|-----------------|--------------|-------------------|-----------------------------------------------------------|
| code            | STRING       |              0000 | 0000 means request is executed                            |
| result          | Object Array |                   |                                                           |
| result.orderId  | STRING       | 16880363408511681 | Order ID                                                  |
| result.code     | STRING       |              0211 | Return error code for each order (For unsuccessful order) |

### Query Order

**GET** `/api/v1/spot/order`

Check a single order information

📘 Note: Request parameter either orderId or origClientOrderId must be sent

**Weight: 1**

**Request Parameters**

| **PARAMETER**     | **TYPE**   | Req'd   | **DESCRIPTION**           |
|-------------------|------------|---------|---------------------------|
| orderId           | STRING     | C       | Order ID                  |
| origClientOrderId | STRING     | C       | Client order ID           |
| accountId         | STRING     |         | Account ID                |
| recvWindow        | LONG       |         | Recv Window. Default 5000 |
| timestamp         | LONG       | Y       | Timestamp                 |

**Response Content**

```
{ "accountId" : "1649292498437183232" , "exchangeId" : "301" , "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "clientOrderId" : "1766133332140288" , "orderId" : "2108873672953505280" , "price" : "0" , "origQty" : "0.1" , "executedQty" : "0.1" , "cummulativeQuoteQty" : "11292.24" , "cumulativeQuoteQty" : "11292.24" , "avgPrice" : "112922.4" , "status" : "FILLED" , "timeInForce" : "IOC" , "type" : "MARKET" , "side" : "SELL" , "stopPrice" : "0.0" , "icebergQty" : "0.0" , "time" : "1766133332319" , "updateTime" : "1766133332383" , "isWorking" : true , "reqAmount" : "0" , "feeCoin" : "" , "feeAmount" : "0" , "sumFeeAmount" : "0" , "ordCxlReason" : "" , "stpMode" : "EXPIRE_TAKER"
}
```

| **PARAMETER**      | **TYPE**         | Example values      | **DESCRIPTION**                                                                                                |
|--------------------|------------------|---------------------|----------------------------------------------------------------------------------------------------------------|
| accountId          | STRING           | 1467298646903017216 | Account number                                                                                                 |
| exchangeId         | STRING           | 301                 | Exchange number                                                                                                |
| symbol             | STRING           | BTCUSD              | Trading pair                                                                                                   |
| symbolName         | STRING           | BTCUSD              | Trading pair name                                                                                              |
| clientOrderId      | STRING           | 1690084460710352    | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| orderId            | STRING           | 1470929500342690304 | System-generated order ID (up to 20 characters)                                                                |
| price              | STRING (decimal) | 28000               | Price                                                                                                          |
| origQty            | STRING (decimal) | 0.01                | Quantity                                                                                                       |
| executedQty        | STRING (decimal) | 0                   | Traded Volume                                                                                                  |
| cumulativeQuoteQty | STRING (decimal) | 0                   | Cumulative volume. Commonly known as Transaction Amount                                                        |
| avgPrice           | STRING (decimal) | 0                   | Average traded price                                                                                           |
| status             | STRING           | NEW                 | Order status (see enumeration definition for more details)                                                     |
| timeInForce        | STRING           | GTC                 | Duration of the order before expiring                                                                          |
| type               | STRING           | LIMIT               | Order type (see enumeration definition for more details)                                                       |
| side               | STRING           | BUY                 | BUY or SELL                                                                                                    |
| stopPrice          | STRING (decimal) | 0.0                 | Not used                                                                                                       |
| icebergQty         | STRING (decimal) | 0.0                 | Not used                                                                                                       |
| time               | STRING (decimal) | 1688036585077       | Order creation Timestamp                                                                                       |
| updateTime         | STRING (decimal) | 1688036585084       | Latest update Timestamp according to status                                                                    |
| isWorking          | BOOLEAN          | TRUE                | Not used                                                                                                       |
| reqAmount          | STRING           | 0                   | Requested Cash amount                                                                                          |
| feeCoin            | STRING           | USDT                | (Deprecated, will return Null)   Fee Currency Name                                                             |
| feeAmount          | STRING           | 0.006               | (Deprecated, will return 0)   Fee amount                                                                       |
| sumFeeAmount       | STRING           | 0.006               | (Deprecated, will return 0)   Sum fee amount                                                                   |
| ordCxlReason       | STRING           |                     | Order cancel reason                                                                                            |
| stpMode            | STRING           | EXPIRE_MAKER        | Self Trade Prevention Mode.   Enum: EXPIRE\_TAKER, EXPIRE\_MAKER   Default EXPIRE\_TAKER if not specified.     |

### Get Current Open Orders

**GET** `/api/v1/spot/openOrders`

Query current active orders

📘 Note: In regards to master API key. The request parameters of "side" and "accountId". If "accountId" is passed, it will only query the orders under the current account. If not passed, it will first query the main account, and if the results are less than 500, it will then query the sub-accounts.

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values      | **DESCRIPTION**                                                                                   |
|-----------------|------------|---------|---------------------|---------------------------------------------------------------------------------------------------|
| accountId       | STRING     |         | 2071958131961800448 | Main / Sub Trading account ID                                                                     |
| fromOrderId     | STRING     |         | 1470930457684189696 | Order ID                                                                                          |
| symbol          | STRING     |         | BTCUSD              | Currency pair. Return all if not specified. If no value specified, return entries for all symbols |
| side            | STRING     |         | BUY                 | Side                                                                                              |
| limit           | INTEGER    |         | 20                  | Default 500, Maximum 1000                                                                         |
| recvWindow      | LONG       |         |                     | Recv Window. Default 5000                                                                         |
| timestamp       | LONG       | Y       |                     | Timestamp                                                                                         |

**Response Content**

```
[ { "accountId" : "1464567707961719552" , "exchangeId" : "301" , "symbol" : "ETHUSD" , "symbolName" : "ETHUSD" , "clientOrderId" : "99999888913" , "orderId" : "1563293653459405312" , "price" : "1900" , "origQty" : "1" , "executedQty" : "0" , "cummulativeQuoteQty" : "0" , "cumulativeQuoteQty" : "0" , "avgPrice" : "0" , "status" : "NEW" , "timeInForce" : "GTC" , "type" : "LIMIT" , "side" : "BUY" , "stopPrice" : "0.0" , "icebergQty" : "0.0" , "time" : "1701095125789" , "updateTime" : "1701095125798" , "isWorking" : true , "reqAmount" : "0" }
]
```

| **PARAMETER**        | **TYPE**         | Example values      | **DESCRIPTION**                                                                                                |
|----------------------|------------------|---------------------|----------------------------------------------------------------------------------------------------------------|
| No                   | Object Array     |                     | Query result array                                                                                             |
| - accountId          | STRING           | 1467298646903017216 | Account number                                                                                                 |
| - exchangeId         | STRING           | 301                 | Exchange number                                                                                                |
| - symbol             | STRING           | BTCUSD              | Trading pair                                                                                                   |
| - symbolName         | STRING           | BTCUSD              | Trading pair name                                                                                              |
| - clientOrderId      | STRING           | 1690084460710352    | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| - orderId            | STRING           | 1470929500342690304 | System-generated order ID (up to 20 characters)                                                                |
| - price              | STRING (decimal) | 28000               | Price                                                                                                          |
| - origQty            | STRING (decimal) | 0.01                | Quantity                                                                                                       |
| - executedQty        | STRING (decimal) | 0                   | Traded Volume                                                                                                  |
| - cumulativeQuoteQty | STRING (decimal) | 0                   | Cumulative volume. Commonly known as Transaction Amount                                                        |
| - avgPrice           | STRING (decimal) | 0                   | Average traded price                                                                                           |
| - status             | STRING           | NEW                 | Order status (see enumeration definition for more details)                                                     |
| - timeInForce        | STRING           | GTC                 | Duration of the order before expiring                                                                          |
| - type               | STRING           | LIMIT               | Order type (see enumeration definition for more details)                                                       |
| - side               | STRING           | BUY                 | BUY or SELL                                                                                                    |
| - stopPrice          | STRING (decimal) | 0.0                 | Not used                                                                                                       |
| - icebergQty         | STRING (decimal) | 0.0                 | Not used                                                                                                       |
| - time               | STRING (decimal) | 1688036585077       | Order creation Timestamp                                                                                       |
| - updateTime         | STRING (decimal) | 1688036585084       | Latest update Timestamp according to status                                                                    |
| - isWorking          | BOOLEAN          | TRUE                | Not used                                                                                                       |
| - reqAmount          | STRING           | 0                   | Requested Cash amount                                                                                          |
| - stpMode            | STRING           | EXPIRE_MAKER        | Self Trade Prevention Mode.   Enum: EXPIRE\_TAKER, EXPIRE\_MAKER   Default EXPIRE\_TAKER if not specified.     |

### Get All Traded Orders

**GET** `/api/v1/spot/tradeOrders`

Retrieve all traded orders

📘 Note: In regards to master API key. The request parameters of "side" and "accountId". If "accountId" is passed, it will only query the orders under the current account. If not passed, it will first query the main account, and if the results are less than 500, it will then query the sub-accounts.

**Weight: 5**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values      | **DESCRIPTION**                                                                              |
|-----------------|------------|---------|---------------------|----------------------------------------------------------------------------------------------|
| fromOrderId     | STRING     |         | 1470930457684189696 | From Order Id, which is used to return orders whose orders' id are smaller than this orderId |
| symbol          | STRING     |         | BTCUSD              | Currency pair                                                                                |
| startTime       | LONG       |         |                     | Start Timestamp                                                                              |
| endTime         | LONG       |         |                     | End Timestamp. Only supports the last 90 days timeframe                                      |
| side            | STRING     |         |                     | Side                                                                                         |
| limit           | INTEGER    |         |                     | Default 500, Maximum 1000                                                                    |
| recvWindow      | LONG       |         |                     | Recv Window. Default 5000                                                                    |
| timestamp       | LONG       | Y       |                     | Timestamp                                                                                    |

**Response Content**

```
[ { "accountId" : "1464567707961719552" , "exchangeId" : "301" , "symbol" : "ETHUSD" , "symbolName" : "ETHUSD" , "clientOrderId" : "99999888912" , "orderId" : "1563291927536863744" , "price" : "1900" , "origQty" : "1" , "executedQty" : "0" , "cummulativeQuoteQty" : "0" , "cumulativeQuoteQty" : "0" , "avgPrice" : "0" , "status" : "CANCELED" , "timeInForce" : "GTC" , "type" : "LIMIT" , "side" : "BUY" , "stopPrice" : "0.0" , "icebergQty" : "0.0" , "time" : "1701094920045" , "updateTime" : "1701094949567" , "isWorking" : true , "reqAmount" : "0" }, { "accountId" : "1464567707961719552" , "exchangeId" : "301" , "symbol" : "ETHUSD" , "symbolName" : "ETHUSD" , "clientOrderId" : "99999888911" , "orderId" : "1563291785660336640" , "price" : "0" , "origQty" : "0" , "executedQty" : "0" , "cummulativeQuoteQty" : "0" , "cumulativeQuoteQty" : "0" , "avgPrice" : "0" , "status" : "CANCELED" , "timeInForce" : "IOC" , "type" : "MARKET" , "side" : "BUY" , "stopPrice" : "0.0" , "icebergQty" : "0.0" , "time" : "1701094903129" , "updateTime" : "1701094903140" , "isWorking" : true , "reqAmount" : "10" }
]
```

| **PARAMETER**        | **TYPE**         | Example values      | **DESCRIPTION**                                                                                                |
|----------------------|------------------|---------------------|----------------------------------------------------------------------------------------------------------------|
| No                   | Object Array     |                     | Query result array                                                                                             |
| - accountId          | STRING           | 1467298646903017216 | Account number                                                                                                 |
| - exchangeId         | STRING           | 301                 | Exchange number                                                                                                |
| - symbol             | STRING           | BTCUSD              | Trading pair                                                                                                   |
| - symbolName         | STRING           | BTCUSD              | Trading pair name                                                                                              |
| - clientOrderId      | STRING           | 1690084460710352    | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| - orderId            | STRING           | 1470929500342690304 | System-generated order ID (up to 20 characters)                                                                |
| - price              | STRING (decimal) | 28000               | Price                                                                                                          |
| - origQty            | STRING (decimal) | 0.01                | Quantity                                                                                                       |
| - executedQty        | STRING (decimal) | 0                   | Traded Volume                                                                                                  |
| - cumulativeQuoteQty | STRING (decimal) | 0                   | Cumulative volume. Commonly known as Transaction Amount                                                        |
| - avgPrice           | STRING (decimal) | 0                   | Average traded price                                                                                           |
| - status             | STRING           | NEW                 | Order status (see enumeration definition for more details)                                                     |
| - timeInForce        | STRING           | GTC                 | Duration of the order before expiring                                                                          |
| - type               | STRING           | LIMIT               | Order type (see enumeration definition for more details)                                                       |
| - side               | STRING           | BUY                 | BUY or SELL                                                                                                    |
| - stopPrice          | STRING (decimal) | 0.0                 | Not used                                                                                                       |
| - icebergQty         | STRING (decimal) | 0.0                 | Not used                                                                                                       |
| - time               | STRING (decimal) | 1688036585077       | Order creation Timestamp                                                                                       |
| - updateTime         | STRING (decimal) | 1688036585084       | Latest update Timestamp according to status                                                                    |
| - isWorking          | BOOLEAN          | TRUE                | Not used                                                                                                       |
| - reqAmount          | STRING           | 0                   | Requested Cash amount                                                                                          |
| - stpMode            | STRING           | EXPIRE_MAKER        | Self Trade Prevention Mode.   Enum: EXPIRE\_TAKER, EXPIRE\_MAKER   Default EXPIRE\_TAKER if not specified.     |

## Futures Trading

### Create New Futures Order

**POST** `/api/v2/futures/order`

This endpoint allows you to create a new Futures order.

📘 Note:  
if your balance does not meet the margin requirement (which is the minimum margin requirement + open position fee + close position fee), "insufficient balance" error message will be returned.

You can get contracts' price, quantity precision configuration data in the [Get Exchange Information](#Get-Exchange-Information) .

**Weight: 1**

**Request Parameters**

```
{ "symbol" : "BTCUSD-PERPETUAL" , "side" : "BUY" , "orderType" : "LIMIT" , "baseQty" : 0.01 , "price" : 90000 , "timeInForce" : "GTC" , "clientOrderId" : "99999989990119a" , "timestamp" : 1714311403031
}
```

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                                                                                                                                    |
|-----------------|------------|-------------|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol          | STRING     | Y           | BTCUSD-PERPETUAL     | Name of contract                                                                                                                                                   |
| side            | STRING     | Y           | BUY                  | Direction of the order. Possible values include: `BUY` `SELL`                                                                                                      |
| orderType       | STRING     | Y           | LIMIT                | The order type, possible types: `LIMIT` `MARKET` `LIMIT_MAKER` `STOP` (If price is inputted, then stop limit order, if price not inputted, then stop market order) |
| baseQty         | STRING     | C           |                      | Amount in base asset   BTC, 0.01 means the contracts of 0.01 BTC   Either baseQty or quoteQty is required                                                          |
| quoteQty        | STRING     | C           |                      | Amount in quote asset   USD, calculated in markPrice, 6000 means the contracts of value 6,000 USD   Either baseQty or quoteQty is required                         |
| price           | STRING     | C           | 3000                 | Price of the order, required if orderType = `LIMIT` , `LIMIT_MAKER`                                                                                                |
| stopPrice       | STRING     | C           | 2800                 | The price at which the trigger order will be executed, required if orderType = `STOP` , triggered by mark price                                                    |
| timeInForce     | STRING     |             | GTC                  | Time in force for LIMIT orders. Possible values include: `GTC` , `FOK` , `IOC` , `LIMIT_MAKER` (place as a maker-only order).                                      |
| clientOrderId   | STRING     | Y           | 99999999980000       | A unique id among open orders. Automatically generated if not sent. Can only be string following the rule: ^[.A-Z:/a-z0-9\_-].   Max length 100                    |
| leverage        | STRING     |             | 5                    | Leverage of the order. Use the current leverage of the contract if not sent                                                                                        |
| reduceOnly      | BOOLEAN    |             | false                | If `true` , the order can only reduce an existing position. Default `false`                                                                                        |
| stpMode         | STRING     | C           | EXPIRE_TAKER         | Self Trade Prevention Mode.   Enum: `EXPIRE_TAKER` , `EXPIRE_MAKER` , `EXPIRE_BOTH` , `NOT_EXPIRE` Default **`EXPIRE_TAKER`** if not specified.                    |
| slTriggerPrice  | DECIMAL    | C           |                      | Stop loss trigger price                                                                                                                                            |
| slTriggerBy     | ENUM       | C           |                      | `last` / `mark` Required when slTriggerPrice is filled                                                                                                             |
| tpTriggerPrice  | DECIMAL    | C           |                      | Take profit trigger price                                                                                                                                          |
| tpTriggerBy     | ENUM       | C           |                      | `last` / `mark` Required when tpTriggerPrice is filled                                                                                                             |
| recvWindow      | LONG       |             | 5000                 | recv Window                                                                                                                                                        |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp                                                                                                                                                          |

**Response Content**

```
{ "time" : "1768794550630" , "orderId" : "2131197590285846784" , "clientOrderId" : "99999989990119a" , "symbol" : "BTCUSD-PERPETUAL" , "status" : "PENDING_NEW"
}
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**                                                                                                 |
|-----------------|------------|----------------------|-----------------------------------------------------------------------------------------------------------------|
| time            | STRING     | 1714403283482        | Timestamp when the order is created                                                                             |
| orderId         | STRING     | 2131197590285846784  | Order ID                                                                                                        |
| clientOrderId   | STRING     | 99999999980001       | A unique ID of the order.                                                                                       |
| symbol          | STRING     | BTCUSD-PERPETUAL     | Name of the contract.                                                                                           |
| status          | STRING     | PENDING_NEW          | The state of the order. Possible values include `PENDING_NEW` (for limit orders), `ORDER_NEW` (for stop orders) |

### Query Futures Order

**GET** `/api/v2/futures/order`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**                                |   **Example values** | **DESCRIPTION**   |
|-----------------|------------|------------------------------------------|----------------------|-------------------|
| orderId         | INTEGER    | REQUIRED for clientOrderId when not sent |  1674945624754144000 | Order Id          |
| clientOrderId   | STRING     | REQUIRED for orderId when not sent       |       99999999980002 | Client Order Id   |
| recvWindow      | LONG       |                                          |                 5000 | recvWindow        |
| timestamp       | LONG       | Y                                        |        1714311403031 | Timestamp         |

**Response Content**

```
{ "time" : "1768812678007" , "orderId" : "2131349653745568000" , "clientOrderId" : "99999989990119c" , "symbol" : "BTCUSD-PERPETUAL" , "baseAsset" : "BTC" , "quoteAsset" : "USD" , "price" : "93000" , "side" : "BUY" , "orderType" : "limit" , "reduceOnly" : false , "leverage" : "5" , "originalBaseQty" : "0.01" , "executedBaseQty" : "0" , "originalQuoteQty" : "930" , "executedQuoteQty" : "0" , "avgPrice" : "0" , "timeInForce" : "GTC" , "status" : "NEW" , "stpMode" : "EXPIRE_TAKER" , "ordCxlReason" : "" , "isLiquidationOrder" : false , "liquidationType" : "" , "slTriggerPrice" : "92500" , "slTriggerBy" : "last" , "tpTriggerPrice" : "100000" , "tpTriggerBy" : "last"
}
```

| **PARAMETER**      | **TYPE**   | **Example values**   | **DESCRIPTION**                                                                                                                                                                                                                                             |
|--------------------|------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| time               | STRING     | 1768794550630        | Timestamp when the order is created                                                                                                                                                                                                                         |
| orderId            | STRING     | 2131197590285846784  | Order ID                                                                                                                                                                                                                                                    |
| clientOrderId      | STRING     | 99999999980001       | A unique ID of the order.                                                                                                                                                                                                                                   |
| symbol             | STRING     | BTCUSD-PERPETUAL     | Name of the contract.                                                                                                                                                                                                                                       |
| baseAsset          | STRING     | BTC                  | Name of the base asset, BTC, ETH, etc                                                                                                                                                                                                                       |
| quoteAsset         | STRING     | USD                  | Name of the quote asset, USDT, USD, etc                                                                                                                                                                                                                     |
| price              | STRING     | 92560                | Price of the order.                                                                                                                                                                                                                                         |
| side               | STRING     | BUY                  | Direction of the order. Possible values include: `BUY` `SELL`                                                                                                                                                                                               |
| orderType          | STRING     | LIMIT                | The order type                                                                                                                                                                                                                                              |
| reduceOnly         | BOOLEAN    | false                |                                                                                                                                                                                                                                                             |
| leverage           | STRING     | 5                    | Leverage of the order.                                                                                                                                                                                                                                      |
| originalBaseQty    | STRING     | 0.01                 | Quantity ordered in Number of baseAsset                                                                                                                                                                                                                     |
| executedBaseQty    | STRING     | 0                    | Quantity that has been executed in Number of baseAsset                                                                                                                                                                                                      |
| originalQuoteQty   | STRING     | 925.6                | Quantity ordered in quoteAsset                                                                                                                                                                                                                              |
| executedQuoteQty   | STRING     | 0                    | Quantity that has been executed in quoteAsset                                                                                                                                                                                                               |
| avgPrice           | STRING     | 0                    | Average price of filled orders.                                                                                                                                                                                                                             |
| timeInForce        | STRING     | GTC                  | Time in force for LIMIT orders. Possible values include: `GTC` , `FOK` , `IOC` .                                                                                                                                                                            |
| status             | STRING     | CANCELED             | The state of the order. Possible values include:  Limit Orders: `NEW` `PARTIALLY_FILLED` `FILLED` `CANCELED` `PARTIALLY_CANCELED` `REJECTED` Stop Orders: `ORDER_NEW` `ORDER_FILLED` `ORDER_REJECTED` `ORDER_CANCELED` `ORDER_FAILED` `ORDER_NOT_EFFECTIVE` |
| stpMode            | STRING     | EXPIRE_TAKER         | Self Trade Prevention Mode.                                                                                                                                                                                                                                 |
| ordCxlReason       | STRING     | USER_CANCEL          | Order cancel reason                                                                                                                                                                                                                                         |
| isLiquidationOrder | BOOLEAN    | false                | Whether the order is a liquidation order                                                                                                                                                                                                                    |
| liquidationType    | STRING     |                      | Available when isLiquidationOrder is true `LIQUIDATION_MAKER_ADL` `LIQUIDATION_MAKER` `LIQUIDATION_TAKER`                                                                                                                                                   |
| slTriggerPrice     | STRING     | 92500                | Stop loss trigger price                                                                                                                                                                                                                                     |
| slTriggerBy        | STRING     | last                 | `last` / `mark`                                                                                                                                                                                                                                             |
| tpTriggerPrice     | STRING     | 100000               | Take profit trigger price                                                                                                                                                                                                                                   |
| tpTriggerBy        | STRING     | last                 | `last` / `mark`                                                                                                                                                                                                                                             |

### Cancel Futures Order

**DELETE** `/api/v2/futures/order`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**                           | **Example values**   | **DESCRIPTION**                                              |
|-----------------|------------|-------------------------------------|----------------------|--------------------------------------------------------------|
| orderId         | LONG       | REQUIRED for clientOrderId not send | 1674945624754144000  | Order Id                                                     |
| clientOrderId   | STRING     | REQUIRED for orderId not send       | 99999999980002       | Client Order Id                                              |
| orderType       | STRING     | Y                                   | LIMIT                | The order type, possible types: `LIMIT` `LIMIT_MAKER` `STOP` |
| recvWindow      | LONG       |                                     | 5000                 | recv Window                                                  |
| timestamp       | LONG       | Y                                   | 1714311403031        | Timestamp                                                    |

**Response Content**

```
{ "code" : 200 , "orderId" : 2131349653745568000 , "clientOrderId" : "99999989990119c" , "orderType" : "LIMIT"
}
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**                                       |
|-----------------|------------|----------------------|-------------------------------------------------------|
| code            | INTEGER    | 200                  | If success, returns 200   If fail, returns error code |
| orderId         | LONG       | 2131349653745568000  | Order ID                                              |
| clientOrderId   | STRING     | 99999989990119c      | A unique ID of the order.                             |
| orderType       | STRING     | BTCUSD-PERPETUAL     | The order type                                        |

### Batch Create New Futures Orders

**POST** `/api/v2/futures/batchOrders`

The batchOrders in RequestBody should fill in the order parameters in list of JSON format.  
Only support placing orders in same orderType.

**Weight: 1**

**Upper Limit: Max 3 for stop order, Max 20 for all other orderTypes**

**Request Parameters**

```
curl --request POST \ --url '/api/v2/futures/batchOrders?timestamp=1714404830102&signature=8c47cf48e****' \ --header 'X-APIKEY: XAzx6DLW2HNs*******' \ --header 'accept: application/json' \ --header 'content-type: application/json' \ --data '
        {
            "symbol":"BTCUSD-PERPETUAL",
            "side":"BUY",
            "orderType":"LIMIT",
            "timeInForce":"GTC",
            "order":[
                {
                    "baseQty":0.01,
                    "price":92561,
                    "clientOrderId":"batchorder0119a"
                },
                {
                    "baseQty":0.05,
                    "price":92562,
                    "clientOrderId":"batchorder0119b"
                }
            ]    
        }
     '
```

| PARAMETER             | TYPE         | Req'd   | Example values   | DESCRIPTION                                                                                                                                                        |
|-----------------------|--------------|---------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol                | STRING       | Y       | BTCUSD-PERPETUAL | Name of contract                                                                                                                                                   |
| side                  | STRING       | Y       | BUY              | Direction of the order. Possible values include: `BUY` `SELL`                                                                                                      |
| orderType             | STRING       | Y       | LIMIT            | The order type, possible types: `LIMIT` `MARKET` `LIMIT_MAKER` `STOP` (If price is inputted, then stop limit order, if price not inputted, then stop market order) |
| positionSide          | STRING       | C       | LONG             | Position side, `LONG` or `SHORT` . Default `LONG` if not sent. Currently only `LONG` is supported                                                                  |
| timeInForce           | STRING       | C       | GTC              | Time in force for LIMIT orders. Possible values include: `GTC` , `FOK` , `IOC` , `LIMIT_MAKER` (place as maker-only orders).                                       |
| order                 | Object Array |         |                  |                                                                                                                                                                    |
| order.baseQty         | STRING       | C       |                  | Amount in base asset   BTC, 0.01 means the contracts of 0.01 BTC   Either baseQty or quoteQty is required                                                          |
| order.quoteQty        | STRING       | C       |                  | Amount in quote asset   USD, calculated in markPrice, 6000 means the contracts of value 6,000 USD   Either baseQty or quoteQty is required                         |
| order.price           | STRING       | C       | 3000             | Price of the order, required if orderType = `LIMIT` , `LIMIT_MAKER`                                                                                                |
| order.stopPrice       | STRING       | C       | 2800             | The price at which the trigger order will be executed, required if orderType = `STOP` , triggered by mark price                                                    |
| order.clientOrderId   | STRING       | Y       |                  | A unique id among open orders. Automatically generated if not sent. Can only be string following the rule: ^[.A-Z:/a-z0-9\_-].   Max length 100                    |
| order.reduceOnly      | BOOLEAN      | C       |                  | If `true` , the order can only reduce an existing position. Default `false`                                                                                        |
| order.stpMode         | STRING       | C       | EXPIRE_TAKER     | Self Trade Prevention Mode.   Enum: `EXPIRE_TAKER` , `EXPIRE_MAKER` , `EXPIRE_BOTH` Default **`EXPIRE_TAKER`** if not specified.                                   |
| order.slTriggerPrice  | DECIMAL      | C       |                  | Stop loss trigger price                                                                                                                                            |
| order.slTriggerBy     | ENUM         | C       |                  | `last` / `mark` Required when slTriggerPrice is filled                                                                                                             |
| order.slPrice         | DECIMAL      | C       |                  | Stop loss order price                                                                                                                                              |
| order.slClientOrderId | STRING       | C       |                  | Client order ID for the stop loss order                                                                                                                            |
| order.tpTriggerPrice  | DECIMAL      | C       |                  | Take profit trigger price                                                                                                                                          |
| order.tpTriggerBy     | ENUM         | C       |                  | `last` / `mark` Required when tpTriggerPrice is filled                                                                                                             |
| order.tpPrice         | DECIMAL      | C       |                  | Take profit order price                                                                                                                                            |
| order.tpClientOrderId | STRING       | C       |                  | Client order ID for the take profit order                                                                                                                          |

**Response Content**

```
{ "code" : "0000" , "result" : [ { "code" : "0000" , "order" : { "orderId" : "2131372568755046656" , "clientOrderId" : "batchorder0119X" , "symbol" : "BTCUSD-PERPETUAL" , "status" : "PENDING_NEW" , "accountId" : "2129188333171126016" , "transactTime" : "1768816219103" } }, { "code" : "0000" , "order" : { "orderId" : "2131372568763435264" , "clientOrderId" : "batchorder0119Y" , "symbol" : "BTCUSD-PERPETUAL" , "status" : "PENDING_NEW" , "accountId" : "2129188333171126016" , "transactTime" : "1768816225000" } } ]
}
```

| **PARAMETER**              | **TYPE**     | Example values      | **DESCRIPTION**                                                                                                 |
|----------------------------|--------------|---------------------|-----------------------------------------------------------------------------------------------------------------|
| code                       | STRING       | 0000                | Return code of request                                                                                          |
| result                     | Object Array |                     | Batch order result                                                                                              |
| result.code                | STRING       | 0000                |                                                                                                                 |
| result.order               | Object Array |                     |                                                                                                                 |
| result.order.orderId       | STRING       | 2131372568763435264 | Order ID                                                                                                        |
| result.order.clientOrderId | STRING       | batchorder0119Y     | A unique ID of the order.                                                                                       |
| result.order.symbol        | STRING       | BTCUSD-PERPETUAL    | Name of the contract.                                                                                           |
| result.order.status        | STRING       | PENDING_NEW         | The state of the order. Possible values include `PENDING_NEW` (for limit orders), `ORDER_NEW` (for stop orders) |
| result.order.accountId     | STRING       | 2129188333171126016 | Future Account Id                                                                                               |
| result.order.transactTime  | STRING       | 1768816225000       | Timestamp when the order is created                                                                             |

### Batch Cancel Futures Orders

**DELETE** `/api/v2/futures/cancelOrders`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                                                                                      |
|-----------------|------------|-------------|----------------------|----------------------------------------------------------------------------------------------------------------------|
| symbol          | STRING     | C           | BTCUSD-PERPETUAL     | Name of the contract. **Cancel all symbols if not specified.**                                                       |
| side            | STRING     | Y           | BUY                  | `BUY` or `SELL`                                                                                                      |
| orderType       | STRING     | Y           |                      | The order type, possible types: `LIMIT` `STOP`                                                                       |
| fromOrderId     | LONG       |             | 1470930457684189696  | From Order ID.   For exmaple, OrderIds:1004,1003,1002,1001, if fromOrderId=1003, then 1002 and 1001 will be canceled |
| limit           | INTEGER    |             | 100                  | Default 100, Range 1 - 200                                                                                           |
| recvWindow      | LONG       |             | 5000                 | recv Window                                                                                                          |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp                                                                                                            |

**Response Content**

```
{ "code" : "0000" , "lastOrderId" : 0
}
```

| **PARAMETER**   | **TYPE**   |   **Example values** | **DESCRIPTION**                                                                                                                                                                                    |
|-----------------|------------|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| code            | STRING     |                 0000 | If success, return 0000, Otherwise return corresponding error code                                                                                                                                 |
| lastOrderId     | LONG       |                    0 | Last Order ID to be canceled (return 0 if no order can be cacencelled)   If the number of orders to be cancelled exceeds 200, this parameter can be used for paging operation to delete in batches |

### Query Futures Trades

**GET** `/api/v2/futures/userTrades`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                           |
|-----------------|------------|-------------|----------------------|-----------------------------------------------------------|
| symbol          | STRING     | Y           | BTCUSD-PERPETUAL     | Name of the contract                                      |
| limit           | INTEGER    | C           | 20                   | The number of trades returned default 20 (max to 1000)    |
| fromId          | LONG       | C           |                      | TradeId to retrieve from                                  |
| toId            | LONG       | C           |                      | TradeId to retrieve to                                    |
| startTime       | LONG       | C           |                      | Start Timestamp, Only supports the last 30 days timeframe |
| endTime         | LONG       | C           |                      | End Timestamp                                             |
| recvWindow      | LONG       |             |                      | recv Window                                               |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp                                                 |

**Response Content**

```
[ { "time" : "1768921741508" , "tradeId" : "2132264544794839413" , "orderId" : "2132264542060153088" , "symbol" : "BTCUSD-PERPETUAL" , "price" : "87900" , "quantity" : "0.002" , "commissionAsset" : "USD" , "commission" : "0.10548" , "makerRebate" : "0" , "type" : "limit" , "side" : "SELL" , "realizedPnl" : "-9.462854" , "isMaker" : false , "ticketId" : "4658973823776567335" }, { "time" : "1768921741508" , "tradeId" : "2132264544794839399" , "orderId" : "2132264542060153088" , "symbol" : "BTCUSD-PERPETUAL" , "price" : "88540.5" , "quantity" : "0.002" , "commissionAsset" : "USD" , "commission" : "0.1062486" , "makerRebate" : "0" , "type" : "limit" , "side" : "SELL" , "realizedPnl" : "-8.181854" , "isMaker" : false , "ticketId" : "4658973823776567334" }
]
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**                                                                                 |
|-----------------|------------|----------------------|-------------------------------------------------------------------------------------------------|
| time            | STRING     | 1768921741508        | Timestamp when the order is created                                                             |
| tradeId         | STRING     | 2132264544794839399  | The ID for the trade                                                                            |
| orderId         | STRING     | 2132264542060153088  | The ID of the order                                                                             |
| symbol          | STRING     | BTCUSD-PERPETUAL     | Name of the contract.                                                                           |
| price           | STRING     | 88540.5              | Price of the trade.                                                                             |
| quantity        | STRING     | 0.002                | Quantity of the trade.                                                                          |
| commissionAsset | STRING     | USD                  | Currency of commission fee                                                                      |
| commission      | STRING     | 0.234                | Commission fee                                                                                  |
| makerRebate     | STRING     | 0                    | Return                                                                                          |
| side            | STRING     | SELL                 | `BUY` or `SELL`                                                                                 |
| type            | STRING     | limit                | The order type, possible types: `LIMIT` `MARKET` `LIMIT_MAKER` `STOP`                           |
| realizedPnl     | STRING     | -8.181854            | Profit and loss                                                                                 |
| isMarker        | BOOLEAN    | false                | Whether the trade is a maker                                                                    |
| ticketId        | STRING     | 4658973823776567334  | The Matching ID for the trade. Both maker and taker share the same ticketId for a single trade. |

### Query Futures Open Orders

**GET** `/api/v2/futures/openOrders`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                                                                                      |
|-----------------|------------|-------------|----------------------|----------------------------------------------------------------------------------------------------------------------|
| symbol          | STRING     | C           | BTCUSD-PERPETUAL     | Name of the contract. **Return all symbols if not specified.**                                                       |
| type            | STRING     | Y           |                      | The order type, possible types: `LIMIT` `STOP`                                                                       |
| fromOrderId     | LONG       | C           | 1470930457684189696  | From Order ID.   For exmaple, OrderIds:1004,1003,1002,1001, if fromOrderId=1003, then 1002 and 1001 will be returned |
| limit           | INTEGER    | C           | 20                   | Default 20, Maximum 500                                                                                              |
| startTime       | LONG       | C           |                      | Start Timestamp, Currently supports the last 7 days timeframe                                                        |
| endTime         | LONG       | C           |                      | End Timestamp                                                                                                        |
| recvWindow      | LONG       |             | 5000                 | recv Window                                                                                                          |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp                                                                                                            |

**Response Content**

```
[ { "time" : "1768983342494" , "orderId" : "2132781291226532106" , "clientOrderId" : "batchorder0121h" , "symbol" : "BTCUSD-PERPETUAL" , "baseAsset" : "BTC" , "quoteAsset" : "USD" , "price" : "88003" , "side" : "BUY" , "orderType" : "limit" , "reduceOnly" : false , "leverage" : "5" , "originalBaseQty" : "0.01" , "executedBaseQty" : "0" , "originalQuoteQty" : "880.03" , "executedQuoteQty" : "0" , "avgPrice" : "0" , "timeInForce" : "GTC" , "status" : "NEW" , "stpMode" : "EXPIRE_TAKER" , "ordCxlReason" : "" , "isLiquidationOrder" : false , "liquidationType" : "" , "slTriggerPrice" : "" , "slTriggerBy" : "" , "tpTriggerPrice" : "" , "tpTriggerBy" : "" }
]
```

| **PARAMETER**      | **TYPE**   | **Example values**   | **DESCRIPTION**                                                                                                   |
|--------------------|------------|----------------------|-------------------------------------------------------------------------------------------------------------------|
| time               | STRING     | 1768794550630        | Timestamp when the order is created                                                                               |
| orderId            | STRING     | 2131197590285846784  | Order ID                                                                                                          |
| clientOrderId      | STRING     | 99999999980001       | A unique ID of the order.                                                                                         |
| symbol             | STRING     | BTCUSD-PERPETUAL     | Name of the contract.                                                                                             |
| baseAsset          | STRING     | BTC                  | Name of the base asset, BTC, ETH, etc                                                                             |
| quoteAsset         | STRING     | USD                  | Name of the quote asset, USDT, USD, etc                                                                           |
| price              | STRING     | 92560                | Price of the order.                                                                                               |
| side               | STRING     | BUY                  | Direction of the order. Possible values include: `BUY` `SELL`                                                     |
| orderType          | STRING     | LIMIT                | The order type                                                                                                    |
| reduceOnly         | BOOLEAN    | false                |                                                                                                                   |
| leverage           | STRING     | 5                    | Leverage of the order.                                                                                            |
| originalBaseQty    | STRING     | 0.01                 | Quantity ordered in Number of baseAsset                                                                           |
| executedBaseQty    | STRING     | 0                    | Quantity that has been executed in Number of baseAsset                                                            |
| originalQuoteQty   | STRING     | 925.6                | Quantity ordered in quoteAsset                                                                                    |
| executedQuoteQty   | STRING     | 0                    | Quantity that has been executed in quoteAsset                                                                     |
| avgPrice           | STRING     | 0                    | Average price of filled orders.                                                                                   |
| timeInForce        | STRING     | GTC                  | Time in force for LIMIT orders. Possible values include: `GTC` , `FOK` , `IOC` .                                  |
| status             | STRING     | CANCELED             | The state of the order. Possible values include:  Limit Orders: `NEW` `PARTIALLY_FILLED` Stop Orders: `ORDER_NEW` |
| stpMode            | STRING     | EXPIRE_TAKER         | Self Trade Prevention Mode.                                                                                       |
| ordCxlReason       | STRING     | USER_CANCEL          | Order cancel reason                                                                                               |
| isLiquidationOrder | BOOLEAN    | false                | Whether the order is a liquidation order                                                                          |
| liquidationType    | STRING     |                      | Available when isLiquidationOrder is true `LIQUIDATION_MAKER_ADL` `LIQUIDATION_MAKER` `LIQUIDATION_TAKER`         |
| slTriggerPrice     | STRING     | 92500                | Stop loss trigger price                                                                                           |
| slTriggerBy        | STRING     | last                 | `last` / `mark`                                                                                                   |
| tpTriggerPrice     | STRING     | 100000               | Take profit trigger price                                                                                         |
| tpTriggerBy        | STRING     | last                 | `last` / `mark`                                                                                                   |

### Query Futures History Orders

**GET** `/api/v2/futures/historyOrders`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   |   **Example values** | **DESCRIPTION**                                                                                                      |
|-----------------|------------|-------------|----------------------|----------------------------------------------------------------------------------------------------------------------|
| symbol          | STRING     | Y           |                      | Name of the contract                                                                                                 |
| fromOrderId     | INTEGER    | C           |                      | From Order ID.   For exmaple, OrderIds:1004,1003,1002,1001, if fromOrderId=1003, then 1002 and 1001 will be returned |
| type            | STRING     | Y           |                      | The order type, possible types: `LIMIT` `STOP`                                                                       |
| startTime       | LONG       | C           |                      | Start Timestamp, Currently supports the last 90 days timeframe                                                       |
| endTime         | LONG       | C           |                      | End Timestamp                                                                                                        |
| limit           | INTEGER    | C           |                   20 | Default 20, Maximum 500                                                                                              |
| recvWindow      | LONG       | C           |                      | recv Window                                                                                                          |
| timestamp       | LONG       | Y           |        1714311403031 | Timestamp                                                                                                            |

**Response Content**

```
[ { "time" : "1768983342494" , "orderId" : "2132781291226532106" , "clientOrderId" : "batchorder0121h" , "symbol" : "BTCUSD-PERPETUAL" , "baseAsset" : "BTC" , "quoteAsset" : "USD" , "price" : "88003" , "side" : "BUY" , "orderType" : "limit" , "reduceOnly" : false , "leverage" : "5" , "originalBaseQty" : "0.01" , "executedBaseQty" : "0.01" , "originalQuoteQty" : "880.03" , "executedQuoteQty" : "880.03" , "avgPrice" : "88003" , "timeInForce" : "GTC" , "status" : "FILLED" , "stpMode" : "EXPIRE_TAKER" , "ordCxlReason" : "" , "isLiquidationOrder" : false , "liquidationType" : "" , "slTriggerPrice" : "" , "slTriggerBy" : "" , "tpTriggerPrice" : "" , "tpTriggerBy" : "" }, { "time" : "1768983342494" , "orderId" : "2132781291226532097" , "clientOrderId" : "batchorder0121g" , "symbol" : "BTCUSD-PERPETUAL" , "baseAsset" : "BTC" , "quoteAsset" : "USD" , "price" : "88002" , "side" : "BUY" , "orderType" : "limit" , "reduceOnly" : false , "leverage" : "5" , "originalBaseQty" : "0.01" , "executedBaseQty" : "0.01" , "originalQuoteQty" : "880.02" , "executedQuoteQty" : "880.02" , "avgPrice" : "88002" , "timeInForce" : "GTC" , "status" : "FILLED" , "stpMode" : "EXPIRE_TAKER" , "ordCxlReason" : "" , "isLiquidationOrder" : false , "liquidationType" : "" , "slTriggerPrice" : "" , "slTriggerBy" : "" , "tpTriggerPrice" : "" , "tpTriggerBy" : "" }
]
```

| **PARAMETER**      | **TYPE**   | **Example values**   | **DESCRIPTION**                                                                                                                                                                                                        |
|--------------------|------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| time               | STRING     | 1768794550630        | Timestamp when the order is created                                                                                                                                                                                    |
| orderId            | STRING     | 2131197590285846784  | Order ID                                                                                                                                                                                                               |
| clientOrderId      | STRING     | 99999999980001       | A unique ID of the order.                                                                                                                                                                                              |
| symbol             | STRING     | BTCUSD-PERPETUAL     | Name of the contract.                                                                                                                                                                                                  |
| baseAsset          | STRING     | BTC                  | Name of the base asset, BTC, ETH, etc                                                                                                                                                                                  |
| quoteAsset         | STRING     | USD                  | Name of the quote asset, USDT, USD, etc                                                                                                                                                                                |
| price              | STRING     | 92560                | Price of the order.                                                                                                                                                                                                    |
| side               | STRING     | BUY                  | Direction of the order. Possible values include: `BUY` `SELL`                                                                                                                                                          |
| orderType          | STRING     | LIMIT                | The order type                                                                                                                                                                                                         |
| reduceOnly         | BOOLEAN    | false                |                                                                                                                                                                                                                        |
| leverage           | STRING     | 5                    | Leverage of the order.                                                                                                                                                                                                 |
| originalBaseQty    | STRING     | 0.01                 | Quantity ordered in Number of baseAsset                                                                                                                                                                                |
| executedBaseQty    | STRING     | 0                    | Quantity that has been executed in Number of baseAsset                                                                                                                                                                 |
| originalQuoteQty   | STRING     | 925.6                | Quantity ordered in quoteAsset                                                                                                                                                                                         |
| executedQuoteQty   | STRING     | 0                    | Quantity that has been executed in quoteAsset                                                                                                                                                                          |
| avgPrice           | STRING     | 0                    | Average price of filled orders.                                                                                                                                                                                        |
| timeInForce        | STRING     | GTC                  | Time in force for LIMIT orders. Possible values include: `GTC` , `FOK` , `IOC` .                                                                                                                                       |
| status             | STRING     | CANCELED             | The state of the order. Possible values include:  Limit Orders: `FILLED` `CANCELED` `PARTIALLY_CANCELED` `REJECTED` Stop Orders: `ORDER_FILLED` `ORDER_REJECTED` `ORDER_CANCELED` `ORDER_FAILED` `ORDER_NOT_EFFECTIVE` |
| stpMode            | STRING     | EXPIRE_TAKER         | Self Trade Prevention Mode.                                                                                                                                                                                            |
| ordCxlReason       | STRING     | USER_CANCEL          | Order cancel reason                                                                                                                                                                                                    |
| isLiquidationOrder | BOOLEAN    | false                | Whether the order is a liquidation order                                                                                                                                                                               |
| liquidationType    | STRING     |                      | Available when isLiquidationOrder is true `LIQUIDATION_MAKER_ADL` `LIQUIDATION_MAKER` `LIQUIDATION_TAKER`                                                                                                              |
| slTriggerPrice     | STRING     | 92500                | Stop loss trigger price                                                                                                                                                                                                |
| slTriggerBy        | STRING     | last                 | `last` / `mark`                                                                                                                                                                                                        |
| tpTriggerPrice     | STRING     | 100000               | Take profit trigger price                                                                                                                                                                                              |
| tpTriggerBy        | STRING     | last                 | `last` / `mark`                                                                                                                                                                                                        |

### Query Futures Positions

**GET** `/api/v2/futures/positions`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                                                                        |
|-----------------|------------|-------------|----------------------|--------------------------------------------------------------------------------------------------------|
| symbol          | STRING     |             | BTCUSD-PERPETUAL     | Name of the contract. **Return results for all symbols if not specified**                              |
| side            | STRING     |             | LONG                 | `LONG` or `SHORT` . Direction of the position. If not sent, positions for both sides will be returned. |
| recvWindow      | LONG       |             | 5000                 | recv window                                                                                            |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp                                                                                              |

**Response Content**

```
[ { "symbol" : "BTCUSD-PERPETUAL" , "baseAsset" : "BTC" , "quoteAsset" : "USD" , "avgPrice" : "91453" , "leverage" : "5" , "lastPrice" : "89897.2" , "baseQty" : "0.195" , "quoteQty" : "17532.0795" , "markPrice" : "89908.1" , "liquidationPrice" : "0" , "margin" : "3506.4163" , "marginRate" : "" , "profitRate" : "-0.0844" , "unrealizedPnL" : "-301.2707" , "realizedPnL" : "-236.7527" , "marginType" : "CROSS" , "positionMode" : "net" , "positionSide" : "LONG" }
]
```

| **PARAMETER**    | **TYPE**   | **Example values**   | **DESCRIPTION**                                                  |
|------------------|------------|----------------------|------------------------------------------------------------------|
| symbol           | STRING     | BTCUSDT-PERPETUAL    | Name of the contract.                                            |
| baseAsset        | STRING     | BTC                  | Name of the base asset                                           |
| quoteAsset       | STRING     | USD                  | Name of the quote asset                                          |
| avgPrice         | STRING     | 100                  | Average price for opening the position.                          |
| leverage         | STRING     | 5                    | Leverage of the position                                         |
| lastPrice        | STRING     | 100                  | Last trade price of the symbol                                   |
| baseQty          | STRING     |                      | Quantity in number of baseAsset                                  |
| quoteQty         | STRING     |                      | Current position value in quoteAsset                             |
| markPrice        | STRING     |                      | Mark Price                                                       |
| liquidationPrice | STRING     | 80                   | Forced liquidation price                                         |
| margin           | STRING     | 20                   | Occupied margin for this position.                               |
| marginRate       | STRING     | 0.2                  | Margin rate for current position                                 |
| profitRate       | STRING     | 0.0000333            | Rate of return for the position                                  |
| unrealizedPnL    | STRING     | 0                    | Unrealized profit and loss for current position held             |
| realizedPnL      | STRING     | 6.8                  | Cumulative realized profit and loss for this symbol              |
| marginType       | STRING     | ISOLATED             | Margin type. Possible values include `CROSS` , `ISOLATED`        |
| positionMode     | STRING     | net                  | `net` or `hedge`                                                 |
| positionSide     | STRING     | LONG                 | Position side, LONG or SHORT. Currently only `LONG` is supported |

### Set Futures Trading Stop

**POST** `/api/v2/futures/position/trading-stop`

**Weight: 3**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                                                                                                                 |
|-----------------|------------|-------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol          | STRING     | Y           |                      | Name of the contract                                                                                                                            |
| positionSide    | ENUM       | C           |                      | Position side， `LONG` or `SHORT` . Default `LONG` . Currently only `LONG` is supported                                                          |
| slTriggerPrice  | STRING     | C           |                      | Stop loss trigger price                                                                                                                         |
| slTriggerBy     | ENUM       | C           |                      | `last` / `mark` Required when slTriggerPrice is filled                                                                                          |
| tpTriggerPrice  | STRING     | C           |                      | Take profit trigger price                                                                                                                       |
| tpTriggerBy     | ENUM       | C           |                      | `last` / `mark` Required when tpTriggerPrice is filled                                                                                          |
| stpMode         | STRING     | C           | EXPIRE_TAKER         | Self Trade Prevention Mode.   Enum: `EXPIRE_TAKER` , `EXPIRE_MAKER` , `EXPIRE_BOTH` , `NOT_EXPIRE` Default **`EXPIRE_TAKER`** if not specified. |
| recvWindow      | LONG       |             | 5000                 | recv window                                                                                                                                     |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp                                                                                                                                       |

**Response Content**

```
{ "symbolId" : "BTCUSD-PERPETUAL" , "positionSide" : "LONG" , "stopProfitPrice" : "95000" , "stopProfitTriggerConditionType" : "MARK_PRICE" , "stopLossPrice" : "85000" , "stopLossTriggerConditionType" : "MARK_PRICE"
}
```

| **PARAMETER**                  | **TYPE**   | **Example values**   | **DESCRIPTION**                                                       |
|--------------------------------|------------|----------------------|-----------------------------------------------------------------------|
| symbol                         | STRING     | BTCUSD-PERPETUAL     | Name of the contract                                                  |
| positionSide                   | STRING     | LONG                 | Position side, `LONG` or `SHORT` . Currently only `LONG` is supported |
| stopProfitPrice                | STRING     | 95000                | Stop profit price                                                     |
| stopProfitTriggerConditionType | STRING     | MARK_PRICE           | `MARK_PRICE` or `CONTRACT_PRICE`                                      |
| stopLossPrice                  | STRING     | 85000                | Stop loss price                                                       |
| stopLossTriggerConditionType   | STRING     | MARK_PRICE           | `MARK_PRICE` or `CONTRACT_PRICE`                                      |

### Query Futures Risk Limit

**GET** `/api/v2/futures/riskLimit`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**       |
|-----------------|------------|-------------|----------------------|-----------------------|
| symbol          | STRING     | Y           | BTCUSD-PERPETUAL     | Name of the contract. |
| recvWindow      | LONG       |             | 5000                 | recv Window           |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp             |

**Response Content**

```
[ { "riskLimitValue" : "125000.00" , "quoteAsset" : "USD" , "maintainMargin" : "0.025" , "initialMargin" : "0.05" , "quickDeduction" : "0.00" , "positionSide" : "BUY" }, { "riskLimitValue" : "125000.00" , "quoteAsset" : "USD" , "maintainMargin" : "0.025" , "initialMargin" : "0.05" , "quickDeduction" : "0.00" , "positionSide" : "SELL" }
]
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**                                         |
|-----------------|------------|----------------------|---------------------------------------------------------|
| riskLimitValue  | STRING     | 125000.00            | Risk limit (Maximum position)                           |
| quoteAsset      | STRING     | USD                  | quoteAsset                                              |
| maintainMargin  | STRING     | 0.025                | Maintenance margin rate                                 |
| initialMargin   | STRING     | 0.05                 | Initial margin rate                                     |
| quickDeduction  | STRING     | 0.00                 | Quickly deduction                                       |
| positionSide    | STRING     | SELL                 | Net mode, `SELL` or `BUY` Hedge mode, `LONG` or `SHORT` |

### Query Futures Leverage

**GET** `/api/v2/futures/leverage`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**      |
|-----------------|------------|-------------|----------------------|----------------------|
| symbol          | STRING     | Y           | BTCUSD-PERPETUAL     | Name of the contract |
| recvWindow      | LONG       |             | 5000                 | recv Window          |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp            |

**Response Content**

```
[ { "symbolId" : "BTCUSD-PERPETUAL" , "leverage" : "5" , "marginType" : "CROSS" }
]
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**                                             |
|-----------------|------------|----------------------|-------------------------------------------------------------|
| symbolId        | STRING     | BTCUSD-PERPETUAL     | Name of the contract                                        |
| leverage        | STRING     | 5                    | Leverage                                                    |
| marginType      | STRING     | CROSS                | Margin type. Possible values include `CROSS` , `ISOLATED` . |

### Change Futures Leverage

**POST** `/api/v2/futures/leverage`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**      |
|-----------------|------------|-------------|----------------------|----------------------|
| symbol          | STRING     | Y           | BTCUSD-PERPETUAL     | Name of the contract |
| leverage        | INTEGER    | Y           | 5                    | Leverage             |
| recvWindow      | LONG       |             | 5000                 | recv Window          |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp            |

**Response Content**

```
{ "code" : "0000" , "symbolId" : "BTCUSD-PERPETUAL" , "leverage" : "5"
}
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**        |
|-----------------|------------|----------------------|------------------------|
| code            | STRING     | 0000                 | Return code of request |
| symbolId        | STRING     | BTCUSD-PERPETUAL     | Name of the contract   |
| leverage        | STRING     | 5                    | Leverage               |

### Query Futures Account Balance

**GET** `/api/v2/futures/balance`

**Weight: 1**

**Request Parameters**

| PARAMETER   | TYPE   | Req'd   | Example values   | DESCRIPTION               |
|-------------|--------|---------|------------------|---------------------------|
| recvWindow  | LONG   |         |                  | Recv Window. Default 5000 |
| timestamp   | LONG   | Y       |                  | Timestamp                 |

**Response Content**

```
[ { "asset" : "USD" , "balance" : "4999769.17379751" , "availableBalance" : "4995106.80365251" }
]
```

| **PARAMETER**    | **TYPE**   | **Example values**   | **DESCRIPTION**                                           |
|------------------|------------|----------------------|-----------------------------------------------------------|
| asset            | STRING     | USD                  | Token Id                                                  |
| balance          | STRING     | 12345.1234           | Token balance                                             |
| availableBalance | STRING     | 10000                | Total + unrealised PnL   sum of dynamic calculated margin |

### Query Futures Funding Rate

**GET** `/api/v2/futures/fundingRate`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                       |
|-----------------|------------|-------------|----------------------|-------------------------------------------------------|
| symbol          | STRING     |             | BTCUSDT-PERPETUAL    | Name of the contract. **Returns [] if not specified** |
| state           | STRING     |             | current              | Funding rate state. Only `current` is supported       |
| recvWindow      | LONG       |             | 5000                 | recv Window                                           |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp                                             |

**Response Content**

```
[ { "symbol" : "BTCUSDT-PERPETUAL" , "rate" : "-0.0005" , "nextFundingTime" : "1769068800000" }
]
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**                    |
|-----------------|------------|----------------------|------------------------------------|
| symbol          | STRING     | BTCUSDT-PERPETUAL    | Name of the contract               |
| rate            | STRING     | -0.0005              | The funding rate for this interval |
| nextFundingTime | STRING     | 1769068800000        | Next fund fee settlement time      |

### Query Futures History Funding Rate

**GET** `/api/v2/futures/historyFundingRate`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                                 |
|-----------------|------------|-------------|----------------------|-----------------------------------------------------------------|
| symbol          | STRING     | Y           | BTCUSD-PERPETUAL     | Name of the contract.                                           |
| fromId          | LONG       |             | 0                    | Start Id                                                        |
| endId           | LONG       |             | 0                    | End Id                                                          |
| limit           | INTEGER    |             | 20                   | Returns the number of entries.   Default 20. (Min 1 to Max 100) |
| recvWindow      | LONG       |             | 5000                 | recv Window                                                     |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp                                                       |

**Response Content**

```
[ { "id" : "40" , "symbol" : "BTCUSD-PERPETUAL" , "settleTime" : "1769040000000" , "settleRate" : "-0.0005" }, { "id" : "36" , "symbol" : "BTCUSD-PERPETUAL" , "settleTime" : "1769011200000" , "settleRate" : "0.000027379608" }
]
```

| **PARAMETER**   | **TYPE**      | **Example values**   | **DESCRIPTION**              |
|-----------------|---------------|----------------------|------------------------------|
| *               | Object Arrays |                      |                              |
| id              | STRING        | 40                   | Unique identifier            |
| symbol          | STRING        | BTCUSD-PERPETUAL     | Name of the contract         |
| settleTime      | STRING        | 1769040000000        | Capital rate settlement time |
| settleRate      | STRING        | -0.0005              | Fund rate                    |

### Query Futures History Funding Fees

**GET** `/api/v2/futures/historyFundingFees`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                                                                    |
|-----------------|------------|-------------|----------------------|----------------------------------------------------------------------------------------------------|
| symbol          | STRING     | Y           | BTCUSDT-PERPETUAL    | Name of the contract                                                                               |
| startTime       | LONG       | Y           | 1714311403031        | Start Timestamp                                                                                    |
| endTime         | LONG       | Y           | 1714311403031        | End Timestamp                                                                                      |
| accountId       | LONG       |             |                      | Futures account ID. Main / Sub trading account. Default to the current futures account if not sent |
| limit           | INTEGER    |             | 500                  | Returns the number of entries. Default 500, Maximum 1000                                           |
| recvWindow      | LONG       |             | 5000                 | recv Window                                                                                        |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp                                                                                          |

**Response Content**

```
[ { "symbol" : "BTCUSDT-PERPETUAL" , "fundingTime" : "1783900800000" , "positionSide" : "LONG" , "positionSize" : "0.01" , "markPrice" : "64033.8" , "fundingRate" : "0.004749619972095341" , "fee" : "-3.04136215369158646" , "feeAsset" : "USDT" }, { "symbol" : "BTCUSDT-PERPETUAL" , "fundingTime" : "1783872000000" , "positionSide" : "LONG" , "positionSize" : "0.01" , "markPrice" : "64331.433333333333269159" , "fundingRate" : "0.003846753938943691" , "fee" : "-2.47467194572893461" , "feeAsset" : "USDT" }
]
```

| **PARAMETER**   | **TYPE**      | **Example values**   | **DESCRIPTION**                                                  |
|-----------------|---------------|----------------------|------------------------------------------------------------------|
| *               | Object Arrays |                      |                                                                  |
| symbol          | STRING        | BTCUSDT-PERPETUAL    | Name of the contract                                             |
| fundingTime     | STRING        | 1769040000000        | Fund fee settlement time                                         |
| positionSide    | STRING        | LONG                 | Position side. `LONG` `SHORT` Currently only `LONG` is supported |
| positionSize    | STRING        | 0.01                 | Position size at settlement                                      |
| markPrice       | STRING        | 88003                | Mark price at settlement                                         |
| fundingRate     | STRING        | -0.0005              | The funding rate for this interval                               |
| fee             | STRING        | -0.440015            | Funding fee. Negative means paid                                 |
| feeAsset        | STRING        | USDT                 | Currency of the funding fee                                      |

### Query Futures Commission Rate

**GET** `/api/v2/futures/commissionRate`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**       |
|-----------------|------------|-------------|----------------------|-----------------------|
| symbol          | STRING     | Y           | BTCUSD-PERPETUAL     | Name of the contract. |
| recvWindow      | LONG       |             | 5000                 | recv Window           |
| timestamp       | LONG       | Y           | 1714311403031        | Timestamp             |

**Response Content**

```
{ "symbol" : "BTCUSD-PERPETUAL" , "makerFeeRate" : "0.0006" , "takerFeeRate" : "0.0006"
}
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**               |
|-----------------|------------|----------------------|-------------------------------|
| symbol          | STRING     | BTCUSD-PERPETUAL     | Name of the contract          |
| makerFeeRate    | STRING     | 0.0006               | The commission rate for maker |
| takerFeeRate    | STRING     | 0.0006               | The commission rate for taker |

## Account

### Get VIP Information

**GET** `/api/v1/account/vipInfo`

Retrieve VIP Level and Trading fee rates

**Weight: 5**

**Request Parameters**

| PARAMETER   | TYPE   | Req'd   | Example values   | DESCRIPTION               |
|-------------|--------|---------|------------------|---------------------------|
| symbols     | STRING |         |                  | Trading pairs             |
| recvWindow  | LONG   |         |                  | Recv Window. Default 5000 |
| timestamp   | LONG   | Y       |                  | Timestamp                 |

**Response Content**

```
{ "code" : 0 , "vipLevel" : "0" , "tradeVol30Day" : "0" , "totalAssetBal" : "0" , "data" : [ { "symbol" : "USDTUSD" , "productType" : "Token-Fiat" , "buyMakerFeeCurrency" : "USD" , "buyTakerFeeCurrency" : "USD" , "sellMakerFeeCurrency" : "USD" , "sellTakerFeeCurrency" : "USD" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "ATOMUSDC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "ATOM" , "buyTakerFeeCurrency" : "ATOM" , "sellMakerFeeCurrency" : "USDC" , "sellTakerFeeCurrency" : "USDC" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "ATOMBTC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "ATOM" , "buyTakerFeeCurrency" : "ATOM" , "sellMakerFeeCurrency" : "BTC" , "sellTakerFeeCurrency" : "BTC" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "BTCHKD" , "productType" : "Token-Fiat" , "buyMakerFeeCurrency" : "HKD" , "buyTakerFeeCurrency" : "HKD" , "sellMakerFeeCurrency" : "HKD" , "sellTakerFeeCurrency" : "HKD" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "EOSUSDC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "EOS" , "buyTakerFeeCurrency" : "EOS" , "sellMakerFeeCurrency" : "USDC" , "sellTakerFeeCurrency" : "USDC" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "ETHUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.00025" , "actualTakerRate" : "0.0006" }, { "symbol" : "BTCUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.00025" , "actualTakerRate" : "0.0006" }, { "symbol" : "ATOMUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "ATOM" , "buyTakerFeeCurrency" : "ATOM" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "EOSUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "QT2USDC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "QT2" , "buyTakerFeeCurrency" : "QT2" , "sellMakerFeeCurrency" : "USDC" , "sellTakerFeeCurrency" : "USDC" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "HSKUSDC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "HSK" , "buyTakerFeeCurrency" : "HSK" , "sellMakerFeeCurrency" : "USDC" , "sellTakerFeeCurrency" : "USDC" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "DOTUSD" , "productType" : "Token-Fiat" , "buyMakerFeeCurrency" : "USD" , "buyTakerFeeCurrency" : "USD" , "sellMakerFeeCurrency" : "USD" , "sellTakerFeeCurrency" : "USD" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "SANDUSD" , "productType" : "Token-Fiat" , "buyMakerFeeCurrency" : "USD" , "buyTakerFeeCurrency" : "USD" , "sellMakerFeeCurrency" : "USD" , "sellTakerFeeCurrency" : "USD" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "BCHUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "BCH" , "buyTakerFeeCurrency" : "BCH" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "QATS4USDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "ETHUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "ETH" , "buyTakerFeeCurrency" : "ETH" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "SHIBUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "ATBTC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "AT" , "buyTakerFeeCurrency" : "AT" , "sellMakerFeeCurrency" : "BTC" , "sellTakerFeeCurrency" : "BTC" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "TONUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "TON" , "buyTakerFeeCurrency" : "TON" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "WIFUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "DOGEUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "DOGE" , "buyTakerFeeCurrency" : "DOGE" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "ETHEOS" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "ETH" , "buyTakerFeeCurrency" : "ETH" , "sellMakerFeeCurrency" : "EOS" , "sellTakerFeeCurrency" : "EOS" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "QATS5USDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "QTBTC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "QT" , "buyTakerFeeCurrency" : "QT" , "sellMakerFeeCurrency" : "BTC" , "sellTakerFeeCurrency" : "BTC" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "ATOMUSD" , "productType" : "Token-Fiat" , "buyMakerFeeCurrency" : "USD" , "buyTakerFeeCurrency" : "USD" , "sellMakerFeeCurrency" : "USD" , "sellTakerFeeCurrency" : "USD" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "DOGEUSDC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "DOGE" , "buyTakerFeeCurrency" : "DOGE" , "sellMakerFeeCurrency" : "USDC" , "sellTakerFeeCurrency" : "USDC" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "MATICUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "MATIC" , "buyTakerFeeCurrency" : "MATIC" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "HTGLUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "HTGL" , "buyTakerFeeCurrency" : "HTGL" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "QTUSDC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "QT" , "buyTakerFeeCurrency" : "QT" , "sellMakerFeeCurrency" : "USDC" , "sellTakerFeeCurrency" : "USDC" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "SANDUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "SAND" , "buyTakerFeeCurrency" : "SAND" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "QATS1USDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "AVAXUSD" , "productType" : "Token-Fiat" , "buyMakerFeeCurrency" : "USD" , "buyTakerFeeCurrency" : "USD" , "sellMakerFeeCurrency" : "USD" , "sellTakerFeeCurrency" : "USD" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "PEPEUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "EOSETH" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "EOS" , "buyTakerFeeCurrency" : "EOS" , "sellMakerFeeCurrency" : "ETH" , "sellTakerFeeCurrency" : "ETH" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "COMPUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "COMP" , "buyTakerFeeCurrency" : "COMP" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "BTCUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "BTC" , "buyTakerFeeCurrency" : "BTC" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "USDCUSD" , "productType" : "Token-Fiat" , "buyMakerFeeCurrency" : "USD" , "buyTakerFeeCurrency" : "USD" , "sellMakerFeeCurrency" : "USD" , "sellTakerFeeCurrency" : "USD" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "NOTUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "NOT" , "buyTakerFeeCurrency" : "NOT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "GMXUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "GMX" , "buyTakerFeeCurrency" : "GMX" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "QATS2USDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "LTCUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "LTC" , "buyTakerFeeCurrency" : "LTC" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "SPICEUSDT" , "productType" : "ST-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "NOTUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "HSKUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "HSK" , "buyTakerFeeCurrency" : "HSK" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "DOTUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "DOT" , "buyTakerFeeCurrency" : "DOT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "SOLUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "ZZZUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "ZZZ" , "buyTakerFeeCurrency" : "ZZZ" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "QTETH" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "QT" , "buyTakerFeeCurrency" : "QT" , "sellMakerFeeCurrency" : "ETH" , "sellTakerFeeCurrency" : "ETH" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "NOTUSDC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "NOT" , "buyTakerFeeCurrency" : "NOT" , "sellMakerFeeCurrency" : "USDC" , "sellTakerFeeCurrency" : "USDC" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "XRPUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "USDTUSDC" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDC" , "sellTakerFeeCurrency" : "USDC" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "DYDXUSDT" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "DYDX" , "buyTakerFeeCurrency" : "DYDX" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0012" , "actualTakerRate" : "0.0012" }, { "symbol" : "AVAXUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "ETHHKD" , "productType" : "Token-Fiat" , "buyMakerFeeCurrency" : "HKD" , "buyTakerFeeCurrency" : "HKD" , "sellMakerFeeCurrency" : "HKD" , "sellTakerFeeCurrency" : "HKD" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" }, { "symbol" : "DOGEUSDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0.0006" , "actualTakerRate" : "0.0006" }, { "symbol" : "QATS3USDT-PERPETUAL" , "productType" : "Token-Token" , "buyMakerFeeCurrency" : "USDT" , "buyTakerFeeCurrency" : "USDT" , "sellMakerFeeCurrency" : "USDT" , "sellTakerFeeCurrency" : "USDT" , "actualMakerRate" : "0" , "actualTakerRate" : "0" }, { "symbol" : "QTUSD" , "productType" : "Token-Fiat" , "buyMakerFeeCurrency" : "USD" , "buyTakerFeeCurrency" : "USD" , "sellMakerFeeCurrency" : "USD" , "sellTakerFeeCurrency" : "USD" , "actualMakerRate" : "0.0015" , "actualTakerRate" : "0.0015" } ], "updateTimestamp" : "1740383504179"
}
```

| **PARAMETER**          | **TYPE**     | Example values   | **DESCRIPTION**                                  |
|------------------------|--------------|------------------|--------------------------------------------------|
| code                   | INTEGER      | 0                | Status code                                      |
| msg                    | STRING       |                  | Error message (if any)                           |
| vipLevel               | STRING       | 0                | VIP Level                                        |
| tradeVol30Day          | STRING       | 300000000        | Total trading volume in Last 30 days (USD)       |
| totalAssetBal          | STRING       | 1000000000       | Total asset balance (USD)                        |
| data                   | Object Array |                  |                                                  |
| - symbol               | STRING       |                  | Trading pair                                     |
| - productType          | STRING       | Token-Token      | Token-Token, Token-Fiat, ST-Token                |
| - buyMakerFeeCurrency  | STRING       | BTC              | Buy maker fee currency                           |
| - buyTakerFeeCurrency  | STRING       | BTC              | Buy taker fee currency                           |
| - sellMakerFeeCurrency | STRING       | USD              | Sell maker fee currency                          |
| - sellTakerFeeCurrency | STRING       | USD              | Sell taker fee currency                          |
| - actualMakerRate      | STRING       | 0.015            | Maker fee including any discount                 |
| - actualTakerRate      | STRING       | 0.015            | Taker fee including any discount                 |
| updateTimeStamp        | STRING       | 1709330424013    | Update timestamp of the request (Daily snapshot) |

### Get Account Information

**GET** `/api/v1/account`

Retrieve account balance

**Weight: 5**

**Request Parameters**

| PARAMETER   | TYPE   | Req'd   |      Example values | DESCRIPTION                                                                                                                    |
|-------------|--------|---------|---------------------|--------------------------------------------------------------------------------------------------------------------------------|
| accountId   | LONG   |         | 1471090223379184384 | Account ID, for Master Key only (Master Key users can check sub trading account information by inputing sub trading accountId) |
| recvWindow  | LONG   |         |                     | Recv Window. Default 5000                                                                                                      |
| timestamp   | LONG   | Y       |                     | Timestamp                                                                                                                      |

**Response Content**

```
{ "balances" : [ { "asset" : "BTC" , "assetId" : "BTC" , "assetName" : "BTC" , "total" : "61.206456639" , "free" : "61.051866639" , "locked" : "0.15459" }, { "asset" : "ETH" , "assetId" : "ETH" , "assetName" : "ETH" , "total" : "1152.49672544" , "free" : "1152.49672544" , "locked" : "0" }, { "asset" : "USDC" , "assetId" : "USDC" , "assetName" : "USDC" , "total" : "4098.36" , "free" : "4098.36" , "locked" : "0" }, { "asset" : "USDT" , "assetId" : "USDT" , "assetName" : "USDT" , "total" : "206381.2785765348009" , "free" : "206381.2785765348009" , "locked" : "0" } ], "userId" : "1649292498445571840"
}
```

| **PARAMETER**      | **TYPE**     | **Example values**   | **DESCRIPTION**       |
|--------------------|--------------|----------------------|-----------------------|
| balances           | Object Array |                      | Query an asset array  |
| balances.asset     | STRING       | BTC                  | Assets                |
| balances.assetId   | STRING       | BTC                  | Asset ID              |
| balances.assetName | STRING       | BTC                  | Asset Name            |
| balances.total     | STRING       | 100.63264            | Total available funds |
| balances.free      | STRING       | 100.63264            | Available funds       |
| balances.locked    | STRING       | 0                    | Frozen funds          |
| userId             | STRING       | 1649292498445571840  | User ID               |

### Get Account Trade List

**GET** `/api/v1/account/trades`

Query account history and transaction records

**Weight: 5**

**Request Parameters**

- If there is only fromId, It will return trades with IDs bigger than fromId, sorted in descending order.
- If there is only toId. It will return trades with IDs less than toId, sorted in descending order
- If both fromId and toId are provided. It will return trades between fromId and toId, sorted in descending order
- If neither fromId or toId is provided, it will return the latest trade records, sorted in descending order.

| **PARAMETER**   | **TYPE**   | Req'd   | **DESCRIPTION**                                           |
|-----------------|------------|---------|-----------------------------------------------------------|
| symbol          | STRING     |         | Trading pair                                              |
| startTime       | LONG       |         | Start Timestamp, Only supports the last 30 days timeframe |
| endTime         | LONG       |         | End Timestamp.                                            |
| clientOrderId   | STRING     |         | Client Order ID                                           |
| fromId          | LONG       |         | Starting ID                                               |
| toId            | LONG       |         | End ID                                                    |
| limit           | INT        |         | Limit of record. Default 500, max 1000                    |
| accountId       | LONG       |         | Account ID                                                |
| recvWindow      | LONG       |         | Recv Window. Default 5000                                 |
| timestamp       | LONG       | Y       | Timestamp                                                 |

**Response Content**

```
[ { "id" : "2133553701515831040" , "clientOrderId" : "1769075420193253" , "ticketId" : "4636458470505791492" , "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "orderId" : "2133553695652194048" , "matchOrderId" : "0" , "price" : "112935.08" , "qty" : "0.01098" , "commission" : "0.000013176" , "commissionAsset" : "BTC" , "time" : "1769075420311" , "isBuyer" : true , "isMaker" : false , "fee" : { "feeCoinId" : "BTC" , "feeCoinName" : "BTC" , "fee" : "0.000013176" , "originCoinId" : "BTC" , "originCoinName" : "BTC" , "originFee" : "0.000013176" }, "feeCoinId" : "BTC" , "feeAmount" : "0.000013176" , "makerRebate" : "0" , "hskDeduct" : false , "hskDeductPrice" : "" }, { "id" : "2133553700836353792" , "clientOrderId" : "1769075420193253" , "ticketId" : "4636458470505791491" , "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "orderId" : "2133553695652194048" , "matchOrderId" : "0" , "price" : "112935.06" , "qty" : "0.035" , "commission" : "0.000042" , "commissionAsset" : "BTC" , "time" : "1769075420311" , "isBuyer" : true , "isMaker" : false , "fee" : { "feeCoinId" : "BTC" , "feeCoinName" : "BTC" , "fee" : "0.000042" , "originCoinId" : "BTC" , "originCoinName" : "BTC" , "originFee" : "0.000042" }, "feeCoinId" : "BTC" , "feeAmount" : "0.000042" , "makerRebate" : "0" , "hskDeduct" : false , "hskDeductPrice" : "" }
]
```

| **PARAMETER**      | **TYPE**         | **Example values**   | **DESCRIPTION**                                                                                                |
|--------------------|------------------|----------------------|----------------------------------------------------------------------------------------------------------------|
| *                  | Object Array     |                      | Check transaction results                                                                                      |
| id                 | STRING           | 1470930841345474561  | Unique transaction ID                                                                                          |
| clientOrderId      | STRING           | 999999999800021      | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| ticketId           | STRING           | 1478144171272585249  | Execution ID, the execution ID is the same for the direction of a single trade.                                |
| symbol             | STRING           | BTCUSD               | Trading pair                                                                                                   |
| symbolName         | STRING           | BTCUSD               | Trading pair name                                                                                              |
| orderId            | STRING           | 1470930841211329280  | Order ID                                                                                                       |
| matchOrderId       | STRING           |                      | //Ignore                                                                                                       |
| price              | STRING (decimal) | 29851.03             | Price                                                                                                          |
| qty                | STRING (decimal) | 0.0005               | Quantity                                                                                                       |
| commission         | STRING (decimal) | 0.02985103           | Commission fee                                                                                                 |
| commissionAsset    | STRING           | USD                  | Currency of commission fee                                                                                     |
| time               | STRING (decimal) | 1690084620567        | Millisecond Timestamp - trade time (traded but not yet settled) 撮合成交时间                                         |
| isBuyer            | BOOLEAN          | false                | Whether the trade is a buyer                                                                                   |
| isMaker            | BOOLEAN          | false                | Whether the trade is a maker                                                                                   |
| fee                | Object           |                      | Fee information                                                                                                |
| fee.feeCoinId      | STRING           | USD                  | Fee currency                                                                                                   |
| fee.feeCoinName    | STRING           | USD                  | Fee currency name                                                                                              |
| fee.fee            | STRING (decimal) | 0.02985103           | Transaction fee amount after HSK deduction                                                                     |
| fee.originFee      | STRING (decimal) | 0.03085103           | The commission fee before HSK deduction.                                                                       |
| fee.originCoinId   | STRING           | USD                  | The commission fee before HSK deduction                                                                        |
| fee.originCoinName | STRING           | USD                  | The commission fee coin                                                                                        |
| feeCoinId          | STRING           | USD                  | Fee currency                                                                                                   |
| feeAmount          | STRING (decimal) | 0.02985103           | Amount of transaction fee                                                                                      |
| makerRebate        | STRING           | 0                    | Return                                                                                                         |
| hskDeduct          | BOOLEAN          | true                 | true: successfully deducted HSK  false                                                                         |
| hskDeductPrice     | STRING           | 0.001                | commission Coin price / HSK price                                                                              |

### Query Account Type

**GET** `/api/v1/account/type`

**Account Type**

|   accountType | Type                     |
|---------------|--------------------------|
|             1 | Main Trading Account     |
|             3 | Futures Account          |
|             5 | Custody Account          |
|             6 | Fiat Account             |
|             7 | OPT Account              |
|             1 | Sub Main Trading Account |
|             3 | Sub Futures Account      |

**Weight: 5**

**Request Parameters**

| PARAMETER   | TYPE   | Req'd   | Example values   | DESCRIPTION               |
|-------------|--------|---------|------------------|---------------------------|
| recvWindow  | LONG   |         |                  | Recv Window. Default 5000 |
| timestamp   | LONG   | Y       |                  | Timestamp                 |

**Response Content**

```
[ { "accountId" : "1933473576343719680" , "accountLabel" : "Main Trading Account" , "accountType" : 1 , "accountIndex" : 0 , "userId" : "1933473576368885504" }, { "accountId" : "1933473576343719683" , "accountLabel" : "Custody Account" , "accountType" : 5 , "accountIndex" : 0 , "userId" : "1933473576368885504" }
]
```

| **PARAMETER**   | **TYPE**     | **Example values**   | **DESCRIPTION**          |
|-----------------|--------------|----------------------|--------------------------|
| *               | Object Array |                      | Query subaccount results |
| accountId       | STRING       | 1954336770171707136  | Account Number           |
| accountLabel    | STRING       | Custody Account      | Account Label            |
| accountType     | INTEGER      | 1                    | Account Type             |
| accountIndex    | INTEGER      | 0                    | //Ignore                 |
| userId          | STRING       | 1954336770188484352  | UserId of the account    |

### Internal Account Transfer

***This endpoint should be called no more than once per second.***

**POST** `/api/v1/account/assetTransfer`

📘 Currently internal transfer endpoint only available to Master account API Key

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**        | Req 'd   | **Example values**   | **DESCRIPTION**                                      |
|-----------------|-----------------|----------|----------------------|------------------------------------------------------|
| fromAccountId   | STRING          | Y        | 1467296062716909568  | Source Account ID                                    |
| toAccountId     | STRING          | Y        | 1473231491689395200  | Destinate Account ID                                 |
| coin            | STRING          | Y        | USDT                 | Coin                                                 |
| quantity        | STRING(DECIMAL) | Y        | 20                   | Transfer amount                                      |
| remark          | STRING          |          | TestingRemark        | Remark                                               |
| clientOrderId   | STRING          |          | 12345678             | Client unique order identifier (up to 64 characters) |
| recvWindow      | LONG            |          |                      | Recv Window. Default 5000                            |
| timestamp       | LONG            | Y        | 1712317312973        | Timestamp                                            |

**Response Content**

```
{ "success" : true , "timestamp" : 1766583205575 , "clientOrderId" : "" , "orderId" : "2112647482861233664"
}
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**                |
|-----------------|------------|----------------------|--------------------------------|
| success         | BOOLEAN    | TRUE                 | Whether successful             |
| timestamp       | LONG       | 1699943911155        | Transfer completed time        |
| clientOrderId   | STRING     | 12345678             | Client unique order identifier |
| orderId         | STRING     | 1555687946987836672  | Transfer Order ID              |

### Get API Key Type

**GET** `/api/v1/account/checkApiKey`

**Weight: 1**

**Request Parameters**

| PARAMETER   | TYPE   | Req'd   | Example values   | DESCRIPTION               |
|-------------|--------|---------|------------------|---------------------------|
| recvWindow  | LONG   |         |                  | Recv Window. Default 5000 |
| timestamp   | LONG   | Y       |                  | Timestamp                 |

**Response Content**

```
{ "accountType" : "Master Account"
}
```

| **PARAMETER**   | **TYPE**   | **Example values**             | **DESCRIPTION**   |
|-----------------|------------|--------------------------------|-------------------|
| accountType     | STRING     | `Master Account` `Sub Account` | Account Type      |

### Get Fund Statement

**GET** `/api/v1/account/balanceFlow`

- Only master account Master API key can call this interface, sub-accounts will return insufficient privilege type error code
- All orders returned are final
- Deposit, Withdrawal failed will not be returned
- Query of trade history supports the past 14 days time range(though the endpoint support up to get 7 days data for each request). The other types support maximum 30 days. Exceeded amount will return error code "Exceed maximum time range of N days"
- Remark can only support up to 128 characters

**Weight: 3**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **DESCRIPTION**                                                                                                                                                        |
|-----------------|------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| accountId       | LONG       |             | Account ID                                                                                                                                                             |
| type            | STRING     | Y           | Transaction type:   "trade"   "deposit"   "fiatDeposit"   "withdraw"   "fiatWithdraw"   "transfer"   "reversal"   "refund"   "voucher"   "fundingFee"   "futuresTrade" |
| clientOrderId   | STRING     |             | Corresponds to types: "trade", "withdraw", "transfer", "futuresTrade"                                                                                                  |
| remark          | STRING     |             | Remark                                                                                                                                                                 |
| startTime       | LONG       | Y           | Start timestamp                                                                                                                                                        |
| endTime         | LONG       | Y           | End timestamp                                                                                                                                                          |
| beginId         | INT        |             | Start record number. Default: 0 E.g. If input ID is 1, return starting ID as 2                                                                                         |
| limit           | INT        |             | Limit                                                                                                                                                                  |
| recvWindow      | LONG       |             | Recv Window. Default 5000                                                                                                                                              |
| timestamp       | LONG       | Y           | Timestamp                                                                                                                                                              |

**Response Content**

**Type = trade**

Supported for the past 7 days time range

```
[ { "id" : "47049" , "accountId" : "1617382306753847296" , "type" : "trade" , "netBaseAmount" : "0.00015" , "baseCcy" : "BTC" , "baseAssetBalance" : "96.53346265" , "netQuoteAmount" : "-9.622275" , "quoteCcy" : "USDC" , "quoteAssetBalance" : "887623.4732212" , "direction" : "BUY" , "fee" : "0.000000225" , "feeCcy" : "BTC" , "clientOrderId" : "99999999980097" , "orderId" : "1733373323360866560" , "tradeId" : "1733373323528638720" , "transactTime" : "1721370202000" //Trade Completed time }, { "id" : "47050" , "accountId" : "1617382306753847296" , "type" : "trade" , "netBaseAmount" : "0.29951" , "baseCcy" : "BTC" , "baseAssetBalance" : "96.83297265" , "netQuoteAmount" : "-9984.7019729" , "quoteCcy" : "USD" , "quoteAssetBalance" : "679.337974140649999999" , "direction" : "BUY" , "fee" : "14.97705295935" , "feeCcy" : "USD" , "clientOrderId" : "99999999980098" , "orderId" : "1733374982912741632" , "tradeId" : "1733374983021793536" , "transactTime" : "1721370400000" //Trade Completed time }
]
```

| **PARAMETER**          | **TYPE**   | **DESCRIPTION**                                                             |
|------------------------|------------|-----------------------------------------------------------------------------|
| id                     | STRING     | Record ID                                                                   |
| accountId              | STRING     | Account ID                                                                  |
| type                   | STRING     | "trade"                                                                     |
| netBaseAmount          | STRING     | Order Quantity Default Value ="" Buy direction (+ve) Sell direction (-ve)   |
| baseCcy                | STRING     | Base currency                                                               |
| baseAssetBalance       | STRING     | Base asset balance Default Value =""                                        |
| netQuoteAmount         | STRING     | Price * Quantity Default Value ="" Buy direction (-ve) Sell direction (+ve) |
| quoteAssetBalance      | STRING     | Quote asset balance Default Value =""                                       |
| quoteCcy               | STRING     | E.g. USDT, USDC, USD                                                        |
| direction              | STRING     | BUY or SELL                                                                 |
| fee                    | STRING     | Trading fee Default Value = 0                                               |
| feeSupplementaryAmount | STRING     | Supplementary commission fee to meet minimum commission fee requirement     |
| feeCcy                 | STRING     | E.g. BTC, ETH, USDC                                                         |
| clientOrderId          | STRING     | Client order ID                                                             |
| orderId                | STRING     | Order ID                                                                    |
| tradeId                | STRING     | Trade ID                                                                    |
| transactTime           | STRING     | Trade completed and settled time 结算完成时间                                     |

**Type = deposit/withdraw/refund**

Supported for the past 30 days time range

```
[ { "id" : "720" , "accountId" : "1978966613676937217" , "type" : "Deposit" , "netVaAmount" : "8989" , "vaCcy" : "USDT" , "vaChainType" : "Tron" , "vaBalance" : "1030784.1498" , "fee" : "0.0001" , "feeCcy" : "USDT" , "orderId" : "D768973742990266368" , "txnId" : "" , "remark" : "" , "transactTime" : "1761145789691" , "clientOrderId" : "" }, { "id" : "343" , "accountId" : "1954346749805043457" , "type" : "Withdraw" , "netVaAmount" : "180" , "vaCcy" : "USDT" , "vaChainType" : "Tron" , "vaBalance" : "0" , "fee" : "0" , "feeCcy" : "USDT" , "orderId" : "W769152094447452160" , "txnId" : "3dafba8abd7a7b2d02ac9161b41313931c9bafa18cf8cec2c98b1a4ec300be32" , "remark" : "" , "transactTime" : "1761188210875" , "clientOrderId" : "usdttron102303" }, { "id" : "335" , "accountId" : "1954346689088298753" , "type" : "Refund" , "netVaAmount" : "100.1199" , "vaCcy" : "USDT" , "vaChainType" : "Tron" , "vaBalance" : "200.2697" , "fee" : "0.0001" , "feeCcy" : "USDT" , "orderId" : "refund_D768944634495336448" , "txnId" : "" , "remark" : "" , "transactTime" : "1761139348000" , "clientOrderId" : "" }
]
```

| **PARAMETER**   | **TYPE**   | **DESCRIPTION**                               |
|-----------------|------------|-----------------------------------------------|
| id              | STRING     | Record ID                                     |
| accountId       | STRING     | Account ID                                    |
| type            | STRING     | "Deposit", "Withdraw", "Refund"               |
| netVaAmount     | STRING     | Deposit/Withdraw: amount Default Value = 0    |
| vaCcy           | STRING     | ETH, BTC, USDC, etc                           |
| vaChainType     | STRING     | Tron                                          |
| vaBalance       | STRING     | Fiat balance in the account Default Value = 0 |
| fee             | STRING     | Deposit/Withdraw Fee Default Value = 0        |
| feeCcy          | STRING     | Fee Currency                                  |
| clientOrderId   | STRING     | The unique ID assigned by the client          |
| orderId         | STRING     | Deposit/Withdraw Order ID                     |
| txnId           | STRING     | Chain Transaction ID                          |
| remark          | STRING     | Remark                                        |
| transactTime    | STRING     | Deposit/Withdraw Completed Time               |

**Type = transfer**

Supported for the past 30 days time range

```
[ { "id" : "2286" , "fromAccountId" : "1471090223379184385" , "toAccountId" : "1471090223379184384" , "type" : "transfer" , "netTransferAmount" : "1" , "transferCcy" : "BTC" , "fromAccountBalance" : "1304.36501272" , "toAccountBalance" : "6080.570119335" , "orderId" : "1944297063069140480" , // Transfer order ID "remark" : "" , "transactTime" : "1746514272000" , "clientOrderId" : "" }, { "id" : "2287" , "fromAccountId" : "1471090223379184385" , "toAccountId" : "1471090223379184384" , "type" : "transfer" , "netTransferAmount" : "1" , "transferCcy" : "BTC" , "fromAccountBalance" : "1303.36501272" , "toAccountBalance" : "6081.570119335" , "orderId" : "1944304593916806656" , // Transfer order ID "remark" : "" , "transactTime" : "1746515169000" , "clientOrderId" : "" }
]
```

| **PARAMETER**      | **TYPE**   | **DESCRIPTION**                                      |
|--------------------|------------|------------------------------------------------------|
| id                 | STRING     | Record ID                                            |
| fromAccountId      | STRING     | From Account ID                                      |
| toAccountId        | STRING     | To Account ID                                        |
| type               | STRING     | "transfer"                                           |
| netTransferAmount  | STRING     | Transfer Amount Default Value = 0                    |
| transferCcy        | STRING     | ETH, BTC, USDC, etc                                  |
| fromAccountBalance | STRING     | From Account balance Default Value = 0               |
| toAccountBalance   | STRING     | To Account balance Default Value = 0                 |
| orderId            | STRING     | Transfer OrderID                                     |
| remark             | STRING     | Remark                                               |
| transactTime       | STRING     | Transfer Completed Time                              |
| clientOrderId      | STRING     | An ID defined by the client for the withdrawal order |

**Type = fundingFee**

Supported for the past 30 days time range

```
[ { "id" : "7" , "accountId" : "2247858875746320640" , "type" : "fundingFee" , "currency" : "USDT" , "beforeBalance" : "99999998.02493143347090987" , "fundingFee" : "-0.04938848" , "afterBalance" : "99999997.97554295347090987" , "positionSide" : "Long" , "transactTime" : "1783526460000" , "symbol" : "BTCUSDT-PERPETUAL" , "fundingRate" : "0.00008" }, { "id" : "8" , "accountId" : "2247858875746320640" , "type" : "fundingFee" , "currency" : "USDT" , "beforeBalance" : "99999997.97554295347090987" , "fundingFee" : "-0.04982348266666666" , "afterBalance" : "99999997.92571947080424321" , "positionSide" : "Long" , "transactTime" : "1783555260000" , "symbol" : "BTCUSDT-PERPETUAL" , "fundingRate" : "0.00008" }
]
```

| **PARAMETER**   | **TYPE**   | **DESCRIPTION**                    |
|-----------------|------------|------------------------------------|
| id              | STRING     | Record ID                          |
| accountId       | STRING     | Account ID                         |
| type            | STRING     | "fundingFee"                       |
| currency        | STRING     | E.g. USDT, USDC                    |
| beforeBalance   | STRING     | Balance before settlement          |
| fundingFee      | STRING     | Funding fee. Negative means paid   |
| afterBalance    | STRING     | Balance after settlement           |
| positionSide    | STRING     | "Long", "Short"                    |
| transactTime    | STRING     | Funding fee settlement time        |
| symbol          | STRING     | Name of the contract               |
| fundingRate     | STRING     | The funding rate for this interval |

**Type = futuresTrade**

Supported for the past 7 days time range

```
[ { "id" : "1" , "accountId" : "2247858875746320640" , "type" : "futuresTrade" , "currency" : "USDT" , "beforeBalance" : "99999997.72327444413757655" , "realizedPnL" : "0" , "afterBalance" : "99999997.68487252413757655" , "fee" : "0.03840192" , "feeSupplementaryAmount" : "0" , "feeCcy" : "USDT" , "clientOrderId" : "1783698931866" , "orderId" : "2256224625931847936" , "tradeId" : "2256224626032511232" , "transactTime" : "1783698934000" , "symbol" : "BTCUSDT-PERPETUAL" }, { "id" : "2" , "accountId" : "2247858875746320640" , "type" : "futuresTrade" , "currency" : "USDT" , "beforeBalance" : "99999997.68487252413757655" , "realizedPnL" : "0" , "afterBalance" : "99999997.60806868413757655" , "fee" : "0.07680384" , "feeSupplementaryAmount" : "0" , "feeCcy" : "USDT" , "clientOrderId" : "1783698931866" , "orderId" : "2256224625931847936" , "tradeId" : "2256224626032511237" , "transactTime" : "1783698934000" , "symbol" : "BTCUSDT-PERPETUAL" }
]
```

| **PARAMETER**          | **TYPE**   | **DESCRIPTION**                                                         |
|------------------------|------------|-------------------------------------------------------------------------|
| id                     | STRING     | Record ID                                                               |
| accountId              | STRING     | Account ID                                                              |
| type                   | STRING     | "futuresTrade"                                                          |
| currency               | STRING     | E.g. USDT, USDC                                                         |
| beforeBalance          | STRING     | Balance before the trade                                                |
| realizedPnL            | STRING     | Realized profit and loss                                                |
| afterBalance           | STRING     | Balance after the trade                                                 |
| fee                    | STRING     | Trading fee                                                             |
| feeSupplementaryAmount | STRING     | Supplementary commission fee to meet minimum commission fee requirement |
| feeCcy                 | STRING     | Fee currency                                                            |
| clientOrderId          | STRING     | Client order ID                                                         |
| orderId                | STRING     | Order ID                                                                |
| tradeId                | STRING     | Trade ID                                                                |
| transactTime           | STRING     | Trade completed and settled time                                        |
| symbol                 | STRING     | Name of the contract                                                    |

### Get ChainType

**GET** `/api/v1/account/chainType`

Get the supported list of ChainType for a specific CoinId(e.g. ETH) ChainType is typically used when deposit &amp; withdrawal

**Weight: 1**

**Request Parameters**

| PARAMETER   | TYPE   | Req'd   | Example values   | DESCRIPTION                  |
|-------------|--------|---------|------------------|------------------------------|
| coinId      | STRING | Y       | USDT             | Coin Name. e.g: "BTC", "ETH" |
| recvWindow  | LONG   |         |                  | Recv Window. Default 5000    |
| timestamp   | LONG   | Y       |                  | Timestamp                    |

**Response Content**

```
[ { "coinId" : "USDT" , "coinName" : "USDT" , "chainTypeList" : [ "ETH" , "Tron" ] }
]
```

| PARAMETER     | TYPE         | Example values   | DESCRIPTION                                         |
|---------------|--------------|------------------|-----------------------------------------------------|
| *             | Object Array |                  |                                                     |
| coinId        | STRING       | USDT             | Coin Name                                           |
| coinName      | STRING       | USDT             | Coin Name                                           |
| chainTypeList | LIST         | ["ETH","Tron"]   | List of supported chain types.                      |
| errorCode     | STRING       | 0001             | Error code, returned only when there is an error    |
| errorMsg      | STRING       | -                | Error message, returned only when there is an error |

### Get Coin Information

**GET** `/api/v1/coinInfo`

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | **DESCRIPTION**                             |
|-----------------|------------|---------|---------------------------------------------|
| coinId          | STRING     | Y       | The unique identifier of the cryptocurrency |

**Response Content**

| **PARAMETER**                  | **TYPE**         | **Example Values**   | **DESCRIPTION**              |
|--------------------------------|------------------|----------------------|------------------------------|
| timezone                       | STRING           | UTC                  | Timezone                     |
| serverTime                     | INTEGER          | 1727068513801        | Server millisecond timestamp |
| coins                          | Object Array     |                      | Coin list                    |
| coins.orgId                    | STRING (integer) | 9001                 | Institution ID               |
| coins.coinId                   | STRING           | ETH                  | Coin ID                      |
| coins.coinName                 | STRING           | ETH                  | Coin name                    |
| coins.coinFullName             | STRING           | ETH                  | Coin full name               |
| coins.allowWithdraw            | BOOLEAN          | true                 | Whether to allow withdrawal  |
| coins.allowDeposit             | BOOLEAN          | true                 | Whether to allow deposit     |
| chainTypes                     | Object Array     |                      | Chain information list       |
| chainTypes.chainType           | STRING           | ETH                  | Chain type                   |
| chainTypes.withdrawFee         | STRING           | 0.0000001            | Withdrawal fee               |
| chainTypes.minWithdrawQuantity | STRING           | 0.0000002            | Minimum withdrawal amount    |
| chainTypes.maxWithdrawQuantity | STRING           | 0                    | Maximum withdrawal amount    |
| chainTypes.minDepositQuantity  | STRING           | 0.002                | Minimum deposit quantity     |
| chainTypes.allowDeposit        | BOOLEAN          | true                 | Whether to allow deposit     |
| chainTypes.allowWithdraw       | BOOLEAN          | true                 | Whether to allow withdrawal  |

### Get HSK Deduction Switch

**GET** `/api/v1/hsk/deductionSwitch`

Query the HSK fee deduction switch status for the master user. Whether the API Key is bound to a master or sub account, the switch always applies to the **master user** .

**Weight: 1**

**Request Parameters**

| PARAMETER   | TYPE   | Req'd   | Example values   | DESCRIPTION               |
|-------------|--------|---------|------------------|---------------------------|
| recvWindow  | LONG   |         |                  | Recv Window. Default 5000 |
| timestamp   | LONG   | Y       |                  | Timestamp                 |

**Response Content**

```
{ "deductionSwitch" : 1 , "updateTime" : "1722230400000"
}
```

| **PARAMETER**   | **TYPE**   |   **Example values** | **DESCRIPTION**                                        |
|-----------------|------------|----------------------|--------------------------------------------------------|
| deductionSwitch | INTEGER    |                    1 | HSK deduction switch `0` = Off `1` = On                |
| updateTime      | STRING     |        1722230400000 | Last update time in milliseconds. `0` if never updated |

### Update HSK Deduction Switch

**POST** `/api/v1/hsk/deductionSwitch`

Update the HSK fee deduction switch for the master user. Whether the API Key is bound to a master or sub account, the switch always applies to the **master user** .

Read-only API Keys are not allowed to call this endpoint (HTTP 403). Enabling the switch may be restricted by user type.

**Weight: 1**

**Request Parameters**

| PARAMETER       | TYPE    | Req'd   |   Example values | DESCRIPTION                             |
|-----------------|---------|---------|------------------|-----------------------------------------|
| deductionSwitch | INTEGER | Y       |                1 | HSK deduction switch `0` = Off `1` = On |
| recvWindow      | LONG    |         |                  | Recv Window. Default 5000               |
| timestamp       | LONG    | Y       |                  | Timestamp                               |

**Response Content**

```
{ "deductionSwitch" : 1 , "updateTime" : "1722230400000"
}
```

| **PARAMETER**   | **TYPE**   |   **Example values** | **DESCRIPTION**                                      |
|-----------------|------------|----------------------|------------------------------------------------------|
| deductionSwitch | INTEGER    |                    1 | HSK deduction switch after update `0` = Off `1` = On |
| updateTime      | STRING     |        1722230400000 | Update time in milliseconds                          |

## Sub Account

### Get Sub Account Open Orders

**GET** `/api/v1/spot/subAccount/openOrders`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**          |
|-----------------|------------|-------------|----------------------|--------------------------|
| subAccountId    | STRING     | Y           | 1650801631044854016  | Sub Account ID           |
| fromOrderId     | LONG       |             | 1470930457684189696  | Order ID                 |
| side            | ENUM       |             |                      | `BUY` or `SELL`          |
| symbol          | STRING     |             | BTCUSD               | Currency Pair            |
| limit           | INT        |             | 500                  | Default 500, Maximum 500 |
| timestamp       | LONG       | Y           | 1712317312973        | Timestamp                |

**Response Content**

```
[ { "accountId" : "1695624199270418688" , "exchangeId" : "301" , "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "clientOrderId" : "1766585803470297" , "orderId" : "2112669276414486016" , "price" : "112930" , "origQty" : "0.1" , "executedQty" : "0" , "cummulativeQuoteQty" : "0" , "cumulativeQuoteQty" : "0" , "avgPrice" : "0" , "status" : "NEW" , "timeInForce" : "GTC" , "type" : "LIMIT" , "side" : "SELL" , "stopPrice" : "0.0" , "icebergQty" : "0.0" , "time" : "1766585803498" , "updateTime" : "1766585803570" , "isWorking" : true , "reqAmount" : "0" , "ordCxlReason" : "" , "stpMode" : "EXPIRE_TAKER" }
]
```

| **PARAMETER**      | **TYPE**         | **Example values**   | **DESCRIPTION**                                                                                                |
|--------------------|------------------|----------------------|----------------------------------------------------------------------------------------------------------------|
| *                  | Object Array     |                      | Query result array                                                                                             |
| accountId          | STRING           | 1471090223379184384  | Account number                                                                                                 |
| exchangeId         | STRING           | 301                  | Exchange Number                                                                                                |
| symbol             | STRING           | BTCUSD               | Trading pair                                                                                                   |
| symbolName         | STRING           | BTCUSD               | Trading pair name                                                                                              |
| clientOrderId      | STRING           | 123456               | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| orderId            | STRING           | 1470930457684189696  | System generated order ID                                                                                      |
| price              | STRING (decimal) | 28000                | Price                                                                                                          |
| origQty            | STRING (decimal) | 0.01                 | Quantity                                                                                                       |
| executedQty        | STRING (decimal) | 0                    | Traded volume                                                                                                  |
| cumulativeQuoteQty | STRING (decimal) | 0                    | Cumulative volume                                                                                              |
| avgPrice           | STRING (decimal) | 0                    | Average traded price                                                                                           |
| status             | STRING           | NEW                  | Order status                                                                                                   |
| timeInForce        | STRING           | GTC                  | Duration of the order before expiring                                                                          |
| type               | STRING           | LIMIT                | Order Type                                                                                                     |
| side               | STRING           | BUY                  | BUY or SELL                                                                                                    |
| stopPrice          | STRING (decimal) | 0.0                  | Not used                                                                                                       |
| icebergQty         | STRING (decimal) | 0.0                  | Not used                                                                                                       |
| time               | STRING           | 1690084574839        | Current Timestamp                                                                                              |
| updateTime         | STRING           | 1690084574843        | Update Timestamp                                                                                               |
| isWorking          | BOOLEAN          | TRUE                 | Not used                                                                                                       |
| reqAmount          | STRING           | 0                    | Requested cash amount                                                                                          |
| ordCxlReason       | STRING           |                      | Order cancel reason                                                                                            |
| stpMode            | STRING           | EXPIRE_MAKER         | Self Trade Prevention Mode.                                                                                    |

### Get Sub Account Trade Orders

**GET** `/api/v1/spot/subAccount/tradeOrders`

**Weight: 5**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example values**   | **DESCRIPTION**                                           |
|-----------------|------------|-------------|----------------------|-----------------------------------------------------------|
| subAccountId    | STRING     | Y           | 1650801631044854016  | Sub Account ID                                            |
| fromOrderId     | LONG       |             | 1470930457684189696  | Order ID                                                  |
| side            | ENUM       |             |                      | `BUY` or `SELL`                                           |
| symbol          | STRING     |             | BTCUSD               | Currency Pair                                             |
| startTime       | LONG       |             |                      | Start Timestamp, Only supports the last 90 days timeframe |
| endTime         | LONG       |             |                      | End Timestamp                                             |
| limit           | INT        |             | 500                  | Default 500, Maximum 500                                  |
| timestamp       | LONG       | Y           | 1712317312973        | Timestamp                                                 |

**Response Content**

```
[ { "accountId" : "1695624199270418688" , "exchangeId" : "301" , "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "clientOrderId" : "1766585741726331" , "orderId" : "2112668758317278720" , "price" : "0" , "origQty" : "0.1" , "executedQty" : "0.1" , "cummulativeQuoteQty" : "11292.24" , "cumulativeQuoteQty" : "11292.24" , "avgPrice" : "112922.4" , "status" : "FILLED" , "timeInForce" : "IOC" , "type" : "MARKET" , "side" : "SELL" , "stopPrice" : "0.0" , "icebergQty" : "0.0" , "time" : "1766585741737" , "updateTime" : "1766585741758" , "isWorking" : true , "reqAmount" : "0" , "ordCxlReason" : "" , "stpMode" : "EXPIRE_TAKER" }
]
```

| **PARAMETER**      | **TYPE**         | **Example values**   | **DESCRIPTION**                                                                                                |
|--------------------|------------------|----------------------|----------------------------------------------------------------------------------------------------------------|
| *                  | Object Array     |                      | Query result array                                                                                             |
| accountId          | STRING           | 1471090223379184384  | Account number                                                                                                 |
| exchangeId         | STRING           | 301                  | Exchange Number                                                                                                |
| symbol             | STRING           | BTCUSD               | Trading pair                                                                                                   |
| symbolName         | STRING           | BTCUSD               | Trading pair name                                                                                              |
| clientOrderId      | STRING           | 123456               | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| orderId            | STRING           | 1470930457684189696  | System generated order ID                                                                                      |
| price              | STRING (decimal) | 28000                | Price                                                                                                          |
| origQty            | STRING (decimal) | 0.01                 | Quantity                                                                                                       |
| executedQty        | STRING (decimal) | 0                    | Traded volume                                                                                                  |
| cumulativeQuoteQty | STRING (decimal) | 0                    | Cumulative volume                                                                                              |
| avgPrice           | STRING (decimal) | 0                    | Average traded price                                                                                           |
| status             | STRING           | NEW                  | Order status                                                                                                   |
| timeInForce        | STRING           | GTC                  | Duration of the order before expiring                                                                          |
| type               | STRING           | LIMIT                | Order Type                                                                                                     |
| side               | STRING           | BUY                  | BUY or SELL                                                                                                    |
| stopPrice          | STRING (decimal) | 0.0                  | Not used                                                                                                       |
| icebergQty         | STRING (decimal) | 0.0                  | Not used                                                                                                       |
| time               | STRING           | 1690084574839        | Current Timestamp                                                                                              |
| updateTime         | STRING           | 1690084574843        | Update Timestamp                                                                                               |
| isWorking          | BOOLEAN          | TRUE                 | Not used                                                                                                       |
| reqAmount          | STRING           | 0                    | Requested cash amount                                                                                          |
| ordCxlReason       | STRING           |                      | Order cancel reason                                                                                            |
| stpMode            | STRING           | EXPIRE_MAKER         | Self Trade Prevention Mode.                                                                                    |

### Get Sub Account Trades

**GET** `/api/v1/subAccount/trades`

**Weight: 5**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req 'd**   | **DESCRIPTION**                                           |
|-----------------|------------|--------------|-----------------------------------------------------------|
| symbol          | STRING     |              | Trading pair                                              |
| subAccountId    | STRING     |              | Sub Account ID                                            |
| startTime       | LONG       |              | Start Timestamp, Only supports the last 30 days timeframe |
| endTime         | LONG       |              | End Timestamp                                             |
| clientOrderId   | STRING     |              | Client Order ID                                           |
| fromId          | LONG       |              | Starting ID                                               |
| toId            | LONG       |              | End ID                                                    |
| limit           | INT        |              | Limit of record. Default 500, Max 1000                    |
| timestamp       | LONG       | Y            | Timestamp                                                 |

**Response Content**

```
[ { "id" : "2112668759961445888" , "clientOrderId" : "1766585741726331" , "ticketId" : "4636458456207560707" , "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "orderId" : "2112668758317278720" , "matchOrderId" : "0" , "price" : "112922.4" , "qty" : "0.02157" , "commission" : "3.653604252" , "commissionAsset" : "USDT" , "time" : "1766585741758" , "isBuyer" : false , "isMaker" : false , "fee" : { "feeCoinId" : "USDT" , "feeCoinName" : "USDT" , "fee" : "3.653604252" , "originCoinId" : "USDT" , "originCoinName" : "USDT" , "originFee" : "3.653604252" }, "feeCoinId" : "USDT" , "feeAmount" : "3.653604252" , "makerRebate" : "0" , "hskDeduct" : false , "hskDeductPrice" : "" }, { "id" : "2112668759617512960" , "clientOrderId" : "1766585741726331" , "ticketId" : "4636458456207560706" , "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "orderId" : "2112668758317278720" , "matchOrderId" : "0" , "price" : "112922.4" , "qty" : "0.035" , "commission" : "5.928426" , "commissionAsset" : "USDT" , "time" : "1766585741758" , "isBuyer" : false , "isMaker" : false , "fee" : { "feeCoinId" : "USDT" , "feeCoinName" : "USDT" , "fee" : "5.928426" , "originCoinId" : "USDT" , "originCoinName" : "USDT" , "originFee" : "5.928426" }, "feeCoinId" : "USDT" , "feeAmount" : "5.928426" , "makerRebate" : "0" , "hskDeduct" : false , "hskDeductPrice" : "" }
]
```

| **PARAMETER**      | **TYPE**         | **Example values**   | **DESCRIPTION**                                                                                                |
|--------------------|------------------|----------------------|----------------------------------------------------------------------------------------------------------------|
| *                  | Object Array     |                      | Check transaction results                                                                                      |
| id                 | STRING           | 1470930841345474561  | Unique transaction ID (This value is the trade_id in v0 API)                                                   |
| clientOrderId      | STRING           | 999999999800021      | An ID defined by the client for the order, it will be automatically generated if it is not sent in the request |
| ticketId           | STRING           | 1478144171272585249  | Execution ID, the execution ID is the same for the direction of a single trade.                                |
| symbol             | STRING           | BTCUSD               | Trading pair                                                                                                   |
| symbolName         | STRING           | BTCUSD               | Trading pair name                                                                                              |
| orderId            | STRING           | 1470930841211329280  | Order ID                                                                                                       |
| matchOrderId       | STRING           | 1470930605684362240  | //Ignore                                                                                                       |
| price              | STRING (decimal) | 29851.03             | Price                                                                                                          |
| qty                | STRING (decimal) | 0.0005               | Quantity                                                                                                       |
| commission         | STRING (decimal) | 0.02985103           | Commission fee                                                                                                 |
| commissionAsset    | STRING           | USD                  | Currency of commission fee                                                                                     |
| time               | STRING (decimal) | 1690084620567        | Millisecond Timestamp                                                                                          |
| isBuyer            | BOOLEAN          | false                | Whether the trade is a buyer                                                                                   |
| isMaker            | BOOLEAN          | false                | Whether the trade is a maker                                                                                   |
| fee                | Object           |                      | Fee information                                                                                                |
| fee.feeCoinId      | STRING           | USD                  | Currency ID for fees                                                                                           |
| fee.feeCoinName    | STRING           | USD                  | Fee currency name                                                                                              |
| fee.fee            | STRING (decimal) | 0.02985103           | Transaction fee amount                                                                                         |
| fee.originFee      | STRING (decimal) | 0.03085103           | The commission fee before HSK deduction.                                                                       |
| fee.originCoinId   | STRING           | USD                  | The commission fee before HSK deduction                                                                        |
| fee.originCoinName | STRING           | USD                  | The commission fee coin                                                                                        |
| feeCoinId          | STRING           | USD                  | Fee currency                                                                                                   |
| feeAmount          | STRING (decimal) | 0.02985103           | Amount of transaction fee                                                                                      |
| makerRebate        | STRING           | 0                    | Return                                                                                                         |
| hskDeduct          | BOOLEAN          | true                 | true: successfully deducted HSK  false                                                                         |
| hskDeductPrice     | STRING           | 0.001                | commission Coin price / HSK price                                                                              |

## Wallet

**📘 To find out the chainType for Deposit and Withdrawal endpoint, please refer to the "Network" field in Deposit and Withdrawal fee tab:** [https://global.hashkey.com/support-fee](https://global.hashkey.com/support-fee)

### Get Deposit Address

**GET** `/api/v1/account/deposit/address`

Retrieve deposit address generated by the system

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req 'd   | **Example values**   | **DESCRIPTION**                                      |
|-----------------|------------|----------|----------------------|------------------------------------------------------|
| coin            | STRING     | Y        | USDT                 | Coin name                                            |
| chainType       | ENUM       | Y        | ETH                  | Chain Type, refer to [Get-ChainType](#Get-ChainType) |
| recvWindow      | LONG       |          |                      | Recv Window. Default 5000                            |
| timestamp       | LONG       | Y        |                      | Timestamp                                            |

**Response Content**

```
{ "canDeposit" : true , "address" : "0xD6bF65d473BFd760E20c7e120E9A4108a912D7c3" , "addressExt" : "" , "minQuantity" : "0.001" , "needAddressTag" : false , "requiredConfirmTimes" : 10 , "canWithdrawConfirmTimes" : 10 , "coinType" : "ERC20_TOKEN"
}
```

| **PARAMETER**           | **TYPE**   | Example values                             | **DESCRIPTION**                                       |
|-------------------------|------------|--------------------------------------------|-------------------------------------------------------|
| canDeposit              | BOOLEAN    | true                                       | Can be deposited                                      |
| address                 | STRING     | 0x7c07adb0D2DE76241b262595860b16Cf90615aa0 | Deposit Address                                       |
| addressExt              | STRING     |                                            | Tag (Not in use)                                      |
| minQuantity             | STRING     | 0.001                                      | Minimum Amount to be deposited                        |
| needAddressTag          | BOOLEAN    | false                                      | Is address tag required (Not in use)                  |
| requiredConfirmTimes    | INTEGER    | 64                                         | Credit to account block confirmation (Reference only) |
| canWithdrawConfirmTimes | INTEGER    | 64                                         | Withdrawal block confirmation (Reference only)        |
| coinType                | STRING     | CHAIN_TOKEN                                | Coin Type                                             |

### Get Deposit History

**GET** `/api/v1/account/depositOrders`

**Deposit Status**

|   **Deposit Type** | **Description**                                           |
|--------------------|-----------------------------------------------------------|
|                  1 | Pending address authentication 待地址认证                      |
|                  2 | Under review 审核中                                          |
|                  3 | Deposit failed 充值失败                                       |
|                  4 | Deposit successful 充值成功                                   |
|                  5 | Refund 退币                                                 |
|                  6 | Refund completed 退币完成                                     |
|                  7 | Refund failed  退币失败                                       |
|                  8 | In the account 上账中                                        |
|                  9 | The first address verification of personal recharge fails |
|                 10 | Internal Failed (rarely happen) 内部错误（极低概率）                |

**Weight: 5**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req 'd   | **Example values**   | **DESCRIPTION**           |
|-----------------|------------|----------|----------------------|---------------------------|
| coin            | STRING     |          | ETH_USDT             | Chain_Coin                |
| startTime       | LONG       |          | 16500121212121       | Start timestamp           |
| endTime         | LONG       |          | 16600131311313       | End timestamp             |
| limit           | INTEGER    |          | 500                  | Default 500; Max 1000     |
| recvWindow      | LONG       |          |                      | Recv Window. Default 5000 |
| timestamp       | LONG       | Y        |                      | Timestamp                 |

**Response Content**

```
[ { "time" : "1753238871066" , "coin" : "BTC" , "coinName" : "BTC" , "address" : "btctestsuc" , "quantity" : "5.00000000000000000000" , "status" : 1 , "statusCode" : "1" , "txId" : "ad504e3af44ec5e3d4af6a4c158c50cf5fdffe9006e4f8d7f00773378a5dea28" }, { "time" : "1753238870846" , "coin" : "BTC" , "coinName" : "BTC" , "address" : "btctestsuc" , "quantity" : "5.00000000000000000000" , "status" : 1 , "statusCode" : "1" , "txId" : "640f63f1ad52c3aef7e43b0afcf2cdb2a844d04ef03d7632821031e832558a61" }, { "time" : "1727574827745" , "coin" : "ETH" , "coinName" : "ETH" , "address" : "0xD655029B870b4689606a1C43CADb2300C0a016B1" , "quantity" : "0.02227914313347269000" , "status" : 10 , "statusCode" : "10" , "txId" : "0x8a895bc0b5cb55b91052f38d0b0afa7697612c94056670ae004a4ce34a0d2d04" }, { "time" : "1727486851608" , "coin" : "USDT" , "coinName" : "USDT" , "address" : "0xf1102fb9c9B5428b3174df9E0345c3f934bee208" , "quantity" : "22.00000000000000000000" , "status" : 1 , "statusCode" : "1" , "txId" : "0x28dc84ebadb2c0f77677ab266fa6f6ac0e96ba1fbaadc2cb0dfad8202b191b56" }
]
```

| **PARAMETER**   | **TYPE**         | **Example values**                                                 | **DESCRIPTION**                 |
|-----------------|------------------|--------------------------------------------------------------------|---------------------------------|
| time            | STRING           | 1691048298420                                                      | Deposit order created Timestamp |
| coin            | STRING           | ETH                                                                | Coin                            |
| coinName        | STRING           | ETH                                                                | Coin name                       |
| address         | STRING           | 0xa0D6AD420C440de473980117877DEC0a89DAFbeF                         | Deposit address                 |
| quantity        | STRING (decimal) | 0.05000000000000000000                                             | Deposit amount                  |
| status          | ENUM             | 4                                                                  | Deposit status                  |
| statusCode      | STRING           | 4                                                                  | Same as status                  |
| txId            | STRING           | 0xbd40b38543767a7d441c87c676ddfaf6cf750e4c7d8d66abd0f1665eb031932a | On-chain transaction ID         |

### Authenticate Deposit Address

**POST** `/api/v1/account/authAddress`

**Weight: 1**

**Request Parameters**

| **PARAMETER**     | **TYPE**   | Req 'd   | **Example values**                                                 | **DESCRIPTION**                                                                                           |
|-------------------|------------|----------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| txid              | STRING     | Y        | 0xbd40b38543767a7d441c87c676ddfaf6cf750e4c7d8d66abd0f1665eb031932a | On-chain transaction ID                                                                                   |
| senderLastName    | STRING     |          | ZHANG                                                              | Either `institutionalName` must be provided, or both `senderFirstName` and `senderLastName` are required. |
| senderFirstName   | STRING     |          | SHEN                                                               | Either `institutionalName` must be provided, or both `senderFirstName` and `senderLastName` are required. |
| institutionalName | STRING     |          |                                                                    | Either `institutionalName` must be provided, or both `senderFirstName` and `senderLastName` are required. |
| exchangeName      | STRING     | Y        | Binance, OKX, Coinbase, Bybit, Kraken                              | The name of the whitelisted exchange you will be depositing                                               |
| isAddressOwner    | BOOLEAN    | Y        | true                                                               | Self declaration that you are the owner of the address by sending "true"                                  |
| recvWindow        | LONG       |          |                                                                    | Recv Window. Default 5000                                                                                 |
| timestamp         | LONG       | Y        |                                                                    | Timestamp                                                                                                 |

**Response Content**

```
{ "success" : true , "msg" : "" , "timestamp" : "1766633944895"
}
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**                   |
|-----------------|------------|----------------------|-----------------------------------|
| success         | BOOLEAN    | true                 | Whether message sent successfully |
| msg             | STRING     |                      |                                   |
| timestamp       | STRING     | 1699943911155        | Message sent time                 |

### Withdraw VA

**POST** `/api/v1/account/withdraw`

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req 'd**   | **Example Values**                         | **DESCRIPTION**                                                                                                         |
|-----------------|------------|--------------|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| coin            | STRING     | Y            | USDT                                       | Assets                                                                                                                  |
| clientOrderId   | STRING     | Y            | w12912                                     | Custom Withdrawal ID                                                                                                    |
| address         | STRING     | Y            | 0x132346ef629483974879a2e68A3557cA1c494D2E | Withdrawal address                                                                                                      |
| addressExt      | STRING     |              | (Not in use currently)                     | Tag  (Not in use currently)                                                                                             |
| platform        | STRING     |              | Refer to **Platform Supported** .          | Platform name                                                                                                           |
| quantity        | DECIMAL    | Y            | 0.2                                        | Withdrawal amount                                                                                                       |
| chainType       | STRING     | Y            | ETH                                        | Chain Type, refer to [Get-ChainType](#Get-ChainType)                                                                    |
| timestamp       | LONG       | Y            | 1712317312973                              | Timestamp                                                                                                               |
| memo            | STRING     |              | 123456                                     | Memo required for some coin and network when withdraw.   Only supports letters and numbers.   Maximum of 20 characters. |

**Platform Supported**

Not case sensitive, doesn't matter if it's uppercase or lowercase

| **Platform Supported**            | **"platform" parameter enum**   |
|-----------------------------------|---------------------------------|
| Binance                           | "BINANCE"                       |
| OKX                               | "OKX"                           |
| Bitget (Individual Investor Only) | "BITGET"                        |
| Bybit (Individual Investor Only)  | "BYBIT"                         |

**Response Content**

```
{ "success" : true , "id" : "0" , "orderId" : "W792076358865207296" , "accountId" : "1649292498437183235"
}
```

| **PARAMETER**   | **TYPE**   | **Example Values**   | **DESCRIPTION**   |
|-----------------|------------|----------------------|-------------------|
| success         | BOOELEAN   | true                 | Error code        |
| id              | STRING     | 0                    | ID                |
| orderId         | STRING     | W476435800487079936  | Order ID          |
| accountId       | STRING     | 1649292498437183235  | Account Id        |

### Get Withdraw History

**GET** `/api/v1/account/withdrawOrders`

Retrieve withdrawal history

**Weight: 5**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req 'd**   | **Example Values**   | **DESCRIPTION**                                                                                                         |
|-----------------|------------|--------------|----------------------|-------------------------------------------------------------------------------------------------------------------------|
| coin            | STRING     |              | USDT                 | Coin                                                                                                                    |
| startTime       | LONG       |              | 1691142675492        | Start Time                                                                                                              |
| endTime         | LONG       |              | 1691142679567        | End Time                                                                                                                |
| remark          | STRING     |              |                      | Remark                                                                                                                  |
| limit           | INTEGER    |              | 10                   | Default 500, Max 1000                                                                                                   |
| timestamp       | LONG       | Y            | 1712317312973        | Timestamp                                                                                                               |
| memo            | STRING     |              | 123456               | Memo required for some coins and networks when withdraw.   Only supports letters and numbers. Maximum of 20 characters. |

**Response Content**

```
[ { "time" : "1766653720032" , "id" : "W792076358865207296" , "coin" : "USDT" , "coinId" : "USDT" , "coinName" : "USDT" , "address" : "0x05aad35f83e62b6323f55ea41efcfdd2f97bd505" , "quantity" : "10.00000000" , "arriveQuantity" : "" , "status" : "withdrawing" , "txId" : "" , "addressUrl" : "0x05aad35f83e62b6323f55ea41efcfdd2f97bd505" , "feeCoinId" : "USDT" , "feeCoinName" : "USDT" , "fee" : "0.00000000" , "remark" : "" , "platform" : "" , "memo" : "" }
]
```

| **PARAMETER**   | **TYPE**         | **Example Values**                                                 | **DESCRIPTION**                                                                                                             |
|-----------------|------------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| *               | Object Array     |                                                                    | Query result list                                                                                                           |
| time            | STRING           | 1691053667700                                                      | Timestamp                                                                                                                   |
| id              | STRING           | W474986756938121216                                                | Withdrawal order ID                                                                                                         |
| coin            | STRING           | ETH                                                                | Coin                                                                                                                        |
| coinId          | STRING           | ETH                                                                | Coin ID                                                                                                                     |
| coinName        | STRING           | ETH                                                                | Coin Name                                                                                                                   |
| address         | STRING           | 0xa0d6ad420c440de473980117877dec0a89dafbef                         | Withdrawal Address                                                                                                          |
| quantity        | STRING (decimal) | 0.05000000                                                         | Withdrawal amount entered by the user                                                                                       |
| arriveQuantity  | STRING (decimal) | 0.05000000                                                         | Net amount received                                                                                                         |
| status          | STRING           | successful                                                         | Status: `failed` `withdrawing` `under_review` `successful` `canceled` `canceling`                                           |
| txId            | STRING           | 0x448345d7d95614e19ad2c499be451cdec8d9fa109889f4dab201e3e50f0a06b4 | Transaction ID                                                                                                              |
| addressUrl      | STRING           | 0xa0d6ad420c440de473980117877dec0a89dafbef                         | Withdrawal address URL (Same as address)                                                                                    |
| feeCoinId       | STRING           | ETH                                                                | Fee Currency ID                                                                                                             |
| feeCoinName     | STRING           | ETH                                                                | Fee Currency Name                                                                                                           |
| fee             | STRING           | 0.00600000                                                         | Handling fee                                                                                                                |
| remark          | STRING           |                                                                    | Remark                                                                                                                      |
| platform        | STRING           | Binance                                                            | Network name                                                                                                                |
| memo            | STRING           | 123456                                                             | Memo required for some coins and networks when withdrawal.   Only supports letters and numbers.   Maximum of 20 characters. |

## Public Market Data (Spot &amp; Futures)

**✅ All market-related APIs do not require signature verification and can directly access production data.**

### Get Exchange Information

**GET** `/api/v1/exchangeInfo`

Retrieve current exchange trading rules and symbol information

**Types of trading restrictions**

| Types          | Description                         |
|----------------|-------------------------------------|
| PRICE_FILTER   | Price limit                         |
| LOT_SIZE       | Limit on the number of transactions |
| MIN_NOTIONAL   | Minimum nominal limit               |
| TRADE_AMOUNT   | Transaction limit                   |
| LIMIT_TRADING  | Limit trading rules                 |
| MARKET_TRADING | Market trading rules                |
| OPEN_QUOTE     | Opening Restrictions                |

**Trading pair status**

| Status     | Description        |
|------------|--------------------|
| IN_PREVIEW | Under preview      |
| TRADING    | Continuous trading |
| HALT       | Trading suspended  |
| RESUMING   | Resuming from Halt |

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req 'd**   | **DESCRIPTION**                                                   |
|-----------------|------------|--------------|-------------------------------------------------------------------|
| symbol          | STRING     | C            | Symbol Name. e.g: "BTCUSDT", "ETHUSDT", "BTCUSD-PERPETUAL"        |
| site            | STRING     | N            | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**Response Content**

```
{ "symbol" : "USDTAED" , "symbolName" : "USDTAED" , "status" : "TRADING" , "baseAsset" : "USDT" , "baseAssetName" : "USDT" , "baseAssetPrecision" : "0.01" , "baseUcid" : "825" , "quoteAsset" : "AED" , "quoteAssetName" : "AED" , "quotePrecision" : "0.00001" , "quoteUcid" : "" , "retailAllowed" : true , "piAllowed" : true , "corporateAllowed" : true , "omnibusAllowed" : true , "icebergAllowed" : false , "isAggregate" : false , "allowMargin" : false , "filters" : [ { "minPrice" : "0.001" , "maxPrice" : "100000.00000000" , "tickSize" : "0.001" , "filterType" : "PRICE_FILTER" }, { "minQty" : "0.3" , "maxQty" : "200000" , "stepSize" : "0.01" , "marketOrderMinQty" : "0.3" , "marketOrderMaxQty" : "100000" , "filterType" : "LOT_SIZE" }, { "minNotional" : "1" , "filterType" : "MIN_NOTIONAL" }, { "minAmount" : "1" , "maxAmount" : "733320" , "minBuyPrice" : "0" , "marketOrderMinAmount" : "1" , "marketOrderMaxAmount" : "366660" , "filterType" : "TRADE_AMOUNT" }, { "maxSellPrice" : "0" , "buyPriceUpRate" : "0.1" , "sellPriceDownRate" : "0.1" , "maxEntrustNum" : 300 , "filterType" : "LIMIT_TRADING" }, { "buyPriceUpRate" : "0.1" , "sellPriceDownRate" : "0.1" , "filterType" : "MARKET_TRADING" }, { "noAllowMarketStartTime" : "0" , "noAllowMarketEndTime" : "0" , "limitOrderStartTime" : "0" , "limitOrderEndTime" : "0" , "limitMinPrice" : "0" , "limitMaxPrice" : "0" , "filterType" : "OPEN_QUOTE" } ], "site" : "mena"
}
```

The `contracts` array describes the available futures (perpetual) trading pairs:

```
{ "contracts" : [ { "filters" : [ { "minPrice" : "0.1" , "maxPrice" : "100000.00000000" , "tickSize" : "0.1" , "filterType" : "PRICE_FILTER" }, { "minQty" : "0.001" , "maxQty" : "10" , "stepSize" : "0.001" , "marketOrderMinQty" : "0.001" , "marketOrderMaxQty" : "3" , "filterType" : "LOT_SIZE" }, { "minNotional" : "0" , "filterType" : "MIN_NOTIONAL" }, { "maxSellPrice" : "999999" , "buyPriceUpRate" : "0.03" , "sellPriceDownRate" : "0.03" , "maxEntrustNum" : 200 , "maxConditionNum" : 200 , "filterType" : "LIMIT_TRADING" }, { "buyPriceUpRate" : "0.03" , "sellPriceDownRate" : "0.03" , "filterType" : "MARKET_TRADING" }, { "noAllowMarketStartTime" : "0" , "noAllowMarketEndTime" : "0" , "limitOrderStartTime" : "0" , "limitOrderEndTime" : "0" , "limitMinPrice" : "0" , "limitMaxPrice" : "0" , "filterType" : "OPEN_QUOTE" } ], "exchangeId" : "301" , "symbol" : "BTCUSD-PERPETUAL" , "symbolName" : "BTCUSD-PERPETUAL" , "status" : "TRADING" , "baseAsset" : "BTC" , "baseAssetPrecision" : "0.001" , "quoteAsset" : "USD" , "quoteAssetPrecision" : "0.1" , "icebergAllowed" : false , "inverse" : false , "index" : "BTCUSD" , "marginToken" : "USD" , "marginPrecision" : "0.0001" , "contractMultiplier" : "0.001" , "underlying" : "BTC" , "riskLimits" : [ { "riskLimitId" : "127" , "quoteQty" : "125000.00" , "initialMargin" : "0.05" , "maintMargin" : "0.025" }, { "riskLimitId" : "128" , "quoteQty" : "250000.00" , "initialMargin" : "0.0526" , "maintMargin" : "0.0263" } ] }, ... ]
}
```

| **PARAMETER**                                                        | **TYPE**         | **Example values**   | **DESCRIPTION**                                                        |
|----------------------------------------------------------------------|------------------|----------------------|------------------------------------------------------------------------|
| timezone                                                             | STRING           | UTC                  | Time zone                                                              |
| serverTime                                                           | INTEGER          | 1690084771517        | Server Millisecond Timestamp                                           |
| symbols                                                              | Object Array     |                      | Currency pair description                                              |
| symbols.symbol                                                       | STRING           | BTCUSD               | Currency pair                                                          |
| symbols.symbolName                                                   | STRING           | BTCUSD               | Currency pair                                                          |
| symbols.status                                                       | ENUM             | TRADING              | Trading pair status                                                    |
| symbols.baseAsset                                                    | STRING           | BTC                  | Base Asset                                                             |
| symbols.baseAssetName                                                | STRING           | BTC                  | Name of base asset                                                     |
| symbols.baseAssetPrecision                                           | STRING           | 0.00001              | Precision of base asset                                                |
| symbols.quoteAsset                                                   | STRING           | USD                  | Quoted Asset                                                           |
| symbols.quoteAssetName                                               | STRING           | USD                  | Name of quoted asset                                                   |
| symbols.quotePrecision                                               | STRING           | 0.00000001           | Precision of quoted asset                                              |
| symbols.retailAllowed                                                | BOOLEAN          | false                | Whether retail client is allowed                                       |
| symbols.piAllowed                                                    | BOOLEAN          | false                | Whether PI client is allowed                                           |
| symbols.corporateAllowed                                             | BOOLEAN          | false                | Whether Corporate client is allowed                                    |
| symbols.omnibusAllowed                                               | BOOLEAN          | true                 | Whether Omnibus client is allowed                                      |
| symbols.icebergAllowed                                               | BOOLEAN          | false                | Currently not in use                                                   |
| symbols.isAggregate                                                  | BOOLEAN          | false                | Currently not in use                                                   |
| symbols.allowMargin                                                  | BOOLEAN          | false                | Currently not in use                                                   |
| symbols.filters                                                      | Object Array     |                      | List of trading pair restrictions                                      |
| symbols.filters.filterType=PRICE_FILTER                              | STRING           | PRICE_FILTER         | Trading restriction type refer to appendix "Trading restriction type"  |
| symbols.filters.minPrice                                             | STRING           | 0.01                 | Depreciated, no longer in-use                                          |
| symbols.filters.maxPrice                                             | STRING           | 100000.00000000      | Depreciated, no longer in-use                                          |
| symbols.filters.tickSize                                             | STRING           | 0.01                 | Minimum price change, only for PRICE_FILTER types                      |
| symbols.filters.filterType=LOT_SIZE                                  | STRING           | LOT_SIZE             | Trading restriction type                                               |
| symbols.filters.minQty                                               | STRING           | 0.0003               | Minimum number of transactions, only for LOT_SIZE types / 最小交易量        |
| symbols.filters.maxQty                                               | STRING           | 4                    | Maximum number of transactions, only for LOT_SIZE types / 最大交易量        |
| symbols.filters.stepSize                                             | STRING           | 0.00001              | Minimal change in quantity, only used for LOT_SIZE types               |
| symbols.filters.marketOrderMinQty                                    | STRING           | 1                    | Minimum no. of coin for base Asset allowed for Market Order            |
| symbols.filters.marketOrderMaxQty                                    | STRING           | 10000                | Maximum no. of coin for base Asset allowed Market Orders               |
| symbols.filters.filterType=MIN_NOTIONAL                              | STRING           | MIN_NOTIONAL         |                                                                        |
| symbols.filters.minNotional                                          | STRING           | 10                   | Minimum notional turnover, only for MIN_NOTIONAL types                 |
| symbols.filters.filterType=TRAD_AMOUNT                               | STRING           | TRADE_AMOUNT         | Trading restriction type                                               |
| symbols.filters.minAmount                                            | STRING           | 10                   | Minimum turnover, only for TRADE_AMOUNT types                          |
| symbols.filters.maxAmount                                            | STRING           | 100000               | Maximum turnover, only for TRADE_AMOUNT types                          |
| symbols.filters.minBuyPrice                                          | STRING           | 0                    | Depreciated, no longer in-use                                          |
| symbols.filters.marketOrderMinAmount                                 | STRING           | 10                   | Minimum cash notional required for Market order / 市价单最小下单金额            |
| symbols.filters.marketOrderMaxAmount                                 | STRING           | 200000               | Maximum cash notional allowed for Market order / 市价单最大下单金额             |
| symbols.filters.filterType=LIMIT_TRADING                             | STRING           |                      |                                                                        |
| symbols.filters.maxSellPrice                                         | STRING           | 0                    | Depreciated, no longer in-use                                          |
| symbols.filters.buyPriceUpRate ("filterType": "LIMIT_TRADING")       | STRING           | 0.2                  | Limit Buy cannot be higher than the mark price / 买入不能高于标记价格            |
| symbols.filters.sellPriceDownRate ("filterType": "LIMIT_TRADING")    | STRING           | 0.2                  | Limit Sell cannot be lower than the mark price / 卖出不能低于标记价格            |
| symbols.filters.filterType=MARKET_TRADING                            | STRING           |                      |                                                                        |
| symbols.filters.buyPriceUpRate ("filterType": "MARKET_TRADING")      | STRING           | 0.2                  | Market buy cannot be higher than the mark price / 买入不能高于标记价格           |
| symbols.filters.sellPriceDownRate ("filterType": "MARKET_TRADING")   | STRING           | 0.2                  | Market sell cannot be lower than the mark price / 卖出不能低于标记价格           |
| symbols.filters.filterType=OPEN_QUOTE                                | STRING           |                      |                                                                        |
| symbols.filters.noAllowMarketStartTime                               | STRING           | 1668483032058        | Market order start time is not allowed, only for OPEN_QUOTE types      |
| symbols.filters.noAllowMarketEndTime                                 | STRING           | 1668483032058        | Market order end time is not allowed, only for OPEN_QUOTE types        |
| symbols.filters.limitOrderStartTime                                  | STRING           | 1668483032058        | Time limit order start time, only for OPEN_QUOTE types                 |
| symbols.filters.limitOrderEndTime                                    | STRING           | 1668483032058        | Time limit order end time, only for OPEN_QUOTE types                   |
| symbols.filters.limitMinPrice                                        | STRING           | 0.1                  | Lowest price for a limited time limit order, only for OPEN_QUOTE types |
| symbols.filters.limitMaxPrice                                        | STRING           | 1000                 | Limit order maximum price, only for OPEN_QUOTE types                   |
| symbols.tradeStatus                                                  | STRING           | TRADABLE             | Trade Status                                                           |
| coins                                                                | Object Array     |                      | Coin description                                                       |
| coins.orgId                                                          | STRING (INTEGER) | 9000                 | Institution ID                                                         |
| coins.coinId                                                         | STRING           | BTC                  | Coin ID                                                                |
| coins.coinName                                                       | STRING           | BTC                  | Coin name                                                              |
| coins.coinFullName                                                   | STRING           | Bitcoin              | Coin full name                                                         |
| coins.allowWithdraw                                                  | BOOLEAN          | true                 | Whether to allow withdrawal                                            |
| coins.allowDeposit                                                   | BOOLEAN          | true                 | Whether to allow deposit                                               |
| coins.tokenType                                                      | STRING           | ERC20_TOKEN          | CHAIN_TOKEN                                                            |
| coins.status                                                         | INTEGER          | 1                    | Coin status                                                            |
| coins.chainTypes                                                     | Object Array     |                      | Chain information list                                                 |
| coins.chainTypes.chainType                                           | STRING           | BTC                  | Chain Type                                                             |
| coins.chainTypes.withdrawFee                                         | STRING           | 0                    | Withdrawal fee                                                         |
| coins.chainTypes.minWithdrawQuantity                                 | STRING           | 0.0001               | Minimum withdrawal amount                                              |
| coins.chainTypes.maxWIthdrawQuantity                                 | STRING           | 100                  | Maximum withdrawal amount                                              |
| coins.chainTypes.minDepositQuantity                                  | STRING           | 0.0002               | Minimum deposit quantity                                               |
| coins.chainTypes.allowDeposit                                        | BOOLEAN          | true                 | Whether to allow deposit                                               |
| coins.chainTypes.allowWithdraw                                       | BOOLEAN          | true                 | Whether to allow withdrawal                                            |
| contracts                                                            | Object Array     |                      | Contracts related info                                                 |
| contracts.exchangeId                                                 | STRING           | 301                  | Exchange ID                                                            |
| contracts.symbol                                                     | STRING           | BTCUSD-PERPETUAL     | Currency pair                                                          |
| contracts.symbolName                                                 | STRING           | BTCUSD-PERPETUAL     | Currency pair name                                                     |
| contracts.status                                                     | STRING           | TRADING              | Trading pair status. (IN_PREVIEW / TRADING / HALT / RESUMING)          |
| contracts.baseAsset                                                  | STRING           | BTC                  | Base Asset                                                             |
| contracts.baseAssetPrecision                                         | STRING           | 0.001                | Precision of base asset                                                |
| contracts.quoteAsset                                                 | STRING           | USD                  | Quote Asset                                                            |
| contracts.quoteAssetPrecision                                        | STRING           | 0.1                  | Precision of quote asset                                               |
| contracts.icebergAllowed                                             | BOOLEAN          | false                | Currently not supported                                                |
| contracts.inverse                                                    | BOOLEAN          | false                | Is reverse contract                                                    |
| contracts.index                                                      | STRING           | BTCUSD               |                                                                        |
| contracts.marginToken                                                | STRING           | USD                  | Quote asset                                                            |
| contracts.marginPrecision                                            | STRING           | 0.0001               | Margin change precision                                                |
| contracts.contractMultiplier                                         | STRING           | 0.001                | Contract multiplier, like 1 contract = 0 001 ETH                       |
| contracts.underlying                                                 | STRING           | BTC                  |                                                                        |
| contracts.riskLimits                                                 | Object Array     |                      | Risk limit tiers                                                       |
| contracts.riskLimits.riskLimitId                                     | STRING           | 127                  | Identifier for the risk limit tier                                     |
| contracts.riskLimits.quoteQty                                        | STRING           | 125000.00            | Maximum notional position size allowed for this tier (in quote asset)  |
| contracts.riskLimits.initialMargin                                   | STRING           | 0.05                 | Initial margin ratio                                                   |
| contracts.riskLimits.maintMargin                                     | STRING           | 0.025                | Maintenance margin ratio                                               |
| contracts.filters                                                    | Object Array     |                      | List of trading pair restrictions                                      |
| contracts.filters.filterType=PRICE_FILTER                            | STRING           | PRICE_FILTER         | Trading restriction type refer to appendix "Trading restriction type"  |
| contracts.filters.minPrice                                           | STRING           | 0.01                 | Depreciated, no longer in-use                                          |
| contracts.filters.maxPrice                                           | STRING           | 100000.00000000      | Depreciated, no longer in-use                                          |
| contracts.filters.tickSize                                           | STRING           | 0.01                 | Minimum price change, only for PRICE_FILTER types                      |
| contracts.filters.filterType=LOT_SIZE                                | STRING           | LOT_SIZE             | Trading restriction type                                               |
| contracts.filters.minQty                                             | STRING           | 0.0003               | Minimum number of transactions, only for LOT_SIZE types / 最小交易量        |
| contracts.filters.maxQty                                             | STRING           | 4                    | Maximum number of transactions, only for LOT_SIZE types / 最大交易量        |
| contracts.filters.stepSize                                           | STRING           | 0.00001              | Minimal change in quantity, only used for LOT_SIZE types               |
| contracts.filters.marketOrderMinQty                                  | STRING           | 1                    | Minimum no. of coin for base Asset allowed for Market Order            |
| contracts.filters.marketOrderMaxQty                                  | STRING           | 10000                | Maximum no. of coin for base Asset allowed Market Orders               |
| contracts.filters.filterType=MIN_NOTIONAL                            | STRING           | MIN_NOTIONAL         |                                                                        |
| contracts.filters.minNotional                                        | STRING           | 10                   | Minimum notional turnover, only for MIN_NOTIONAL types                 |
| contracts.filters.filterType=LIMIT_TRADING                           | STRING           |                      |                                                                        |
| contracts.filters.maxSellPrice                                       | STRING           | 0                    | Depreciated, no longer in-use                                          |
| contracts.filters.buyPriceUpRate ("filterType": "LIMIT_TRADING")     | STRING           | 0.2                  | Limit Buy cannot be higher than the mark price / 买入不能高于标记价格            |
| contracts.filters.sellPriceDownRate ("filterType": "LIMIT_TRADING")  | STRING           | 0.2                  | Limit Sell cannot be lower than the mark price / 卖出不能低于标记价格            |
| contracts.filters.maxEntrustNum ("filterType": "LIMIT_TRADING")      | INTEGER          | 200                  | Max regular limit orders allowed                                       |
| contracts.filters.maxConditionNum ("filterType": "LIMIT_TRADING")    | INTEGER          | 200                  | Max conditional orders allowed                                         |
| contracts.filters.filterType=MARKET_TRADING                          | STRING           |                      |                                                                        |
| contracts.filters.buyPriceUpRate ("filterType": "MARKET_TRADING")    | STRING           | 0.2                  | Market buy cannot be higher than the mark price / 买入不能高于标记价格           |
| contracts.filters.sellPriceDownRate ("filterType": "MARKET_TRADING") | STRING           | 0.2                  | Market sell cannot be lower than the mark price / 卖出不能低于标记价格           |
| contracts.filters.filterType=OPEN_QUOTE                              | STRING           |                      |                                                                        |
| contracts.filters.noAllowMarketStartTime                             | STRING           | 1668483032058        | Market order start time is not allowed, only for OPEN_QUOTE types      |
| contracts.filters.noAllowMarketEndTime                               | STRING           | 1668483032058        | Market order end time is not allowed, only for OPEN_QUOTE types        |
| contracts.filters.limitOrderStartTime                                | STRING           | 1668483032058        | Time limit order start time, only for OPEN_QUOTE types                 |
| contracts.filters.limitOrderEndTime                                  | STRING           | 1668483032058        | Time limit order end time, only for OPEN_QUOTE types                   |
| contracts.filters.limitMinPrice                                      | STRING           | 0.1                  | Lowest price for a limited time limit order, only for OPEN_QUOTE types |
| contracts.filters.limitMaxPrice                                      | STRING           | 1000                 | Limit order maximum price, only for OPEN_QUOTE types                   |
| brokerFilters                                                        | Object Array     |                      | Not currently in use                                                   |
| options                                                              | Object Array     |                      | Not currently in use                                                   |
| site                                                                 | STRING           | mena                 | Market site. Enum: `hk` , `mena`                                       |

### Get Order book

**GET** `/quote/v1/depth`

Retrieve the current order book depth

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values   | **DESCRIPTION**                                                                |
|-----------------|------------|---------|------------------|--------------------------------------------------------------------------------|
| symbol          | STRING     | Y       | ETHUSD           | Currency pair                                                                  |
| limit           | INTEGER    | C       | 200              | The number of layers for each direction. Maximum value is 200. Default is 100. |
| site            | STRING     | N       | MENA             | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified.              |

**Response Content**

```
{ "t" : 1764059245287 , "b" : [ [ "87473.15" , "0.05805" ], [ "87473.14" , "0.01143" ] ], "a" : [ [ "87474.35" , "0.00114" ], [ "87476.61" , "0.00045" ] ]
}
```

| **PARAMETER**   | **TYPE**        |   **Example values** | **DESCRIPTION**   |
|-----------------|-----------------|----------------------|-------------------|
| t               | LONG            |        1764059245287 | Timestamp         |
| b               | Array of Arrays |                      | Buying direction  |
| 1st element     | STRING          |             29830.76 | Bid price         |
| 2nd element     | STRING          |               0.0005 | Bid quantity      |
| ...             |                 |                      |                   |
| a               | Array of Arrays |                      | Selling direction |
| 1st element     | STRING          |             29938.49 | Ask price         |
| 2nd element     | STRING          |               0.0005 | Ask quantity      |
| ...             |                 |                      |                   |

### Get Recent Trade List

**GET** `/quote/v1/trades`

Retrieve the recent trade information

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values   | **DESCRIPTION**                                                   |
|-----------------|------------|---------|------------------|-------------------------------------------------------------------|
| symbol          | STRING     | Y       | ETHUSD           | Currency pair                                                     |
| limit           | INTEGER    | C       | 100              | The number of trades. Maximum value is 100. Default is 100.       |
| site            | STRING     | N       | MENA             | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**Response Content**

```
[ { "t" : 1764059593000 , "p" : "87371.47" , "q" : "0.02" , "ibm" : false }, { "t" : 1764059593105 , "p" : "87371.47" , "q" : "0.16" , "ibm" : false }, { "t" : 1764059594244 , "p" : "87380.06" , "q" : "0.01" , "ibm" : false }
]
```

| **PARAMETER**   | **TYPE**     | **Example values**   | **DESCRIPTION**                                         |
|-----------------|--------------|----------------------|---------------------------------------------------------|
| *               | Object Array |                      | Latest trades list                                      |
| t               | LONG         | 1764059594244        | Traded timestamp                                        |
| p               | STRING       | 87380.06             | Traded price                                            |
| q               | STRING       | 0.01                 | Volume                                                  |
| ibm             | BOOLEAN      | true                 | true: buyer's maker order   false: seller's maker order |

### Get Kline

**GET** `/quote/v1/klines`

**K-line/candlestick chart interval**

m → minutes; h → hours; d → days; w → weeks; M → months

- 1m
- 3m
- 5m
- 15m
- 30m
- 1h
- 2h
- 4h
- 6h
- 8h
- 12h
- 1d
- 1w
- 1M

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req 'd   | **Example values**   | **DESCRIPTION**                                                   |
|-----------------|------------|----------|----------------------|-------------------------------------------------------------------|
| symbol          | STRING     | Y        | ETHUSDT              | Currency pair                                                     |
| interval        | ENUM       | Y        | 1m                   | Time interval                                                     |
| limit           | INTEGER    |          | 10                   | Return the number of bars, the maximum value is 1000              |
| startTime       | INTEGER    |          | 1478692862000        | Start Time                                                        |
| endTime         | INTEGER    |          | 1478696782000        | End Time                                                          |
| site            | STRING     | N        | MENA                 | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**Response Content**

```
[ [ 1766718300000 , "89037.52" , "89037.52" , "89037.52" , "89037.52" , "0" , 0 , "0" , 0 , "0" , "0" ], [ 1766718360000 , "89037.52" , "89037.52" , "89037.52" , "89037.52" , "0" , 0 , "0" , 0 , "0" , "0" ], [ 1766718420000 , "89101.5" , "89101.5" , "89101.5" , "89101.5" , "0.00012" , 0 , "10.69218" , 1 , "0.00012" , "10.69218" ]
]
```

| **PARAMETER**                  | **TYPE**        |   **Example values** | **DESCRIPTION**              |
|--------------------------------|-----------------|----------------------|------------------------------|
| -                              | Array of Arrays |                      | Kline information list       |
| (kline_open_time)              | LONG            |        1764060600000 | Opening timestamp            |
| (open_price)                   | STRING          |             29871.34 | Open Price                   |
| (high_price)                   | STRING          |             29871.34 | High Price                   |
| (low_price)                    | STRING          |             29773.82 | Low Price                    |
| (close_price)                  | STRING          |             29863.45 | Close Price                  |
| (volume)                       | STRING          |              0.00602 | Trading volume               |
| (kline_close_time)             | INTEGER         |                    0 | Closing timestamp            |
| (quote_asset_volume)           | STRING          |          179.5946714 | Quote Asset Volume           |
| (number_of_trades)             | INTEGER         |                   14 | Number of Trades             |
| (taker_buy_base_asset_volume)  | STRING          |                0.004 | Taker buy base asset volume  |
| (taker_buy_quote_asset_volume) | STRING          |            119.41295 | Taker buy quote asset volume |

### Get 24hr Ticker Price Change

**GET** `/quote/v1/ticker/24hr`

Retrieve the 24 hours rolling price change

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values   | **DESCRIPTION**                                                                            |
|-----------------|------------|---------|------------------|--------------------------------------------------------------------------------------------|
| symbol          | STRING     |         | ETHUSD           | Currency pair                                                                              |
| instType        | STRING     |         | SPOT             | `SPOT` : Default Value `FUTURES` : FUTURES Trading Pairs only `ANY` : all instrument types |
| site            | STRING     | N       | MENA             | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified.                          |

**Response Content**

```
[ { "t" : 1766718180001 , "s" : "BTCUSDT-PERPETUAL" , "c" : "89164.2" , "h" : "89323.6" , "l" : "86850.6" , "o" : "87828.6" , "b" : "89056.6" , "a" : "89056.7" , "v" : "823" , "qv" : "72224.7966" , "it" : "FUTURES" }
]
```

| **PARAMETER**   | **TYPE**     | **Example Values**   | **DESCRIPTION**                     |
|-----------------|--------------|----------------------|-------------------------------------|
| -               | Object Array |                      | 24hrs price change list             |
| t               | LONG         | 1764061080001        | Millisecond timeStamp               |
| s               | STRING       | BTCUSD               | Symbol                              |
| c               | STRING       | 29832.76             | Latest traded price                 |
| h               | STRING       | 30050.21             | Highest price                       |
| l               | STRING       | 29568.84             | Lowest price                        |
| o               | STRING       | 29845.03             | Opening price                       |
| b               | STRING       | 29830.76             | Highest bid                         |
| a               | STRING       | 29938.49             | Highest selling price               |
| v               | STRING       | 2.09774              | Total trade volume (in base asset)  |
| qv              | STRING       | 62639.2417592        | Total trade volume (in quote asset) |
| it              | STRING       | SPOT                 | SPOT、FUTURES、ANY                    |

### Get Symbol Price Ticker

**GET** `/quote/v1/ticker/price`

Retrieve the latest price by ticker

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values   | **DESCRIPTION**                                                   |
|-----------------|------------|---------|------------------|-------------------------------------------------------------------|
| symbol          | STRING     |         | ETHUSD           | Currency pair                                                     |
| site            | STRING     | N       | MENA             | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**Response Content**

```
[ { "s" : "USDTUSD" , "p" : "0.9992" }
]
```

| **PARAMETER**   | **TYPE**     | **Example Values**   | **DESCRIPTION**          |
|-----------------|--------------|----------------------|--------------------------|
| -               | Object Array |                      | Latest transaction price |
| s               | STRING       | BTCUSD               | Symbol                   |
| p               | STRING       | 87037.97             | Latest traded price      |

### Get Symbol current Top of book

**GET** `/quote/v1/ticker/bookTicker`

Retrieve current top order book by symbol

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values   | **DESCRIPTION**                                                   |
|-----------------|------------|---------|------------------|-------------------------------------------------------------------|
| symbol          | STRING     | Y       | ETHUSD           | Currency pair                                                     |
| site            | STRING     | N       | MENA             | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**Response Content**

```
[ { "s" : "BTCUSDT" , "b" : "89110.8" , "bq" : "0.00067" , "a" : "89110.81" , "aq" : "0.00067" , "t" : 1766718404772 }
]
```

| **PARAMETER**   | **TYPE**     | **Example values**   | **DESCRIPTION**                           |
|-----------------|--------------|----------------------|-------------------------------------------|
| -               | Object Array |                      | Retrieve current top order book by symbol |
| s               | STRING       | BTCUSD               | Symbol                                    |
| b               | STRING       | 86953.92             | Top of book Bid Price                     |
| bq              | STRING       | 1.01969              | Top of book Bid Quantity                  |
| a               | STRING       | 86953.93             | Top of book Ask Price                     |
| aq              | STRING       | 0.07897              | Top of book Ask Quantity                  |
| t               | LONG         | 1764061843241        | Timestamp                                 |

### Get Merge Depth

**GET** `/quote/v1/depth/merged`

Query aggregation market depth

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values   | **DESCRIPTION**                                                                                                                                                                                                                                                                            |
|-----------------|------------|---------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol          | STRING     | Y       | BTCUSD           | Currency pair                                                                                                                                                                                                                                                                              |
| limit           | INTEGER    |         | 10               | The number of layers for each direction. Maximum value is 200. Default is 100.                                                                                                                                                                                                             |
| scale           | INTEGER    |         | 1                | Price aggregation precision. `scale=1, 2, 3, ...` aggregates to 1, 2, 3 decimal places respectively. `scale=-1, -2, -3, ...` aggregates to the ones, tens, hundreds place respectively. `scale=0` has no meaning. Default is the maximum number of decimal places supported by the symbol. |
| site            | STRING     | N       | MENA             | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified.                                                                                                                                                                                                                          |

**Response Content**

```
{ "t" : 1766718663907 , "b" : [ [ "89210.22" , "0.00067" ], [ "89194.19" , "0.1" ], [ "89194.02" , "0.00748" ] ], "a" : [ [ "89210.32" , "0.00067" ], [ "89269.69" , "0.12333" ], [ "89294.11" , "0.1" ] ]
}
```

| **PARAMETER**   | **TYPE**        |   **Example values** | **DESCRIPTION**   |
|-----------------|-----------------|----------------------|-------------------|
| t               | LONG            |        1764059245287 | Timestamp         |
| b               | Array of Arrays |                      | Buying direction  |
| 1st element     | STRING          |             29830.76 | Bid price         |
| 2nd element     | STRING          |               0.0005 | Bid quantity      |
| ...             |                 |                      |                   |
| a               | Array of Arrays |                      | Selling direction |
| 1st element     | STRING          |             29938.49 | Ask price         |
| 2nd element     | STRING          |               0.0005 | Ask quantity      |
| ...             |                 |                      |                   |

### Get Mark Price

**GET** `/quote/v2/markPrice`

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values   | **DESCRIPTION**                                                   |
|-----------------|------------|---------|------------------|-------------------------------------------------------------------|
| symbol          | STRING     | Y       | BTCUSD-PERPETUAL | Currency pair                                                     |
| site            | STRING     | N       | MENA             | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**Response Content**

```
{ "symbolId" : "BTCUSD-PERPETUAL" , "price" : "89768.358" , "time" : 1769068545000
}
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**   |
|-----------------|------------|----------------------|-------------------|
| symbolId        | STRING     | BTCUSD-PERPETUAL     | Symbol            |
| price           | STRING     | 89768.358            | Mark price        |
| time            | LONG       | 1769068545000        | Timestamp         |

### Get Index Price

**GET** `/quote/v2/index`

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req'd   | Example values   | **DESCRIPTION**                                                   |
|-----------------|------------|---------|------------------|-------------------------------------------------------------------|
| symbol          | STRING     |         | BTCUSD           | Currency pair                                                     |
| site            | STRING     | N       | MENA             | Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**Response Content**

```
{ "index" : { "BTCUSD" : "89932.112" }, "edp" : { "BTCUSD" : "89950.99238048" }
}
```

| **PARAMETER**   | **TYPE**   |   **Example values** | **DESCRIPTION**                                  |
|-----------------|------------|----------------------|--------------------------------------------------|
| index           | OBJECT     |                      | Index Price                                      |
| index.BTCUSD    | STRING     |            88872.674 |                                                  |
| ...             |            |                      |                                                  |
| edp             | OBJECT     |                      | The average of the index for the last 10 minutes |
| edp.BTCUSD      | STRING     |          88871.27269 |                                                  |
| ...             |            |                      |                                                  |

## Market Place

### Get MP Quote Pairs

**GET** `/api/v1/market-place/get-pairs`

Get a list of tradable quote pairs

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   |   **Example Values** | **DESCRIPTION**           |
|-----------------|------------|-------------|----------------------|---------------------------|
| recvWindow      | LONG       |             |                      | Recv Window. Default 5000 |
| timestamp       | LONG       | Y           |        1714311403031 | Timestamp                 |

**Response Content**

```
{ "quotePair" : [ { "baseCcy" : "USDT" , "quoteCcy" : "USD" , "basePrecision" : "0.0001" , "quotePrecision" : "0.01" , "retailAllowed" : true , "minTradeBaseQuantity" : "10" , "maxTradeBaseQuantity" : "10000000" , "minTradeQuoteQuantity" : "10" , "maxTradeQuoteQuantity" : "10000000" , "piAllowed" : true , "corporateAllowed" : true , "omnibusAllowed" : true , "institutionAllowed" : true , "tradingStatus" : "OPENED" } ]
}
```

| **Parameter**         | **Type**     | **Example Value**   | **Description**                                        |
|-----------------------|--------------|---------------------|--------------------------------------------------------|
| quotePair             | Object Array | ETHUSD              | Returns a list of currency pairs for Request for Quote |
| baseCcy               | STRING       | ETH                 | Base currency                                          |
| quoteCcy              | STRING       | USD                 | Quote currency                                         |
| basePrecision         | STRING       | 0.0001              | Precision of base currency                             |
| quotePrecision        | STRING       | 0.000001            | Precision of quote currency                            |
| retailAllowed         | BOOLEAN      | TRUE                | Whether retail clients are allowed                     |
| minTradeBaseQuantity  | STRING       | 10000               | minTradeQuantity of baseCcy defined in OPM             |
| maxTradeBaseQuantity  | STRING       | 1000000             | maxTradeQuantity of baseCcy defined in OPM             |
| minTradeQuoteQuantity | STRING       | 10000               | minTradeQuantity of quoteCcy defined in OPM            |
| maxTradeQuoteQuantity | STRING       | 1000000             | maxTradeQuantity of quoteCcy defined in OPM            |
| piAllowed             | BOOLEAN      | TRUE                | Whether PI clients are allowed                         |
| corporateAllowed      | BOOLEAN      | TRUE                | Whether Corporate clients are allowed                  |
| omnibusAllowed        | BOOLEAN      | TRUE                | Whether Omnibus clients are allowed                    |
| institutionAllowed    | BOOLEAN      | TRUE                | Whether Institution clients are allowed                |
| tradingStatus         | ENUM         | OPENED, CLOSED      | Quote pair status                                      |

### Create MP RFQ

**POST** `/api/v1/market-place/create-rfq`

Customer creates the RFQ

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example**   | **DESCRIPTION**                                                                                                            |
|-----------------|------------|-------------|---------------|----------------------------------------------------------------------------------------------------------------------------|
| rfqClOrderId    | STRING     | C           | RFQ12345666   | (Optional) An ID defined by the client for the quote order. It will be automatically generated if not sent in the request. |
| buyCcy          | STRING     | Y           | BTC           |                                                                                                                            |
| sellCcy         | STRING     | Y           | USDT          |                                                                                                                            |
| sellAmount      | DECIMAL    | Y           | 130000        | Selling amount                                                                                                             |
| rfqMode         | STRING     | Y           |               | `real-time` , `delayed`                                                                                                    |
| expireSec       | INT        |             | 1800          | RFQ valid period in seconds, default 1800 = 30 minutes, allowed 10-60 mins                                                 |
| recvWindow      | LONG       |             |               | Recv Window. Default 5000                                                                                                  |
| timestamp       | LONG       | Y           | 1714311403031 | Timestamp                                                                                                                  |

**Response Content**

```
{ "rfqId" : "RFQ638459562162049024" , "rfqClOrderId" : "RFQ12345666" , "status" : "new"
}
```

| **PARAMETER**   | **TYPE**   | **Example values**    | **DESCRIPTION**                                                                                                            |
|-----------------|------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------|
| rfqClOrderId    | STRING     | RFQ12345666           | (Optional) An ID defined by the client for the quote order. It will be automatically generated if not sent in the request. |
| rfqId           | STRING     | RFQ638459562162049024 | A unique reference ID for this quote.                                                                                      |
| status          | STRING     | new                   |                                                                                                                            |

### Accept MP Quote

**POST** `/api/v1/market-place/accept-quote`

Customer accepts the quote

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example**           | **DESCRIPTION**                                                           |
|-----------------|------------|-------------|-----------------------|---------------------------------------------------------------------------|
| quoteId         | STRING     | Y           | quote789456123        | The unique quote id auto generated for each quote when creation           |
| rfqId           | STRING     | Y           | rfq638459562162049024 | A unique reference ID for this quote.                                     |
| action          | STRING     | Y           | accept, decline       | `decline` only works for manual order (after decline, rfq becomes failed) |
| recvWindow      | LONG       |             |                       | Recv Window. Default 5000                                                 |
| timestamp       | LONG       | Y           | 1714311403031         | Timestamp                                                                 |

**Response Content**

```
{ "rfqId" : "rfq638459562162049024" , "quoteId" : "quote789456123" , "status" : "accepted" , "expiryTime" : 1717392500
}
```

| **PARAMETER**   | **TYPE**   | **Example values**    | **DESCRIPTION**                                                               |
|-----------------|------------|-----------------------|-------------------------------------------------------------------------------|
| quoteId         | STRING     | quote789456123        | The unique quote id auto generated for each quote when creation               |
| rfqId           | STRING     | rfq638459562162049024 | A unique reference ID for this quote.                                         |
| status          | STRING     | accepted              |                                                                               |
| expiryTime      | LONG       | 1800                  | Min of quote and rfq expiry time, if action = decline,expiryTime will be null |

### Get MP RFQ history

**GET** `/api/v1/market-place/rfqs`

Customer check the RFQ history

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example**   | **DESCRIPTION**                                                              |
|-----------------|------------|-------------|---------------|------------------------------------------------------------------------------|
| rfqId           | STRING     |             | 122456        | The orderId generated by HashKey. If not specified, will return all records. |
| quoteId         | STRING     |             |               | The unique quote id auto generated for each quote when creation              |
| rfqClOrderId    | STRING     |             | 122455        | A client-defined ID for the order, autogenerated if not specified.           |
| limit           | INT        |             |               | Limit per page for records. - Default: 500, Max: 1000.                       |
| status          | ENUM       |             | `new`         | status filter                                                                |
| startTime       | LONG       | Y           | 1764645641000 | createTime filter, max last 90 days                                          |
| endTime         | LONG       | Y           | 1766373641000 | createTime filter, max last 90 days                                          |
| recvWindow      | LONG       |             |               | Recv Window. Default 5000                                                    |
| timestamp       | LONG       | Y           | 1714311403031 | Timestamp                                                                    |

**Response Content**

```
[ { "rfqCreateTime" : 1716002500 , "rfqId" : "RFQ638459562162049024" , "quoteId" : "QUOTE_789456123" , "rfqClOrderId" : "QUOTE_789456123" , "rfqMode" : "real-time" , "quoteMode" : "real-time" , "buyCcy" : "BTC" , "sellCcy" : "USDT" , "buyAmount" : "2" , "sellAmount" : "" , "price" : "65000" , "status" : "successful" , "executedTime" : 1717392500 }
]
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|-----------------|------------|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rfqCreateTime   | LONG       | 1617315200           | Timestamp that the rfg was created                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| rfqId           | STRING     | 122456               | The unique orderId generated by HashKey.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| quoteId         | STRING     |                      | The unique quote id auto generated for each quote when creation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| rfqClOrderId    | STRING     | 122455               | A client-defined ID for the order, autogenerated if not specified.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| rfqMode         | STRING     |                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| quoteMode       | STRING     |                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| buyCcy          | STRING     |                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| sellCcy         | STRING     |                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| buyAmount       | STRING     |                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| sellAmount      | STRING     |                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| price           | STRING     |                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| status          | ENUM       | `new`                | • `new` : active   • `accepted` : quote accepted   • `processing` : On-chain/funds are locked (Real-time orders will be executed immediately, while delayed orders will remain in this status pending settlement, up to T+2)   • `successful` : Settlement successful   • `expired` : Quote expired   • `cancelled` : Cancelled by HSK operations   • `declined` : Manual quote rejected by client   • `manual-order` : Awaiting manual quote   • `manual-order-confirmation` : Manual quote received, awaiting confirmation from the quoting party |
| executedTime    | LONG       |                      | Timestamp that the rfq was executed and status = successful                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

### Get all Active MP Quotes

**GET** `/api/v1/market-place/rfq-active/{rfqId}`

Customer check the RFQ history

**Weight: 1**

**Request Parameters**

| **PARAMETER**          | **TYPE**   | **Req'd**   |   **Example** | **DESCRIPTION**                   |
|------------------------|------------|-------------|---------------|-----------------------------------|
| rfqId (path parameter) | STRING     | Y           |        123456 | The orderId generated by HashKey. |
| recvWindow             | LONG       |             |               | Recv Window. Default 5000         |
| timestamp              | LONG       | Y           | 1714311403031 | Timestamp                         |

**Response Content**

```
[ { "quoteMode" : "REAL_TIME" , "sellCcy" : "USD" , "rfqId" : "MP740508620175265792" , "quoteId" : "MPQ740508741768138752" , "rfqClOrderId" : "MP740508620175265792" , "buyCcy" : "BTC" , "rfqMode" : "REAL_TIME" , "buyAmount" : "0.00009" , "expireTime" : 1754359101795 , "sellAmount" : "10" , "price" : "101000" , "rank" : 1 , "status" : "new" }, { "quoteMode" : "REAL_TIME" , "sellCcy" : "USD" , "rfqId" : "MP740508620175265792" , "quoteId" : "MPQ740508741768138792" , "rfqClOrderId" : "MP740508620175265792" , "buyCcy" : "BTC" , "rfqMode" : "REAL_TIME" , "buyAmount" : "0.00009" , "expireTime" : 1754359101795 , "sellAmount" : "10" , "price" : "102000" , "rank" : 2 , "status" : "new" }
]
```

| **PARAMETER**   | **TYPE**   | **Example values**   | **DESCRIPTION**   |
|-----------------|------------|----------------------|-------------------|
| quoteMode       | STRING     |                      |                   |
| sellCcy         | STRING     |                      |                   |
| rfqId           | STRING     |                      |                   |
| quoteId         | STRING     |                      |                   |
| rfqClOrderId    | STRING     |                      |                   |
| buyCcy          | STRING     |                      |                   |
| rfqMode         | STRING     |                      |                   |
| buyAmount       | STRING     |                      |                   |
| expireTime      | LONG       |                      |                   |
| sellAmount      | STRING     |                      |                   |
| price           | STRING     |                      |                   |
| rank            | INTEGER    |                      |                   |
| status          | STRING     |                      |                   |

## Miscellaneous

### Test Connectivity

**GET** `/api/v1/ping`

Test connectivity to ensure valid Status 200 OK

**Weight: 1**

**Request Parameters**

Empty

**Response Content**

```
{}
```

{}

### Check Server Time

**GET** `/api/v1/time`

Test the connection and returns the current server time (in UNIX timestamp in milliseconds)

**Weight: 1**

**Request Parameters**

Empty

**Response Content**

```
{ "serverTime" : 1764229341307
}
```

| **PARAMETER**   | **TYPE**   |   Example values | **DESCRIPTION**              |
|-----------------|------------|------------------|------------------------------|
| serverTime      | LONG       |    1764229341307 | Server Millisecond Timestamp |

### Create Listen Key

**POST** `/api/v1/userDataStream`

Create a single Listen Key. Valid for 60 minutes.

**Reminder**

- Start a new user data stream.
- The stream will close after **60 minutes** unless a keepalive is sent.
- Recommended to send a reset request every 30 minutes. [Reset-Listen-Key](#Reset-Listen-Key)

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req 'd   | **DESCRIPTION**           |
|-----------------|------------|----------|---------------------------|
| recvWindow      | LONG       |          | Recv Window. Default 5000 |
| timestamp       | LONG       | Y        | Timestamp                 |

**Response Content**

```
{ "listenKey" : "MKxPTRoLXBBhlRseAUaDyWyZVjiNxCVqcaUasZidmByckGjUcLBKKcopKbvUfORD"
}
```

| **PARAMETER**   | **TYPE**   | **Example Values**                                               | **DESCRIPTION**                  |
|-----------------|------------|------------------------------------------------------------------|----------------------------------|
| listenKey       | STRING     | MKxPTRoLXBBhlRseAUaDyWyZVjiNxCVqcaUasZidmByckGjUcLBKKcopKbvUfORD | Key to subscribe websocket feeds |

### Reset Listen Key

**PUT** `/api/v1/userDataStream`

Reset validity time of a listenKey to 60 minutes.

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req 'd   | **DESCRIPTION**           |
|-----------------|------------|----------|---------------------------|
| listenKey       | STRING     | Y        | Key to reset              |
| recvWindow      | LONG       |          | Recv Window. Default 5000 |
| timestamp       | LONG       | Y        | Timestamp                 |

**Response Content**

```
{}
```

{}

### Delete Listen Key

**DELETE** `/api/v1/userDataStream`

Delete a single Listen Key.

**Weight: 1**

**Request Parameters**

| **PARAMETER**   | **TYPE**   | Req 'd   | **DESCRIPTION**           |
|-----------------|------------|----------|---------------------------|
| listenKey       | STRING     | Y        | Key to delete             |
| recvWindow      | LONG       |          | Recv Window. Default 5000 |
| timestamp       | LONG       | Y        | Timestamp                 |

**Response Content**

```
{}
```

{}

## Error Codes

List of error codes

**Note:** **`%s`** **is a placeholder** 💬

|   **ERROR CODE** |   **HTTP Status Code** | **ERROR MESSAGE**                                                                                                   | **DESCRIPTION**                                                                                                                                                          |
|------------------|------------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|              200 |                    200 |                                                                                                                     | Success request                                                                                                                                                          |
|             0000 |                    200 | success                                                                                                             | Success request                                                                                                                                                          |
|             0001 |                    400 | Required field `%s` missing or invalid                                                                              | Required field `%s` missing or invalid. E.g. Required field quantity missing or invalid                                                                                  |
|             0001 |                    400 | Incorrect signature                                                                                                 | The server is not able to valid your signature request. Please check your signature whether it have the correct signing.                                                 |
|             0003 |                    400 | Rate limit exceeded                                                                                                 | Rate limit exceed per configuration. Please manage the number of your request                                                                                            |
|             0102 |                    400 | Invalid APIKey                                                                                                      | There was an issue validating your API Key permission. Please check your API Key permission                                                                              |
|             0103 |                    400 | APIKey expired                                                                                                      | API-key has expired. Please login to Account management console to renew the API key                                                                                     |
|             0104 |                    400 | accountId is not allowed                                                                                            | The accountId defined is not permissible                                                                                                                                 |
|             0201 |                    400 | Instrument not found                                                                                                | The instrument defined cannot be located                                                                                                                                 |
|             0202 |                    400 | Invalid IP                                                                                                          | Our server detected the IP addresses submitted for the API request does not match API key whitelisted IP address                                                         |
|             0206 |                    400 | Unsupported order type                                                                                              | Invalid order type being sent to the server                                                                                                                              |
|             0207 |                    400 | Invalid price                                                                                                       | Invalid price being sent to the server                                                                                                                                   |
|             0209 |                    400 | Invalid price precision                                                                                             | The precision price is over the maximum allowed for this asset                                                                                                           |
|             0210 |                    400 | Price outside of allowed range                                                                                      | Price of the order below minPrice or exceeds maxPrice range. Please check exchangeInfo                                                                                   |
|             0211 |                    400 | Order not found                                                                                                     | Our server not able to locate the orderId defined                                                                                                                        |
|             0212 |                    400 | Order has already been completed (filled, canceled, etc) or does not exist. Please check the order status to verify | Order has already been completed (filled, canceled, etc) or does not exist. Please check the order status to verify                                                      |
|             0401 |                    400 | Insufficient asset                                                                                                  | There is insufficient balance to submit the order                                                                                                                        |
|            -1000 |                    400 | An unknown error occurred while processing the request                                                              | An issue generated by our server                                                                                                                                         |
|            -1001 |                    400 | Internal error                                                                                                      | Unable to process your request. Please try again                                                                                                                         |
|            -1002 |                    400 | Unauthorized operation                                                                                              | Server is not able to validate your API Key. Please ensure you have the valid API Key to the corresponding environment                                                   |
|            -1004 |                    400 | Bad request                                                                                                         | There was an issue with to process your request. Please check your parameters or values are valid                                                                        |
|            -1005 |                    400 | No permission                                                                                                       | It appears there is insufficient trading permission. Please check your permission                                                                                        |
|            -1006 |                    400 | Execution status unknown                                                                                            | An unexpected response was received from the message bus                                                                                                                 |
|            -1007 |                    400 | Timeout waiting for response from server                                                                            | Timeout waiting for response from backend server. Send status unknown; execution status unknown                                                                          |
|            -1014 |                    400 | Unsupported order combination                                                                                       | The order combination specified is not supported                                                                                                                         |
|            -1015 |                    400 | Too many new orders, current limit is `%s` orders per `%s`                                                          | Reach the rate limit .Please slow down your request speed.        Too many new orders.                                                                                   |
|            -1020 |                    400 | Unsupported operation                                                                                               | User operation is not supported                                                                                                                                          |
|            -1021 |                    400 | Timestamp for this request is outside of the recvWindow                                                             | Timestamp for this request was 1000ms ahead of the server's time.        Please check the difference between your local time and server time                             |
|            -1024 |                    400 | Duplicate request                                                                                                   | Duplicate request received                                                                                                                                               |
|            -1101 |                    400 | Feature has been offline                                                                                            | Feature has been offline, please check with API team for further details                                                                                                 |
|            -1102 |                    400 | Illegal parameter                                                                                                   | Illegal parameter                                                                                                                                                        |
|            -1115 |                    400 | Invalid timeInForce                                                                                                 | Invalid time in force being sent                                                                                                                                         |
|            -1117 |                    400 | Invalid order side                                                                                                  | Invalid side being sent                                                                                                                                                  |
|            -1123 |                    400 | Invalid client order id                                                                                             | Invalid client order ID being sent                                                                                                                                       |
|            -1124 |                    400 | Invalid price                                                                                                       | Invalid price being sent                                                                                                                                                 |
|            -1126 |                    400 | Invalid quantity                                                                                                    | Invalid quantity being sent                                                                                                                                              |
|            -1129 |                    400 | Invalid parameters, quantity and amount are not allowed to be sent at the same time.                                | The combination of quantity and amount is not allowed to be submitted at the same time                                                                                   |
|            -1130 |                    400 | Illegal parameter `%s`                                                                                              | Invalid data sent for a parameter. E.g. "Illegal parameter 'symbol'"                                                                                                     |
|            -1132 |                    400 | Order price greater than the maximum                                                                                | Order price exceeds maxPrice. Check ExchangeInfo                                                                                                                         |
|            -1133 |                    400 | Order price lower than the minimum                                                                                  | Order price below the threshold minPrice. Check ExchangeInfo                                                                                                             |
|            -1135 |                    400 | Order quantity greater than the maximum                                                                             | Order quantity exceeds the maxQty. Check ExchangeInfo                                                                                                                    |
|            -1136 |                    400 | Order quantity lower than the minimum                                                                               | Order quantity below threshold minQty. Check ExchangeInfo                                                                                                                |
|            -1137 |                    400 | Order quantity precision too large                                                                                  | Order quantity precision is too large                                                                                                                                    |
|            -1139 |                    400 | Order has been filled                                                                                               | Unable to fulfill request as order has been filled                                                                                                                       |
|            -1140 |                    400 | Order amount lower than the minimum                                                                                 | The transaction amount is below the threshold minAmount. Check ExchangeInfo                                                                                              |
|            -1141 |                    400 | Duplicate order                                                                                                     | The server have detected an existing clientOrderId sent before                                                                                                           |
|            -1142 |                    400 | Order has been cancelled                                                                                            | Unable to fulfill rquest as order has been canceled                                                                                                                      |
|            -1143 |                    400 | Order not found on order book                                                                                       | Unable to locate orderbook                                                                                                                                               |
|            -1144 |                    400 | Order has been locked                                                                                               | Order has been locked                                                                                                                                                    |
|            -1145 |                    400 | Cancellation on this order type not supported                                                                       | This order type does not support cancellation                                                                                                                            |
|            -1146 |                    400 | Order creation timeout                                                                                              | Not able to create the order and timed out                                                                                                                               |
|            -1147 |                    400 | Order cancellation timeout                                                                                          | Not able to cancel the order and timed out                                                                                                                               |
|            -1148 |                    400 | Order amount precision too large                                                                                    | Market Cash Amount precision is too long                                                                                                                                 |
|            -1149 |                    400 | Order creation failed                                                                                               | Order creation failed                                                                                                                                                    |
|            -1150 |                    400 | Order cancellation failed                                                                                           | Order cancellation failed                                                                                                                                                |
|            -1151 |                    400 | The trading pair is not open yet                                                                                    | The trading is not yet listed for trading                                                                                                                                |
|            -1152 |                    400 | User does not exist                                                                                                 | Unable to find user                                                                                                                                                      |
|            -1153 |                    400 | Invalid price type                                                                                                  | Invalid price type being sent                                                                                                                                            |
|            -1154 |                    400 | Invalid position side                                                                                               | Invalid side being sent                                                                                                                                                  |
|            -1155 |                    400 | The trading pair is not available for api trading                                                                   | API trading is suspended for API trading                                                                                                                                 |
|            -1156 |                    400 | Limit maker order rejected: Improper price may cause immediate fill.                                                | Creation of limit maker order failed as the order execute immediately. **For HashKey Global only.**                                                                      |
|            -1160 |                    400 | Account does not exist                                                                                              | Account does not exist                                                                                                                                                   |
|            -1161 |                    400 | Balance transfer failed                                                                                             | Transfer internal funds failed                                                                                                                                           |
|            -1162 |                    400 | Unsupport contract address                                                                                          | Contract address submitted is not valid                                                                                                                                  |
|            -1163 |                    400 | Illegal withdrawal address                                                                                          | Withdraw address is not valid                                                                                                                                            |
|            -1164 |                    400 | Withdraw failed                                                                                                     | Withdraw failed, check if the withdrawal amount meets the minimum withdrawal amount                                                                                      |
|            -1165 |                    400 | Withdrawal amount cannot be null                                                                                    | Withdrawal amount needs to be more than 0                                                                                                                                |
|            -1166 |                    400 | Withdrawal amount exceeds the daily limit                                                                           | Withdrawal amount exceeded the daily limit allowed                                                                                                                       |
|            -1167 |                    400 | Withdrawal amount less than the minimum                                                                             | Withdrawal amount less than the min withdraw amount limit                                                                                                                |
|            -1168 |                    400 | Illegal withdrawal amount                                                                                           | Withdrawal amount characters are not valid                                                                                                                               |
|            -1169 |                    400 | Withdraw not allowed                                                                                                | Withdrawal is currently suspended                                                                                                                                        |
|            -1170 |                    400 | Deposit not allowed                                                                                                 | Deposit is currently suspended                                                                                                                                           |
|            -1171 |                    400 | Withdrawal address not in whitelist                                                                                 | Withdrawal address has not yet been whitelisted                                                                                                                          |
|            -1172 |                    400 | Invalid from account id                                                                                             | The fromAccountId is invalid                                                                                                                                             |
|            -1173 |                    400 | Invalid to account id                                                                                               | The toAccountId is invalid                                                                                                                                               |
|            -1174 |                    400 | Transfer not allowed between the same account                                                                       | The fromAccount should not be equal toAccount                                                                                                                            |
|            -1175 |                    400 | Invalid fiat deposit status                                                                                         | The fiat deposit status submitted is invalid                                                                                                                             |
|            -1176 |                    400 | Invalid fiat withdrawal status                                                                                      | The fiat withdrawal status submitted is invalid                                                                                                                          |
|            -1177 |                    400 | Invalid fiat order type                                                                                             | The fiat order type submitted is invalid                                                                                                                                 |
|            -1182 |                    400 | The newly whitelisted withdrawal address will take effect in 30 min. Please try it later.                           | The newly whitelisted withdrawal address will take effect after a certain time period for the sake of safety. During the mean time, the address is not available         |
|            -1186 |                    400 | Placing orders via api is not allowed, please check the API permission                                              | Placing orders via api is not allowed, please check the API permission                                                                                                   |
|            -1193 |                    400 | Order creation count exceeds the limit                                                                              | Order count have exceeded the amount allowed                                                                                                                             |
|            -1194 |                    400 | Market order creation forbidden                                                                                     | Creation of market order is forbidden                                                                                                                                    |
|            -1200 |                    400 | Order buy quantity too small                                                                                        | Buy limit quantity below the threshold minQty. Check ExchangeInfo                                                                                                        |
|            -1201 |                    400 | Order buy quantity too large                                                                                        | Buy limit quantity exceeds maxQty. Check ExchangeInfo                                                                                                                    |
|            -1202 |                    400 | Order sell quantity too small                                                                                       | Sell limit quantity below the threshold minQty. Check ExchangeInfo                                                                                                       |
|            -1203 |                    400 | Order sell quantity too large                                                                                       | Sell limit quantity exceeds the maxQty. Check ExchangeInfo                                                                                                               |
|            -1204 |                    400 | From account must be a main account                                                                                 | Transfer fromAccountId needs to be a main account                                                                                                                        |
|            -1205 |                    400 | Account not authorized                                                                                              | Account is not authorised                                                                                                                                                |
|            -1206 |                    400 | Order amount greater than the maximum                                                                               | The transaction amount is below the threshold maxAmount. Check ExchangeInfo                                                                                              |
|            -1207 |                    400 | The status of deposit is invalid                                                                                    | The status of deposit submitted is invalid                                                                                                                               |
|            -1208 |                    400 | The orderType of fiat is invalid                                                                                    | The status of orderType is not valid                                                                                                                                     |
|            -1209 |                    400 | The status of withdraw is invalid                                                                                   | The status of withdraw is not valid                                                                                                                                      |
|            -1210 |                    400 | The deposit amount `%s` must not be less than the minimum deposit amount `%s %s` .                                  | The deposit amount `%s` must not be less than the minimum deposit amount `%s %s` .                                                                                       |
|            -1211 |                    400 | Withdrawal in progress                                                                                              | Withdrawal in progress                                                                                                                                                   |
|            -1212 |                    400 | The order of deposit does not exist                                                                                 | The order of deposit does not exist                                                                                                                                      |
|            -1213 |                    400 | The status of deposit cannot apply refund                                                                           | The status of deposit cannot apply refund                                                                                                                                |
|            -1214 |                    400 | The account of deposit does not exist                                                                               | The account of deposit does not exist                                                                                                                                    |
|            -1215 |                    400 | User account status is abnormal                                                                                     | User account status is abnormal                                                                                                                                          |
|            -1218 |                    400 | User type does not support HSK deduction                                                                            | User type does not support enabling HSK fee deduction                                                                                                                    |
|            -1300 |                    400 | Sorry we can not locate this depositOrderId, please check and try again.                                            | Sorry we can not locate this depositOrderId, please check and try again.                                                                                                 |
|            -1301 |                    400 | Please contact the support team for historical orders                                                               | Please contact the support team for historical orders                                                                                                                    |
|            -1302 |                    400 | The refund via api can not be processed due to order status, please contact support team                            | The refund via api can not be processed due to order status, please contact support team                                                                                 |
|            -1303 |                    400 | The refund request via api can not be processed due to failure reason, please contact support team                  | The refund request via api can not be processed due to failure reason, please contact support team                                                                       |
|            -1304 |                    400 | Please upload supporting docs as required, only image files .jpg, .png, .jpeg allowed.                              | Please upload supporting docs as required, only image files .jpg, .png, .jpeg allowed.                                                                                   |
|            -1305 |                    400 | Image size exceeds 1M, please revise and try again                                                                  | Image size exceeds 1M, please revise and try again                                                                                                                       |
|            -2010 |                    400 | Limit maker order rejected: Improper price may cause immediate fill.                                                | New order request was rejected. Usually this is due to new LIMIT\_MAKER order not able to be maker, our system will auto reject the order **For HashKey Hong Kong only** |
|            -2011 |                    400 | Order cancellation rejected                                                                                         | Cancel request was rejected                                                                                                                                              |
|            -2016 |                    400 | API key creation exceeds the limit                                                                                  | The number of API key created have exceeded the limit                                                                                                                    |
|            -2017 |                    400 | Open orders exceeds the limit of the trading pair                                                                   | The number of open orders have exceeded the limit for the trading pair                                                                                                   |
|            -2018 |                    400 | Trade user creation exceeds the limit                                                                               | The number of trade user created have exceeded the limit                                                                                                                 |
|            -2019 |                    400 | Trader and omnibus user not allowed to login app                                                                    | The trader and omnibus user is not allowed to login to the app                                                                                                           |
|            -2020 |                    400 | Not allowed to trade this trading pair                                                                              | Not allowed to trade this trading pair                                                                                                                                   |
|            -2021 |                    400 | Not allowed to trade this trading pair                                                                              | Not allowed to trade this trading pair                                                                                                                                   |
|            -2022 |                    400 | Order batch size exceeds the limit                                                                                  | The number of orders in batchOrders request exceeds its limit                                                                                                            |
|            -2023 |                    400 | Need to pass KYC verification                                                                                       | Need to pass KYC verification in order to use API trading                                                                                                                |
|            -2024 |                    400 | Fiat account does not exist                                                                                         | Fiat account ID defined does not exist                                                                                                                                   |
|            -2025 |                    400 | Custody account not exist                                                                                           | Custody account ID defined does not exist                                                                                                                                |
|            -2026 |                    400 | Invalid type                                                                                                        | The type defined is invalid                                                                                                                                              |
|            -2027 |                    400 | Exceed maximum time range of 30 days                                                                                | The startTime and endTime defined for Fund statement request exceeds the 30 days limit                                                                                   |
|            -2028 |                    400 | The search is limited to data within the last one month                                                             | The search is limited to data within the last one month                                                                                                                  |
|            -2029 |                    400 | The search is limited to data within the last three months                                                          | The search is limited to data within the last three months                                                                                                               |
|            -2030 |                    400 | Order batch size exceeds the limit                                                                                  | Order batch size exceeds the limit                                                                                                                                       |
|            -3117 |                    400 | Invalid permission                                                                                                  | Invalid permission is detected. E.g. APIKey does not have the accountID permission to query the balance of the account                                                   |
|            -3143 |                    400 | Currently, your trading account has exceeded its limit and is temporarily unable to perform trades                  | The trading account have exceeds its limit capacity. We have temporarily suspended your trading                                                                          |
|            -3144 |                    400 | Currently, your trading account has exceeded its limit and is temporarily unable to perform transfers               | The trading account have exceeds its limit capacity. We have temporarily suspended your transfer                                                                         |
|            -3145 |                    400 | Please DO NOT submit request too frequently                                                                         | We have detected the rate of your API request have been submitted too frequently. Please manage your API request.                                                        |
|            -4000 |                    400 | Invalid bank account number                                                                                         | Invalid bank account number                                                                                                                                              |
|            -4001 |                    400 | Invalid asset                                                                                                       | The asset specified is invalid                                                                                                                                           |
|            -4002 |                    400 | Withdrawal amount less than the minimum withdrawal amount                                                           | The withdrawal amount submitted is less than the minimum amount                                                                                                          |
|            -4003 |                    400 | Insufficient Balance                                                                                                | There was insufficient balance for the asset you are trying to withdraw                                                                                                  |
|            -4004 |                    400 | Invalid bank account number                                                                                         | The bank account has not been whitelisted yet                                                                                                                            |
|            -4005 |                    400 | Assets are not listed                                                                                               | Assets are not listed                                                                                                                                                    |
|            -4006 |                    400 | Kyc is not certified                                                                                                | The user has not passed KYC                                                                                                                                              |
|            -4007 |                    400 | Withdrawal channels are not supported                                                                               | The withdrawal channel is not yet supported via API                                                                                                                      |
|            -4008 |                    400 | This currency does not support this customer type                                                                   | The currency is not supported for the client type                                                                                                                        |
|            -4009 |                    400 | No withdrawal permission                                                                                            | The API Key do not have withdrawal permission                                                                                                                            |
|            -4010 |                    400 | Withdrawals on the same day exceed the maximum limit for a single day                                               | The withdrawal request exceeds the daily maximum limit                                                                                                                   |
|            -4011 |                    400 | System error                                                                                                        | The system has an internal error. Please contact our API Team                                                                                                            |
|            -4012 |                    400 | Parameter error                                                                                                     | The parameter entered was invalid                                                                                                                                        |
|            -4013 |                    400 | Withdraw repeatedly                                                                                                 | The withdrawal has been submitted multiple times. Please wait and try again                                                                                              |
|            -4014 |                    400 | The type of whitelist is invalid                                                                                    | The type of whitelist is invalid                                                                                                                                         |
|            -4016 |                    400 | twoFaToken missing. Please send valid twoFaToken as 2FA is enabled for this action                                  | twoFaToken missing. Please send valid twoFaToken as 2FA is enabled for this action                                                                                       |
|            -4017 |                    400 | twoFaToken wrong, please send valid twoFaToken                                                                      | twoFaToken wrong, please send valid twoFaToken                                                                                                                           |
|            -4018 |                    400 | twoFaToken used before. Please wait and try again later                                                             | twoFaToken used before. Please wait and try again later                                                                                                                  |
|            -4019 |                    400 | The withdraw exceeded the predefined maximum limit, and has been rejected                                           | The withdraw exceeded the predefined maximum limit, and has been rejected                                                                                                |
|            -4020 |                    400 | The withdrawal happened during abnormal operation hours, and had been rejected                                      | The withdrawal happened during abnormal operation hours, and had been rejected                                                                                           |
|            -5000 |                    400 | Duplicate IN-KIND subscription order                                                                                | Duplicate IN-KIND subscription order                                                                                                                                     |
|            -5001 |                    400 | Fund code is invalid                                                                                                | Fund code is invalid                                                                                                                                                     |
|            -5002 |                    400 | Deposit address does not exist                                                                                      | Deposit address does not exist                                                                                                                                           |
|            -5003 |                    400 | Invalid address. Please verify                                                                                      | Invalid address. Please verify                                                                                                                                           |
|            -5004 |                    400 | Signature verification failed because the address had been whitelisted by another account.                          | Signature verification failed because the address had been whitelisted by another account.                                                                               |
|            -5005 |                    400 | Signature verification fails because client submits incorrect signature result.                                     | Signature verification fails because client submits incorrect signature result.                                                                                          |
|            -5006 |                    400 | Signature verification failed because the address had been whitelisted before.                                      | Signature verification failed because the address had been whitelisted before.                                                                                           |
|            -5011 |                    400 | No Subscription found.                                                                                              | No Subscription found.                                                                                                                                                   |
|            -5012 |                    400 | Unknown subscriptionId                                                                                              | Unknown subscriptionId                                                                                                                                                   |
|            -5013 |                    400 | Subscription failed.                                                                                                | Subscription failed.                                                                                                                                                     |
|            -5021 |                    400 | Only one of 'buyAmount' or 'sellAmount' must be specified.                                                          | Only one of 'buyAmount' or 'sellAmount' must be specified.                                                                                                               |
|            -5022 |                    400 | quoteId expired. Please get a quote again.                                                                          | quoteId expired. Please get a quote again.                                                                                                                               |
|            -5023 |                    400 | Insufficient Fund Position.                                                                                         | Insufficient Fund Position.                                                                                                                                              |
|            -5024 |                    400 | The amount is below the minimum required: 100 USD or equivalent USD.                                                | The amount is below the minimum required: 100 USD or equivalent USD.                                                                                                     |
|            -5025 |                    400 | Exceed the maximum buy amount.                                                                                      | Exceed the maximum buy amount.                                                                                                                                           |
|            -5026 |                    400 | Unsupported Quote Pair.                                                                                             | Unsupported Quote Pair.                                                                                                                                                  |
|            -5027 |                    400 | Invalid orderId: `%s` provided.                                                                                     | Invalid orderId: `%s` provided.                                                                                                                                          |
|            -5030 |                    400 | The Length of `%s` cannot exceed `%s`                                                                               | The Length of `%s` cannot exceed `%s`                                                                                                                                    |
|            -5031 |                    400 | Unsupported quote pair                                                                                              | Unsupported quote pair                                                                                                                                                   |
|            -5032 |                    400 | Precision illegal                                                                                                   | Precision illegal                                                                                                                                                        |
|            -5033 |                    400 | Precision illegal                                                                                                   | Precision illegal                                                                                                                                                        |
|            -5034 |                    400 | Fail to generate the clientOrderId                                                                                  | Fail to generate the clientOrderId                                                                                                                                       |
|            -5035 |                    400 | `%s`                                                                                                                | `%s`                                                                                                                                                                     |
|            -5036 |                    400 | `%s`                                                                                                                | `%s`                                                                                                                                                                     |
|            -6000 |                    400 | lpId invalid or access not granted                                                                                  | lpId invalid or access not granted                                                                                                                                       |
|            -6001 |                    400 | No enough asset in your account                                                                                     | No enough asset in your account                                                                                                                                          |
|            -6002 |                    400 | Quantity does not meet requirement                                                                                  | Quantity does not meet requirement                                                                                                                                       |
|            -6003 |                    400 | Quote pair not supported                                                                                            | Quote pair not supported                                                                                                                                                 |
|            -6004 |                    400 | rfqClOrderId not unique                                                                                             | rfqClOrderId not unique                                                                                                                                                  |
|            -6011 |                    400 | rfqId not exist or already expired                                                                                  | rfqId not exist or already expired                                                                                                                                       |
|            -6012 |                    400 | quoteId not exist or already expired                                                                                | quoteId not exist or already expired                                                                                                                                     |
|            -6013 |                    400 | accepted quote already expired, can not double confirm                                                              | accepted quote already expired, can not double confirm                                                                                                                   |
|            -6014 |                    400 | Risk exposure too high, please raise balance in your account                                                        | Risk exposure too high, please raise balance in your account                                                                                                             |
|            -6015 |                    400 | quoteClOrderId not unique                                                                                           | quoteClOrderId not unique                                                                                                                                                |
|            -6016 |                    400 | Self trade not allowed                                                                                              | Self trade not allowed                                                                                                                                                   |
|            -6017 |                    400 | You can only decline manual order                                                                                   | You can only decline manual order                                                                                                                                        |
|            -6018 |                    400 | No enough asset, can not confirm real-time order                                                                    | No enough asset, can not confirm real-time order                                                                                                                         |
|            -6019 |                    400 | accepted quote already double confirmed, can not re-confirm                                                         | accepted quote already double confirmed, can not re-confirm                                                                                                              |
|            -6020 |                    400 | Price outside of allowed range                                                                                      | Price outside of allowed range                                                                                                                                           |
|            -6021 |                    400 | The RFQ has already accepted quote, please check the latest status                                                  | The RFQ has already accepted quote, please check the latest status                                                                                                       |
|            -6022 |                    400 | Out of RFQ service hour                                                                                             | Out of RFQ service hour                                                                                                                                                  |
|            -6023 |                    400 | No permission for this quote pair                                                                                   | No permission for this quote pair                                                                                                                                        |
|            -6025 |                    400 | Insufficient balance to create quote for STO OPT order                                                              | Insufficient balance to create quote for STO OPT order                                                                                                                   |
|            -6100 |                    400 | User operation not allowed, please contact support                                                                  | User operation not allowed, please contact support                                                                                                                       |
|            -6101 |                    400 | Parameters sent not in valid range, please update accordingly                                                       | Parameters sent not in valid range, please update accordingly                                                                                                            |

### Cancel Reject Reasons

| Error Msg         | Error Msg ZH   | Memo                                                                                                                                                                                                    |
|-------------------|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SYSTEM_CANCEL     | 系统撤单(默认)       | Default Error Message. Also include scenes: Solicited Cancellation by System or Operation Staff.   默认的拒绝错误文案。也包括系统自动执行的或者运营人员执行的撤单操作。                                                                   |
| USER_CANCEL       | 客户自主撤单         | The customer initiates the order cancellation actively.   客户主动发起的撤单                                                                                                                                     |
| RISKLIMIT_CANCEL  | 风控撤单           | Covers order cancellations caused by trading rule restrictions (such as changes in risk-preference levels, IOC order situations, liquidity protection, etc.)   涵盖交易规则限制（如风险偏好等级变化、IOC 订单情况、流动性保护等）导致的撤单 |
| BLOCKED_CANCEL    | 账户禁用撤单         | Cancellation due to the account being disabled.   当账户被禁用时执行的撤单操作                                                                                                                                        |
| CLOSED_CANCEL     | 交易所闭市撤单        | Cancellation when the exchange closes urgently.   交易所因紧急情况闭市时进行的撤单                                                                                                                                      |
| OFFLINE_CANCEL    | 交易对下架撤单        | Cancellation when the trading pair is delisted.   交易对下架时进行的撤单操作                                                                                                                                         |
| SELF_TRADE_CANCEL | 自成交撤单          | Cancellation to avoid self-trade.   为避免自成交而进行的撤单                                                                                                                                                        |

# WEBSOCKET API

## Access URL

Python Public Stream Sample

```
import hashlib
import hmac
import json
import time
import websocket
import logging
import threading
########################################################################################################################
# Test Websocket API
# Copyright: Hashkey Trading 2023
########################################################################################################################
class WebSocketClient : def __init__ ( self ): self . _logger = logging . getLogger ( __name__ ) self . _ws = None self . _ping_thread = None def _on_message ( self , ws , message ): self . _logger . info ( f "Received message: { message } " ) data = json . loads ( message ) if "pong" in data : # Received a pong message from the server self . _logger . info ( "Received pong message" ) # Handle the received market data here def _on_error ( self , ws , error ): self . _logger . error ( f "WebSocket error: { error } " ) def _on_close ( self , ws ): self . _logger . info ( "Connection closed" ) def _on_open ( self , ws ): self . _logger . info ( "Subscribe topic" ) sub = { "symbol" : "BTCUSD" , "topic" : "trade" , "event" : "sub" , "site" : "MENA" , "params" : { "binary" : False }, "id" : 1 } ws . send ( json . dumps ( sub )) # Start the ping thread after connecting self . _start_ping_thread () def _start_ping_thread ( self ): def send_ping (): while self . _ws : ping_message = { "ping" : int ( time . time () * 1000 ) # Send a timestamp as the ping message } self . _ws . send ( json . dumps ( ping_message )) self . _logger . info ( f "Send ping message: { ping_message } " ) time . sleep ( 5 ) self . _ping_thread = threading . Thread ( target = send_ping ) self . _ping_thread . daemon = True self . _ping_thread . start () def unsubscribe ( self ): if self . _ws : self . _logger . info ( "Unsubscribe topic" ) unsub = { "symbol" : "BTCUSD" , "topic" : "trade" , "event" : "cancel" , "params" : { "binary" : False }, "id" : 1 } self . _ws . send ( json . dumps ( unsub )) def connect ( self ): base_url = 'wss://stream-pro.sim.hashkeydev.com' endpoint = 'quote/ws/v1' stream_url = f " { base_url } / { endpoint } " self . _logger . info ( stream_url ) self . _logger . info ( f "Connecting to { stream_url } " ) self . _ws = websocket . WebSocketApp ( stream_url , on_message = self . _on_message , on_error = self . _on_error , on_close = self . _on_close ) self . _ws . on_open = self . _on_open self . _ws . run_forever ()
if __name__ == '__main__' : logging . basicConfig ( level = logging . INFO ) client = WebSocketClient () client . connect ()
```

Python Private Stream Sample

```
import hashlib
import hmac
import json
import time
import websocket
import logging
import threading
import requests
import datetime
########################################################################################################################
# Test Websocket API
# Copyright: Hashkey Trading 2023
########################################################################################################################
class WebSocketClient : def __init__ ( self , user_key , user_secret , subed_topic = None ): if subed_topic is None : subed_topic = [] self . user_key = user_key self . user_secret = user_secret self . subed_topic = subed_topic self . listen_key = None self . _logger = logging . getLogger ( __name__ ) self . _ws = None self . _ping_thread = None self . last_listen_key_extend = time . time () def generate_listen_key ( self ): params = { 'timestamp' : int ( time . time () * 1000 ), } api_headers = { 'X-APIKEY' : self . user_key , 'content-type' : 'application/x-www-form-urlencoded;charset=UTF-8' , } signature = self . create_hmac256_signature ( secret_key = self . user_secret , params = params ) params . update ({ 'signature' : signature , }) response = requests . post ( url = f "/api/v1/userDataStream" , headers = api_headers , data = params ) data = response . json () if 'listenKey' in data : self . listen_key = data [ 'listenKey' ] self . _logger . info ( f "Generated listen key: { self . listen_key } " ) else : raise Exception ( "Failed to generate listen key" ) def extend_listenKey_timeLimit ( self ): params = { 'timestamp' : int ( time . time () * 1000 ), 'listenKey' : self . listen_key , } api_headers = { 'X-APIKEY' : self . user_key , 'content-type' : 'application/x-www-form-urlencoded;charset=UTF-8' , } signature = self . create_hmac256_signature ( secret_key = self . user_secret , params = params ) params . update ({ 'signature' : signature , }) response = requests . put ( url = f "/api/v1/userDataStream" , headers = api_headers , data = params ) if response . status_code == 200 : self . _logger . info ( "Successfully extended listen key validity." ) else : self . _logger . error ( "Failed to extend listen key validity." ) def create_hmac256_signature ( self , secret_key , params , data = "" ): for k , v in params . items (): data = data + str ( k ) + "=" + str ( v ) + "&" signature = hmac . new ( secret_key . encode (), data [: - 1 ]. encode (), digestmod = hashlib . sha256 ). hexdigest () return signature def _on_message ( self , ws , message ): current_time = datetime . datetime . now (). strftime ( "%Y-%m-%d %H:%M:%S.%f" ) self . _logger . info ( f " { current_time } - Received message: { message } " ) data = json . loads ( message ) if "pong" in data : self . _logger . info ( "Received pong message" ) # Handle other messages here def _on_error ( self , ws , error ): self . _logger . error ( f "WebSocket error: { error } " ) def _on_close ( self , ws ): self . _logger . info ( "Connection closed" ) def _on_open ( self , ws ): self . _logger . info ( "Subscribing to topics" ) for topic in self . subed_topic : sub = { "symbol" : "BTCUSD" , "topic" : topic , "event" : "sub" , "params" : { "limit" : "100" , "binary" : False }, "id" : 1 } ws . send ( json . dumps ( sub )) self . _start_ping_thread () def _start_ping_thread ( self ): def send_ping (): while self . _ws : current_time = time . time () if current_time - self . last_listen_key_extend > 1800 : # Extend listen key every 30 minutes self . extend_listenKey_timeLimit () self . last_listen_key_extend = current_time ping_message = { "ping" : int ( time . time () * 1000 )} self . _ws . send ( json . dumps ( ping_message )) self . _logger . info ( f "Sent ping message: { ping_message } " ) time . sleep ( 5 ) self . _ping_thread = threading . Thread ( target = send_ping ) self . _ping_thread . daemon = True self . _ping_thread . start () def unsubscribe ( self ): if self . _ws : self . _logger . info ( "Unsubscribing from topics" ) for topic in self . subed_topic : unsub = { "symbol" : "BTCUSD" , "topic" : topic , "event" : "cancel_all" , "params" : { "limit" : "100" , "binary" : False }, "id" : 1 } self . _ws . send ( json . dumps ( unsub )) def connect ( self ): if not self . listen_key : self . generate_listen_key () base_url = 'wss://stream-pro.sim.hashkeydev.com' endpoint = f 'api/v1/ws/ { self . listen_key } ' stream_url = f " { base_url } / { endpoint } " self . _logger . info ( f "Connecting to { stream_url } " ) self . _ws = websocket . WebSocketApp ( stream_url , on_message = self . _on_message , on_error = self . _on_error , on_close = self . _on_close ) self . _ws . on_open = self . _on_open self . _ws . run_forever ()
if __name__ == '__main__' : logging . basicConfig ( level = logging . INFO ) user_key = "YOUR_USER_KEY" user_secret = "YOUR_USER_SECRET" subed_topics = [ "trade" ] client = WebSocketClient ( user_key , user_secret , subed_topics ) client . connect ()
```

**Sandbox Environment**

- MarketData public stream V1: `wss://stream-pro.sim.hashkeydev.com/quote/ws/v1`
- MarketData public stream V2: `wss://stream-pro.sim.hashkeydev.com/quote/ws/v2`
- MarketPlace public stream: `wss://stream-pro.sim.hashkeydev.com/mp/ws/v1`
- Private stream: `wss://stream-pro.sim.hashkeydev.com/api/v1/ws/{listenKey}`

**Production Environment**

- MarketData public stream V1: `wss://stream-pro.hashkey.com/quote/ws/v1`
- MarketData public stream V2: `wss://stream-pro.hashkey.com/quote/ws/v2`
- MarketPlace public stream: `wss://stream-pro.hashkey.com/mp/ws/v1`
- Private stream: `wss://stream-pro.hashkey.com/api/v1/ws/{listenKey}`

**Note:** Replace `{listenKey}` with your actual listen key obtained from the [Obtain ListenKey](#Create-Listen-Key) .

**For example in Postman, you can test our websocket in steps:**

1. Create a new request and select Websocket
<!-- 🖼️❌ Image not available. Please use `PdfPipelineOptions(generate_picture_images=True)` -->
2. Input `wss://stream-pro.sim.hashkeydev.com/quote/ws/v1` or `wss://stream-pro.sim.hashkeydev.com/api/v1/ws/{listenKey}` and click "Connect"
<!-- 🖼️❌ Image not available. Please use `PdfPipelineOptions(generate_picture_images=True)` -->

## Heartbeat check

### PublicStream Heartbeat

Ping message format is as follows:

```
// From Sent by the user
{ " ping " : 1748503859938
}
```

Pong message format is as follows:

```
// Public Stream, return server's timestamp
{ " pong " : 1748503865406
}
```

When a user's websocket client application successfully connects to HashKey websocket server, the client is recommended to initiate a periodic heartbeat message (ping message) every 10 seconds, which is used to keep alive the connection.

### PrivateStream Heartbeat

```
// From Websocket Server
{ " ping " : 1748504490208 , " channelId " : " 02ac86fffe5fdf52-00000001-00266eb0-74a37ad40fb20d81-0cda790b "
}
// Respond from client
{ " pong " : 1748504490208
}
```

**Automatic disconnection mechanism (Only for Private Stream)**

The websocket server will send a ping message every 30 seconds. We recommend clients respond with a pong message containing the same timestamp. It's not necessary to include the channelId. A mismatched pong timestamp will not affect the connection - we mainly care about receiving the pong itself, which indicates the connection is alive. (This mechanism is primarily used for internal latency calculation and statistics.) If the client has no heartbeat activity for 60 minutes, the session will be closed by the server.

## Public Market Data Stream

### V1

**Use Public stream V1**

- Sandbox: `wss://stream-pro.sim.hashkeydev.com/quote/ws/v1`
- Production: `wss://stream-pro.hashkey.com/quote/ws/v1`

#### Kline

Request Example:

```
{ "symbol" : "BTCUSDT" , "topic" : "kline_1m" , "event" : "sub" , "site" : "MENA" , "params" : { "binary" : false }
}
```

Response content:

```
{ "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "topic" : "kline" , "params" : { "realtimeInterval" : "24h" , "klineType" : "1m" , "binary" : "false" }, "data" : [ { "t" : 1766727660000 , "s" : "BTCUSDT" , "sn" : "BTCUSDT" , "c" : "88888.01" , "h" : "88888.01" , "l" : "88888.01" , "o" : "88888.01" , "v" : "0" , "et" : 0 , "qv" : "0" , "td" : 0 , "tb" : "0" , "tq" : "0" } ], "f" : true , "sendTime" : 1766727675969 , "shared" : false , "site" : "mena"
}
```

Update frequency: 300ms

**Subscription parameters:**

`topic` is a pattern like `kline_$interval` , interval could be:

- `1m` - 1 minute
- `3m` - 3 minutes
- `5m` - 5 minutes
- `15m` - 15 minutes
- `30m` - 30 minutes
- `1h` - 1 hour
- `2h` - 2 hours
- `4h` - 4 hours
- `6h` - 6 hours
- `8h` - 8 hours
- `12h` - 12 hours
- `1d` - 1 day
- `1w` - 1 week
- `1M` - 1 month

| **PARAMETER**   | **TYPE**    | Req'd   | **Example values**   | **DESCRIPTION**                                                             |
|-----------------|-------------|---------|----------------------|-----------------------------------------------------------------------------|
| symbol          | STRING      | Y       | BTCUSDT              | Name of currency pair                                                       |
| topic           | STRING      | Y       | kline_1m             | Topic name                                                                  |
| event           | STRING      | Y       | sub                  | Event type                                                                  |
| params          | JSON Object | Y       |                      | Request expanded parameters                                                 |
| params.binary   | BOOLEAN     | Y       | false                | True will return zip binary file                                            |
| site            | STRING      | N       | MENA                 | Optional. Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**WS Push Demo**

| **PARAMETER**           | **TYPE**         | **Example values**   | **DESCRIPTION**                      |
|-------------------------|------------------|----------------------|--------------------------------------|
| symbol                  | STRING           | BTCUSDT              | Currency pair ID                     |
| symbolName              | STRING           | BTCUSDT              | Currency pair name                   |
| topic                   | STRING           | kline                | Topic name                           |
| params                  | JSON Object      |                      | Request expanded parameters          |
| params.realtimeInterval | STRING           | 24h                  | Time period, only support 24h        |
| params.klineType        | STRING           | 1m                   | Kline Type                           |
| params.binary           | STRING           | false                | Whether it is a binary type          |
| data                    | JSON Array       |                      | Return data                          |
| data.t                  | LONG             | 1688199660000        | Timestamp in Milliseconds            |
| data.s                  | STRING           | BTCUSDT              | Currency pair ID                     |
| data.sn                 | STRING           | BTCUSDT              | Currency pair name                   |
| data.c                  | STRING           | 10002                | Close price                          |
| data.h                  | STRING           | 10002                | High price                           |
| data.l                  | STRING           | 10002                | Low price                            |
| data.o                  | STRING           | 10002                | Open price                           |
| data.v                  | STRING           | 0                    | Base Asset Volume                    |
| data.et                 | INTEGER          | 0                    | Closing timestamp                    |
| data.qv                 | STRING (decimal) | 927.9672557          | Quote Asset Volume                   |
| data.td                 | INTEGER          | 4                    | Number of Trades                     |
| data.tb                 | STRING (decimal) | 0.00045              | Taker buy base asset volume          |
| data.tq                 | STRING (decimal) | 39.2087177           | Taker buy quote asset volume         |
| f                       | BOOLEAN          | true                 | Whether it is the first return value |
| sendTime                | LONG             | 1688199337756        | Timestamp in milliseconds            |
| shared                  | BOOLEAN          | false                | Whether to share (No longer in use)  |
| site                    | STRING           | mena                 | Market site. Enum: `hk` , `mena`     |

#### Realtimes

Request Example:

```
{ "symbol" : "BTCUSDT" , "topic" : "realtimes" , "event" : "sub" , "site" : "MENA" , "params" : { "binary" : false }
}
```

Response content:

```
{ "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "topic" : "realtimes" , "params" : { "realtimeInterval" : "24h" , "binary" : "false" }, "data" : [ { "t" : 1764598623773 , "s" : "BTCUSDT" , "sn" : "BTCUSDT" , "c" : "86127.13" , "h" : "91854.4" , "l" : "84834.68" , "o" : "91592.99" , "v" : "23.90583" , "qv" : "2071254.823793" , "m" : "-0.0597" , "e" : 301 } ], "f" : false , "sendTime" : 1764598623952 , "shared" : false , "site" : "mena"
}
```

Update frequency: 500ms

**Subscription parameters:**

| **PARAMETER**   | **TYPE**    | Req'd   | **Example values**   | **DESCRIPTION**                                                             |
|-----------------|-------------|---------|----------------------|-----------------------------------------------------------------------------|
| symbol          | STRING      | Y       | BTCUSDT              | Currency pair                                                               |
| topic           | STRING      | Y       | realtimes            | Topic name, default: "realtimes"                                            |
| event           | STRING      | Y       | sub                  | Event Type                                                                  |
| params          | JSON Object | Y       |                      | Request expanded parameters                                                 |
| params.binary   | BOOLEAN     | Y       | false                | True will return zip binary file                                            |
| site            | STRING      | N       | MENA                 | Optional. Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**WS Push Demo**

| **PARAMETER**           | **TYPE**    | **Example values**   | **DESCRIPTION**                      |
|-------------------------|-------------|----------------------|--------------------------------------|
| symbol                  | STRING      | BTCUSDT              | Currency pair ID                     |
| symbolName              | STRING      | BTCUSDT              | Currency pair name                   |
| topic                   | STRING      | realtimes            | Topic name                           |
| params                  | JSON Object |                      | Request expanded parameter           |
| params.realtimeInterval | STRING      | 24h                  | Time period                          |
| params.binary           | STRING      | false                | Whether it is a binary type          |
| data                    | JSON Array  |                      | Return data                          |
| data.t                  | LONG        | 1688199300011        | Timestamp in Milliseconds            |
| data.s                  | STRING      | BTCUSDT              | Currency pair ID                     |
| data.sn                 | STRING      | BTCUSDT              | Currency pair name                   |
| data.c                  | STRING      | 10002                | Close price                          |
| data.h                  | STRING      | 10002                | High price                           |
| data.l                  | STRING      | 10002                | Low price                            |
| data.o                  | STRING      | 10002                | Open price                           |
| data.v                  | STRING      | 0                    | Volume (in base currency)            |
| data.qv                 | STRING      | 0                    | Volume(in quote currency)            |
| data.m                  | STRING      | 0                    | 24H range                            |
| data.e                  | INT64       | 301                  | Exchange ID                          |
| f                       | BOOLEAN     | true                 | Whether it is the first return value |
| sendTime                | LONG        | 1688199337756        | Timestamp in milliseconds            |
| shared                  | BOOLEAN     | false                | Whether to share (No longer in use)  |
| site                    | STRING      | mena                 | Market site. Enum: `hk` , `mena`     |

#### Trade

Request Example:

```
{ "symbol" : "BTCUSDT" , "topic" : "trade" , "event" : "sub" , "site" : "MENA" , "params" : { "binary" : false }
}
```

Response content:

```
{ "symbol" : "BTCUSDT" , "symbolName" : "BTCUSDT" , "topic" : "trade" , "params" : { "realtimeInterval" : "24h" , "binary" : "false" }, "data" : [ { "v" : "4620696243481038848" , "t" : 1764598927887 , "p" : "86101.4" , "q" : "0.00314" , "m" : false } ], "f" : false , "sendTime" : 1764598928016 , "shared" : false , "site" : "mena"
}
```

Upon successful subscription to our WebSocket API, you will receive an update of the most recent 60 trades for the symbol pair subscribed.

Update frequency: 300ms

**Subscription parameters:**

| **PARAMETER**   | **TYPE**    | Req'd   | **Example values**   | **DESCRIPTION**                                                             |
|-----------------|-------------|---------|----------------------|-----------------------------------------------------------------------------|
| symbol          | STRING      | Y       | BTCUSDT              | Currency pair                                                               |
| topic           | STRING      | Y       | trade                | Topic name, default: "trade"                                                |
| event           | STRING      | Y       | sub                  | Event type                                                                  |
| params          | JSON Object | Y       |                      | Request expanded parameters                                                 |
| params.binary   | BOOLEAN     | Y       | false                | True will return zip binary file                                            |
| site            | STRING      | N       | MENA                 | Optional. Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**WS Push Demo**

| **PARAMETER**           | **TYPE**    | **Example values**   | **DESCRIPTION**                                             |
|-------------------------|-------------|----------------------|-------------------------------------------------------------|
| symbol                  | STRING      | BTCUSDT              | Currency pair ID                                            |
| symbol                  | STRING      | BTCUSDT              | Currency pair name                                          |
| topic                   | STRING      | trade                | Topic name                                                  |
| params                  | JSON Object |                      | Request expanded parameters                                 |
| params.realtimeInterval | STRING      | 24h                  | Time period                                                 |
| params.binary           | BOOLEAN     | false                | Whether it is a binary type                                 |
| data                    | JSON Array  |                      | Return data                                                 |
| data.v                  | STRING      | 1447335405363150849  | Transaction record ID                                       |
| data.t                  | STRING      | 1687271825415        | Timestamp corresponding to transaction time in milliseconds |
| data.p                  | STRING      | 10001                | Traded price                                                |
| data.q                  | STRING      | 0.001                | Traded quantity                                             |
| data.m                  | STRING      | false                | isMaker (true: maker, false: taker)                         |
| f                       | BOOLEAN     | true                 | Whether it is the first return value                        |
| sendTime                | LONG        | 1688199337756        | Timestamp in milliseconds                                   |
| shared                  | BOOLEAN     | false                | Whether to share (No longer in use)                         |
| site                    | STRING      | mena                 | Market site. Enum: `hk` , `mena`                            |

#### Depth

Request Example:

```
{ "symbol" : "BTCUSD" , "topic" : "depth" , "event" : "sub" , "site" : "MENA" , "params" : { "binary" : false }
}
```

```
{ "symbol" : "BTCUSD" , "topic" : "mergedDepth" , "event" : "sub" , "site" : "MENA" , "params" : { "dumpScale" : 2 }
}
```

Response content:

```
{ "symbol" : "BTCUSD" , "symbolName" : "BTCUSD" , "topic" : "depth" , "params" : { "realtimeInterval" : "24h" , "binary" : "false" }, "data" : [ { "e" : 301 , "s" : "BTCUSD" , "t" : 1788838692240 , "v" : "1811627276_18" , "b" : [ [ "78924.09" , "0.78641" ], [ "78920.98" , "2.13771" ] ], "a" : [ [ "78924.1" , "6.75267" ], [ "78924.99" , "0.7864" ] ], "o" : 0 } ], "f" : true , "sendTime" : 1788838692794 , "channelId" : "027d87fffe05ad9d-00000001-001e8de0-e8cc19537084d667-76ea8e82" , "shared" : false , "site" : "mena"
}
```

Request the depth of the order book, can request up to limit of 200. Aggregated depth: `mergedDepth` (full snapshot each push) and `diffMergedDepth` (incremental; first push is a full snapshot). Precision is controlled by `params.dumpScale` .

Update frequency: 300ms

**Subscription parameters:**

| **PARAMETER**    | **TYPE**    | Req'd   | **Example values**   | **DESCRIPTION**                                                                                                                                                                                                                                                    |
|------------------|-------------|---------|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol           | STRING      | Y       | BTCUSD               | Currency pair                                                                                                                                                                                                                                                      |
| topic            | STRING      | Y       | depth                | Topic name. `depth` : order book. `mergedDepth` : full aggregated depth. `diffMergedDepth` : incremental aggregated depth (first push is a full snapshot).                                                                                                         |
| event            | STRING      | Y       | sub                  | Event type                                                                                                                                                                                                                                                         |
| params           | JSON Object | Y       |                      | Request expanded parameters                                                                                                                                                                                                                                        |
| params.binary    | BOOLEAN     | N       | false                | True will return zip binary file                                                                                                                                                                                                                                   |
| params.dumpScale | INTEGER     | N       | 2                    | Aggregation precision for `mergedDepth` / `diffMergedDepth` . Positive values map to decimal places ( `2` = `0.01` ). Negative values aggregate to integers ( `-1` = `1` , `-2` = `10` ). Default is the maximum number of decimal places supported by the symbol. |
| site             | STRING      | N       | MENA                 | Optional. Market site. Enum: `MENA` , `HK` . Default `HK` if not specified.                                                                                                                                                                                        |

**WS Push Demo**

| **PARAMETER**           | **TYPE**    | **Example values**                                           | **DESCRIPTION**                                                                                                                                    |
|-------------------------|-------------|--------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol                  | STRING      | BTCUSD                                                       | Currency pair                                                                                                                                      |
| symbolName              | STRING      | BTCUSD                                                       | Currency pair name                                                                                                                                 |
| topic                   | STRING      | depth                                                        | Topic name. `depth` / `mergedDepth` / `diffMergedDepth`                                                                                            |
| params                  | JSON Object |                                                              | Echoed subscription parameters                                                                                                                     |
| params.realtimeInterval | STRING      | 24h                                                          | Time period                                                                                                                                        |
| params.binary           | STRING      | false                                                        | Whether it is a binary type. Echoed when `binary` is sent in the subscription                                                                      |
| params.dumpScale        | STRING      | 2                                                            | Present for `mergedDepth` / `diffMergedDepth` . Echo of the subscribed scale                                                                       |
| data                    | JSON Array  |                                                              | Return data                                                                                                                                        |
| data.e                  | INT64       | 301                                                          | Exchange ID                                                                                                                                        |
| data.s                  | STRING      | BTCUSD                                                       | Currency pair. Present on snapshot pushes; omitted on subsequent `diffMergedDepth` increments                                                      |
| data.t                  | LONG        | 1788838692240                                                | Timestamp in milliseconds (data time)                                                                                                              |
| data.v                  | STRING      | 1811627276_18                                                | Version string                                                                                                                                     |
| data.o                  | INT64       | 0                                                            | `0` on snapshot ( `depth` , `mergedDepth` , first `diffMergedDepth` ). Subsequent `diffMergedDepth` pushes use an increasing sequence number       |
| data.a                  | JSON Array  | ["78924.1", "6.75267"]                                       | Ask price and quantity. For `diffMergedDepth` increments, only changed levels are included; quantity `0` removes the price level                   |
| data.b                  | JSON Array  | ["78924.09", "0.78641"]                                      | Bid price and quantity. For `diffMergedDepth` increments, only changed levels are included; quantity `0` removes the price level. Side may be `[]` |
| f                       | BOOLEAN     | true                                                         | `true` on the first push after subscribe; `false` afterwards. For `diffMergedDepth` , the first push is a full snapshot                            |
| sendTime                | LONG        | 1788838692794                                                | Timestamp in milliseconds                                                                                                                          |
| channelId               | STRING      | 027d87fffe05ad9d-00000001-001e8de0-e8cc19537084d667-76ea8e82 | Connection channel ID                                                                                                                              |
| shared                  | BOOLEAN     | false                                                        | Whether to share (No longer in use)                                                                                                                |
| site                    | STRING      | mena                                                         | Market site. Enum: `hk` , `mena`                                                                                                                   |

### V2

**Use Public stream V2**

- Sandbox: `wss://stream-pro.sim.hashkeydev.com/quote/ws/v2`
- Production: `wss://stream-pro.hashkey.com/quote/ws/v2`

#### Kline

Request Example:

```
{ "topic" : "kline" , "event" : "sub" , "site" : "MENA" , "params" :{ "symbol" : "BTCUSDT" , "klineType" : "1m" }
}
```

Response content:

```
{ "site" : "mena" , "topic" : "kline" , "params" : { "symbol" : "BTCUSDT" , "klineType" : "1m" }, "data" : { "t" : 1766728080000 , "s" : "BTCUSDT" , "sn" : "BTCUSDT" , "c" : "88947.71" , "h" : "88947.71" , "l" : "88947.71" , "o" : "88947.71" , "v" : "0" }
}
```

Update frequency: Real-time push

**Subscription parameters:**

`klineType` could be:

- `1m` - 1 minute
- `3m` - 3 minutes
- `5m` - 5 minutes
- `15m` - 15 minutes
- `30m` - 30 minutes
- `1h` - 1 hour
- `2h` - 2 hours
- `4h` - 4 hours
- `6h` - 6 hours
- `8h` - 8 hours
- `12h` - 12 hours
- `1d` - 1 day
- `1w` - 1 week
- `1M` - 1 month

| **PARAMETER**    | **TYPE**   | **Req'd**   | **Example**   | **DESCRIPTION**                                                             |
|------------------|------------|-------------|---------------|-----------------------------------------------------------------------------|
| topic            | STRING     | Y           | kline         | Topic for "kline" data push                                                 |
| event            | STRING     | Y           | sub           | Subscribe ("sub") or Unsubscribe ("cancel")                                 |
| params           | DICTIONARY | Y           |               | Request Parameters                                                          |
| params.symbol    | STRING     | Y           | ETHUSDT       | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information)     |
| params.klineType | STRING     | Y           | 1m            | Type of Kline.                                                              |
| site             | STRING     | N           | MENA          | Optional. Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**WS Push Demo**

| **PARAMETER**   | **TYPE**         | **Example**   | **DESCRIPTION**                                                         |
|-----------------|------------------|---------------|-------------------------------------------------------------------------|
| topic           | STRING           | kline         | Topic for "kline" data push                                             |
| params          | DICTIONARY       |               | Request Parameters                                                      |
| `>` symbol      | STRING           | ETHUSDT       | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information) |
| `>` klineType   | STRING           | 1m            | Type of Kline                                                           |
| data            | DICTIONARY       |               | WS Push Contenet Data                                                   |
| `>` t           | LONG             | 1730100300000 | Data Time (milisecond)                                                  |
| `>` s           | STRING           | ETHUSDT       | Trading Pair                                                            |
| `>` sn          | STRING           | ETHUSDT       | Trading Pair Name                                                       |
| `>` c           | STRING (decimal) | 1803.02       | close                                                                   |
| `>` h           | STRING (decimal) | 1806.97       | high                                                                    |
| `>` l           | STRING (decimal) | 1803.02       | low                                                                     |
| `>` o           | STRING (decimal) | 1806.07       | open                                                                    |
| `>` v           | STRING (decimal) | 0.075         | Total traded base asset volume                                          |
| site            | STRING           | mena          | Market site. Enum: `hk` , `mena`                                        |

#### Realtimes

Request Example:

```
{ "topic" : "realtimes" , "event" : "sub" , "site" : "MENA" , "params" :{ "symbol" : "BTCUSDT" }
}
```

Response content:

```
{ "site" : "mena" , "topic" : "realtimes" , "params" : { "symbol" : "BTCUSDT" }, "data" : { "t" : 1766728440004 , "s" : "BTCUSDT" , "o" : "87740.12" , "h" : "89270.33" , "l" : "86971.82" , "c" : "88910.23" , "v" : "0.20041" , "qv" : "17621.0846565" , "m" : "0.0133" }
}
```

Update frequency: Real-time push

**Subscription parameters:**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example**   | **DESCRIPTION**                                                             |
|-----------------|------------|-------------|---------------|-----------------------------------------------------------------------------|
| topic           | STRING     | Y           | realtimes     | Topic for "realtimes" data push                                             |
| event           | STRING     | Y           | sub           | Subscribe ("sub") or Unsubscribe ("cancel")                                 |
| params          | DICTIONARY | Y           |               | Request Parameters                                                          |
| params.symbol   | STRING     | Y           | ETHUSDT       | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information)     |
| site            | STRING     | N           | MENA          | Optional. Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**WS Push Demo**

| **PARAMETER**   | **TYPE**         | **Example**   | **DESCRIPTION**                                                         |
|-----------------|------------------|---------------|-------------------------------------------------------------------------|
| topic           | STRING           | realtimes     | Topic for "realtimes" data push                                         |
| params          | DICTIONARY       | -             | Request Parameters                                                      |
| `>` symbol      | STRING           | ETHUSDT       | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information) |
| data            | DICTIONARY       | -             | WS Push Content Data                                                    |
| `>` t           | LONG             | 1730100239050 | Data Time (milisecond)                                                  |
| `>` s           | STRING           | ETHUSDT       | Trading Pair                                                            |
| `>` o           | STRING (decimal) | 1808.48       | Open price                                                              |
| `>` h           | STRING (decimal) | 1808.48       | High price                                                              |
| `>` l           | STRING (decimal) | 1803.02       | Low price                                                               |
| `>` c           | STRING (decimal) | 1806.62       | Close price                                                             |
| `>` v           | STRING (decimal) | 0.247         | Volume (in base currency)                                               |
| `>` qv          | STRING (decimal) | 445.91714     | Volume(in quote currency)                                               |
| `>` m           | STRING (decimal) | 0.0105        | 24H range                                                               |
| site            | STRING           | mena          | Market site. Enum: `hk` , `mena`                                        |

#### Trade

Request Example:

```
{ "topic" : "trade" , "event" : "sub" , "site" : "MENA" , "params" :{ "symbol" : "ETHUSDT" }
}
```

Response content:

```
{ "site" : "mena" , "topic" : "trade" , "params" : { "symbol" : "ETHUSDT" }, "data" : { "v" : "4645465192627367936" , "t" : 1766728952350 , "p" : "2974.53" , "q" : "0.0089" , "m" : false }
}
```

Update frequency: Real-time push

**Subscription parameters:**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example**   | **DESCRIPTION**                                                             |
|-----------------|------------|-------------|---------------|-----------------------------------------------------------------------------|
| topic           | STRING     | Y           | trade         | Topic for "trade" data push                                                 |
| event           | STRING     | Y           | sub           | Subscribe ("sub") or Unsubscribe ("cancel")                                 |
| params          | DICTIONARY | Y           |               | Request Parameters                                                          |
| params.symbol   | STRING     | Y           | ETHUSDT       | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information)     |
| site            | STRING     | N           | MENA          | Optional. Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**WS Push Demo**

| **PARAMETER**   | **TYPE**         | **Example**         | **DESCRIPTION**                                                         |
|-----------------|------------------|---------------------|-------------------------------------------------------------------------|
| topic           | STRING           | trade               | Topic for "trade" data push                                             |
| params          | DICTIONARY       | -                   | Request Parameters                                                      |
| `>` symbol      | STRING           | ETHUSDT             | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information) |
| data            | DICTIONARY       | -                   | WS Push Content Data                                                    |
| `>` v           | STRING           | 4620696263626366976 | Transaction record ID                                                   |
| `>` t           | LONG             | 1730100239050       | Data Time (milisecond)                                                  |
| `>` p           | STRING (decimal) | ETHUSDT             | Traded price                                                            |
| `>` q           | STRING (decimal) | 1808.48             | Traded quantity                                                         |
| `>` m           | BOOLEAN          | true                | true: buyer is the maker   false: buyer is the taker                    |
| site            | STRING           | mena                | Market site. Enum: `hk` , `mena`                                        |

#### Depth

Request Example:

```
{ "topic" : "depth" , "event" : "sub" , "site" : "MENA" , "params" :{ "symbol" : "BTCUSDT" }
}
```

Response content:

```
{ "site" : "mena" , "topic" : "depth" , "params" : { "symbol" : "BTCUSDT" }, "data" : { "s" : "BTCUSDT" , "t" : 1764659869550 , "v" : "735962141_2" , "b" : [ [ "86962.98" , "0.04215" ], [ "86961.35" , "0.00057" ] ], "a" : [ [ "86962.99" , "0.34497" ], [ "86963.94" , "0.00114" ] ] }
}
```

Update frequency: 100ms

**Subscription parameters:**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example**   | **DESCRIPTION**                                                             |
|-----------------|------------|-------------|---------------|-----------------------------------------------------------------------------|
| topic           | STRING     | Y           | depth         | Topic for "depth" data push                                                 |
| event           | STRING     | Y           | sub           | Subscribe ("sub") or Unsubscribe ("cancel")                                 |
| params          | DICTIONARY | Y           |               | Request Parameters                                                          |
| params.symbol   | STRING     | Y           | ETHUSDT       | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information)     |
| site            | STRING     | N           | MENA          | Optional. Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**WS Push Demo**

| **PARAMETER**   | **TYPE**   | **Example**          | **DESCRIPTION**                                                         |
|-----------------|------------|----------------------|-------------------------------------------------------------------------|
| topic           | STRING     | depth                | Topic for "depth" data push                                             |
| params          | DICTIONARY | -                    | Request Parameters                                                      |
| `>` symbol      | STRING     | -                    | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information) |
| data            | DICTIONARY | -                    | WS Push Contenet Data                                                   |
| `>` s           | STRING     | ETHUSDT              | Trading Pair                                                            |
| `>` t           | LONG       | 1730100300000        | Data Time (milisecond)                                                  |
| `>` v           | STRING     | 55834575325_3        | Message Version                                                         |
| `>` b           | JSON Array | ["0.704", "28.477"]  | Bid price and quantity                                                  |
| `>` a           | JSON Array | ["0.703", "46.671" ] | Ask price and quantity                                                  |
| site            | STRING     | mena                 | Market site. Enum: `hk` , `mena`                                        |

#### BBO

Request Example:

```
{ "topic" : "bbo" , "event" : "sub" , "site" : "MENA" , "params" :{ "symbol" : "ETHUSDT" }
}
```

Response content:

```
{ "site" : "mena" , "topic" : "bbo" , "params" : { "symbol" : "ETHUSDT" }, "data" : { "s" : "ETHUSDT" , "b" : "2974.52" , "bz" : "0.0202" , "a" : "2974.85" , "az" : "0.2838" , "t" : 1766729017183 }
}
```

Update frequency: Real-time push

**Subscription parameters:**

| **PARAMETER**   | **TYPE**   | **Req'd**   | **Example**   | **DESCRIPTION**                                                             |
|-----------------|------------|-------------|---------------|-----------------------------------------------------------------------------|
| topic           | STRING     | Y           | bbo           | Topic for "bbo" data push                                                   |
| event           | STRING     | Y           | sub           | Subscribe ("sub") or Unsubscribe ("cancel")                                 |
| params          | DICTIONARY | Y           |               | Request Parameters                                                          |
| params.symbol   | STRING     | Y           | ETHUSDT       | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information)     |
| site            | STRING     | N           | MENA          | Optional. Market site. Enum: `MENA` , `HK` . Default `HK` if not specified. |

**WS Push Demo**

| **PARAMETER**   | **TYPE**         | **Example**   | **DESCRIPTION**                                                         |
|-----------------|------------------|---------------|-------------------------------------------------------------------------|
| topic           | STRING           | bbo           | Topic for "bbo" data push                                               |
| params          | DICTIONARY       | -             | Request Parameters                                                      |
| `>` symbol      | STRING           | ETHUSDT       | Trading Pairs see [Get-Exchange-Information](#Get-Exchange-Information) |
| data            | DICTIONARY       | -             | WS Push Contenet Data                                                   |
| `>` s           | STRING           | ETHUSDT       | Trading Pair                                                            |
| `>` t           | LONG             | 1730100239050 | Data Time (milisecond)                                                  |
| `>` b           | STRING (decimal) | 1802.04       | Bid Price                                                               |
| `>` bz          | STRING (decimal) | 0.008         | Bid Quantity                                                            |
| `>` a           | STRING (decimal) | 1803.5        | Ask Price                                                               |
| `>` az          | STRING (decimal) | 0.001         | Ask Quantity                                                            |
| site            | STRING           | mena          | Market site. Enum: `hk` , `mena`                                        |

## User Data Stream

**Use Private stream**

- Sandbox: `wss://stream-pro.sim.hashkeydev.com/api/v1/ws/{listenKey}`
- Production: `wss://stream-pro.hashkey.com/api/v1/ws/{listenKey}`

**Note:** Replace `{listenKey}` with your actual listen key obtained from the [Obtain ListenKey](#Create-Listen-Key) .

### Account Update

```
[ { "e" : "outboundAccountInfo" , "E" : "1764932840383" , "T" : true , "W" : true , "D" : true , "B" : [ { "a" : "BTC" , "f" : "6086.715847759989968887" , "l" : "0" , "r" : "" } ] }
]
```

**Trading/Custody/Fiat/OPT Account update**

**WS Push Parameter**

| **PARAMETER**   | **TYPE**     | **Example Values**   | **DESCRIPTION**                                                                          |
|-----------------|--------------|----------------------|------------------------------------------------------------------------------------------|
| -               | Object Array |                      |                                                                                          |
| e               | STRING       | outboundAccountInfo  | Event type: `outboundAccountInfo` `outboundCustodyAccountInfo` `outboundFiatAccountInfo` |
| E               | STRING       | 1764932840383        | Event timeStamp                                                                          |
| T               | BOOLEAN      | true                 | can trade                                                                                |
| W               | BOOLEAN      | true                 | can withdraw                                                                             |
| D               | BOOLEAN      | true                 | can deposit                                                                              |
| B               | Object Array |                      |                                                                                          |
| &gt; `a`        | STRING       | BTC                  | asset                                                                                    |
| &gt; `f`        | STRING       | 6086.7               | free amount                                                                              |
| &gt; `l`        | STRING       | 0                    | locked amount                                                                            |
| &gt; `v`        | STRING       | 0                    | Voucher amount, will only return when amount > 0                                         |
| &gt; `r`        | STRING       |                      | remark                                                                                   |

```
[ { "e" : "outboundContractAccountInfo" , "E" : "1769069566346" , "T" : true , "W" : true , "D" : true , "B" : [ { "a" : "USD" , "t" : "4999777.908366280931145965" , "f" : "4995055.805095280931145965" , "r" : "" } ] }
]
```

**Futures Account update**

**WS Push Parameter**

| **PARAMETER**   | **TYPE**     | **Example Values**          | **DESCRIPTION**   |
|-----------------|--------------|-----------------------------|-------------------|
| -               | Object Array |                             |                   |
| e               | STRING       | outboundContractAccountInfo | Event type        |
| E               | STRING       | 1769069566346               | Event timeStamp   |
| T               | BOOLEAN      | true                        | can trade         |
| W               | BOOLEAN      | true                        | can withdraw      |
| D               | BOOLEAN      | true                        | can deposit       |
| B               | Object Array |                             |                   |
| &gt; `a`        | STRING       | USD                         | asset             |
| &gt; `t`        | STRING       | 4999777.908366280931145965  | total amount      |
| &gt; `f`        | STRING       | 4995055.805095280931145965  | free amount       |
| &gt; `r`        | STRING       |                             | remark            |

### Order Update

```
[ { "e" : "" , "E" : "1764935787849" , "s" : "ETHUSD" , "c" : "1764935787802434" , "S" : "SELL" , "o" : "MARKET_OF_BASE" , "f" : "IOC" , "q" : "0.01" , "p" : "0" , "X" : "NEW" , "i" : "2098827941690738688" , "M" : "0" , "l" : "0" , "z" : "0" , "L" : "0" , "n" : "0" , "F" : "0" , "N" : "" , "u" : true , "w" : true , "m" : false , "O" : "1764935787818" , "U" : "1764935787818" , "Z" : "0" , "A" : "2232682771796522222" , "C" : false , "v" : "0" , "reqAmt" : "0" , "d" : "" , "r" : "0.01" , "V" : "0" , "x" : "" , "rt" : "taker" , "T" : "123456789" }, { "e" : "executionReport" , "E" : "1764935787849" , "s" : "ETHUSD" , "c" : "1764935787802434" , "S" : "SELL" , "o" : "MARKET_OF_BASE" , "f" : "IOC" , "q" : "0.01" , "p" : "0" , "X" : "FILLED" , "i" : "2098827941690738688" , "M" : "0" , "l" : "0.01" , "z" : "0.01" , "L" : "3150.11" , "n" : "1.99" , "F" : "0" , "N" : "USD" , "u" : true , "w" : true , "m" : false , "O" : "1764935787818" , "U" : "1764935787823" , "Z" : "31.5011" , "A" : "2232682771796522222" , "C" : false , "v" : "0" , "reqAmt" : "0" , "d" : "2098827941783013377" , "r" : "0" , "V" : "3150.11" , "x" : "" , "rt" : "taker" , "T" : "123456789" }
]
```

**Spot Trading Execution Report**

**WS Push Parameter**

| **PARAMETER**   | **TYPE**     | **Example Values**   | **DESCRIPTION**                            |
|-----------------|--------------|----------------------|--------------------------------------------|
| -               | Object Array |                      |                                            |
| e               | STRING       | executionReport      | Execution Report                           |
| E               | STRING       | 1764936108760        | Event timeStamp                            |
| s               | STRING       | ETHUSD               | symbol                                     |
| c               | STRING       | 1764936108734433     | client order ID                            |
| S               | STRING       | SELL                 | side                                       |
| o               | STRING       | LIMIT                | order type                                 |
| f               | STRING       | GTC                  | time in force                              |
| q               | STRING       | 0.01                 | order quantity                             |
| p               | STRING       | 3150                 | order price                                |
| X               | STRING       | FILLED               | current order status                       |
| i               | STRING       | 2098830633787983872  | order ID                                   |
| M               | STRING       | 0                    | match order ID, ignore for now             |
| l               | STRING       | 0.01                 | last executed quantity                     |
| z               | STRING       | 0.01                 | cumulative filled quantity                 |
| L               | STRING       | 3150.11              | last executed price                        |
| n               | STRING       | 1.99                 | commission amount                          |
| F               | STRING       | 0                    | Fee rebill                                 |
| N               | STRING       | USD                  | commission asset                           |
| u               | BOOLEAN      | true                 | is the trade normal？ ignore for now        |
| w               | BOOLEAN      | true                 | is the order working? Stops will have      |
| m               | BOOLEAN      | false                | if the order is a limit maker order        |
| O               | STRING       | 1764936108741        | order creation time                        |
| U               | STRING       | 1764936108745        | order update time                          |
| Z               | STRING       | 31.5011              | cumulative quote asset transacted quantity |
| A               | STRING       | 0                    | match Account ID, ignore for now           |
| C               | BOOLEAN      | false                | is close, Is the buy close or sell close   |
| v               | STRING       | 0                    | leverage                                   |
| reqAmt          | STRING       | 0                    | requested cash amount                      |
| d               | STRING       | 2098830633863481345  | execution ID                               |
| r               | STRING       | 0                    | unfilled quantity                          |
| V               | STRING       | 3150.11              | average executed price                     |
| x               | STRING       |                      | order cancel reject reason                 |
| rt              | STRING       | taker                | role type                                  |
| T               | STRING       | 123456789            | ticket_id                                  |

```
[ { "e" : "contractExecutionReport" , "E" : "1769069566346" , "s" : "BTCUSD-PERPETUAL" , "c" : "0122test01" , "S" : "BUY" , "o" : "LIMIT" , "f" : "GTC" , "obq" : "0.001" , "p" : "89800" , "X" : "NEW" , "i" : "2133504589195380992" , "l" : "0" , "ebq" : "0" , "L" : "" , "n" : "0" , "N" : "" , "u" : true , "w" : true , "m" : false , "O" : "1769069566331" , "eqq" : "0" , "v" : "4" , "oqq" : "89.8" , "d" : "" , "r" : "0.001" , "V" : "0" , "lo" : false , "lt" : "" , "x" : "" , "rt" : "taker" , "T" : "123456789" }, { "e" : "contractExecutionReport" , "E" : "1769069566346" , "s" : "BTCUSD-PERPETUAL" , "c" : "0122test01" , "S" : "BUY" , "o" : "LIMIT" , "f" : "GTC" , "obq" : "0.001" , "p" : "89800" , "X" : "FILLED" , "i" : "2133504589195380992" , "l" : "0.001" , "ebq" : "0.001" , "L" : "89797.8" , "n" : "0.05387868" , "N" : "USD" , "u" : true , "w" : true , "m" : false , "O" : "1769069566331" , "eqq" : "89.7978" , "v" : "4" , "oqq" : "89.8" , "d" : "2133504589262489856" , "r" : "0" , "V" : "89797.8" , "lo" : false , "lt" : "" , "x" : "" , "rt" : "taker" , "T" : "123456789" }
]
```

**Futures Trading Execution Report**

**WS Push Parameter**

| **PARAMETER**   | **TYPE**     | **Example Values**      | **DESCRIPTION**                                                                      |
|-----------------|--------------|-------------------------|--------------------------------------------------------------------------------------|
| -               | Object Array |                         |                                                                                      |
| e               | STRING       | contractExecutionReport | Contract Execution Report                                                            |
| E               | STRING       | 1769069566346           | Event timeStamp                                                                      |
| s               | STRING       | BTCUSD-PERPETUAL        | symbol                                                                               |
| c               | STRING       | 1764936108734433        | client order ID                                                                      |
| S               | STRING       | SELL                    | side                                                                                 |
| o               | STRING       | LIMIT                   | order type                                                                           |
| f               | STRING       | GTC                     | time in force                                                                        |
| obq             | STRING       |                         | original base asset quantity                                                         |
| p               | STRING       | 3150                    | order price                                                                          |
| X               | STRING       | FILLED                  | current order status                                                                 |
| i               | STRING       | 2098830633787983872     | order ID                                                                             |
| l               | STRING       | 0.01                    | last executed quantity                                                               |
| ebq             | STRING       |                         | executed base asset quantity                                                         |
| L               | STRING       | 3150.11                 | last executed price                                                                  |
| n               | STRING       | 1.99                    | commission amount                                                                    |
| N               | STRING       | USD                     | commission asset                                                                     |
| u               | BOOLEAN      | true                    | is the trade normal？ ignore for now                                                  |
| w               | BOOLEAN      | true                    | is the order working? Stops will have                                                |
| m               | BOOLEAN      | false                   | if the order is a limit maker order                                                  |
| O               | STRING       | 1764936108741           | order creation time                                                                  |
| eqq             | STRING       |                         | executed quote asset quantity                                                        |
| v               | STRING       | 0                       | leverage                                                                             |
| oqq             | STRING       |                         | original quote asset quantity                                                        |
| d               | STRING       | 2098830633863481345     | execution ID                                                                         |
| r               | STRING       | 0                       | unfilled quantity                                                                    |
| V               | STRING       | 3150.11                 | average executed price                                                               |
| lo              | BOOLEAN      | true                    | Is liquidation Order                                                                 |
| lt              | STRING       | LIQUIDATION_MAKER       | Liquidation type `LIQUIDATION_MAKER_ADL` , `LIQUIDATION_MAKER` , `LIQUIDATION_TAKER` |
| x               | STRING       |                         | order cancel reject reason                                                           |
| rt              | STRING       | taker                   | role type                                                                            |
| T               | STRING       | 123456789               | ticket_id                                                                            |

### Ticket Push

```
[ { "e" : "ticketInfo" , "E" : "1764938485090" , "s" : "ETHUSD" , "q" : "0.10" , "t" : "1764938485085" , "p" : "3153.80" , "T" : "4629700489901088768" , "o" : "2098850567964329984" , "c" : "1764938485067417" , "O" : "0" , "a" : "1471090223379184384" , "A" : "0" , "m" : false , "S" : "BUY" }
]
```

**WS Push Parameter**

| **PARAMETER**   | **TYPE**     | **Example Values**   | **DESCRIPTION**                  |
|-----------------|--------------|----------------------|----------------------------------|
| -               | Object Array |                      |                                  |
| e               | STRING       | ticketInfo           |                                  |
| E               | STRING       | 1764936108760        | Event timeStamp                  |
| s               | STRING       | ETHUSD               | symbol                           |
| q               | STRING       | 0.01                 | order quantity                   |
| t               | STRING       | 1764938485085        | order matching time              |
| p               | STRING       | 3150                 | order price                      |
| T               | STRING       | 4629700489901088768  | ticketId                         |
| o               | STRING       | 2098850567964329984  | order ID                         |
| c               | STRING       | 1764938485067417     | clientOrderId                    |
| O               | STRING       | 0                    | match Order ID, ignore for now   |
| a               | STRING       | 1471090223379184384  | account ID                       |
| A               | STRING       | 0                    | match Account ID, ignore for now |
| m               | BOOLEAN      | false                | isMaker                          |
| S               | STRING       | BUY                  | side  SELL or BUY                |

### Position Push

```
[ { "e" : "outboundContractPositionInfo" , "E" : "1769069566346" , "A" : "2129188333171126016" , "s" : "BTCUSD-PERPETUAL" , "S" : "LONG" , "p" : "91444.6" , "P" : "0.196" , "f" : "0" , "m" : "4400.349" , "r" : "-236.80662126" , "up" : "-321.7542" , "pr" : "-0.0731" , "pv" : "17601.3962" , "v" : "4" , "mt" : "CROSS" }
]
```

**WS Push Parameter**

| **PARAMETER**   | **TYPE**     | **Example Values**           | **DESCRIPTION**                            |
|-----------------|--------------|------------------------------|--------------------------------------------|
| -               | Object Array |                              |                                            |
| e               | STRING       | outboundContractPositionInfo | Event Type                                 |
| E               | STRING       | 1764936108760                | Event timeStamp                            |
| A               | STRING       | 2129188333171126016          | Account ID                                 |
| s               | STRING       | BTCUSD-PERPETUAL             | symbol                                     |
| S               | STRING       | LONG                         | side, `LONG` or `SHORT`                    |
| p               | STRING       | 91444.6                      | avg Price                                  |
| P               | STRING       | 0.196                        | total position                             |
| f               | STRING       | 0                            | liquidation price                          |
| m               | STRING       | 4400.349                     | portfolio margin                           |
| r               | STRING       | -236.80662126                | realised profit and loss (Pnl)             |
| up              | STRING       | -321.7542                    | unrealized profit and loss (unrealizedPnL) |
| pr              | STRING       | -0.0731                      | profit rate of current position            |
| pv              | STRING       | 17601.3962                   | position value (USD)                       |
| v               | STRING       | 4                            | leverage                                   |
| mt              | STRING       | CROSS                        | position type                              |

## Market Place Stream

### Public Stream

**Use Public stream V1**

- Sandbox: `wss://stream-pro.sim.hashkeydev.com/mp/ws/v1`
- Production: `wss://stream-pro.hashkey.com/mp/ws/v1`

Request Example:

```
{ "event" : "SUBSCRIBE" , "topic" : "rfqs-mena"
}
```

**Subscription parameters:**

| Parameter   | Type   | Required   | Example value   | Description                                |
|-------------|--------|------------|-----------------|--------------------------------------------|
| event       | STRING | Y          |                 | `SUBSCRIBE` , `UNSUBSCRIBE sub` , `cancel` |
| topic       | STRING | Y          |                 | `rfqs-mena` , `quotes-mena`                |

**topic=** **`rfqs-mena`**

- Public channel, push all "new" RFQs
- newly created rfqs or rfqs becomes "new" again (like accepted quote expired before confirmation, the rfq will become "new")

```
{ "event" : "rfqCreated" , "topic" : "rfqs-mena" , "data" : { "rfqId" : "RFQ_123" , "buyCcy" : "BTC" , "sellCcy" : "USDT" , "buyAmount" : "2" , "sellAmount" : "" , "rfqMode" : "real-time" , "expire_time" : 1717410000 }
}
```

**topic=** **`quotes-mena`**

- Public channel, push all quotes once created

```
{ "event" : "quotesCreated" , "topic" : "quotes-mena" , "data" : { "quoteId" : "QUOTE_789456123" , "rfqId" : "RFQ638459562162049024" , "buyCcy" : "BTC" , "sellCcy" : "USDT" , "buyAmount" : "2" , "sellAmount" : "" , "price" : "68900" , "expireTime" : 1717394200 }
}
```

**WS Push Demo 👉**

### Private Stream

**topic=** **`bestQuote`**

- Push the best quote portfolio to the channel (if at least 3 valid quotations are met within 3s, or all valid quotes after 3s)
- Only list the latest quote from each LP
- Ranking principle: rfqMode &gt; Price &gt; quote time

```
{ "topic" : "bestQuote" , "data" : [ { "id" : 9 , "inquiryOrderId" : "MP738048140639408128" , //rfqId "lpName" : "WX" , "quoteOrderId" : "MPQ738048203885318144" , //quoteId "direction" : 1 , "status" : 0 , "buyAssetId" : "BTC" , "buyAmount" : "0.0942" , "sellAssetId" : "USDT" , "sellAmount" : "10000" , "price" : "106050" , "submitTime" : 1753772404507 , "dateExpiry" : 1753772464507 , "expirySeconds" : 60 , "remainingTime" : 1122 , "inquirySettleType" : 2 , "quoteSettleType" : 1 , // 1 : delayed 2 : real-time "rank" : 1 , "isBestPrice" : true , "isRecommendPrice" : true }, { "id" : 10 , "inquiryOrderId" : "MP738048140639408128" , //rfqId "lpName" : "GSR" , "quoteOrderId" : "MPQ738048203885318145" , //quoteId "direction" : 1 , "status" : 0 , "buyAssetId" : "BTC" , "buyAmount" : "0.0942" , "sellAssetId" : "USDT" , "sellAmount" : "10000" , "price" : "106059" , "submitTime" : 1753772404507 , "dateExpiry" : 1753772464507 , "expirySeconds" : 60 , "remainingTime" : 1122 , "inquirySettleType" : 2 , "quoteSettleType" : 1 , // 1 : delayed 2 : real-time "rank" : 2 , "isBestPrice" : false , "isRecommendPrice" : false }, ]
}
```

**topic=** **`rfqUpdates`**

```
{ "event" : "update" , "topic" : "rfqUpdates" , "data" : { "rfqId" : "RFQ_123" , "rfqClOrderId" : "RFQClOrder_123" , "buyCcy" : "BTC" , "sellCcy" : "USDT" , "buyAmount" : "" , "sellAmount" : "2" , "rfqMode" : "real-time" , "quoteId" : "quote_123" , "price" : 120001 , "quoteMode" : "real-time" , "status" : "accepted" , "statusInt" : "2" , "isLPReject" : false , "expiryTime" : 1717410000 }
}
```

**Use Private stream**

- Sandbox: `wss://stream-pro.sim.hashkeydev.com/api/v1/ws/{listenKey}`
- Production: `wss://stream-pro.hashkey.com/api/v1/ws/{listenKey}`

**Note:** Replace `{listenKey}` with your actual listen key obtained from the [Obtain ListenKey](#Create-Listen-Key) .

**WS Push Demo 👉**

<!-- 🖼️❌ Image not available. Please use `PdfPipelineOptions(generate_picture_images=True)` -->

<!-- 🖼️❌ Image not available. Please use `PdfPipelineOptions(generate_picture_images=True)` -->

[English ✓](/uae/en) 繁體中文 Coming Soon