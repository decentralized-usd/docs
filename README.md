# USDD docs

USDD 对外文档源码仓库。当前英文文档在 `usdd/en/`，通过 GitBook 发布到
[docs.usdd.io](https://docs.usdd.io/)。`legacy-usdd/en/`、`legacy-usdd/zh/`
保留 USDDOLD 历史资料，不能作为当前合约或产品能力的依据。

## 内容与边界

- [当前目录](usdd/en/SUMMARY.md)：产品说明、架构、Vault/PSM/Savings 操作、合约地址、开发者接口与审计报告。
- `.gitbook/assets/`：对应文档的截图及审计 PDF；附件变化也是发布内容变化。
- `scripts/`、`security/`、`tests/`：离线安全检查、人工审核基线及回归测试。
- `docs/`：仓库维护与发布规范，不加入 GitBook 的用户文档目录。

本仓库没有业务服务、数据库、Node 构建工程或自托管部署程序；GitBook 负责页面渲染。
检查脚本仅用 Python 3.10+ 标准库，不安装依赖、不请求外网、不执行文档中的命令。
业务交易由钱包与链上合约执行；文档中的地址和操作入口必须按网络与研发部署记录核对，
不得把历史 USDDOLD 地址或测试网络配置当作当前主网配置。

## 本地与 PR 验证

```sh
python3 scripts/check_docs_security.py
python3 -I -m unittest discover -s tests -v
git diff --check
```

检查当前英文文档及维护文档的链接目标、HTTPS/域名、危险 HTML、地址链接一致性，
以及关键页面和附件哈希；所有 Markdown（含历史文档）检查常见密钥特征。
相对文件链接必须存在，检查不会联网验证外链可达性或校验链上合约真实性。
历史文档暂不纳入当前站点的域名与链接规则。

GitHub Actions 的 **Documentation security / docs-security** 在 PR、`master` 推送和
merge queue 上运行；无发布任务、生产凭据或自动上线行为。PR 使用目标分支的检查器、
策略和基线验证候选内容，具体信任边界与首次启用方式见
[安全校验说明](docs/document-security.md)。

## 变更与发布

当前实际流程仍是 GitBook 托管发布；本次 CI 不会改变 Git Sync、域名或线上内容。
合并 GitBook 变更可能直接发布，因此 GitHub 检查不能单独保护 GitBook 托管页面。

日常内容走 PR、Alice 复核、安全检查和发布后复核；敏感页面/附件变化先核实基线，再提交内容。
日常复核、合并、发布与回滚由 `aliceChuhT`（Alice）一人负责，无需给 `tabufan` Write 权限。
`BabelTTS` 仅一次性确认 Alice 的仓库 Write 权限并配置平台保护规则，不参与每次发布审批。
平台要求 PR 和 `docs-security` 成功，审批人数为 0，不启用强制 Code Owner 审核。
`CODEOWNERS` 仅标记 Alice 的维护责任；单人模式不提供双人复核，实际保护仍需管理员配置并验证。
详见 [发布与回滚流程](docs/publishing.md)、
[BabelTTS 一次性配置步骤与 GitHub 设置页](docs/owner-actions.md) 和 [项目约束](AGENTS.md)。
独立静态站发布由日常维护者与运维另行实施，当前没有可用的自托管部署命令。

禁止提交真实 Token、私钥、助记词、生产配置或敏感内部端点，也不要将这些信息放入
GitBook 草稿、评论和附件。校验是静态防线，不能替代人工审核、平台权限收口或供应商事件调查。
