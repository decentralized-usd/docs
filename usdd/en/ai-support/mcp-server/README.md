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

* **Balances**: ERC20 / TRC20 token balances across TRON, Ethereum, and BNB Smart Chain
* **Allowances**: Read token allowance for any spender, compare against a required amount for USDD protocol interactions
* **Approvals**: Approve token spending for USDD protocol interactions
* **Protocol Discovery**: Configured contract addresses, collateral types (ilks), PSM joins, and debt ceilings per network
* **Wallet**: Configured signing address resolution per network
* **Networks**: Supported network list with chain keys (`tron`, `eth`, `bsc`)

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

The server supports two signing modes:

* **Browser mode (recommended)**: connect a TronLink-compatible browser wallet and sign in browser.
* **Agent mode**: Encrypted local wallet via `set_wallet_mode` with `mode="agent"` — keys stored in `~/.agent-wallet/`.

For TRON writes, each Claude session shows a one-time signing-mode confirmation reminder before the first write.

You can also manage wallets via **CLI** or **MCP tools**:

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

**MCP Tools (runtime)**

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

```
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

```
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

```
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

#### Wallet & Network<br>

<table><thead><tr><th width="229.76953125">Tool</th><th width="450.47265625">Description</th><th>Write?</th></tr></thead><tbody><tr><td><code>get_supported_networks</code></td><td>List supported networks</td><td>No</td></tr><tr><td><code>set_network</code></td><td>Set default network for one family (<code>tron</code>/<code>eth</code>/<code>bsc</code>), supports aliases like <code>mainnet</code>, <code>nile</code></td><td>Yes</td></tr><tr><td><code>get_network</code></td><td>Get per-family default networks</td><td>No</td></tr><tr><td><code>get_wallet_mode</code></td><td>Get active wallet signing mode (<code>agent</code>/<code>browser</code>)</td><td>No</td></tr><tr><td><code>set_wallet_mode</code></td><td>Switch active signing mode</td><td>Yes</td></tr><tr><td><code>connect_browser_wallet</code></td><td>Connect a browser wallet and activate browser mode</td><td>Yes</td></tr><tr><td><code>get_wallet_address</code></td><td>Show current address for the target network</td><td>No</td></tr><tr><td><code>list_wallets</code></td><td>List wallets and per-family active pointers (<code>tron</code>/<code>evm</code>)</td><td>No</td></tr><tr><td><code>set_active_wallet</code></td><td>Switch active wallet by ID (supports optional <code>walletType</code>)</td><td>Yes</td></tr><tr><td><code>import_wallet</code></td><td>Import private key/mnemonic into encrypted local store</td><td>Yes</td></tr></tbody></table>

#### Common

<table><thead><tr><th width="229.9140625">Tool</th><th width="450.203125">Description</th><th>Write?</th></tr></thead><tbody><tr><td><code>get_protocol_overview</code></td><td>Show configured protocol addresses, ilks, PSMs, and ceilings</td><td>No</td></tr><tr><td><code>get_supported_ilks</code></td><td>List configured collateral types and PSM joins</td><td>No</td></tr><tr><td><code>get_native_balance</code></td><td>Read native balance (<code>TRX</code> / <code>ETH</code> / <code>BNB</code>)</td><td>No</td></tr><tr><td><code>get_token_balance</code></td><td>Read ERC20/TRC20 balance</td><td>No</td></tr><tr><td><code>check_allowance</code></td><td>Read ERC20/TRC20 allowance and compare against an optional amount</td><td>No</td></tr><tr><td><code>approve_token</code></td><td>Approve token allowance</td><td>Yes</td></tr></tbody></table>

#### Vault

<table data-header-hidden><thead><tr><th width="229.890625"></th><th width="454.9296875"></th><th></th></tr></thead><tbody><tr><td>Tool</td><td>Description</td><td>Write?</td></tr><tr><td><code>get_oracle_status</code></td><td>Inspect oracle and liquidation configuration for an ilk</td><td>No</td></tr><tr><td><code>get_user_vaults</code></td><td>List vault IDs for a wallet</td><td>No</td></tr><tr><td><code>get_vault_summary</code></td><td>Show collateral, debt, and liquidation metrics</td><td>No</td></tr><tr><td><code>analyze_vault_risk</code></td><td>Summarize risk with warnings</td><td>No</td></tr><tr><td><code>open_vault</code></td><td>Open a new vault via DSProxy</td><td>Yes</td></tr><tr><td><code>deposit_and_mint</code></td><td>Open-and-mint or add collateral and mint</td><td>Yes</td></tr><tr><td><code>mint_usdd</code></td><td>Draw more USDD from a vault</td><td>Yes</td></tr><tr><td><code>repay_usdd</code></td><td>Repay vault debt</td><td>Yes</td></tr><tr><td><code>withdraw_collateral</code></td><td>Withdraw collateral from a vault</td><td>Yes</td></tr><tr><td><code>close_vault</code></td><td>Wipe all debt and free collateral</td><td>Yes</td></tr></tbody></table>

#### PSM

<table data-header-hidden data-full-width="false"><thead><tr><th width="229.89453125"></th><th width="455.41796875"></th><th width="242.421875"></th></tr></thead><tbody><tr><td>Tool</td><td>Description</td><td>Write?</td></tr><tr><td><code>get_psm_status</code></td><td>Inspect PSM fees and enablement</td><td>No</td></tr><tr><td><code>psm_swap_to_usdd</code></td><td>Swap gem into USDD</td><td>Yes</td></tr><tr><td><code>psm_swap_from_usdd</code></td><td>Swap USDD into gem</td><td>Yes</td></tr></tbody></table>

#### USDD Savings

<table data-header-hidden><thead><tr><th width="229.75"></th><th width="454.59375"></th><th></th></tr></thead><tbody><tr><td>Tool</td><td>Description</td><td>Write?</td></tr><tr><td><code>get_savings_status</code></td><td>Show USDD Savings metrics</td><td>No</td></tr><tr><td><code>deposit_savings</code></td><td>Deposit USDD into <code>sUSDD</code></td><td>Yes</td></tr><tr><td><code>withdraw_savings</code></td><td>Withdraw USDD from <code>sUSDD</code></td><td>Yes</td></tr></tbody></table>

### Prompts

<table data-header-hidden><thead><tr><th width="230.25"></th><th></th></tr></thead><tbody><tr><td>Prompt</td><td>Description</td></tr><tr><td><code>open_usdd_vault</code></td><td>Open a vault and verify post-trade risk</td></tr><tr><td><code>manage_vault_lifecycle</code></td><td>Run full vault lifecycle flows</td></tr><tr><td><code>use_psm</code></td><td>Use PSM with fee checks</td></tr><tr><td><code>use_savings</code></td><td>Use USDD Savings with inspection and verification</td></tr><tr><td><code>review_vault_risk</code></td><td>Explain risk for a vault</td></tr><tr><td><code>repay_and_close_vault</code></td><td>Repay and close with verification</td></tr></tbody></table>

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
│   │   └── services/
│   │       ├── clients.ts
│   │       ├── contracts.ts
│   │       ├── protocol.ts
│   │       ├── vault.ts
│   │       ├── psm.ts
│   │       ├── savings.ts
│   │       ├── tokens.ts
│   │       ├── wallet.ts
│   │       └── utils.ts
│   ├── index.ts
│   └── server/
│       ├── server.ts
│       └── http-server.ts
└── build/
```

### Notes

* Vault writes assume the configured wallet can sign on the target chain.
* ERC20/TRC20 flows often require `approve_token` first.
* TRON, ETH, and BSC deployments have similar USDD protocol structure but different addresses and token decimals.
* This version intentionally excludes migration and auction actions so we can iterate the Vault + PSM + Savings core first.

### Security Considerations

* Private keys are encrypted and stored locally in `~/.agent-wallet/`.
* Private keys are never returned by MCP tools.
* The optional `AGENT_WALLET_PASSWORD` is intended for automation and CI environments.
* Write operations should be treated as state-changing actions and reviewed carefully before execution.
* Vault prompts include risk-review steps so borrowing decisions are checked against current collateral health.
* Test on a safe environment or with small amounts before using mainnet-sized positions.
* Be cautious with large or unlimited token approvals when using `approve_token`.
* Never share local MCP client configuration files if they contain private keys or sensitive RPC credentials.

### Example Conversations

* "What vault types are available on Ethereum?" -> AI calls `get_supported_ilks` with `network=eth` and summarizes the supported vault collateral types.
* "Open a TRX-A vault on Tron and mint 500 USDD" -> AI uses `open_usdd_vault`: checks wallet, reviews oracle status, executes `deposit_and_mint`, then verifies the new vault risk.
* "Am I close to liquidation on vault 123?" -> AI calls `get_vault_summary` and `analyze_vault_risk`, then explains the health factor and collateral buffer.
* "Repay part of my vault debt on BSC" -> AI uses `manage_vault_lifecycle` with `action=repay`: checks USDD balance and allowance, calls `repay_usdd`, then verifies the updated vault state.
* "Close my vault and withdraw the collateral" -> AI uses `repay_and_close_vault`: checks debt, balance, allowance, calls `close_vault`, then confirms the vault state after repayment.
* "What are the current PSM fees on Ethereum?" -> AI calls `get_psm_status` with `network=eth` and reports fee-in, fee-out, and whether swaps are enabled.
* "Swap 10,000 USDT into USDD through the PSM" -> AI uses `use_psm`: checks PSM status, then calls `psm_swap_to_usdd` and reports the transaction result.
* "Swap 5,000 USDD back to USDC on BSC" -> AI calls `get_psm_status`, then executes `psm_swap_from_usdd` and reminds the user to re-check balances.
* "What is my USDD balance on Tron?" -> AI calls `get_protocol_overview` to identify the USDD token address, then calls `get_token_balance`.
* "Do I have enough allowance for the USDT PSM?" -> AI calls `check_allowance` with the token and PSM spender, then suggests `approve_token` only if needed.
* "What is the current Savings status on Ethereum?" -> AI calls `get_savings_status` and summarizes `chi`, `dsr`, total assets, and wallet shares.
* "Deposit 2,000 USDD into sUSDD" -> AI uses `use_savings`: checks savings status, calls `deposit_savings`, then re-checks savings metrics.
* "Withdraw 500 USDD from sUSDD on BSC" -> AI calls `get_savings_status`, executes `withdraw_savings`, and confirms the updated share balance.



<br>

<br>
