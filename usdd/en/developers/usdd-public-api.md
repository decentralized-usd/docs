# USDD Public API

USDD exposes a set of public, read-only REST APIs for protocol data — supply, yield, collateral, Vaults and Smart Allocator allocations. All endpoints are free to use, require no API key, and support CORS.

***

### 1. Common — Network & Auth <a href="#id-1" id="id-1"></a>

<table><thead><tr><th width="188.87890625">Item</th><th>Value</th></tr></thead><tbody><tr><td>Base URL</td><td><mark style="color:blue;"><code>https://openapi.usdd.io</code></mark></td></tr><tr><td>Method</td><td><code>GET</code> only</td></tr><tr><td>Authentication</td><td>None — all endpoints are public, no API key</td></tr><tr><td>Content-Type</td><td><code>application/json</code> (except the two bare-number endpoints, §6.1 / §6.2)</td></tr><tr><td>CORS</td><td>Enabled — callable directly from browsers</td></tr><tr><td>Rate limit</td><td>No documented per-key limit; treat as best-effort and cache where possible</td></tr></tbody></table>

All request examples below use the absolute Base URL, so they are copy-pasteable without consulting this table.

***

### 2. Common — Conventions <a href="#id-2" id="id-2"></a>

#### 2.1 Response envelope <a href="#id-3" id="id-3"></a>

Most endpoints return a standard JSON envelope:

```json
{ "code": 0, "message": "SUCCESS", "data": { ... } }
```

<table><thead><tr><th width="130.31640625">Field</th><th width="150.0703125">Type</th><th width="129.91796875">Existence</th><th>Description</th></tr></thead><tbody><tr><td>code</td><td>integer</td><td>always</td><td><code>0</code> = success; non-zero = error (see §3)</td></tr><tr><td>message</td><td>string</td><td>always</td><td><code>SUCCESS</code>, or an error description when <code>code != 0</code></td></tr><tr><td>data</td><td>object | array</td><td>always</td><td>Payload; shape depends on the endpoint</td></tr></tbody></table>

Two endpoints — `GET /totalSupply` and `GET /circulatingSupply` — return a **bare numeric value** with no envelope.

#### 2.2 Data conventions <a href="#id-4" id="id-4"></a>

<table><thead><tr><th width="210.2109375">Topic</th><th>Convention</th></tr></thead><tbody><tr><td>Number types</td><td>Numeric fields may be returned as <code>number</code> or <code>string</code>; string-encoded numbers are exact and can be parsed safely as high-precision decimals</td></tr><tr><td>Precision</td><td>Some APY fields carry up to 29 digits of precision — transport them as strings and truncate (typically to 4 decimal places) for display</td></tr><tr><td><code>*DailyChange</code> fields</td><td>Change versus the previous day, based on the 00:00 UTC+8 daily snapshot; the value can be negative</td></tr><tr><td>Field stability</td><td>Published field names are not renamed within a version; new fields are added in a non-breaking way</td></tr></tbody></table>

#### 2.3 Units <a href="#id-5" id="id-5"></a>

Every response field table includes a `Unit` column. The possible values:

<table><thead><tr><th width="160.3046875">Unit</th><th>Where it appears</th><th>How to read it</th></tr></thead><tbody><tr><td><code>USDD</code> / <code>sUSDD</code></td><td><code>totalSupply</code>, <code>mintedUSDD</code>, <code>curMinted</code>, <code>debt</code>, <code>line</code>, <code>usdd[]</code>, <code>susdd[]</code>, etc.</td><td>Token amount, already de-scaled. Use as-is; USDD and sUSDD are each ≈ 1 USD</td></tr><tr><td><code>USD</code></td><td><code>tvl</code>, <code>totalCollateralValue</code>, <code>earnTvl</code>, <code>earnSa</code>, <code>lockedValue</code>, <code>holdingAmount</code>, <code>*DailyChange</code>, etc.</td><td>Already de-scaled US dollars. Use as-is</td></tr><tr><td><code>decimal</code></td><td><code>tronApy</code>, <code>ethApy</code>, <code>bscApy</code>, <code>currentApy</code>, <code>stabilityFee</code>, <code>psmFee</code>, <code>earnApy</code>, etc.</td><td>Annualized rate as a decimal. <code>0.045</code> means 4.5% — multiply by 100 for a percentage</td></tr><tr><td><code>percent</code></td><td><code>apy</code> of <code>smart-allocator/detail-overview</code> only</td><td>Already a percentage. <code>3.4268</code> means 3.4268% — use as-is</td></tr><tr><td><code>ratio</code></td><td><code>collateralRatio</code>, <code>minCollateralRatio</code></td><td>A multiple. <code>2.6</code> means 260%; <code>1.2</code> means 120%</td></tr><tr><td><code>epoch ms</code></td><td><code>statisticTime</code></td><td>Millisecond Unix timestamp</td></tr><tr><td><code>datetime</code></td><td><code>time</code></td><td>Human-readable date-time string (UTC+8)</td></tr><tr><td><code>address</code></td><td><code>contractAddress</code>, <code>operatorAddress</code></td><td>Blockchain address — TRON Base58 or EVM hex depending on chain</td></tr><tr><td><code>enum</code></td><td><code>chain</code></td><td>One value from a fixed set, e.g. <code>tron</code> / <code>eth</code> / <code>bsc</code></td></tr><tr><td><code>text</code></td><td><code>symbol</code>, <code>ilk</code>, <code>vaultType</code>, <code>platform</code>, <code>gemSymbol</code>, <code>strategy</code>, <code>tag</code></td><td>Free-form string identifier</td></tr><tr><td><code>—</code></td><td><code>items[]</code> and other array containers</td><td>The row is a container, not a value — it has no unit</td></tr></tbody></table>

#### 2.4 Existence column <a href="#id-6" id="id-6"></a>

Response field tables include an `Existence` column so an agent knows whether a missing or null value is normal:

<table><thead><tr><th width="169.91015625">Existence</th><th>Meaning</th></tr></thead><tbody><tr><td><code>always</code></td><td>The field is always present with a non-null value</td></tr><tr><td><code>nullable</code></td><td>The field is always present, but its value may be <code>null</code></td></tr><tr><td><code>conditional</code></td><td>The field is present only when a stated condition holds</td></tr></tbody></table>

#### 2.5 Empty result ≠ error <a href="#id-7" id="id-7"></a>

An empty or zero-valued result is a **successful** response, not an error.\
Examples: a Vault with no debt returns `curMinted: "0"` and `totalCollateral: "0"`; a chain with no Earn deployment returns `earnTvl: 0`. Do not treat these as failures or retry them.

#### 2.6 Context tips <a href="#id-8" id="id-8"></a>

Several endpoints return long arrays — the APY history (§6.8), supply history (§6.9), collateral history (§6.10) and per-chain history (§6.13). When only the latest point is needed, read the last array element instead of loading the full series, and prefer the snapshot endpoints (§6.1, §6.6, §6.12) over history endpoints.

***

### 3. Common — Errors <a href="#id-9" id="id-9"></a>

**Error model.** Business-level errors are returned as **HTTP 200** with a non-zero `code` in the JSON envelope; the HTTP status is not used to signal business errors. The only exception is an unknown URL path, which returns a real **HTTP 404** with a non-JSON nginx page. An agent should therefore branch on the `code` field, not on the HTTP status (except for routing 404s).

#### 3.1 Code table <a href="#id-10" id="id-10"></a>

<table><thead><tr><th width="140.203125">code</th><th width="249.56640625">message</th><th>Meaning</th></tr></thead><tbody><tr><td>0</td><td><code>SUCCESS</code></td><td>Request succeeded</td></tr><tr><td>1</td><td><code>FAIL</code></td><td>Request failed</td></tr><tr><td>404</td><td><code>NOT_FOUND</code></td><td>URI does not exist</td></tr><tr><td>500</td><td><code>INTERNAL_SERVER_ERROR</code></td><td>Internal server error</td></tr><tr><td>10001</td><td><code>PARAMETER_MISSING</code></td><td>A required parameter is missing</td></tr><tr><td>10002</td><td><code>PARAMETER_ERROR</code></td><td>A parameter value is invalid</td></tr></tbody></table>

#### 3.2 Common error cases <a href="#id-11" id="id-11"></a>

<table><thead><tr><th width="235.06640625">Case</th><th>Trigger</th><th>Actual response</th></tr></thead><tbody><tr><td>Missing required parameter</td><td>Omit <code>chain</code> on §6.12, or <code>chain</code>/<code>interval</code> on §6.13</td><td>HTTP 200, <code>code: 1</code>, message <code>Required request parameter '...' is not present</code></td></tr><tr><td>Invalid parameter value</td><td>Unsupported <code>chain</code> (e.g. <code>solana</code>) or <code>interval</code></td><td>HTTP 200, <code>code: 10002</code>, message <code>Invalid chain.</code> / <code>Invalid interval.</code></td></tr><tr><td>Unknown path</td><td>Request a path that does not exist</td><td>HTTP 404, non-JSON nginx page</td></tr></tbody></table>

> Note: code `10001 PARAMETER_MISSING` is defined, but a fully absent required query parameter currently returns `code: 1` via framework-level validation.

***

### 4. Endpoint Index <a href="#id-12" id="id-12"></a>

<table><thead><tr><th width="99.95703125">#</th><th width="99.83203125">Group</th><th>Name</th><th>Path</th></tr></thead><tbody><tr><td>6.1</td><td>A</td><td>Total Supply</td><td><code>GET /totalSupply</code></td></tr><tr><td>6.2</td><td>A</td><td>Circulating Supply</td><td><code>GET /circulatingSupply</code></td></tr><tr><td>6.3</td><td>A</td><td>Earn APY</td><td><code>GET /api/v1/external/earn-apy</code></td></tr><tr><td>6.4</td><td>A</td><td>USDD Supply by Chain</td><td><code>GET /api/v1/external/total-supply/usdd</code></td></tr><tr><td>6.5</td><td>A</td><td>sUSDD Supply by Chain</td><td><code>GET /api/v1/external/total-supply/susdd</code></td></tr><tr><td>6.6</td><td>B</td><td>Protocol Overview</td><td><code>GET /api/v1/market-site/overview</code></td></tr><tr><td>6.7</td><td>B</td><td>Protocol Overview (with 24h change)</td><td><code>GET /api/v1/data-platform/overview/info</code></td></tr><tr><td>6.8</td><td>B</td><td>DSR APY (current / average / history)</td><td><code>GET /api/v1/market-site/overview/apy</code></td></tr><tr><td>6.9</td><td>B</td><td>USDD Total Supply History</td><td><code>GET /api/v1/data-platform/overview/supply-value-history</code></td></tr><tr><td>6.10</td><td>B</td><td>Total Collateral Value History</td><td><code>GET /api/v1/data-platform/overview/collateral-value-history</code></td></tr><tr><td>6.11</td><td>B</td><td>Vault Configuration List</td><td><code>GET /api/v1/vault/collaterals</code></td></tr><tr><td>6.12</td><td>B</td><td>Per-chain Collateral Snapshot</td><td><code>GET /api/v1/data-platform/latest-collateral</code></td></tr><tr><td>6.13</td><td>B</td><td>Per-chain Historical Series</td><td><code>GET /api/v1/data-platform/collateral-history</code></td></tr><tr><td>6.14</td><td>B</td><td>Smart Allocator Detail</td><td><code>GET /api/v1/smart-allocator/detail-overview</code></td></tr></tbody></table>

***

### 5. Endpoint Reference <a href="#id-13" id="id-13"></a>

### 6.1 Total Supply <a href="#id-14" id="id-14"></a>

**Overview.** True total supply of USDD: USDD in circulation + sUSDD.\
Typical use: a single headline supply figure.\
When not to use: for a per-chain breakdown use §6.4 / §6.5; for USD value use §6.6.

**Endpoint.** `GET /totalSupply` — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```bash
curl "https://openapi.usdd.io/totalSupply"
```

**Response.** A bare numeric value (no JSON envelope), unit `USDD`.

```json
1541470086
```

**Errors.** See §3. This endpoint takes no parameters, so only routing 404 or 5xx apply.

***

### 6.2 Circulating Supply <a href="#id-15" id="id-15"></a>

**Overview.** True circulating supply of USDD: USDD in circulation + sUSDD.\
Typical use: a single headline circulating-supply figure.\
When not to use: same as §6.1.

**Endpoint.** <mark style="color:blue;">`GET /circulatingSupply`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```bash
curl "https://openapi.usdd.io/circulatingSupply"
```

**Response.** A bare numeric value (no JSON envelope), unit `USDD`.

```json
1541470086
```

**Errors.** See §3.

***

### 6.3 Earn APY <a href="#id-16" id="id-16"></a>

**Overview.** Current Earn (DSR) annual yield for each chain.\
Typical use: show the current savings rate per chain.\
When not to use: for historical APY use §6.8.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/external/earn-apy`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```bash
curl "https://openapi.usdd.io/api/v1/external/earn-apy"
```

**Response fields.**

<table><thead><tr><th width="105.4765625">Field</th><th width="110.29296875">Type</th><th width="114.95703125">Existence</th><th width="110.49609375">Unit</th><th>Description</th></tr></thead><tbody><tr><td>tronApy</td><td>string</td><td>always</td><td>decimal</td><td>Earn APY on TRON, 4 decimal places (<code>0.0400</code> = 4.00%)</td></tr><tr><td>ethApy</td><td>string</td><td>always</td><td>decimal</td><td>Earn APY on Ethereum, 4 decimal places</td></tr><tr><td>bscApy</td><td>string</td><td>always</td><td>decimal</td><td>Earn APY on BNB Chain, 4 decimal places</td></tr></tbody></table>

**Response example.**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": { "tronApy": "0.0400", "ethApy": "0.0400", "bscApy": "0.0400" }
}
```

**Errors.** See §3.

***

### 6.4 USDD Supply by Chain <a href="#id-17" id="id-17"></a>

**Overview.** USDD circulating supply (excluding sUSDD), broken down by chain. Refreshes every 5 minutes.\
Typical use: per-chain USDD distribution.\
When not to use: for the combined supply use §6.1; for sUSDD use §6.5.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/external/total-supply/usdd`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```json
curl "https://openapi.usdd.io/api/v1/external/total-supply/usdd"
```

**Response fields.**

<table><thead><tr><th width="120.14453125">Field</th><th width="104.63671875">Type</th><th width="115.29296875">Existence</th><th width="110.453125">Unit</th><th>Description</th></tr></thead><tbody><tr><td>symbol</td><td>string</td><td>always</td><td>text</td><td>Always <code>USDD</code></td></tr><tr><td>totalSupply</td><td>number</td><td>always</td><td>USDD</td><td>USDD in circulation across all chains, excluding sUSDD</td></tr><tr><td>tron</td><td>number</td><td>always</td><td>USDD</td><td>USDD supply on TRON</td></tr><tr><td>eth</td><td>number</td><td>always</td><td>USDD</td><td>USDD supply on Ethereum</td></tr><tr><td>bsc</td><td>number</td><td>always</td><td>USDD</td><td>USDD supply on BNB Chain</td></tr></tbody></table>

**Response example.**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "symbol": "USDD",
    "totalSupply": 1251507751.55,
    "tron": 1188091183.19,
    "eth": 59487923.50,
    "bsc": 3928644.86
  }
}
```

**Errors.** See §3.

***

### 6.5 sUSDD Supply by Chain <a href="#id-18" id="id-18"></a>

**Overview.** sUSDD supply broken down by chain. Refreshes every 5 minutes.\
Typical use: per-chain sUSDD distribution.\
When not to use: for USDD use §6.4.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/external/total-supply/susdd`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```bash
curl "https://openapi.usdd.io/api/v1/external/total-supply/susdd"
```

**Response fields.**

<table><thead><tr><th width="119.640625">Field</th><th width="120.1640625">Type</th><th width="116.8671875">Existence</th><th width="109.59765625">Unit</th><th>Description</th></tr></thead><tbody><tr><td>symbol</td><td>string</td><td>always</td><td>text</td><td>Always <code>sUSDD</code></td></tr><tr><td>totalSupply</td><td>number</td><td>always</td><td>sUSDD</td><td>sUSDD supply across all chains</td></tr><tr><td>tron</td><td>number</td><td>always</td><td>sUSDD</td><td>sUSDD supply on TRON</td></tr><tr><td>eth</td><td>number</td><td>always</td><td>sUSDD</td><td>sUSDD supply on Ethereum</td></tr><tr><td>bsc</td><td>number</td><td>always</td><td>sUSDD</td><td>sUSDD supply on BNB Chain</td></tr></tbody></table>

**Response example.**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "symbol": "sUSDD",
    "totalSupply": 275673868.67,
    "tron": 0,
    "eth": 260154414.60,
    "bsc": 15519454.07
  }
}
```

**Errors.** See §3. A chain with no sUSDD returns `0` — empty ≠ error (§2.5).

***

### 6.6 Protocol Overview <a href="#id-19" id="id-19"></a>

**Overview.** Real-time cross-chain core metrics for the USDD protocol.\
Typical use: a protocol dashboard snapshot.\
When not to use: for 24-hour deltas use §6.7; for `totalCollateralValue` use §6.7 (this endpoint does not return it); for history use §6.8–§6.10.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/market-site/overview`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```json
curl "https://openapi.usdd.io/api/v1/market-site/overview"
```

**Response fields.**

<table><thead><tr><th width="154.62109375">Field</th><th width="111.359375">Type</th><th width="115.34375">Existence</th><th width="109.890625">Unit</th><th>Description</th></tr></thead><tbody><tr><td>totalSupply</td><td>number</td><td>always</td><td>USDD</td><td>Total USDD circulating supply across all chains</td></tr><tr><td>totalSupplyValue</td><td>number</td><td>always</td><td>USD</td><td>Total value of USDD + sUSDD across all chains</td></tr><tr><td>tvl</td><td>number</td><td>always</td><td>USD</td><td>Protocol total collateral locked value</td></tr><tr><td>earnTvl</td><td>number</td><td>always</td><td>USD</td><td>Earn (DSR) module locked value</td></tr><tr><td>tronApy</td><td>number</td><td>always</td><td>decimal</td><td>Current DSR APY on TRON</td></tr><tr><td>ethApy</td><td>number</td><td>always</td><td>decimal</td><td>Current DSR APY on Ethereum (precision up to 29 digits)</td></tr><tr><td>bscApy</td><td>number</td><td>always</td><td>decimal</td><td>Current DSR APY on BNB Chain (precision up to 29 digits)</td></tr></tbody></table>

**Response example.**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "totalSupply": 1228735758.44,
    "totalSupplyValue": 1520297361.08,
    "tvl": 2325598188.48,
    "earnTvl": 291561602.64,
    "tronApy": 0.04,
    "ethApy": 0.04000000189078800616471198737,
    "bscApy": 0.04000000189078800616471198737
  }
}
```

**Errors.** See §3.

***

### 6.7 Protocol Overview (with 24h change) <a href="#id-20" id="id-20"></a>

**Overview.** Aggregated protocol metrics with 24-hour deltas. Authoritative source for `totalCollateralValue` and `earnSa`.\
Typical use: a dashboard that shows day-over-day movement.\
When not to use: for a plain real-time snapshot use §6.6.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/data-platform/overview/info`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```json
curl "https://openapi.usdd.io/api/v1/data-platform/overview/info"
```

**Response fields.**

<table><thead><tr><th width="190.2734375">Field</th><th width="110.0390625">Type</th><th width="115.80859375">Existence</th><th width="109.70703125">Unit</th><th>Description</th></tr></thead><tbody><tr><td>totalSupplyValue</td><td>string</td><td>always</td><td>USD</td><td>Total value of USDD + sUSDD across all chains</td></tr><tr><td>totalSupplyValueDailyChange</td><td>string</td><td>always</td><td>USD</td><td>Change versus the previous day of <code>totalSupplyValue</code></td></tr><tr><td>totalCollateralValue</td><td>string</td><td>always</td><td>USD</td><td>Total collateral value across all chains</td></tr><tr><td>totalCollateralValueDailyChange</td><td>string</td><td>always</td><td>USD</td><td>Change versus the previous day of <code>totalCollateralValue</code></td></tr><tr><td>earnTvl</td><td>string</td><td>always</td><td>USD</td><td>Earn module locked value</td></tr><tr><td>earnTvlDailyChange</td><td>string</td><td>always</td><td>USD</td><td>Change versus the previous day of <code>earnTvl</code></td></tr><tr><td>earnSa</td><td>string</td><td>always</td><td>USD</td><td>Cumulative investment profits generated across all Vaults on every chain</td></tr><tr><td>earnSaDailyChange</td><td>string</td><td>always</td><td>USD</td><td>Change versus the previous day of <code>earnSa</code></td></tr></tbody></table>

**Response example.**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "totalSupplyValue": "1520295454.82",
    "totalSupplyValueDailyChange": "-4718213.19",
    "totalCollateralValue": "2314589444.69",
    "totalCollateralValueDailyChange": "-3657583.32",
    "earnTvl": "291561602.64",
    "earnTvlDailyChange": "-3009326.74",
    "earnSa": "17454150.49",
    "earnSaDailyChange": "44532.14"
  }
}
```

**Errors.** See §3. `*DailyChange` values can be negative — that is normal.

***

### 6.8 DSR APY (current / average / history) <a href="#id-21" id="id-21"></a>

**Overview.** Aggregate current and historical-average APY, plus a per-chain daily time series.\
Typical use: render an APY history chart.\
When not to use: for just the current APY use §6.3 or §6.6.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/market-site/overview/apy`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```json
curl "https://openapi.usdd.io/api/v1/market-site/overview/apy"
```

**Response fields.**

<table><thead><tr><th width="190.06640625">Field</th><th width="105.03515625">Type</th><th width="115.30859375">Existence</th><th width="112.15234375">Unit</th><th>Description</th></tr></thead><tbody><tr><td>averageApy</td><td>string</td><td>always</td><td>decimal</td><td>Cross-chain historical average APY</td></tr><tr><td>currentApy</td><td>string</td><td>always</td><td>decimal</td><td>Cross-chain current APY</td></tr><tr><td>items[]</td><td>array</td><td>always</td><td>—</td><td>Per-chain breakdown</td></tr><tr><td>items[].chain</td><td>string</td><td>always</td><td>enum</td><td><code>tron</code> / <code>eth</code> / <code>bsc</code></td></tr><tr><td>items[].currentApy</td><td>string</td><td>always</td><td>decimal</td><td>Current APY for the chain</td></tr><tr><td>items[].averageApy</td><td>string</td><td>always</td><td>decimal</td><td>Historical average APY for the chain</td></tr><tr><td>items[].items[]</td><td>array</td><td>always</td><td>—</td><td>Per-chain APY time series</td></tr><tr><td>items[].items[].statisticTime</td><td>number</td><td>always</td><td>epoch ms</td><td>Timestamp</td></tr><tr><td>items[].items[].apy</td><td>string</td><td>always</td><td>decimal</td><td>APY value at that point</td></tr></tbody></table>

**Response example (truncated).**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "averageApy": "0.07510406",
    "currentApy": "0.04000000",
    "items": [
      {
        "chain": "eth",
        "currentApy": "0.04000000189078800616471198737",
        "averageApy": "0.07572265",
        "items": [
          { "statisticTime": 1757088000000, "apy": "0" },
          { "statisticTime": 1759161600000, "apy": "0.11999999670235172999355199863" }
        ]
      }
    ]
  }
}
```

**Errors.** See §3. Context tip (§2.6): the nested `items[].items[]` series can be long.

***

### 6.9 USDD Total Supply History <a href="#id-22" id="id-22"></a>

**Overview.** Daily history of USDD and sUSDD supply across the three chains.\
Typical use: render a Total Supply line chart.\
When not to use: for the current value use §6.4 / §6.5.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/data-platform/overview/supply-value-history`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```json
curl "https://openapi.usdd.io/api/v1/data-platform/overview/supply-value-history"
```

**Response fields.** `data` is an array; each element:

<table><thead><tr><th width="131.91796875">Field</th><th width="115.4765625">Type</th><th width="115.23046875">Existence</th><th width="115.4140625">Unit</th><th>Description</th></tr></thead><tbody><tr><td>statisticTime</td><td>number</td><td>always</td><td>epoch ms</td><td>Timestamp</td></tr><tr><td>usdd</td><td>string[3]</td><td>always</td><td>USDD</td><td>USDD amount per chain, order <code>[tron, eth, bsc]</code></td></tr><tr><td>susdd</td><td>string[3]</td><td>always</td><td>sUSDD</td><td>sUSDD amount per chain, order <code>[tron, eth, bsc]</code></td></tr></tbody></table>

**Response example (truncated).**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": [
    {
      "statisticTime": 1737302400000,
      "usdd": ["10.00000", "0", "0"],
      "susdd": ["0", "0", "0"]
    }
  ]
}
```

**Errors.** See §3. Context tip (§2.6): the array spans the full protocol history.

***

### 6.10 Total Collateral Value History <a href="#id-23" id="id-23"></a>

**Overview.** Daily history of total collateral value across the three chains.\
Typical use: render a Collateral Value line chart.\
When not to use: for the current value use §6.7.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/data-platform/overview/collateral-value-history`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```bash
curl "https://openapi.usdd.io/api/v1/data-platform/overview/collateral-value-history"
```

**Response fields.** `data` is an array; each element:

<table><thead><tr><th width="149.890625">Field</th><th width="112.625">Type</th><th width="114.78515625">Existence</th><th width="111.4375">Unit</th><th>Description</th></tr></thead><tbody><tr><td>statisticTime</td><td>number</td><td>always</td><td>epoch ms</td><td>Timestamp</td></tr><tr><td>collateralValue</td><td>string[3]</td><td>always</td><td>USD</td><td>Collateral value per chain, order <code>[tron, eth, bsc]</code></td></tr></tbody></table>

**Response example (truncated).**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": [
    { "statisticTime": 1737331200000, "collateralValue": ["5.94", "0", "0"] }
  ]
}
```

**Errors.** See §3.

***

### 6.11 Vault Configuration List <a href="#id-24" id="id-24"></a>

**Overview.** Static contract-level configuration of all Vault types.\
Typical use: list Vault parameters (collateral ratio, stability fee, ceiling).\
When not to use: for real-time per-Vault state use §6.12.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/vault/collaterals`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```bash
curl "https://openapi.usdd.io/api/v1/vault/collaterals"
```

**Response fields.**

<table><thead><tr><th width="190.47265625">Field</th><th width="102.8984375">Type</th><th width="115.265625">Existence</th><th width="104.76953125">Unit</th><th>Description</th></tr></thead><tbody><tr><td>items[]</td><td>array</td><td>always</td><td>—</td><td>Vault list</td></tr><tr><td>items[].ilk</td><td>string</td><td>always</td><td>text</td><td>Vault identifier, e.g. <code>TRX-A</code>, <code>USDT-A</code></td></tr><tr><td>items[].minCollateralRatio</td><td>string</td><td>always</td><td>ratio</td><td>Minimum collateral ratio (<code>1.2</code> = 120%)</td></tr><tr><td>items[].stabilityFee</td><td>string</td><td>always</td><td>decimal</td><td>Annual stability fee (<code>0.005</code> = 0.5%)</td></tr><tr><td>items[].maxMinted</td><td>string</td><td>always</td><td>USDD</td><td>Debt ceiling</td></tr><tr><td>items[].dust</td><td>string</td><td>always</td><td>USDD</td><td>Dust Limit / Debt Floor — minimum USDD that can be minted per Vault</td></tr><tr><td>items[].curMinted</td><td>string</td><td>always</td><td>USDD</td><td>Currently minted USDD</td></tr><tr><td>items[].totalCollateral</td><td>string</td><td>always</td><td>USD</td><td>Total locked collateral value (not native units)</td></tr></tbody></table>

Current Vault types: `TRX-A`, `TRX-B`, `TRX-C`, `USDT-A`, `STRX-A`, `WBTC-A`, `WBTC-B`.

**Response example (truncated).**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "items": [
      {
        "ilk": "TRX-A",
        "minCollateralRatio": "1.2",
        "stabilityFee": "0.005",
        "maxMinted": "400000000",
        "dust": "1000",
        "curMinted": "170405778.276294",
        "totalCollateral": "445798872.688855"
      }
    ]
  }
}
```

**Errors.** See §3. A Vault with no usage returns `curMinted: "0"` and `totalCollateral: "0"` — empty ≠ error (§2.5).

***

### 6.12 Per-chain Collateral Snapshot <a href="#id-25" id="id-25"></a>

**Overview.** Real-time collateral and supply state for a specific chain, with a per-Vault breakdown. Items include regular Vaults, PSM Vaults and Smart Allocator Vaults.\
Typical use: a per-chain Vault dashboard.\
When not to use: for static config use §6.11; for history use §6.13.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/data-platform/latest-collateral`</mark> — Base URL & auth see §1.

**Request parameters.**

<table><thead><tr><th width="118.39453125">Parameter</th><th width="88.68359375">In</th><th width="86.94921875">Type</th><th width="115.9375">Required</th><th width="100.01953125">Default</th><th>Description</th></tr></thead><tbody><tr><td>chain</td><td>query</td><td>string</td><td>yes</td><td>—</td><td><code>tron</code> / <code>eth</code> / <code>bsc</code></td></tr></tbody></table>

**Request example.**

```bash
curl "https://openapi.usdd.io/api/v1/data-platform/latest-collateral?chain=tron"
```

**Response fields — top level.**

<table><thead><tr><th width="190.00390625">Field</th><th width="114.625">Type</th><th width="115.0234375">Existence</th><th width="105.05859375">Unit</th><th>Description</th></tr></thead><tbody><tr><td>apy</td><td>number</td><td>always</td><td>decimal</td><td>Current DSR APY on this chain</td></tr><tr><td>usddTotalSupply</td><td>number</td><td>always</td><td>USDD</td><td>USDD circulating supply on this chain</td></tr><tr><td>totalSupplyValue</td><td>number</td><td>always</td><td>USD</td><td>USDD + sUSDD value on this chain</td></tr><tr><td>totalSupplyValueDailyChange</td><td>number</td><td>always</td><td>USD</td><td>Change versus the previous day of <code>totalSupplyValue</code></td></tr><tr><td>totalCollateralValue</td><td>number</td><td>always</td><td>USD</td><td>Total collateral value on this chain</td></tr><tr><td>totalCollateralValueDailyChange</td><td>number</td><td>always</td><td>USD</td><td>Change versus the previous day of <code>totalCollateralValue</code></td></tr><tr><td>earnTvl</td><td>number</td><td>always</td><td>USD</td><td>Earn locked value on this chain</td></tr><tr><td>earnTvlDailyChange</td><td>number</td><td>always</td><td>USD</td><td>Change versus the previous day of <code>earnTvl</code></td></tr><tr><td>items[]</td><td>array</td><td>always</td><td>—</td><td>Per-Vault breakdown</td></tr></tbody></table>

**Response fields — `items[]`.**

<table><thead><tr><th width="189.43359375">Field</th><th width="132.0078125">Type</th><th width="119.3515625">Existence</th><th width="108.01171875">Unit</th><th>Description</th></tr></thead><tbody><tr><td>vaultType</td><td>string</td><td>always</td><td>text</td><td>Vault identifier, e.g. <code>TRX-A</code>, <code>PSM-USDT-A</code>, <code>SA001-A</code></td></tr><tr><td>chain</td><td>string</td><td>always</td><td>enum</td><td>Chain identifier</td></tr><tr><td>collateralType</td><td>number</td><td>always</td><td>1 / 2 / 3</td><td><code>1</code> = regular Vault, <code>2</code> = PSM, <code>3</code> = Smart Allocator</td></tr><tr><td>contractAddress</td><td>string</td><td>always</td><td>address</td><td>Vault contract address</td></tr><tr><td>mintedUSDD</td><td>number</td><td>always</td><td>USDD</td><td>Minted USDD</td></tr><tr><td>debt</td><td>number</td><td>always</td><td>USDD</td><td>Current debt including accumulated stability fees</td></tr><tr><td>lockedValue</td><td>number</td><td>always</td><td>USD</td><td>Locked collateral value</td></tr><tr><td>collateralRatio</td><td>number</td><td>always</td><td>ratio</td><td>Current collateral ratio</td></tr><tr><td>minCollateralRatio</td><td>string</td><td>always</td><td>ratio</td><td>Minimum collateral ratio</td></tr><tr><td>stabilityFee</td><td>string</td><td>always</td><td>decimal</td><td>Annual stability fee</td></tr><tr><td>line</td><td>string</td><td>always</td><td>USDD</td><td>Debt ceiling</td></tr><tr><td>apy</td><td>number | null</td><td>nullable</td><td>decimal</td><td>Vault APY; <code>null</code> for regular Vaults</td></tr><tr><td>estimatedAnnualEarnings</td><td>number | null</td><td>nullable</td><td>USD</td><td>Estimated annual earnings; <code>null</code> when not applicable</td></tr><tr><td>psmFee</td><td>string | null</td><td>nullable</td><td>decimal</td><td>PSM swap fee; <code>null</code> for non-PSM Vaults</td></tr></tbody></table>

**Response example (truncated).**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "apy": 0.04,
    "usddTotalSupply": 1175039825.64,
    "totalSupplyValue": 1175039825.64,
    "totalSupplyValueDailyChange": 7633351.69,
    "totalCollateralValue": 1969026838.01,
    "totalCollateralValueDailyChange": 8788306.71,
    "earnTvl": 0,
    "earnTvlDailyChange": 0,
    "items": [
      {
        "vaultType": "TRX-A",
        "chain": "tron",
        "collateralType": 1,
        "contractAddress": "TJ1VWPvFVq7sVsN7J7dWJVZz4SLT14qRUr",
        "mintedUSDD": 170176779.31,
        "debt": 170405778.28,
        "lockedValue": 445798872.69,
        "collateralRatio": 2.6161,
        "minCollateralRatio": "1.2",
        "stabilityFee": "0.00500000096840569341338778031",
        "line": "400000000",
        "apy": null,
        "estimatedAnnualEarnings": null,
        "psmFee": null
      }
    ]
  }
}
```

**Errors.** See §3. Missing `chain` → `code: 1`; invalid `chain` → `code: 10002`.

***

### 6.13 Per-chain Historical Series <a href="#id-26" id="id-26"></a>

**Overview.** Time-series data for a specific chain — used to render 7D / 1M / 6M / 1Y charts.\
Typical use: a per-chain history chart.\
When not to use: for the current snapshot use §6.12.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/data-platform/collateral-history`</mark> — Base URL & auth see §1.

**Request parameters.**

<table><thead><tr><th width="119.984375">Parameter</th><th width="90.390625">In</th><th width="95.25390625">Type</th><th width="109.71875">Required</th><th width="100.4453125">Default</th><th>Description</th></tr></thead><tbody><tr><td>chain</td><td>query</td><td>string</td><td>yes</td><td>—</td><td><code>tron</code> / <code>eth</code> / <code>bsc</code></td></tr><tr><td>interval</td><td>query</td><td>string</td><td>yes</td><td>—</td><td><code>WEEKLY</code> (7 days) / <code>MONTHLY</code> (1 month) / <code>BIANNUAL</code> (6 months) / <code>ANNUAL</code> (1 year)</td></tr></tbody></table>

**Request example.**

```bash
curl "https://openapi.usdd.io/api/v1/data-platform/collateral-history?chain=tron&interval=WEEKLY"
```

**Response fields.** `data.items` is an array; each element:

<table><thead><tr><th width="151.796875">Field</th><th width="120.6171875">Type</th><th width="115.19921875">Existence</th><th width="110.21875">Unit</th><th>Description</th></tr></thead><tbody><tr><td>statisticTime</td><td>number</td><td>always</td><td>epoch ms</td><td>Timestamp</td></tr><tr><td>time</td><td>string | null</td><td>nullable</td><td>datetime</td><td>Human-readable time (UTC+8); the latest entry may be <code>null</code></td></tr><tr><td>collateralValue</td><td>number</td><td>always</td><td>USD</td><td>Collateral value at this point</td></tr><tr><td>debt</td><td>number</td><td>always</td><td>USDD</td><td>Debt amount</td></tr><tr><td>mintedUSDD</td><td>number</td><td>always</td><td>USDD</td><td>Minted USDD</td></tr><tr><td>usddTotalSupply</td><td>number</td><td>always</td><td>USDD</td><td>USDD circulating supply</td></tr><tr><td>totalSupplyValue</td><td>number</td><td>always</td><td>USD</td><td>USDD + sUSDD value</td></tr><tr><td>earnTvl</td><td>number</td><td>always</td><td>USD</td><td>Earn locked value</td></tr><tr><td>earnApy</td><td>number</td><td>always</td><td>decimal</td><td>APY at this point</td></tr></tbody></table>

**Response example (truncated).**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "items": [
      {
        "statisticTime": 1778515200000,
        "time": "2026-05-13 00:00 (UTC+8)",
        "collateralValue": 1913492361.67,
        "debt": 1137814656.28,
        "mintedUSDD": 1137814656.28,
        "usddTotalSupply": 1136731489.13,
        "totalSupplyValue": 1136731489.13,
        "earnTvl": 0,
        "earnApy": 0.04
      }
    ]
  }
}
```

**Errors.** See §3. Missing `chain`/`interval` → `code: 1`; invalid value → `code: 10002`. The latest `time` may be `null` — that is normal, not an error.

***

### 6.14 Smart Allocator Detail <a href="#id-27" id="id-27"></a>

**Overview.** Allocation and earnings detail of USDD protocol reserves across DeFi platforms.\
Typical use: show where reserve funds are deployed and what they earn.\
When not to use: for cumulative profit (`earnSa`) use §6.7 — it is not here.

**Endpoint.** <mark style="color:blue;">`GET /api/v1/smart-allocator/detail-overview`</mark> — Base URL & auth see §1.

**Request parameters.** None.

**Request example.**

```bash
curl "https://openapi.usdd.io/api/v1/smart-allocator/detail-overview"
```

**Response fields — top level.**

<table><thead><tr><th width="152.625">Field</th><th width="104.9453125">Type</th><th width="115.42578125">Existence</th><th width="114.84375">Unit</th><th>Description</th></tr></thead><tbody><tr><td>apy</td><td>number</td><td>always</td><td>percent</td><td>Smart Allocator blended APY — a <strong>percentage</strong> (<code>3.4268</code> = 3.4268%)</td></tr><tr><td>debt</td><td>number</td><td>always</td><td>USDD</td><td>Total debt managed by Smart Allocator</td></tr><tr><td>platformSummaryInfos[]</td><td>array</td><td>always</td><td>—</td><td>Positions per (platform × chain × asset)</td></tr><tr><td>vaultInfos[]</td><td>array</td><td>always</td><td>—</td><td>Smart Allocator Vaults per chain</td></tr></tbody></table>

**Response fields — `platformSummaryInfos[]`.**

<table><thead><tr><th width="150.203125">Field</th><th width="116.4296875">Type</th><th width="115.0625">Existence</th><th width="115.46875">Unit</th><th>Description</th></tr></thead><tbody><tr><td>platform</td><td>string</td><td>always</td><td>text</td><td>DeFi platform, e.g. <code>Aave</code>, <code>Morpho</code>, <code>JustLend</code>, <code>Spark</code>, <code>Venus</code>, <code>ListaDAO</code></td></tr><tr><td>chain</td><td>string</td><td>always</td><td>enum</td><td>Chain, e.g. <code>eth</code>, <code>tron</code>, <code>bsc</code>, <code>plasma</code></td></tr><tr><td>gemSymbol</td><td>string</td><td>always</td><td>text</td><td>Asset symbol, e.g. <code>USDT</code>, <code>USDC</code>, <code>USDS</code>, <code>USDT0</code></td></tr><tr><td>holdingAmount</td><td>number</td><td>always</td><td>USD</td><td>Current holding</td></tr><tr><td>apyHoldingAmount</td><td>number</td><td>always</td><td>USD</td><td>APY-weighted holding amount used in the blended APY calculation</td></tr><tr><td>apy</td><td>number</td><td>always</td><td>decimal</td><td>Position APY</td></tr><tr><td>actualEarnings</td><td>number</td><td>always</td><td>USD</td><td>Cumulative actual earnings</td></tr><tr><td>operatorAddress</td><td>string</td><td>always</td><td>address</td><td>Operator address</td></tr><tr><td>strategy</td><td>string</td><td>always</td><td>text</td><td>Strategy type, e.g. <code>Investment</code></td></tr><tr><td>tag</td><td>string | null</td><td>nullable</td><td>text</td><td>Risk-curator tag, e.g. <code>Gauntlet</code>, <code>Steakhouse</code>; may be empty or <code>null</code></td></tr></tbody></table>

**Response fields — `vaultInfos[]`.**

<table><thead><tr><th width="152.9140625">Field</th><th width="110.06640625">Type</th><th width="114.51953125">Existence</th><th width="115.28515625">Unit</th><th>Description</th></tr></thead><tbody><tr><td>chain</td><td>string</td><td>always</td><td>enum</td><td>Chain</td></tr><tr><td>vaultType</td><td>string</td><td>always</td><td>text</td><td>SA Vault identifier, e.g. <code>SA001-A</code></td></tr><tr><td>contractAddress</td><td>string</td><td>always</td><td>address</td><td>Vault contract address</td></tr><tr><td>debt</td><td>number</td><td>always</td><td>USDD</td><td>Current Vault debt</td></tr></tbody></table>

**Response example (truncated).**

```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "apy": 3.4268,
    "debt": 837933499.00,
    "platformSummaryInfos": [
      {
        "platform": "Aave",
        "chain": "eth",
        "gemSymbol": "USDT",
        "holdingAmount": 43488409.16,
        "apyHoldingAmount": 119040213.57,
        "apy": 2.737286,
        "actualEarnings": 3550427.88,
        "operatorAddress": "0xD00e0079B8CAB524F3fa20EA879a7736E512a5Fc",
        "strategy": "Investment",
        "tag": ""
      }
    ],
    "vaultInfos": [
      {
        "chain": "tron",
        "vaultType": "SA001-A",
        "contractAddress": "TYyC3kxzMYC1sGKpui79VAzwn992jCA6fN",
        "debt": 589698996.00
      }
    ]
  }
}
```

**Errors.** See §3. Note `apy` here is a percentage, unlike every other APY field in this document.

***

### 7. Quick Reference for AI Agents <a href="#id-28" id="id-28"></a>

<table><thead><tr><th width="292.359375">To query</th><th width="104.08984375">Call</th><th>Key fields</th></tr></thead><tbody><tr><td>Total / circulating supply (single number)</td><td>§6.1 / §6.2</td><td>bare numeric value</td></tr><tr><td>Earn APY per chain</td><td>§6.3</td><td><code>tronApy</code> / <code>ethApy</code> / <code>bscApy</code></td></tr><tr><td>USDD or sUSDD supply by chain</td><td>§6.4 / §6.5</td><td><code>totalSupply</code>, <code>tron</code>, <code>eth</code>, <code>bsc</code></td></tr><tr><td>Protocol size, real-time</td><td>§6.6</td><td><code>totalSupply</code>, <code>tvl</code></td></tr><tr><td>Protocol size with 24h change</td><td>§6.7</td><td><code>*DailyChange</code></td></tr><tr><td>Cumulative Vault investment profits</td><td>§6.7</td><td><code>earnSa</code></td></tr><tr><td>APY history curve</td><td>§6.8</td><td><code>items[].items[]</code></td></tr><tr><td>USDD supply history</td><td>§6.9</td><td><code>usdd[3]</code>, <code>susdd[3]</code></td></tr><tr><td>Collateral value history</td><td>§6.10</td><td><code>collateralValue[3]</code></td></tr><tr><td>Vault list and configuration</td><td>§6.11</td><td><code>items[]</code></td></tr><tr><td>Vault real-time state per chain</td><td>§6.12</td><td><code>items[].collateralRatio</code>, <code>mintedUSDD</code></td></tr><tr><td>Single-chain history (debt / supply / apy)</td><td>§6.13</td><td><code>items[]</code></td></tr><tr><td>Smart Allocator allocations and earnings</td><td>§6.14</td><td><code>platformSummaryInfos[]</code></td></tr></tbody></table>

Rules for automated consumption:

* Branch on the `code` field, not the HTTP status — business errors return HTTP 200 (§3).
* Always check `code == 0` before reading `data` (except §6.1 / §6.2, bare numbers).
* Treat APY as a decimal, except `smart-allocator/detail-overview.apy`, which is a percentage.
* Null-check `nullable` fields: `apy`, `estimatedAnnualEarnings`, `psmFee`, `tag`, `time`.
* An empty or zero result is success, not an error (§2.5).
* In history arrays of length 3, element order is fixed: `[tron, eth, bsc]`.
* Use a high-precision decimal type for APY fields, which may carry 29 digits.
