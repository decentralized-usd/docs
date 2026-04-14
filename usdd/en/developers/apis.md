# APIs

Public REST APIs for accessing USDD protocol data — no authentication required.

**Base URL:** `https://app-api.usdd.io`

***

### Endpoints <a href="#endpoints" id="endpoints"></a>

<table><thead><tr><th width="100.453125">Method</th><th width="332.28125">Endpoint</th><th>Description</th></tr></thead><tbody><tr><td>GET</td><td><code>/totalSupply</code></td><td>True total supply of USDD: USDD in circulation + sUSDD</td></tr><tr><td>GET</td><td><code>/circulatingSupply</code></td><td>True circulating supply of USDD: USDD in circulation + sUSDD</td></tr><tr><td>GET</td><td><code>/api/v1/external/earn-apy</code></td><td>USDD savings yield across all chains</td></tr><tr><td>GET</td><td><code>/api/v1/external/total-supply/usdd</code></td><td>USDD circulating supply per chain</td></tr><tr><td>GET</td><td><code>/api/v1/external/total-supply/susdd</code></td><td>sUSDD circulating supply per chain</td></tr></tbody></table>

***

### GET USDD Total Supply <a href="#get-total-supply-combined" id="get-total-supply-combined"></a>

Returns the true total supply of USDD across all chains as a plain numeric value.

> When users stake USDD, they receive sUSDD — a yield-bearing token deployed in on-chain investment strategies. The staked USDD is no longer in circulation. This endpoint returns USDD in circulation + sUSDD, which is the correct figure for total supply tracking.

```
GET /totalSupply
```

**Parameters:** None

**Response**

Returns a single numeric value (no JSON wrapper).

**Example Request**

```bash
curl https://app-api.usdd.io/totalSupply
```

**Example Response**

```json
1010300157
```

***

### GET USDD Circulating Supply <a href="#get-circulating-supply-combined" id="get-circulating-supply-combined"></a>

Returns the true circulating supply of USDD across all chains as a plain numeric value. Equals USDD in circulation + sUSDD.

```
GET /circulatingSupply
```

**Parameters:** None

**Response**

Returns a single numeric value (no JSON wrapper).

**Example Request**

```bash
curl https://app-api.usdd.io/circulatingSupply
```

**Example Response**

```json
1010300157
```

***

### GET Earn APY <a href="#get-earn-apy" id="get-earn-apy"></a>

Returns the current USDD savings annual yield for each supported chain.

```
GET /api/v1/external/earn-apy
```

**Parameters:** None

**Response Parameters**

<table><thead><tr><th width="180.2734375">Field</th><th width="149.64453125">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>tronApy</code></td><td>String</td><td>Annual yield on TRON, 4 decimal places</td></tr><tr><td><code>ethApy</code></td><td>String</td><td>Annual yield on Ethereum, 4 decimal places</td></tr><tr><td><code>bscApy</code></td><td>String</td><td>Annual yield on BNB Chain, 4 decimal places</td></tr></tbody></table>

**Example Request**

```bash
curl "https://app-api.usdd.io/api/v1/external/earn-apy"
```

<details>

<summary><strong>Example Response</strong></summary>

<pre class="language-json"><code class="lang-json"><strong>{
</strong>  "code": 0,
  "data": {
    "tronApy": "0.0800",
    "ethApy": "0.1200",
    "bscApy": "0.1200"
  },
  "message": "SUCCESS"
}
</code></pre>

</details>

**Error Codes**

| Code  | Description           |
| ----- | --------------------- |
| `0`   | Success               |
| `500` | Internal server error |

***

### GET USDD Supply <a href="#get-usdd-total-supply" id="get-usdd-total-supply"></a>

Returns the current USDD supply in circulation across all chains, **excluding sUSDD**. Updated every **5 minutes**.

> Note: When users stake USDD, they receive sUSDD — a yield-bearing token whose value grows over time as the underlying USDD is deployed in on-chain investment strategies. This endpoint only reflects USDD tokens currently in circulation, not the USDD value staked as sUSDD. To get the true total supply of USDD (including the portion staked as sUSDD), use `/totalSupply`.

```
GET /api/v1/external/total-supply/usdd
```

**Parameters:** None

**Response Parameters**

<table><thead><tr><th width="179.96484375">Field</th><th width="150.21484375">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>symbol</code></td><td>String</td><td>Token identifier, always <code>"USDD"</code></td></tr><tr><td><code>totalSupply</code></td><td>Number</td><td>USDD in circulation across all chains (excludes sUSDD)</td></tr><tr><td><code>tron</code></td><td>Number</td><td>USDD in circulation on TRON</td></tr><tr><td><code>eth</code></td><td>Number</td><td>USDD in circulation on Ethereum</td></tr><tr><td><code>bsc</code></td><td>Number</td><td>USDD in circulation on BNB Chain</td></tr></tbody></table>

**Example Request**

```bash
curl "https://app-api.usdd.io/api/v1/external/total-supply/usdd"
```

<details>

<summary><strong>Example Response</strong></summary>

```json
{
  "code": 0,
  "data": {
    "symbol": "USDD",
    "totalSupply": 210785566.7,
    "tron": 48992362.03,
    "eth": 138316391.29,
    "bsc": 23476813.38
  },
  "message": "SUCCESS"
}
```

</details>

**Error Codes**

| Code  | Description           |
| ----- | --------------------- |
| `0`   | Success               |
| `500` | Internal server error |

***

### GET sUSDD Supply <a href="#get-susdd-total-supply" id="get-susdd-total-supply"></a>

Returns the current sUSDD circulating supply across all chains. Updated every **5 minutes**.

> sUSDD is a yield-bearing token received when staking USDD. Its value grows over time as the underlying USDD is deployed in on-chain investment strategies. sUSDD can be redeemed for USDD at any time.

```
GET /api/v1/external/total-supply/susdd
```

**Parameters:** None

**Response Parameters**

<table><thead><tr><th width="179.64453125">Field</th><th width="150.3359375">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>symbol</code></td><td>String</td><td>Token identifier, always <code>"sUSDD"</code></td></tr><tr><td><code>totalSupply</code></td><td>Number</td><td>sUSDD supply across all chains</td></tr><tr><td><code>tron</code></td><td>Number</td><td>sUSDD supply on TRON</td></tr><tr><td><code>eth</code></td><td>Number</td><td>sUSDD supply on Ethereum</td></tr><tr><td><code>bsc</code></td><td>Number</td><td>sUSDD supply on BNB Chain</td></tr></tbody></table>

**Example Request**

```bash
curl "https://app-api.usdd.io/api/v1/external/total-supply/susdd"
```

<details>

<summary><strong>Example Response</strong></summary>

```json
{
  "code": 0,
  "data": {
    "symbol": "sUSDD",
    "totalSupply": 1890027.46,
    "tron": 0,
    "eth": 1201916.02,
    "bsc": 688111.44
  },
  "message": "SUCCESS"
}
```

</details>



**Error Codes**

| Code  | Description           |
| ----- | --------------------- |
| `0`   | Success               |
| `500` | Internal server error |

***

### Quick Start <a href="#quick-start" id="quick-start"></a>

{% tabs %}
{% tab title="JavaScript" %}
```js
// Get USDD Total Supply
const res = await fetch('https://app-api.usdd.io/api/v1/external/total-supply/usdd');
const { data } = await res.json();
console.log('Total Supply:', data.totalSupply);
// → Total Supply: 210785566.7
```
{% endtab %}

{% tab title="Python" %}
```python
import requests

res = requests.get('https://app-api.usdd.io/api/v1/external/total-supply/usdd')
data = res.json()['data']
print(f"Total Supply: {data['totalSupply']:,.2f}")
# → Total Supply: 210,785,566.70
```
{% endtab %}
{% endtabs %}
