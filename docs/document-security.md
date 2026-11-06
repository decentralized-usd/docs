# 文档安全校验

## 当前实现

Python 3.10+ 标准库脚本离线扫描候选文件，不联网、不执行文档命令、不导入候选树代码。

| 范围 | 检查 |
| --- | --- |
| 所有 Markdown，含 `legacy-usdd/` | 常见 GitHub/AWS 凭据、PEM 私钥、钱包私钥和部分凭据字面量；错误只报告位置与规则，不打印命中内容 |
| 当前 `usdd/en/`、维护 Markdown/SVG | HTTPS 与精确域名名单、URL 中凭据、危险 URL 协议、主动 HTML/事件属性、相对文件链接、地址文字与链接目标一致性 |
| 当前敏感页面 | 地址所在页面、安装指南及显式关键页面的完整 SHA-256；地址或同域路径被替换、字段位置被调换也会失败 |
| 当前附件 | 文件类型、文件存在性和完整 SHA-256；新附件、替换或删除都需审核基线 |
| 候选树 | 拒绝符号链接及越出仓库的路径 |

`security/doc-policy.json` 是域名与关键页面策略，`security/doc-baseline.json` 是人工审核清单。
初始基线取自事件前公开提交 `9dfffc07706f5a2eac824f663f018d9f2eea9842`。
初始 49 个公开页面的地址/外链、5 份审计 PDF 已与该版本对照；这不代表每个地址都重新做了链上验真。
`usdd/en/` 的 50 个 Markdown 包含目录文件，不能与公开页面数量混为一谈。

唯一 HTTP 例外是现有安装指南的本地健康检查地址；不能用它放行外部 HTTP 服务。
域名名单只比较精确 hostname，不接受通配符或后缀匹配。

## 命令与合法更新

```sh
python3 scripts/check_docs_security.py
python3 -I -m unittest discover -s tests -v
git diff --check
```

新域名、敏感文件或附件需先准备经过核实的候选内容，在本地生成候选基线：

```sh
python3 scripts/check_docs_security.py --refresh-baseline
```

此命令只生成待审核清单，不代表批准，且在 `CI` 环境下禁止运行。不得把刷新基线作为失败修复捷径。
提交前逐项解释哈希变化，提供部署记录、产品依据、审计方原件或经过验证的软件包版本。

PR 检查采用**目标分支**的脚本、策略和基线：同一个 PR 修改内容并改基线仍会被目标分支规则拒绝。
合法变更分两步：

1. 策略/基线 PR：保留原文内容，只提交 Alice 对照来源证据核实的未来域名/页面/附件哈希，并提供待变更内容或另一个草稿 PR 的链接。Alice 单独复核后合并，不要求他人 Approve 或 `BabelTTS` 逐次审批。
2. 内容 PR：包含对应内容与必要新增文件；基于更新后的目标分支重新运行检查，Alice 复核且检查通过后合并。

刷新会为已改文件同时保留旧/新两个已审核哈希；新增/计划删除文件列入 `optional_files` 过渡清单。
因此先合并基线 PR 时旧内容仍可通过，内容 PR 再使用新哈希。过渡仅接受这两个确切版本，不允许任意内容。
内容发布验证完成后运行以下命令，另提清理 PR，只保留当前哈希并恢复文件必需性；不能长期保留旧版本放行：

```sh
python3 scripts/check_docs_security.py --finalize-baseline
```

若内容 PR 取消，用 revert PR 撤回对应过渡基线。第三个版本必须在前一过渡清理后再审核。

## CI 信任边界与首次启用

`.github/workflows/docs-security.yml` 使用 `pull_request`，不用具有额外权限的目标上下文事件。
固定 checkout Action 的完整提交 SHA，使用 GitHub 托管的 `ubuntu-24.04` Runner，
仅授予 `contents: read`，不保留 checkout 凭据、不缓存、不读取 Secrets、不执行部署。
候选脚本回归测试只在该隔离环境执行。

首次引入此功能时目标分支还没有检查器，CI 会明确标记 **Bootstrap only**，使用候选检查器验证。
由 Alice 人工审阅工作流、脚本、基线、来源证据及回归测试，单人模式不要求他人 Approve；
首次绿色结果不能证明已经启用了平台门禁。
`BabelTTS` 一次性确认 `aliceChuhT` 的仓库 Write 权限，开启必要的 Actions 能力及首次 fork 运行审批。
若首个 PR 没有触发 CI，先由管理员检查 Actions 与 fork 审批配置；Alice 复核完整差异、运行本地验证并完成首次合并后，
从 `master` 执行 `workflow_dispatch` 验证真实 Runner 上的检查和测试，不能把 Checks 0 当成成功。
若合并前已有 CI 运行，须先排除真实失败；首次启用不用于绕过失败检查。
随后由 `BabelTTS` 要求通过 PR 合并、将 `docs-security` 设为 required check，启用分支保持最新及禁止绕过。
审批人数设为 0，不启用强制 Code Owner 审核、最新提交需他人批准或 Merge queue。后续运行、复核与发布由 Alice 完成。

工作流本身也能被 PR 修改或删除，`.github/`、`scripts/`、`security/`、`tests/` 和审核规范的改动需 Alice 逐项复核。
`CODEOWNERS` 仅列出 `aliceChuhT`，标记维护责任，不作为强制审批门禁；作者不能给自己的 PR 提交有效批准。
单人维护不提供独立审核，也不能阻止 Alice 账号失陷后修改工作流、策略或基线。基线与内容分开提交保留核对记录，
不能将它描述为双人控制。维护者变更时需同步更新名单、权限和平台验证。

## 限制

- 这是定向静态检查，不是完整 Markdown 渲染器、熵检测器或完整密钥扫描产品；例如自然语言助记词仍需人工/专用工具排查。
- 不验证 URL 重定向、远端内容、链接存活、链上状态或当前合约参数；上线前仍需对照来源证据复核。
- 不解析 PDF/PNG 内部内容；哈希只能发现相对已审核版本的变化，不能证明初始文件安全。
- 历史文档目前只做密钥特征检查；不是对所有历史外链的安全背书。
- CI 和 CODEOWNERS 不保护被供应商基础设施绕过的 GitBook 页面；见 [发布流程](publishing.md)。
- 本地修改检查器或策略会改变本地检查结果；可信结果必须来自受保护目标分支的 CI 与人工审核。
