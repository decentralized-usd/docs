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

GitBook 合并可能直接更新官网；GitHub 的 `master` 使用合并队列，两者是独立状态。
GitBook 当前向 `master` 直接推送会被队列规则拒绝，自动同步尚未恢复。
现阶段将已审核并发布的 GitBook 内容整理为独立 GitHub PR，由 Alice 复核后经队列合入。
PR 应记录 GitBook 变更链接、公开页面、核对结果及附件变化。

更换 GitBook 同步分支或连接账号需另外配置并核对授权；不能通过豁免保护规则修复同步。
重新连接时，落后的 GitHub 分支不能作为覆盖官网的初始同步来源。
回滚仓库使用 revert PR；若需回滚官网，须同时恢复 GitBook 已审核版本并检查公开页面。

不提交密钥、助记词、Token、生产配置或内部敏感端点。地址和操作入口须按网络核对官方来源，
静态文档审查不能替代链上验证或实际产品交易测试。
