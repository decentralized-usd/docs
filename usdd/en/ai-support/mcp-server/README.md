# MCP Server

### What It Is

The USDD MCP Server is a [Model Context Protocol](https://modelcontextprotocol.io/) implementation that allows AI agents to interact with the **USDD decentralized stablecoin protocol** across **TRON, Ethereum, and BNB Smart Chain**. The server enables both core protocol operations — Vault/CDP, PSM, and Savings — and general-purpose chain utilities such as token balance queries and allowance management.

**GitHub**: [https://github.com/decentralized-usd/mcp-server-usdd](https://github.com/decentralized-usd/mcp-server-usdd)

### Key Capabilities

**USDD Protocol**

* **Vault / CDP**: Full vault lifecycle management — open vaults, deposit collateral, mint USDD, repay debt, withdraw, and close. Includes real-time oracle and liquidation configuration per collateral type.
* **Vault Risk Monitoring**: AI-guided risk assessment with collateral ratio checks, liquidation threshold warnings, and vault health summaries.
* **PSM (Peg Stability Module)**: Real-time fee and enablement status for each PSM. Swap supported stablecoins into USDD or redeem USDD back to the underlying gem.
* **USDD Savings**: Inspect current savings rate, sUSDD metrics, and wallet share positions. Deposit and withdraw USDD through the savings module.
* **Token Approvals**: Check allowances and approve token spending for USDD protocol interactions.

**General Chain**

* **Balances**: Native (TRX / ETH / BNB) and ERC20 / TRC20 token balances across TRON, Ethereum, and BNB Smart Chain (plus internal testnets).
* **Allowances & Approvals**: Read token allowance for any spender, compare against a required amount, and approve token spending for USDD protocol interactions.
* **Protocol Discovery**: Configured contract addresses, collateral types (ilks), PSM joins, and debt ceilings per network.
* **Networks**: Supported network list with chain keys (`tron`, `eth`, `bsc` + internal testnets); per-family default network selection with aliases (`mainnet`, `nile`).
* **Wallet**: Signing-address resolution per network, dual signing modes (browser / agent), and wallet management — connect browser wallet, list / switch / import wallets.
* **Token Transfers**: Two-step preview → confirm flow for safe asset transfers across TRX, TRC20, ETH / BNB native, and ERC20. The AI must present transfer details and wait for explicit user confirmation; pending previews expire after 10 minutes.

**Protocol Analytics**

* **Protocol & Chain Metrics**: Aggregated USDD protocol metrics and per-chain metrics (collateral breakdown, USDD supply, utilization) from mainnet data feeds.
* **Collateral Prices**: Latest highest-price data per collateral type from the website API.
* **Treasury**: Latest USDD treasury report summary and JST buyback & burn statistics.
* **Smart Allocator**: Investment overview (debt, invested amount, earnings, APY), asset breakdown by protocol / network / asset, proof-of-reserve platform details, and debt overview grouped by network vault.

### Supported Networks

<table><thead><tr><th width="193.8828125">Network</th><th width="185.46875">Key</th><th>Notes</th></tr></thead><tbody><tr><td>TRON</td><td><code>tron</code></td><td>TRON-native vault and PSM support</td></tr><tr><td>Ethereum</td><td><code>eth</code></td><td>Vault, PSM, USDD Savings</td></tr><tr><td>BNB Smart Chain</td><td><code>bsc</code></td><td>Mirrors ETH deployment structure</td></tr><tr><td>TRON Nile</td><td><code>tron_nile</code></td><td>Internal testnet deployment</td></tr><tr><td>Ethereum Sepolia</td><td><code>eth_sepolia</code></td><td>Internal testnet deployment</td></tr><tr><td>BSC Testnet</td><td><code>bsc_testnet</code></td><td>Internal testnet deployment</td></tr></tbody></table>

### Prerequisites

* Node.js 20+
* Optional but recommended:
  * `TRONGRID_API_KEY` for more reliable TRON access
  * dedicated `ETH_RPC_URL`
  * dedicated `BSC_RPC_URL`

### Developer

#### Installation

```
git clone https://github.com/decentralized-usd/mcp-server-usdd
cd mcp-server-usdd
npm install
```

#### Usage

```
npm start
npm run start:http
npm run dev
```

### Configuration

#### Wallet Modes

<table><thead><tr><th width="198.09765625">Mode</th><th>When to use</th><th>Key storage</th></tr></thead><tbody><tr><td><strong>Browser</strong> (TronLink-compatible)</td><td>Sign in a browser extension (TronLink)</td><td>Wallet extension</td></tr><tr><td><strong>Agent</strong></td><td>Automation / CI / headless; required for EVM signing</td><td>Encrypted local file under <code>~/.agent-wallet/</code>, never exported</td></tr></tbody></table>

Private keys are **never** returned by any MCP tool.

**CLI (agent-wallet)**

The server uses [@bankofai/agent-wallet](https://github.com/BofAI/agent-wallet) for encrypted local wallet storage. On first startup it will automatically initialize \~/.agent-wallet/ and create a default wallet if none exists.

```
# Import an existing private key or mnemonic
npx agent-wallet add

# Generate a new wallet
npx agent-wallet generate

# List all wallets
npx agent-wallet list

# Switch active wallet
npx agent-wallet activate <wallet-id>
```

**Wallet management MCP tools(runtime)**

<table data-header-hidden><thead><tr><th width="225.05078125">Tool</th><th>Description</th></tr></thead><tbody><tr><td><code>get_wallet_address</code></td><td>Shows current address (auto-generates wallet if needed)</td></tr><tr><td><code>connect_browser_wallet</code></td><td>Connect TronLink / browser wallet for signing</td></tr><tr><td><code>set_wallet_mode</code></td><td>Switch between browser and agent signing</td></tr><tr><td><code>get_wallet_mode</code></td><td>Show current signing mode and addresses</td></tr><tr><td><code>list_wallets</code></td><td>List wallets with per-family active status (<code>tron</code> and <code>evm</code>)</td></tr><tr><td><code>set_active_wallet</code></td><td>Switch active wallet by ID, optionally scoped by <code>walletType</code> (<code>tron</code>/<code>evm</code>)</td></tr></tbody></table>

#### Environment Variables

```
# Strongly recommended — avoids TronGrid 429 rate limiting on mainnet
export TRONGRID_API_KEY="your_trongrid_api_key"
```

#### Client Configuration

**Claude Desktop**

Add the following config to:

`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mcp-server-usdd": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@usdd/mcp-server-usdd"],
      "env": {
        "TRONGRID_API_KEY": "your_trongrid_api_key"
      }
    }
  }
}
```

**Claude Code**

Create `.mcp.json` in the project root directory:

```json
{
  "mcpServers": {
    "mcp-server-usdd": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@usdd/mcp-server-usdd"],
      "env": {
        "TRONGRID_API_KEY": "your_trongrid_api_key"
      }
    }
  }
}
```

**Cursor**

Add to .cursor/mcp.json:

```json
{
  "mcpServers": {
    "mcp-server-usdd": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@usdd/mcp-server-usdd"],
      "env": {
        "TRONGRID_API_KEY": "your_trongrid_api_key"
      }
    }
  }
}
```

### Tools

#### Side-Effect & Risk Classification <a href="#side-effect-26-risk-classification" id="side-effect-26-risk-classification"></a>

All tools are classified by side-effect level. Hosts MUST surface `remote-write` and `destructive` operations to the user before execution.

<table><thead><tr><th width="164.97265625">Level</th><th>Definition</th><th>Tools</th></tr></thead><tbody><tr><td><code>safe</code></td><td>Pure local read, no network</td><td><p><code>get_supported_networks</code>, </p><p><code>get_network</code>, </p><p><code>get_wallet_mode</code>, </p><p><code>get_wallet_address</code>, </p><p><code>list_wallets</code></p></td></tr><tr><td><code>network-read</code></td><td>Read-only on-chain or HTTP query</td><td><p><code>get_protocol_overview</code>, </p><p><code>get_supported_ilks</code>, </p><p><code>get_native_balance</code>, </p><p><code>get_token_balance</code>, </p><p><code>check_allowance</code>, </p><p><code>get_oracle_status</code>, </p><p><code>get_user_vaults</code>, </p><p><code>get_vault_summary</code>, </p><p><code>analyze_vault_risk</code>, </p><p><code>get_psm_status</code>, </p><p><code>get_savings_status</code>, </p><p><code>get_protocol_metrics</code>, </p><p><code>get_chain_metrics</code>, </p><p><code>get_collateral_prices</code>, </p><p><code>get_psm_metrics</code>, </p><p><code>get_treasury_summary</code>, <code>get_jst_buyback_stats</code>, </p><p><code>get_smart_allocator_overview</code>, </p><p><code>get_assets_breakdown</code>, </p><p><code>get_proof_of_reserve</code>, </p><p><code>get_debt_overview</code></p></td></tr><tr><td><code>local-write</code></td><td>Modifies local config / wallet store</td><td><p><code>set_network</code>, </p><p><code>set_wallet_mode</code>, </p><p><code>set_active_wallet</code>, </p><p><code>import_wallet</code>, </p><p><code>connect_browser_wallet</code></p></td></tr><tr><td><code>remote-write</code></td><td>Broadcasts a tx, costs gas, HITL required</td><td><p><code>approve_token</code>, </p><p><code>open_vault</code>, </p><p><code>deposit_and_mint</code>,</p><p> <code>mint_usdd</code>,</p><p> <code>repay_usdd</code>, </p><p><code>withdraw_collateral</code>, </p><p><code>psm_swap_to_usdd</code>, </p><p><code>psm_swap_from_usdd</code>, </p><p><code>deposit_savings</code>, </p><p><code>withdraw_savings</code>, </p><p><code>prepare_token_transfer</code>, </p><p><code>confirm_token_transfer</code>, </p><p><code>close_vault</code></p></td></tr></tbody></table>

**Safe to retry**: `safe`, `network-read`, and all `prepare_*` previews.\
**NOT safe to retry**: every `remote-write`  tool — a duplicate call may broadcast a second tx.

#### Wallet & Network <a href="#id-8.1-wallet-26-network" id="id-8.1-wallet-26-network"></a>

<table><thead><tr><th width="215.08984375">Tool</th><th width="229.9375">Description</th><th width="94.6875">Write?</th><th>Input schema</th></tr></thead><tbody><tr><td><code>get_supported_networks</code></td><td>List supported networks</td><td>No</td><td>—</td></tr><tr><td><code>set_network</code></td><td>Set the default network for a family (<code>tron</code>/<code>eth</code>/<code>bsc</code>); accepts <code>mainnet</code> / <code>nile</code> aliases</td><td>Yes</td><td><strong>Required</strong>: <code>network: string</code> (key or alias) · <strong>Optional</strong>: <code>family: "tron" \| "eth" \| "bsc"</code></td></tr><tr><td><code>get_network</code></td><td>Show per-family default networks</td><td>No</td><td>—</td></tr><tr><td><code>get_wallet_mode</code></td><td>Show current signing mode and addresses</td><td>No</td><td><strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>set_wallet_mode</code></td><td>Switch signing mode: <code>agent</code> / <code>browser</code></td><td>Yes</td><td><strong>Required</strong>: <code>mode: "browser" \| "agent"</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>connect_browser_wallet</code></td><td>Connect a browser wallet and activate browser mode</td><td>Yes</td><td><strong>Optional</strong>: <code>network</code>, <code>address: string</code></td></tr><tr><td><code>get_wallet_address</code></td><td>Show the current address for the target network</td><td>No</td><td><strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>list_wallets</code></td><td>List wallets with <code>tron</code> and <code>evm</code> active pointers</td><td>No</td><td>—</td></tr><tr><td><code>set_active_wallet</code></td><td>Switch active wallet by ID (optional <code>walletType: tron/evm</code>)</td><td>Yes</td><td><strong>Required</strong>: <code>walletId: string</code> · <strong>Optional</strong>: <code>walletType: "tron" \| "evm"</code></td></tr><tr><td><code>import_wallet</code></td><td>Import a private key / mnemonic into the encrypted keystore</td><td>Yes</td><td><strong>Required</strong>: <code>walletType: "tron" \| "evm"</code>, <code>secretType: "private_key" \| "mnemonic"</code>, <code>secret: string</code> · <strong>Optional</strong>: <code>index: int ≥ 0</code> (mnemonic derivation index, default <code>0</code>)</td></tr></tbody></table>

#### Common <a href="#id-16" id="id-16"></a>

<table><thead><tr><th width="204.52734375">Tool</th><th width="230.18359375">Description</th><th width="95.30078125">Write?</th><th>Input schema</th></tr></thead><tbody><tr><td><code>get_protocol_overview</code></td><td>Protocol addresses, ilks, PSMs, debt ceilings</td><td>No</td><td><strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>get_supported_ilks</code></td><td>Configured collateral types and PSM joins</td><td>No</td><td><strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>get_native_balance</code></td><td>Read TRX / ETH / BNB balance</td><td>No</td><td><strong>Optional</strong>: <code>owner: string</code> (defaults to active wallet), <code>network</code></td></tr><tr><td><code>get_token_balance</code></td><td>Read ERC20 / TRC20 balance</td><td>No</td><td><strong>Required</strong>: <code>token: string</code> (contract) · <strong>Optional</strong>: <code>owner: string</code>, <code>decimals: int > 0</code>, <code>network</code></td></tr><tr><td><code>check_allowance</code></td><td>Read allowance, optionally compare against an <code>amount</code></td><td>No</td><td><strong>Required</strong>: <code>token: string</code>, <code>spender: string</code> · <strong>Optional</strong>: <code>owner: string</code>, <code>amount: string</code> (human-readable), <code>decimals: int > 0</code>, <code>network</code></td></tr><tr><td><code>approve_token</code></td><td>Approve a token allowance</td><td>Yes</td><td><strong>Required</strong>: <code>token: string</code>, <code>spender: string</code>, <code>amount: string</code> (human-readable or <code>"max"</code>) · <strong>Optional</strong>: <code>decimals: int > 0</code>, <code>network</code></td></tr></tbody></table>

#### Vault <a href="#id-17" id="id-17"></a>

<table><thead><tr><th width="190.30859375">Tool</th><th width="230.62890625">Description</th><th width="94.859375">Write?</th><th>Input schema</th></tr></thead><tbody><tr><td><code>get_oracle_status</code></td><td>Inspect oracle and liquidation configuration for an ilk</td><td>No</td><td><strong>Required</strong>: <code>ilk: string</code> (e.g. <code>TRX-A</code>, <code>WBTC-A</code>, <code>USDT-A</code>, <code>PSM-USDT</code>) · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>get_user_vaults</code></td><td>List vault IDs for a wallet</td><td>No</td><td><strong>Optional</strong>: <code>address: string</code>, <code>network</code></td></tr><tr><td><code>get_vault_summary</code></td><td>Collateral, debt, and liquidation metrics</td><td>No</td><td><strong>Required</strong>: <code>cdpId: string</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>analyze_vault_risk</code></td><td>Risk summary with warnings</td><td>No</td><td><strong>Required</strong>: <code>cdpId: string</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>open_vault</code></td><td>Open a new vault via DSProxy</td><td>Yes</td><td><strong>Required</strong>: <code>ilk: string</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>deposit_and_mint</code></td><td>Open-and-mint, or add collateral and mint (idempotent: reuses an existing vault for the same ilk)</td><td>Yes</td><td><strong>Required</strong>: <code>ilk: string</code>, <code>collateralAmount: string</code>, <code>drawAmount: string</code> · <strong>Optional</strong>: <code>cdpId: string</code> (reuses if omitted), <code>transferFrom: boolean</code> (default <code>true</code>), <code>network</code></td></tr><tr><td><code>mint_usdd</code></td><td>Draw more USDD from a vault</td><td>Yes</td><td><strong>Required</strong>: <code>cdpId: string</code>, <code>amount: string</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>repay_usdd</code></td><td>Repay vault debt</td><td>Yes</td><td><strong>Required</strong>: <code>cdpId: string</code>, <code>amount: string</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>withdraw_collateral</code></td><td>Withdraw collateral from a vault</td><td>Yes</td><td><strong>Required</strong>: <code>cdpId: string</code>, <code>ilk: string</code>, <code>amount: string</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>close_vault</code></td><td>Wipe all debt and free all collateral</td><td>Yes</td><td><strong>Required</strong>: <code>cdpId: string</code>, <code>ilk: string</code>, <code>amountToFree: string</code> · <strong>Optional</strong>: <code>network</code></td></tr></tbody></table>

#### PSM <a href="#id-18" id="id-18"></a>

<table><thead><tr><th width="189.68359375">Tool</th><th width="229.921875">Description</th><th width="94.9296875">Write?</th><th>Input schema</th></tr></thead><tbody><tr><td><code>get_psm_status</code></td><td>PSM fees and enablement</td><td>No</td><td><strong>Required</strong>: <code>market: string</code> (e.g. <code>PSM-USDT</code>) · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>get_psm_metrics</code></td><td>PSM route metrics (from / to / available / fee)</td><td>No</td><td><strong>Required</strong>: <code>market: string</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>psm_swap_to_usdd</code></td><td>Swap gem into USDD</td><td>Yes</td><td><strong>Required</strong>: <code>market: string</code>, <code>amount: string</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>psm_swap_from_usdd</code></td><td>Swap USDD into gem</td><td>Yes</td><td><strong>Required</strong>: <code>market: string</code>, <code>amount: string</code> · <strong>Optional</strong>: <code>network</code></td></tr></tbody></table>

#### USDD Savings <a href="#id-19" id="id-19"></a>

<table><thead><tr><th width="189.55859375">Tool</th><th width="230.3671875">Description</th><th width="95.55859375">Write?</th><th>Input schema</th></tr></thead><tbody><tr><td><code>get_savings_status</code></td><td>USDD Savings metrics</td><td>No</td><td><strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>deposit_savings</code></td><td>Deposit USDD to receive sUSDD</td><td>Yes</td><td><strong>Required</strong>: <code>amount: string</code> · <strong>Optional</strong>: <code>network</code></td></tr><tr><td><code>withdraw_savings</code></td><td>Redeem USDD from sUSDD</td><td>Yes</td><td><strong>Required</strong>: <code>amount: string</code> · <strong>Optional</strong>: <code>network</code></td></tr></tbody></table>

#### Token Transfers <a href="#id-20" id="id-20"></a>

Two-step preview → confirm flow for safe asset transfers. The AI **must** present the transfer details to the user and wait for explicit confirmation before executing.

Supports: TRX, TRC20, ETH / BNB, ERC20.\
Pending confirmations expire after 10 minutes&#x20;

<table><thead><tr><th width="200.34765625">Tool</th><th width="220.10546875">Description</th><th width="94.984375">Write?</th><th>Input schema</th></tr></thead><tbody><tr><td><code>prepare_token_transfer</code></td><td>Preview a transfer; returns a <code>confirmationId</code> and details</td><td>No</td><td><strong>Required</strong>: <code>to: string</code>, <code>amount: string</code> (human-readable) · <strong>Optional</strong>: <code>tokenAddress: string</code> (omit for native), <code>decimals: int > 0</code>, <code>network</code></td></tr><tr><td><code>confirm_token_transfer</code></td><td>Execute the previewed transfer after user confirmation</td><td>Yes</td><td><strong>Required</strong>: <code>confirmationId: string</code>, <code>confirm: boolean</code> (pass <code>false</code> to cancel)</td></tr></tbody></table>

#### Protocol Metrics <a href="#id-21" id="id-21"></a>

<table><thead><tr><th width="214.44140625">Tool</th><th width="225.484375">Description</th><th width="95.44140625">Write?</th><th>Input schema</th></tr></thead><tbody><tr><td><code>get_protocol_metrics</code></td><td>Aggregated USDD protocol metrics</td><td>No</td><td>—</td></tr><tr><td><code>get_chain_metrics</code></td><td>Chain-level metrics for <code>tron</code> / <code>eth</code> / <code>bsc</code></td><td>No</td><td><strong>Required</strong>: <code>chain: "tron" \| "eth" \| "bsc"</code></td></tr><tr><td><code>get_collateral_prices</code></td><td>Latest highest-price data per collateral</td><td>No</td><td>—</td></tr><tr><td><code>get_psm_metrics</code></td><td>PSM route metrics (from / to / available / fee) — also listed under §8.4 PSM</td><td>No</td><td><strong>Required</strong>: <code>market: string</code> · <strong>Optional</strong>: <code>network</code></td></tr></tbody></table>

#### Treasury <a href="#id-22" id="id-22"></a>

<table><thead><tr><th width="209.61328125">Tool</th><th width="240.4765625">Description</th><th width="94.671875">Write?</th><th>Input schema</th></tr></thead><tbody><tr><td><code>get_treasury_summary</code></td><td>Latest USDD treasury report summary</td><td>No</td><td>—</td></tr><tr><td><code>get_jst_buyback_stats</code></td><td>JST buyback and burn statistics</td><td>No</td><td>—</td></tr></tbody></table>

#### Smart Allocator <a href="#id-23" id="id-23"></a>

<table><thead><tr><th width="207.82421875">Tool</th><th width="229.62890625">Description</th><th width="95.44140625">Write?</th><th>Input schema</th></tr></thead><tbody><tr><td><code>get_smart_allocator_overview</code></td><td>Overview: debt, invested amount, earnings, APY</td><td>No</td><td>—</td></tr><tr><td><code>get_assets_breakdown</code></td><td>Breakdown by <code>protocol</code> / <code>network</code> / <code>asset</code></td><td>No</td><td><strong>Required</strong>: <code>dimension: "protocol" \| "network" \| "asset"</code></td></tr><tr><td><code>get_proof_of_reserve</code></td><td>Proof-of-reserve style platform investment details</td><td>No</td><td>—</td></tr><tr><td><code>get_debt_overview</code></td><td>Debt overview grouped by vault per network</td><td>No</td><td>—</td></tr></tbody></table>

### Prompts

<table data-header-hidden><thead><tr><th width="230.25"></th><th></th></tr></thead><tbody><tr><td>Prompt</td><td>Description</td></tr><tr><td><code>open_usdd_vault</code></td><td>Open a vault and verify post-trade risk</td></tr><tr><td><code>manage_vault_lifecycle</code></td><td>Run full vault lifecycle flows</td></tr><tr><td><code>use_psm</code></td><td>Use PSM with fee checks</td></tr><tr><td><code>use_savings</code></td><td>Use USDD Savings with inspection and verification</td></tr><tr><td><code>review_vault_risk</code></td><td>Explain risk for a vault</td></tr><tr><td><code>repay_and_close_vault</code></td><td>Repay and close with verification</td></tr><tr><td><code>transfer_tokens</code></td><td>Transfer tokens with two-step preview and explicit confirmation</td></tr></tbody></table>

### Notes

* Vault writes assume the configured wallet can sign on the target chain.
* All tools default to the family-specific defaults set by `set_network`; if `network` is omitted, tron-family default is used unless the tool call explicitly passes `network`.
* ERC20/TRC20 flows often require `approve_token` first.
* Browser mode now supports real transaction signing on TRON networks (`tron`, `tron_nile`) via `tronlink-signer` (TronLink/TIP-6963 flow). EVM networks currently continue to use agent-wallet signing.
* `deposit_and_mint` is idempotent with respect to vault creation: it checks for an existing vault for the given ilk before opening a new one. If no vault exists, it submits two separate transactions — `open` then `lockGemAndDraw` — to avoid combined-tx reliability issues on TRON.
* Token transfers use a two-step flow: `prepare_token_transfer` returns a preview and `confirmationId`; `confirm_token_transfer` executes only after the user explicitly approves. Pending confirmations expire after 10 minutes.
* Protocol analytics tools (`get_protocol_metrics`, `get_chain_metrics`, `get_collateral_prices`, etc.) read from mainnet data feeds only — they do not reflect testnet state.
* TRON, ETH, BSC, and internal testnet deployments have similar protocol structure but different addresses and token decimals.
* This version intentionally excludes migration and auction actions so we can iterate the Vault + PSM + USDD Savings core first.

### Security Model <a href="#security-model" id="security-model"></a>

#### Wallet & keys <a href="#id-12.1-wallet-26-keys-ready-to-publish-e2-80-94-verbatim-from-readme" id="id-12.1-wallet-26-keys-ready-to-publish-e2-80-94-verbatim-from-readme"></a>

* Private keys are encrypted and stored locally in `~/.agent-wallet/`.
* Private keys are never returned by MCP tools.
* The optional `AGENT_WALLET_PASSWORD` is intended for automation and CI environments.
* Never share local MCP client configuration files if they contain private keys or sensitive RPC credentials.

#### HITL boundary  <a href="#id-31" id="id-31"></a>

Only one HITL boundary is **enforced by the server**: `confirm_token_transfer` requires a `confirmationId` previously issued by `prepare_token_transfer`, which expires after 10 minutes.

The server also enforces one **session-level prompt**: before the first TRON write in any Claude session, the user must confirm the signing mode (`wallet.ts:465`).

For all other write tools (`approve_token`, every vault write, PSM swaps, savings deposit/withdraw), HITL is enforced by the MCP host’s confirmation dialog — the server does not intercept the call. Documentation should recommend that hosts confirm every tool marked `Write? = Yes` by default.

#### Operational risk  <a href="#id-32" id="id-32"></a>

* Treat write operations as state-changing actions and review them carefully.
* Vault prompts include risk-review steps so borrowing decisions are checked against current collateral health.
* Test on a safe environment or with small amounts before using mainnet-sized positions.
* Be cautious with large or unlimited token approvals when using `approve_token`.

### Troubleshooting  <a href="#id-13.-troubleshooting-ready-to-publish-e2-80-94-only-verified-commands-e2-80-94-5bp0-5d" id="id-13.-troubleshooting-ready-to-publish-e2-80-94-only-verified-commands-e2-80-94-5bp0-5d"></a>

#### Health check <a href="#id-36" id="id-36"></a>

```bash
# stdio: after npm start, you should see on stderr:
#   @usdd/mcp-server-usdd v1.0.0 initialized
#   Supported networks: tron, eth, bsc, tron_nile, eth_sepolia, bsc_testnet
#   ...
npm start

# HTTP: liveness only, does NOT provide an MCP transport
curl http://127.0.0.1:3101/health
```

#### MCP Inspector <a href="#id-37" id="id-37"></a>

```bash
npx @modelcontextprotocol/inspector npx -y @usdd/mcp-server-usdd
```

#### Common errors <a href="#id-38" id="id-38"></a>

<table><thead><tr><th width="247.48046875">Symptom / error message</th><th width="142.46484375">Source</th><th>Fix</th></tr></thead><tbody><tr><td><code>Unsupported network: …</code></td><td><code>chains.ts</code></td><td>Use a key from §3 (note underscores)</td></tr><tr><td><code>Insufficient … balance.</code></td><td><code>transfer.ts</code></td><td>Check on-chain balance</td></tr><tr><td><code>Unable to detect token decimals …</code></td><td><code>transfer.ts</code></td><td>Pass <code>decimals</code> explicitly to <code>prepare_token_transfer</code></td></tr><tr><td><code>Unknown confirmationId …</code></td><td><code>tools.ts</code></td><td>Already consumed or server restarted; call prepare again</td></tr><tr><td><code>This confirmation has expired.</code></td><td><code>tools.ts</code></td><td>Over 10 minutes; call prepare again</td></tr><tr><td><code>STOP — TRON wallet signing mode has not been confirmed …</code></td><td><code>wallet.ts</code></td><td>Call <code>set_wallet_mode</code> or confirm the default mode</td></tr><tr><td><code>Browser wallet signing is only supported for TRON networks …</code></td><td><code>wallet.ts</code></td><td>Use agent mode for EVM writes</td></tr></tbody></table>

### Versioning & Compatibility <a href="#id-14.-versioning-26-compatibility-ready-to-publish-e2-80-94-5bp0-5d" id="id-14.-versioning-26-compatibility-ready-to-publish-e2-80-94-5bp0-5d"></a>

<table><thead><tr><th width="185.5078125">Field</th><th width="353.3359375">Value</th><th>Source</th></tr></thead><tbody><tr><td>Package name</td><td><code>@usdd/mcp-server-usdd</code></td><td><code>package.json</code></td></tr><tr><td>Package version</td><td><strong><code>1.0.3</code></strong></td><td><code>package.json</code></td></tr><tr><td>MCP SDK</td><td><code>@modelcontextprotocol/sdk@1.27.1</code></td><td><code>package.json</code></td></tr><tr><td>Node.js</td><td><code>>= 20.0.0</code></td><td><code>package.json#engines</code></td></tr><tr><td>TypeScript</td><td><code>5.9.3</code></td><td>devDependencies</td></tr><tr><td>License</td><td><strong>MIT</strong> (SPDX: <code>MIT</code>), Copyright © 2026 USDD</td><td><code>LICENSE</code></td></tr><tr><td>Repository</td><td><code>https://github.com/decentralized-usd/mcp-server-usdd</code></td><td><code>package.json</code></td></tr></tbody></table>

**Transports**:

<table><thead><tr><th width="118.03515625">Transport</th><th>Command</th><th>Status</th></tr></thead><tbody><tr><td>stdio</td><td><code>npm start</code> / <code>npx -y @usdd/mcp-server-usdd</code></td><td>Production-ready</td></tr><tr><td>HTTP</td><td><code>npm run start:http</code></td><td>Currently exposes only <code>/health</code>; no MCP transport mounted. Use for liveness probes only.</td></tr></tbody></table>

### Example Conversations

**Vault**

* “What vault types are available on Ethereum?” → AI calls `get_supported_ilks` with `network=eth` and summarizes the supported vault collateral types.
* “Open a TRX-A/USDT-A/WBTC-A vault on Tron and mint 500 USDD” → AI uses `open_usdd_vault`: checks wallet, reviews oracle status, executes `deposit_and_mint` (auto-opens a new vault if none exists for that ilk), then verifies the new vault risk.
* “Am I close to liquidation on vault 123?” → AI calls `get_vault_summary` and `analyze_vault_risk`, then explains the health factor and collateral buffer.
* “Repay part of my vault debt on BSC” → AI uses `manage_vault_lifecycle` with `action=repay`: checks USDD balance and allowance, calls `repay_usdd`, then verifies the updated vault state.
* “Close my vault and withdraw the collateral” → AI uses `repay_and_close_vault`: checks debt, balance, allowance, calls `close_vault`, then confirms the vault state after repayment.

**PSM**

* “What are the current PSM fees on Ethereum?” → AI calls `get_psm_status` with `network=eth` and reports fee-in, fee-out, and whether swaps are enabled.
* “Show me available PSM liquidity for USDT on TRON” → AI calls `get_psm_metrics` with the PSM-USDT market and reports available amounts and fees for both directions.
* “Swap 10,000 USDT into USDD through the PSM” → AI uses `use_psm`: checks PSM status, then calls `psm_swap_to_usdd` and reports the transaction result.
* “Swap 5,000 USDD back to USDC on BSC” → AI calls `get_psm_status`, then executes `psm_swap_from_usdd` and reminds the user to re-check balances.

**Token & Balances**

* “What is my USDD balance on Tron?” → AI calls `get_protocol_overview` to identify the USDD token address, then calls `get_token_balance`.
* “Do I have enough allowance for the USDT PSM?” → AI calls `check_allowance` with the token and PSM spender, then suggests `approve_token` only if needed.
* “Send 100 USDD to TXxxx… on Tron” → AI calls `prepare_token_transfer` and displays the transfer preview (from, to, amount, balance). After the user confirms, AI calls `confirm_token_transfer` to execute.
* “Transfer 0.5 ETH to 0xabc…” → AI calls `prepare_token_transfer` for native ETH, presents the details, then waits for user approval before executing.

**USDD Savings**

* “What is the current USDD Savings status on Ethereum?” → AI calls `get_savings_status` and summarizes total assets, savings rate, and wallet shares.
* “Deposit 2,000 USDD into sUSDD” → AI uses `use_savings`: checks savings status, calls `deposit_savings`, then re-checks savings metrics.
* “Withdraw 500 USDD from sUSDD on BSC” → AI calls `get_savings_status`, executes `withdraw_savings`, and confirms the updated share balance.

**Protocol Analytics**

* “What are the overall USDD protocol metrics?” → AI calls `get_protocol_metrics` and reports total collateral, debt ceiling, and utilization.
* “Show me TRON chain metrics” → AI calls `get_chain_metrics` with `chain=tron` and summarizes collateral breakdown and USDD supply on TRON.
* “What are the latest collateral prices?” → AI calls `get_collateral_prices` and lists each collateral type with its current highest price.

**Treasury & Smart Allocator**

* “Show me the USDD treasury summary” → AI calls `get_treasury_summary` and reports reserve breakdown, collateral ratio, and recent changes.
* “How much JST has been bought back and burned?” → AI calls `get_jst_buyback_stats` and summarizes cumulative JST buyback volume and burn totals.
* “What is the Smart Allocator overview?” → AI calls `get_smart_allocator_overview` and reports total debt allocated, current invested amount, accumulated earnings, and APY.
* “Break down Smart Allocator investments by protocol” → AI calls `get_assets_breakdown` with `dimension=protocol` and lists each DeFi protocol with its allocated amount.
* “Show me the Smart Allocator proof of reserve” → AI calls `get_proof_of_reserve` and details each platform investment with amounts and verification status.
* “What does the Smart Allocator debt look like by network?” → AI calls `get_debt_overview` and summarizes debt positions grouped by TRON/ETH/BSC vaults.

### Architecture

```
mcp-server-usdd/
├── src/
│   ├── core/
│   │   ├── chains.ts
│   │   ├── abis.ts
│   │   ├── tools.ts
│   │   ├── prompts.ts
│   │   ├── resources.ts
│   │   ├── browser-signer.ts
│   │   └── services/
│   │       ├── clients.ts
│   │       ├── contracts.ts
│   │       ├── protocol.ts
│   │       ├── vault.ts
│   │       ├── psm.ts
│   │       ├── savings.ts
│   │       ├── tokens.ts
│   │       ├── transfer.ts        ← token/native transfer (prepare + confirm)
│   │       ├── treasury.ts        ← treasury report and JST buyback stats
│   │       ├── smart-allocator.ts ← Smart Allocator analytics
│   │       ├── website-metrics.ts ← protocol metrics, chain metrics, collateral prices
│   │       ├── wallet.ts
│   │       └── utils.ts
│   ├── index.ts
│   └── server/
│       ├── server.ts
│       └── http-server.ts
└── build/
```



<br>
