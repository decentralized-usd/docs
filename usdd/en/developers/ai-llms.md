# AI / LLMs

USDD provides machine-readable documentation endpoints optimized for LLMs and AI coding tools. Use these resources to give your AI assistant accurate, up-to-date context about the USDD protocol.

### Available Endpoints <a href="#available-endpoints" id="available-endpoints"></a>

<table><thead><tr><th width="186.625">File</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://docs.usdd.io/llms.txt">llms.txt</a></td><td>Curated index of key pages with one-line descriptions. Start here.</td></tr><tr><td><a href="https://docs.usdd.io/llms-full.txt">llms-full.txt</a></td><td>Complete documentation in plain Markdown, organized by section. Use when your tool supports large context.</td></tr></tbody></table>

> **Note:** Each documentation page is also available as plain Markdown by appending `.md` to any URL. Example: `https://docs.usdd.io/user-guide/psm-peg-stability-module.md`

### Which File Should I Use? <a href="#which-file-should-i-use" id="which-file-should-i-use"></a>

<table><thead><tr><th width="520.46484375">Use Case</th><th>Recommended</th></tr></thead><tbody><tr><td>Quick lookups, scoped questions</td><td><code>llms.txt</code></td></tr><tr><td>Full protocol understanding, complex integrations</td><td><code>llms-full.txt</code></td></tr><tr><td>Single-page deep dive</td><td><code>[page-url].md</code></td></tr></tbody></table>

### Add to Your AI Tool <a href="#add-to-your-ai-tool" id="add-to-your-ai-tool"></a>

#### Cursor <a href="#cursor" id="cursor"></a>

1. Navigate to **Cursor Settings > Features > Docs**
2. Select **Add new doc** and paste one of the following URLs:

```
https://docs.usdd.io/llms.txt
```

```
https://docs.usdd.io/llms-full.txt
```

3. Use `@docs → USDD` to reference the documentation in your chat.

#### Claude Code <a href="#claude-code" id="claude-code"></a>

Run in your terminal:

```bash
claude --add-docs https://docs.usdd.io/llms.txt
```

Or for full context:

```bash
claude --add-docs https://docs.usdd.io/llms-full.txt
```

#### Other Tools <a href="#other-tools" id="other-tools"></a>

Any tool that supports custom documentation URLs can use:

```
https://docs.usdd.io/llms-full.txt
```

Or for a lighter-weight index:

```
https://docs.usdd.io/llms.txt
```

### Coverage <a href="#coverage" id="coverage"></a>

The documentation covers all USDD 2.0 modules across Tron, Ethereum, and BNB Chain:

* **PSM** — 1:1 stablecoin swaps (Tron / Ethereum / BNB Chain)
* **Vault** — Over-collateralized USDD minting (Tron only)
* **Earn / sUSDD** — Yield-bearing savings (Tron / Ethereum / BNB Chain)
* **Liquidation & Auction** — Keeper integration and auction mechanics
* **Oracle** — Median → OSM → Spot price feed architecture
* **Core Contracts** — Vat, Dog, Clip, Jug, PSM module specs
* **Deployment Addresses** — All contract addresses across three chains
