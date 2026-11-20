# USDD docs

USDD 对外文档源码，通过 GitBook 发布到 [docs.usdd.io](https://docs.usdd.io/)。
当前英文文档入口是 [导航目录](usdd/en/SUMMARY.md) 和 [首页](usdd/en/README.md)；
`legacy-usdd/en/`、`legacy-usdd/zh/` 保留历史资料，不代表当前产品或网络支持范围。

## 内容与目录

- `usdd/en/introduction/`、`system-architecture/`：产品、网络范围、协议架构和 sUSDD 机制。
- `usdd/en/user-guide/`：Vault 抵押与铸币、偿还与提取、清算与拍卖、PSM 兑换及 Savings 操作。各功能和参数以对应网络指南及当前应用为准。
- `usdd/en/developers/`：合约接口、部署地址、预言机和公开 API。
- `usdd/en/legals/`、`security/`：用户条款、隐私政策、安全说明和审计资料。
- `usdd/en/.gitbook/assets/`：页面截图和审计附件；正文与附件共同构成发布内容。

Vault 通过抵押品支持 USDD 债务，偿还债务后可提取抵押品；抵押率不足时可能进入清算与拍卖。
PSM 提供稳定币兑换，sUSDD 收益体现在每份 sUSDD 可兑换的 USDD 数量中。
具体支持网络、费率和限制见对应指南，不从历史文档推断当前业务规则。

## 维护与验证

使用 Git 编辑 Markdown，GitBook 负责渲染和托管。本仓库没有应用服务、数据库、依赖安装、
本地构建或自托管部署工程。维护约束见 [AGENTS.md](AGENTS.md)。

```sh
git diff --check
```

同步时逐页对照已发布 Markdown，保留 front matter 和导航，核对本地附件引用、网络范围、
法律日期、步骤和链接。新附件应核对内容及哈希。PR #1 提议的安全检查器与 CI 尚未合入
当前 `master`，因此没有可声称已启用的自动安全门禁。

## 发布与已知限制

目标流程是：未发布的 GitBook 草稿空间 → `codex/gitbook-draft` → GitHub PR →
Alice 复核并通过合并队列合入 `master` → 正式 GitBook 空间同步 → `docs.usdd.io`。
GitBook 草稿合并不会自动创建 GitHub PR；待同步连接完成后使用
[候选分支对比入口](https://github.com/decentralized-usd/docs/compare/master...codex/gitbook-draft?expand=1) 建立 PR。

**当前仍在配置，不能视为发布门禁已生效。** 独立草稿空间和候选分支已创建；正式空间
已成功导入 Alice 合并的 PR #3。草稿 Git Sync 尚待连接，正式空间仍缺少禁止直接合并的
平台限制。GitBook 向 `master` 直接推送会被队列拒绝，但这不会阻止正式空间先发布。
日常内容修改从现在起只在草稿空间或 GitHub 分支中准备，勿在正式空间合并。

空间入口、配置参数、剩余权限依赖、验收和回滚步骤见 [发布流程](docs/publishing.md)。
不通过 GitBook 豁免规则修复同步，不用落后的 GitHub 内容覆盖官网，不在正式站点测试草稿。
回滚同样走 revert PR，由 Alice 合入 `master` 后等待正式空间同步并检查公开页面。

不提交密钥、助记词、Token、生产配置或内部敏感端点。地址和操作入口须按网络核对官方来源，
静态文档审查不能替代链上验证或实际产品交易测试。
