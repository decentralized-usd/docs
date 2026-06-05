# USDD Skills

> AI Agent skills for the USDD stablecoin protocol. This package teaches agents how to query public analytics, inspect wallet-aware protocol state, and safely route Vault, PSM, and Earn writes through the official USDD MCP server.

This page describes the published USDD Skills package and its companion MCP server:

* Package: `@usdd/usdd-skills`
* Version: `1.0.0`
* License: MIT
* Repository: [decentralized-usd/usdd-skills](https://github.com/decentralized-usd/usdd-skills)
* Runtime: Node.js `>=20.0.0`
* Local analytics MCP: `scripts/mcp_server.mjs`
* CLI: `scripts/usdd_api.mjs`
* Write-capable MCP dependency: `@usdd/mcp-server-usdd`
* Official MCP repository: [decentralized-usd/mcp-server-usdd](https://github.com/decentralized-usd/mcp-server-usdd)

USDD Skills is a **Skills + MCP/CLI hybrid package**. It ships 4 Agent Skills, a local read-only analytics MCP server, CLI access to the same analytics layer, and install helpers for common MCP clients.

***

### Overview <a href="#id-2" id="id-2"></a>

#### What it is <a href="#id-3" id="id-3"></a>

USDD Skills provides structured instructions for agents using USDD across two MCP servers:

* **Analytics MCP** from this package: 14 read-only tools backed by public `openapi.usdd.io` endpoints.
* **Official MCP** from `@usdd/mcp-server-usdd`: wallet/network state, protocol reads, Vault/PSM/Savings writes, token transfers, treasury, and Smart Allocator tools.

The local analytics MCP never signs transactions and does not hold private keys. All write-capable workflows are delegated to the official MCP.

#### Who it is for <a href="#id-4" id="id-4"></a>

* Web3 users who want agent-assisted Vault, PSM, or Earn workflows.
* Analysts who need public USDD supply, APY, collateral, and Smart Allocator data.
* Agent and tooling builders integrating USDD into Claude Desktop, Claude Code, Cursor, Codex, project-level MCP configs, or compatible MCP hosts.

#### When not to use it <a href="#id-5" id="id-5"></a>

* Do not use it for unattended trading, liquidation bots, or automated transaction execution. Write skills require a fresh chat confirmation after prechecks.
* Do not use public analytics output as an oracle or settlement source. Analytics data is informational.
* Do not use this package to store or pass private keys. Wallet handling belongs to the official MCP and wallet tooling.
* Do not guess protocol addresses from docs or local tables. The skills require Chainlog-backed official MCP resolution.

***

### Which Mode to Use <a href="#id-6" id="id-6"></a>

<table><thead><tr><th width="266.4453125">You want to…</th><th width="222.984375">Use</th><th>Reason</th></tr></thead><tbody><tr><td>Compare Earn APY, supply, sUSDD supply, collateral history, public overview, Smart Allocator detail</td><td>Local Analytics MCP</td><td>Public, read-only, no wallet required</td></tr><tr><td>Run the same public analytics in a terminal or CI</td><td>CLI <code>scripts/usdd_api.mjs</code></td><td>Scriptable JSON output, no agent required</td></tr><tr><td>Read wallet balance, allowance, wallet address, Vault ownership, PSM status, Savings status</td><td>Official MCP</td><td>Requires live chain, wallet-aware, or current protocol state</td></tr><tr><td>Open/manage Vaults, swap through PSM, deposit/withdraw Savings</td><td>Official MCP via Skill workflow</td><td>Holds wallet context and performs writes</td></tr><tr><td>Transfer tokens</td><td>Official MCP token-transfer flow</td><td>Uses <code>prepare_token_transfer</code> -> user confirmation -> <code>confirm_token_transfer</code></td></tr></tbody></table>

Rule of thumb:

* Public dashboard analytics -> local analytics MCP or CLI.
* Wallet, current chain state, addresses, allowances, and all writes -> official MCP.

***

### Architecture <a href="#id-7" id="id-7"></a>

Two MCP servers are intentionally non-overlapping.

| Server           | Package/source                         | Role                                                                                      | Writes? |
| ---------------- | -------------------------------------- | ----------------------------------------------------------------------------------------- | ------- |
| `usdd-analytics` | This package, `scripts/mcp_server.mjs` | 14 read-only tools over public USDD API                                                   | No      |
| `usdd-full`      | `@usdd/mcp-server-usdd`                | Wallet/network state, on-chain reads, Vault/PSM/Savings writes, treasury, Smart Allocator | Yes     |

Agents must call the MCP tools. Skill workflows explicitly say not to fetch upstream API URLs directly.

***

### Requirements <a href="#id-8" id="id-8"></a>

| Requirement                       | Actual package behavior                                                                                                                                                               |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Node.js                           | Required `>=20.0.0`; setup rejects older Node versions                                                                                                                                |
| Package version                   | `@usdd/usdd-skills` version `1.0.0`                                                                                                                                                   |
| Official MCP                      | `@usdd/mcp-server-usdd` is installed by setup unless skipped                                                                                                                          |
| Local analytics dependencies      | `@modelcontextprotocol/sdk`, `dotenv`                                                                                                                                                 |
| Public analytics auth             | No API key required for the wrapped public analytics endpoints                                                                                                                        |
| RPC env keys                      | Optional keys are passed only to `usdd-full`: `TRONGRID_API_KEY`, `TRON_FULL_NODE`, `TRON_NILE_FULL_NODE`, `ETH_RPC_URL`, `ETH_SEPOLIA_RPC_URL`, `BSC_RPC_URL`, `BSC_TESTNET_RPC_URL` |
| Supported official MCP networks   | `tron`, `eth`, `bsc`, `tron_nile`, `eth_sepolia`, `bsc_testnet`                                                                                                                       |
| Local analytics chain args        | `tron`, `eth`, `bsc` for chain-scoped analytics tools                                                                                                                                 |
| Local analytics history intervals | `WEEKLY`, `MONTHLY`, `BIANNUAL`, `ANNUAL`                                                                                                                                             |

The local analytics MCP does not use a `NETWORK` value. Network selection for official MCP tools is passed in tool arguments as `network`.

***

### Installation <a href="#id-9" id="id-9"></a>

#### Recommended setup <a href="#id-10" id="id-10"></a>

The CLI exposes:

```bash
usdd-skills setup [options]
usdd-skills mcp-server
usdd-skills list-tools
```

Recommended GitHub package setup:

```bash
npx --yes \
  --package=git+https://github.com/decentralized-usd/usdd-skills.git \
  usdd-skills setup --yes
```

Current setup behavior:

* Checks Node.js v20+.
* Installs global `usdd-skills` and `@usdd/mcp-server-usdd`, unless `--skip-global-install` or `--dry-run` is used.
* Writes MCP config for selected clients with timestamped backups.
* Creates a skills symlink at `~/.agents/skills/usdd-skills`.
* Registers:
  * `usdd-analytics` -> `usdd-skills mcp-server`
  * `usdd-full` -> `mcp-server-usdd`

Supported setup clients:

```bash
usdd-skills setup --client project,claude-desktop,cursor,codex --yes
```

The special values are:

* `auto`: detect project plus existing Claude Desktop, Cursor, and Codex config locations.
* `all`: configure `project`, `claude-desktop`, `cursor`, and `codex`.

#### Dry run <a href="#id-11" id="id-11"></a>

Use dry run to inspect planned config writes without changing files:

```bash
usdd-skills setup --client all --dry-run --yes
```

#### Local checkout setup <a href="#id-12" id="id-12"></a>

```bash
git clone https://github.com/decentralized-usd/usdd-skills.git
cd usdd-skills
bash install.sh
```

Actual `install.sh` behavior:

* Checks Node.js v20+.
* Runs `npm install`.
* Installs global `@usdd/mcp-server-usdd`.
* Creates `.env` from `.env.example` if missing.
* Runs `node bin/usdd-skills.mjs setup --local-source --skip-global-install --yes`.

For project config with local source, setup writes a portable `.mcp.json` using `node` plus a relative `./scripts/mcp_server.mjs` path. User-level client configs use the current Node executable plus an absolute analytics script path.

#### Verify <a href="#id-13" id="id-13"></a>

```bash
usdd-skills list-tools
node scripts/usdd_api.mjs total-supply
npm test
```

Expected:

* `usdd-skills list-tools` prints the 14 analytics MCP tools.
* CLI commands print JSON on stdout.
* Tests run with `node --test scripts/*.test.mjs`.

#### Upgrade <a href="#id-14" id="id-14"></a>

```bash
usdd-skills setup --client codex --yes
```

For a local checkout, update the checkout first, then rerun `bash install.sh`.

#### Uninstall <a href="#id-15" id="id-15"></a>

The included `uninstall.sh` is intentionally narrow:

```bash
bash uninstall.sh
```

It must be run from the `@usdd/usdd-skills` project root. It removes local `node_modules` and `.env`, then prints that full removal requires deleting the directory.

To remove a user-level install, remove the skills symlink and uninstall the global packages:

```bash
rm ~/.agents/skills/usdd-skills
npm uninstall -g @usdd/usdd-skills @usdd/mcp-server-usdd
```

Also remove `usdd-analytics` and `usdd-full` from any MCP client configs that were configured.

***

### Client Configuration <a href="#id-16" id="id-16"></a>

Both MCP servers use stdio transport. After editing client config, fully restart the client.

#### Project-local `.mcp.json` <a href="#id-17" id="id-17"></a>

The portable template is:

```json
{
  "mcpServers": {
    "usdd-analytics": {
      "type": "stdio",
      "command": "node",
      "args": ["./scripts/mcp_server.mjs"],
      "env": {}
    },
    "usdd-full": {
      "type": "stdio",
      "command": "mcp-server-usdd",
      "args": [],
      "env": {}
    }
  }
}
```

Generated local `.mcp.json` files should not be committed.

#### Claude Desktop <a href="#id-18" id="id-18"></a>

Config path on macOS:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Minimal config shape:

```json
{
  "mcpServers": {
    "usdd-analytics": {
      "command": "usdd-skills",
      "args": ["mcp-server"]
    },
    "usdd-full": {
      "command": "mcp-server-usdd",
      "env": {
        "TRONGRID_API_KEY": "your_key_optional",
        "TRON_FULL_NODE": "your_tron_url_optional",
        "TRON_NILE_FULL_NODE": "your_nile_url_optional",
        "ETH_RPC_URL": "your_url_optional",
        "ETH_SEPOLIA_RPC_URL": "your_sepolia_url_optional",
        "BSC_RPC_URL": "your_url_optional",
        "BSC_TESTNET_RPC_URL": "your_bsc_testnet_url_optional"
      }
    }
  }
}

```

#### Claude Code <a href="#id-19" id="id-19"></a>

```bash
claude mcp add -s project usdd-analytics -- usdd-skills mcp-server
claude mcp add -s project usdd-full -- mcp-server-usdd
```

#### Cursor <a href="#id-20" id="id-20"></a>

Setup writes or merges:

```
~/.cursor/mcp.json
```

Use the same `mcpServers` shape as Claude Desktop.

#### Codex <a href="#id-21" id="id-21"></a>

Setup writes or merges:

```bash
~/.codex/mcp.json
```

Recommended:

```bash
npx --yes \
  --package=git+https://github.com/decentralized-usd/usdd-skills.git \
  usdd-skills setup --client codex --yes

```

Manual config shape is the same two-server `mcpServers` block shown above. Restart Codex after editing config.

Verify:

```bash
ls ~/.agents/skills/usdd-skills
usdd-skills list-tools
```

The skills directory should contain:

```
usdd-vault-v1/
usdd-psm-v1/
usdd-earn-v1/
usdd-analytics-v1/
```

#### OpenCode <a href="#id-22" id="id-22"></a>

The package includes an OpenCode plugin shim at:

```
.opencode/plugins/usdd-skills.js
```

That shim registers the 4 skills and the local `usdd-analytics` MCP server with:

```json
command: "node"
args: ["./scripts/mcp_server.mjs"]
```

The setup installer currently supports `project`, `claude-desktop`, `cursor`, and `codex` clients. It does not list `opencode` as a setup client option.

#### PATH fallback <a href="#id-23" id="id-23"></a>

If a desktop client cannot find `usdd-skills` or `mcp-server-usdd`, use an absolute command path or run local-source setup so the analytics MCP uses the current Node executable and an absolute script path for user-level configs.

***

### Skill Catalog <a href="#id-24" id="id-24"></a>

| Skill               | Scope                                                               | Writes? | Primary MCP dependency                                           |
| ------------------- | ------------------------------------------------------------------- | ------- | ---------------------------------------------------------------- |
| `usdd-vault-v1`     | Vault/CDP: open, deposit, mint, repay, withdraw, close, risk review | Yes     | Official MCP                                                     |
| `usdd-psm-v1`       | PSM stablecoin <-> USDD swaps                                       | Yes     | Official MCP                                                     |
| `usdd-earn-v1`      | Savings: deposit USDD -> sUSDD, withdraw USDD from sUSDD            | Yes     | Official MCP plus local analytics for APY/supply                 |
| `usdd-analytics-v1` | Public read-only analytics and routing                              | No      | Local analytics MCP, official MCP for current wallet-aware state |

#### Global routing rules <a href="#id-25" id="id-25"></a>

* Chain-dependent official MCP work requires an explicit `network` before any MCP tool call.
* Never default to TRON, mainnet, testnet, `set_network`, `get_network`, or a configured default when the user omitted the network.
* Protocol, token, Vault join, PSM, and Savings addresses must come from official Chainlog-backed tools: `get_protocol_addresses({ network })` or `get_chainlog_address({ network, key })`.
* Do not use local full-address tables or copy addresses from docs.
* If Chainlog resolution fails with TronGrid `429` or another RPC error and no cache is available, stop and ask the user to configure the relevant RPC or `TRONGRID_API_KEY`.
* Official write tools use the active MCP wallet and do not accept a `from` argument. Call `get_wallet_address({ network })` before confirmation.

***

### Tool Reference <a href="#id-26" id="id-26"></a>

#### Local Analytics MCP tools <a href="#id-27" id="id-27"></a>

<table><thead><tr><th width="250.203125">Tool</th><th width="208.8046875">Inputs</th><th>Description</th></tr></thead><tbody><tr><td><code>get_earn_apy</code></td><td>none</td><td>USDD Savings APY per chain</td></tr><tr><td><code>get_susdd_supply</code></td><td>none</td><td>sUSDD total supply by chain</td></tr><tr><td><code>get_usdd_supply</code></td><td>none</td><td>USDD supply by chain, excluding sUSDD</td></tr><tr><td><code>get_supply_history</code></td><td>none</td><td>Daily USDD and sUSDD supply time series</td></tr><tr><td><code>get_collateral_history</code></td><td>none</td><td>Daily protocol-wide collateral value by chain</td></tr><tr><td><code>get_circulating_supply</code></td><td>none</td><td>Raw USDD circulating supply number</td></tr><tr><td><code>get_total_supply</code></td><td>none</td><td>Raw USDD total supply number</td></tr><tr><td><code>get_public_protocol_overview</code></td><td>none</td><td>Public protocol overview with total supply, TVL, Earn TVL, APY fields</td></tr><tr><td><code>get_public_protocol_overview_info</code></td><td>none</td><td>Public overview with 24h change fields</td></tr><tr><td><code>get_public_dsr_apy</code></td><td>none</td><td>DSR APY current, average, and history</td></tr><tr><td><code>get_vault_collaterals</code></td><td>none</td><td>Public Vault collateral configuration list</td></tr><tr><td><code>get_latest_collateral</code></td><td><code>chain</code>: <code>tron</code>, <code>eth</code>, <code>bsc</code></td><td>Per-chain collateral snapshot</td></tr><tr><td><code>get_chain_collateral_history</code></td><td><code>chain</code>, <code>interval</code></td><td>Per-chain collateral history for <code>WEEKLY</code>, <code>MONTHLY</code>, <code>BIANNUAL</code>, <code>ANNUAL</code></td></tr><tr><td><code>get_smart_allocator_detail</code></td><td>none</td><td>Smart Allocator allocations, earnings, and vault info</td></tr></tbody></table>

Every local analytics response adds:

```json
{
  "_meta": {
    "dataTime": "ISO8601 fetch time",
    "source": "openapi.usdd.io"
  }
}
```

`dataTime` is the moment this package fetched the data, not necessarily the upstream record timestamp.

#### Official MCP tool groups used by skills <a href="#id-28" id="id-28"></a>

<table><thead><tr><th width="198.7109375">Group</th><th>Tools referenced by actual skills</th></tr></thead><tbody><tr><td>Wallet/network</td><td><code>get_supported_networks</code>, <code>set_network</code>, <code>get_network</code>, <code>connect_browser_wallet</code>, <code>set_wallet_mode</code>, <code>get_wallet_mode</code>, <code>get_wallet_address</code>, <code>list_wallets</code>, <code>import_wallet</code>, <code>set_active_wallet</code></td></tr><tr><td>Common preflight</td><td><code>get_native_balance</code>, <code>get_token_balance</code>, <code>check_allowance</code>, <code>approve_token</code></td></tr><tr><td>Protocol reads</td><td><code>get_protocol_addresses</code>, <code>get_chainlog_address</code>, <code>get_protocol_overview</code>, <code>get_supported_ilks</code>, <code>get_oracle_status</code>, <code>get_protocol_metrics</code>, <code>get_chain_metrics</code>, <code>get_collateral_prices</code></td></tr><tr><td>Vault</td><td><code>get_user_vaults</code>, <code>get_vault_summary</code>, <code>analyze_vault_risk</code>, <code>open_vault</code>, <code>deposit_and_mint</code>, <code>mint_usdd</code>, <code>repay_usdd</code>, <code>withdraw_collateral</code>, <code>close_vault</code></td></tr><tr><td>PSM</td><td><code>get_psm_status</code>, <code>get_psm_metrics</code>, <code>psm_swap_to_usdd</code>, <code>psm_swap_from_usdd</code></td></tr><tr><td>Savings</td><td><code>get_savings_status</code>, <code>deposit_savings</code>, <code>withdraw_savings</code></td></tr><tr><td>Token transfer</td><td><code>prepare_token_transfer</code>, <code>confirm_token_transfer</code></td></tr><tr><td>Treasury / allocator</td><td><code>get_treasury_summary</code>, <code>get_jst_buyback_stats</code>, <code>get_smart_allocator_overview</code>, <code>get_assets_breakdown</code>, <code>get_proof_of_reserve</code>, <code>get_debt_overview</code></td></tr></tbody></table>

For full schemas, use the official MCP documentation/source for `@usdd/mcp-server-usdd`.

***

### CLI Reference <a href="#id-29" id="id-29"></a>

The CLI mirrors the local analytics MCP and prints JSON to stdout.

```
node scripts/usdd_api.mjs <command> [args]
```

| Command                    | Args                 |
| -------------------------- | -------------------- |
| `earn-apy`                 | none                 |
| `usdd-supply`              | none                 |
| `susdd-supply`             | none                 |
| `supply-history`           | none                 |
| `collateral-history`       | none                 |
| `circulating-supply`       | none                 |
| `total-supply`             | none                 |
| `public-overview`          | none                 |
| `public-overview-info`     | none                 |
| `dsr-apy`                  | none                 |
| `vault-collaterals`        | none                 |
| `latest-collateral`        | `<chain>`            |
| `chain-collateral-history` | `<chain> <interval>` |
| `smart-allocator-detail`   | none                 |

Exit behavior:

* Success: exit `0`, JSON on stdout.
* Unknown command: command list on stdout, exit `1`.
* No command: command list on stdout, exit `0`.
* Error: `Execution Error: <message>` on stderr, exit `1`.

The CLI is read-only and never signs transactions.

***

### Agent Workflows <a href="#id-30" id="id-30"></a>

#### Workflow 1: Analytics APY comparison <a href="#id-31" id="id-31"></a>

User:

```
Which chain has the highest USDD Earn APY today?
```

Agent route:

1. Use `usdd-analytics-v1`.
2. Call local MCP `get_earn_apy`.
3. Compare returned chains.
4. Present the answer with the freshness footer.

Expected answer shape:

```
Highest Earn APY: <chain> at <apy>.
Other chains: <summary>.
Data time: <ISO8601> - Source: openapi.usdd.io
```

#### Workflow 2: Missing network for PSM write <a href="#id-32" id="id-32"></a>

User:

```
Swap 500 USDT to USDD.
```

Agent route:

1. Use `usdd-psm-v1`.
2. Because the user omitted network, ask which network before any MCP call.
3. Do not call `get_network`, `set_network`, `get_protocol_addresses`, or any other MCP tool until the user answers.

Expected response:

```
Which network should I use: tron, eth, bsc, tron_nile, eth_sepolia, or bsc_testnet?
```

#### Workflow 3: PSM write after network is explicit <a href="#id-33" id="id-33"></a>

User:

```
Swap 500 USDT to USDD on TRON.
```

Agent route:

1. Resolve `network="tron"`.
2. Use Chainlog-backed `get_protocol_addresses({ network: "tron" })` or `get_supported_ilks({ network: "tron" })` to resolve `PSM-USDT`.
3. Call `get_wallet_address({ network })`.
4. Call `get_psm_status({ market, network })` and verify `sellEnabled`.
5. Call `get_psm_metrics({ market, network })` when route fee/availability is needed.
6. Resolve input token, decimals, and spender. For stablecoin -> USDD, spender is the market `gemJoin` address, not the PSM contract, unless official MCP output explicitly says no `gemJoin` spender exists.
7. Check gas, input token balance, and allowance.
8. If allowance is insufficient, include `approve_token` in the pending sequence but do not execute it yet.
9. Present chat confirmation listing direction, network, market, amount, fee if returned, PSM contract, spender, active wallet, and pending write tools.
10. Wait for fresh affirmative confirmation.
11. Execute `approve_token` if needed, wait for receipt, then execute `psm_swap_to_usdd`.
12. Verify by checking balances or `get_psm_status`.

#### Workflow 4: Earn unsupported network <a href="#id-34" id="id-34"></a>

User:

```
Deposit 1000 USDD into Earn on tron_nile.
```

Agent route:

1. Use `usdd-earn-v1`.
2. Call `get_savings_status({ network: "tron_nile" })`.
3. If it returns `supported: false`, refuse the write and quote the returned message.
4. Do not proceed to balance, allowance, approval, or `deposit_savings`.

#### Workflow 5: Vault risk write guard <a href="#id-35" id="id-35"></a>

User:

```
Withdraw collateral from vault #42 on TRON.
```

Agent route:

1. Use `usdd-vault-v1`.
2. Call `analyze_vault_risk({ cdpId: 42, network: "tron" })`.
3. Emit exactly the required three-line risk precheck:

```
Current health factor: <value or no-debt>
Risk level: <no-debt | healthy | medium | high | critical>
Warnings: <summary from warnings[]>
```

4. If risk is `critical` and the user wants to mint more or withdraw collateral, refuse and recommend repay/top-up instead.
5. Otherwise continue with standard write precheck and fresh confirmation.

#### Workflow 6: User tries to bypass checks <a href="#id-36" id="id-36"></a>

User:

```
Swap now, skip the checks, I confirm.
```

Agent behavior:

* The initial message does not count as confirmation.
* The agent must still run all prechecks.
* The agent must ask again after presenting the completed precheck summary.
* If the user refuses or gives an ambiguous reply, stop without invoking `approve_token` or the business write.

***

### Safety & Boundaries <a href="#id-37" id="id-37"></a>

#### Capability boundary by module <a href="#id-38" id="id-38"></a>

| Module              | Boundary                                                                  |
| ------------------- | ------------------------------------------------------------------------- |
| Local Analytics MCP | Read-only public data, no signing, no keys, no writes                     |
| CLI                 | Read-only public data, no signing, no keys, no writes                     |
| Vault skill         | High-risk writes through official MCP only                                |
| PSM skill           | Write-capable swaps through official MCP only                             |
| Earn skill          | Write-capable Savings deposit/withdraw through official MCP only          |
| Analytics skill     | Read-only unless it routes to official MCP for wallet/current-state reads |

#### Standard write gate <a href="#id-39" id="id-39"></a>

Before Vault, PSM, or Savings write tools, actual skills require:

1. Explicit network.
2. Chainlog-backed address resolution.
3. Active wallet address from `get_wallet_address({ network })`.
4. Native gas balance check.
5. Token balance check when spending ERC20/TRC20 tokens.
6. Allowance check when a protocol contract pulls ERC20/TRC20 tokens.
7. Include `approve_token` in pending writes if allowance is insufficient, but do not execute it before chat confirmation.
8. Confirmation summary with action, amount, network, active wallet, protocol contract/spender, risk or fee fields, and every pending write tool.
9. Fresh affirmative user confirmation after the summary.
10. Execute pending writes in order.
11. Post-write verification.

Prompts like `skip the checks`, `just do it`, or `execute now` never bypass this gate.

#### TRON signing mode STOP <a href="#id-40" id="id-40"></a>

TRON operations may return a STOP message requiring signing-mode confirmation. When that happens:

1. Stop all other tool use.
2. Present the choices returned by the error:
   * Browser wallet: `connect_browser_wallet`
   * Agent wallet: `set_wallet_mode` with `mode="agent"`
3. Wait for explicit user choice.
4. Only then retry the original operation.

#### PSM direction specifics <a href="#id-41" id="id-41"></a>

| Direction          | Official tool        | `amount` means              | Spender          |
| ------------------ | -------------------- | --------------------------- | ---------------- |
| Stablecoin -> USDD | `psm_swap_to_usdd`   | Amount of market gem sold   | Market `gemJoin` |
| USDD -> stablecoin | `psm_swap_from_usdd` | Amount of market gem to buy | PSM contract     |

For `psm_swap_from_usdd`, if the user says “spend 100 USDD”, compute or ask for the target gem amount before calling the tool. Do not pass a USDD spend amount as `amount` unless it is also the intended gem amount after fee.

#### Vault risk specifics <a href="#id-42" id="id-42"></a>

* Existing-vault writes require `analyze_vault_risk` before standard write precheck.
* Official risk levels are `no-debt`, `healthy`, `medium`, `high`, and `critical`.
* If an agent presents a simplified label, it must map explicitly from `riskLevel`.
* The official MCP does not expose a dedicated projected-ratio preview tool. Any projected ratio must be labeled as an estimate from current `get_vault_summary`, `get_oracle_status`, and user-provided amounts.

#### Earn specifics <a href="#id-43" id="id-43"></a>

* Before any Earn write, call `get_savings_status({ network })`.
* If `supported: false`, refuse the write and quote the returned message.
* Deposit approval is USDD -> sUSDD contract from official MCP output.
* `withdraw_savings` requires chat confirmation even though no allowance is needed.

***

### Data & Privacy <a href="#id-44" id="id-44"></a>

#### Data this package reads <a href="#id-45" id="id-45"></a>

| Data type                                                                               | Source                              | Used by                                  |
| --------------------------------------------------------------------------------------- | ----------------------------------- | ---------------------------------------- |
| Public supply, APY, collateral, overview, Smart Allocator data                          | `openapi.usdd.io`                   | Local analytics MCP and CLI              |
| Wallet address, balances, allowances, Vault, PSM, Savings, treasury/current-state reads | Official MCP                        | Write-capable and wallet-aware workflows |
| RPC credentials                                                                         | User MCP config env for `usdd-full` | Official MCP only                        |

#### Data this package stores <a href="#id-46" id="id-46"></a>

The actual local analytics code does not implement a database, response cache, analytics event sink, or telemetry client. It fetches public API data and returns JSON with `_meta`.

Setup does write local configuration artifacts:

* MCP client config files such as project `.mcp.json`, `~/.cursor/mcp.json`, `~/.codex/mcp.json`, or Claude Desktop config.
* Timestamped backups of existing config files before overwriting.
* A symlink at `~/.agents/skills/usdd-skills`.
* For local checkout install, `.env` copied from `.env.example` if missing.

Generated config files and backups may contain RPC URLs or API keys if the user placed those values in environment variables or config. Treat them as sensitive local files.

#### Credentials and secrets <a href="#id-47" id="id-47"></a>

| Secret or credential                    | Where it belongs                                     | Notes                                                 |
| --------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| `TRONGRID_API_KEY`                      | `usdd-full` MCP env                                  | Recommended for live TRON reads/writes to avoid `429` |
| `TRON_FULL_NODE`, `TRON_NILE_FULL_NODE` | `usdd-full` MCP env                                  | Optional node overrides                               |
| `ETH_RPC_URL`, `ETH_SEPOLIA_RPC_URL`    | `usdd-full` MCP env                                  | Optional node overrides                               |
| `BSC_RPC_URL`, `BSC_TESTNET_RPC_URL`    | `usdd-full` MCP env                                  | Optional node overrides                               |
| Wallet/private-key material             | Official MCP/wallet tooling, not local analytics MCP | This package never signs transactions                 |

The local analytics MCP does not require API keys for the wrapped public endpoints.

Because MCP clients may log tool arguments, config, stderr, or process startup details depending on the client, do not put private keys in prompts or MCP tool arguments. Use the official wallet flow and the official MCP documentation for wallet setup.

#### Logs <a href="#id-48" id="id-48"></a>

Actual local logs are minimal:

* Local MCP startup writes `USDD analytics MCP server running on stdio.` to stderr.
* Fatal MCP errors are written to stderr.
* CLI failures are written as `Execution Error: <message>` to stderr.
* MCP tool failures return `isError: true` with `Error: <message>`.

The package does not implement log redaction. Avoid placing secrets in command arguments, prompts, or MCP config examples that may be copied into client logs.

#### Third-party data flow <a href="#id-49" id="id-49"></a>

* Local analytics requests go to `https://openapi.usdd.io`.
* Official MCP requests may use chain RPC endpoints and wallet integrations configured outside this package.
* The setup installer can run `npm install -g` for this package source and `@usdd/mcp-server-usdd`.

***

### Error & Reliability Contract <a href="#id-50" id="id-50"></a>

#### Local analytics MCP and CLI <a href="#id-51" id="id-51"></a>

The actual analytics client:

* Uses `https://openapi.usdd.io` as the default base URL.
* Retries each request up to 3 attempts with delays of `0`, `200`, and `600` ms.
* Applies a 10 second request timeout per attempt.
* Treats non-2xx HTTP responses as errors.
* Treats upstream JSON with `code != 0` as a business error.
* Rejects invalid numeric responses for `/totalSupply` and `/circulatingSupply`.
* Validates chain args as `tron`, `eth`, or `bsc`.
* Validates interval args as `WEEKLY`, `MONTHLY`, `BIANNUAL`, or `ANNUAL`.

Local analytics reads are idempotent and safe to retry.

#### Official MCP workflows <a href="#id-52" id="id-52"></a>

If an MCP returns `isError: true`, the skills require the agent to surface the error clearly and stop the workflow. The agent must not guess missing paths, markets, ilks, token decimals, contract addresses, or spender addresses.

#### Address resolution failure <a href="#id-53" id="id-53"></a>

When Chainlog-backed protocol address resolution fails with TronGrid `429` or another RPC error and no cache is available:

1. Stop the workflow.
2. Ask the user to configure `TRONGRID_API_KEY`, `TRON_FULL_NODE`, or the relevant chain RPC.
3. Do not fallback to `get_protocol_overview` just to discover addresses.
4. Do not guess addresses.

***

### Troubleshooting <a href="#id-54" id="id-54"></a>

| Symptom                                                 | Likely cause                                                     | Fix                                                                                                       |
| ------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `Node.js v20+ is required`                              | Node version is below 20                                         | Install Node.js 20+ and rerun setup                                                                       |
| MCP tools do not appear                                 | Client not fully restarted or config path wrong                  | Fully quit/reopen the client; inspect the configured MCP JSON                                             |
| Desktop client cannot find `usdd-skills`                | Client process has minimal `PATH`                                | Use local-source setup or absolute command paths                                                          |
| `usdd-skills list-tools` does not show 14 tools         | Analytics MCP startup/config issue                               | Run `usdd-skills list-tools`; from checkout run `node scripts/mcp_server.mjs --list-tools`                |
| CLI exits `1` with `Execution Error`                    | Network, timeout, invalid arg, or upstream business error        | Read the endpoint/status message and retry if it is transient                                             |
| `latest-collateral` rejects chain                       | Chain arg is not `tron`, `eth`, or `bsc`                         | Use one of the supported local analytics chains                                                           |
| `chain-collateral-history` rejects interval             | Interval arg is invalid                                          | Use `WEEKLY`, `MONTHLY`, `BIANNUAL`, or `ANNUAL`                                                          |
| Agent starts a write without network                    | Skill violation                                                  | Stop and ask for `tron`, `eth`, `bsc`, `tron_nile`, `eth_sepolia`, or `bsc_testnet` before any MCP call   |
| PSM market ambiguous                                    | User provided only a token symbol and multiple markets may match | Ask clarifying question or resolve only after explicit network with official protocol data                |
| PSM `psm_swap_from_usdd` amount feels wrong             | Official tool amount means gem amount to buy                     | Ask for or compute the target gem amount before calling the tool                                          |
| Allowance insufficient                                  | Protocol needs token approval                                    | Include `approve_token` in pending writes, show it in confirmation, execute only after fresh confirmation |
| User refuses confirmation or says “skip checks”         | Confirmation gate not satisfied                                  | Stop without invoking `approve_token` or business write                                                   |
| Savings returns `supported: false`                      | Savings not deployed/usable on that network                      | Refuse the write and quote the returned message                                                           |
| TronGrid `429` on live reads/writes                     | Public TRON RPC rate limit                                       | Configure `TRONGRID_API_KEY` or `TRON_FULL_NODE` in `usdd-full` env                                       |
| Chainlog address lookup fails and no cache is available | RPC/key issue                                                    | Configure the relevant RPC/key; do not guess addresses                                                    |
| Need per-ilk historical collateral data                 | Tool is not available                                            | Offer chain-level collateral history or current Vault/oracle reads instead                                |
| Setup overwrote existing MCP config                     | Setup creates timestamped backups                                | Restore from the `.bak-<timestamp>` file if needed                                                        |

Diagnostics:

```
usdd-skills list-tools
node scripts/usdd_api.mjs total-supply
npm test
```

***

### Versioning & License <a href="#id-55" id="id-55"></a>

<table><thead><tr><th width="264.04296875">Item</th><th>Current fact</th></tr></thead><tbody><tr><td>Package name</td><td><code>@usdd/usdd-skills</code></td></tr><tr><td>Package version</td><td><code>1.0.0</code></td></tr><tr><td>Repository</td><td><a href="https://github.com/decentralized-usd/usdd-skills">decentralized-usd/usdd-skills</a></td></tr><tr><td>Skill IDs</td><td><code>usdd-vault-v1</code>, <code>usdd-psm-v1</code>, <code>usdd-earn-v1</code>, <code>usdd-analytics-v1</code></td></tr><tr><td>Official MCP package</td><td><code>@usdd/mcp-server-usdd</code>, versioned independently</td></tr><tr><td>Official MCP repository</td><td><a href="https://github.com/decentralized-usd/mcp-server-usdd">decentralized-usd/mcp-server-usdd</a></td></tr><tr><td>Node engine</td><td><code>>=20.0.0</code></td></tr><tr><td>Package license field</td><td><code>MIT</code></td></tr><tr><td>SPDX identifier</td><td><code>MIT</code></td></tr><tr><td>Local changelog file</td><td>Not present in the actual package files reviewed for this document</td></tr></tbody></table>

Breaking changes to a skill should use a new skill ID suffix. The current package uses `-v1` suffixes.

***

### Known Limits <a href="#id-56" id="id-56"></a>

* No local analytics MCP tool named `get_ilk_collateral_history`.
* Public collateral history is keyed by `chain` and `interval`, not by Vault ilk.
* `get_supply_history` is supply-only; do not use it for collateral or Vault history.
* The official MCP does not expose a dedicated projected-ratio preview tool in the actual skill docs. Any projection must be labeled as an estimate.
* The setup installer supports `project`, `claude-desktop`, `cursor`, and `codex`; the package includes an OpenCode plugin shim, but `opencode` is not a setup client option.
* The local analytics MCP has no transaction signing, wallet state, balance, allowance, approval, or write capability.
* The local analytics MCP does not require a `NETWORK` env value.
