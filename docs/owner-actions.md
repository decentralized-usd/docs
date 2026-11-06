# BabelTTS 一次性授权与保护配置

日常维护者仅为 `aliceChuhT`（Alice），自行复核、合并、发布与回滚，不要求 `tabufan` 获得 Write 权限，
也不要求其他人或 `BabelTTS` 逐次审批。本 PR 仅修改仓库文件，不会自动变更以下平台设置。
2026-11-06 已确认 Alice 的 Write 权限生效；现有 fork PR 可继续使用，无需重建。
当天核查 master 的 Active 规则仅包含禁止删除、禁止强推和 Merge queue，尚无必需审批或安全检查。

以下设置页需使用 `BabelTTS` 的 GitHub Owner 身份打开；若返回 404 或没有设置入口，先确认登录账号。
为减少 Owner 参与次数，Alice 先按第 4 步完成首次复核和 CI 验证，再请 BabelTTS 将第 3、5 步一次保存。
第 2 步仅在 Actions 实际受阻时处理；第 6 步属于供应商事件的一次性授权核查，不是每次发布前置审批。
不要在工作流尚未跑通时添加必需检查，避免首次启用被卡住。

## 1. 确认 Alice 的 Write 权限（已完成）

打开 [docs 仓库成员权限设置](https://github.com/decentralized-usd/docs/settings/access)，
导航为 **Settings → Collaborators & teams → Manage access**。

找到 `aliceChuhT`，确认 Role 为 **Write** 即可；不需要仓库 Admin、组织 Owner 或第二名 Write 维护者。
其他账号不因本流程扩大权限。

验收：Alice 可在原仓库创建分支、合并满足规则的 PR、运行已进入默认分支的工作流。
后续日常 PR 可直接从原仓库分支发起。

## 2. Actions 受阻时才处理（BabelTTS）

若 Actions 已能正常运行，无需为首次启用再找 Owner。
若工作流被禁用或等待管理员放行，打开 [Actions → General](https://github.com/decentralized-usd/docs/settings/actions)，核实以下设置：

- **Actions permissions**：选择允许组织内部及选定外部 Actions 的选项，启用 **Allow actions created by GitHub**，以运行 PR 使用的 `actions/checkout`；无需允许所有第三方 Actions。
- **Workflow permissions**：选择 **Read repository contents and packages permissions**。
- 不开启 **Allow GitHub Actions to create and approve pull requests**。
- 保留外部 fork 工作流审批限制；如 [PR #1](https://github.com/decentralized-usd/docs/pull/1) 显示待批准，审阅后批准首次运行。
- 若设置被组织策略锁定，在 [组织 Actions 设置](https://github.com/organizations/decentralized-usd/settings/actions) 核实并仅为必要范围放行，不为此放宽全部仓库。

本次工作流使用 GitHub 托管 Runner、完整 SHA 固定的 Action 和只读 token，不需要 Secrets 或生产网络访问。

## 3. 一次配置 master 保护（BabelTTS，首次 CI 成功后）

打开 [Rulesets 设置](https://github.com/decentralized-usd/docs/settings/rules)，编辑现有 `master` 规则集，
按下表及第 5 步一起保存；若该规则已不存在，再选择 **New ruleset → New branch ruleset** 创建，避免重复配置：

| 设置 | 值 |
| --- | --- |
| Ruleset name | 现有 `master`；新建时可用 `docs-master-protection` |
| Enforcement status | **Active** |
| Target branches | **Include by pattern**，填写 `master` |
| Bypass list | 留空，不给 GitBook App 或日常维护者 bypass |
| Require a pull request before merging | 开启 |
| Required approvals | **0** |
| Require review from Code Owners | 关闭 |
| Require approval of the most recent reviewable push | 关闭 |
| Require merge queue | 关闭；单人维护使用普通 PR 合并 |
| Restrict deletions | 开启 |
| Block force pushes | 开启 |

第 5 步的必需检查与本表在同一次操作中配置，不设置他人审批门槛。
其余规则按实际需要另行评估；不要启用 **Restrict updates** 把所有日常合并都限制成只能由 bypass 身份操作。

## 4. 首次复核、合并与 CI 验证（Alice）

1. Alice 复核 [PR #1](https://github.com/decentralized-usd/docs/pull/1) 的完整差异，核实检查器、策略、基线来源和工作流，执行 README 中三项本地验证后完成首次合并。单人模式无需他人 Approve。
2. 打开 [Actions 页面](https://github.com/decentralized-usd/docs/actions)，选择 **Documentation security**，确认任务 **docs-security** 绿色成功。
3. 若没有自动运行，在该工作流页面点击 **Run workflow**，Branch 选择 `master`，再点击运行。
4. 保存成功运行链接；**Checks 0 不算通过**。手动运行按钮要求工作流已进入默认分支，Write 权限即可操作，无需领导执行。

首次 PR 的目标分支尚无检查器，因此 Alice 的完整复核和本地验证不能省略。
若 CI 在合并前已运行，应先确认成功；首次启用流程不能用于绕过真实失败的检查。

## 5. 增加必需安全检查（BabelTTS）

首次 CI 成功后，在 [Rulesets 设置](https://github.com/decentralized-usd/docs/settings/rules) 中与第 3 步一次完成：

- 开启 **Require status checks to pass**，添加真实运行过的 **docs-security**；若可选来源，选择 **GitHub Actions**。
- 开启 **Require branches to be up to date before merging**。
- 保存，确认规则仍为 **Active**、目标仍为 `master`、Bypass list 仍为空，其他基础规则保持启用。
- 保持审批人数 **0**、强制 Code Owner 审核和最新提交需他人批准关闭；不设置另一人或领导的部署审批。

[PR 中的 CODEOWNERS](https://github.com/aliceChuhT/docs/blob/codex/docs-security-release-controls/.github/CODEOWNERS) 已配置：

```text
* @aliceChuhT
```

该文件仅标记维护责任，不作为强制审批门禁。GitHub 不允许作者批准自己的 PR，
所以不能同时要求 Alice 自己提交、自己 Approve；审批人数为 0 时，Alice 复核且安全检查通过即可合并。

## 6. 收紧 GitBook App 和生产资源授权（BabelTTS，按需协调运维）

打开 [组织 GitHub Apps 设置](https://github.com/organizations/decentralized-usd/settings/installations)，找到 **GitBook → Configure**：

1. 修改前保存当前 Permissions、Repository access 和授权仓库列表。
2. 有同步需求：**Repository access → Only select repositories → 仅选 docs → Save**。
3. 无同步需求：选择 **Suspend** 暂停访问，不因恢复服务默认重新授权。
4. 确认业务、合约、运维仓库不在范围；同步方向不是只读权限的证明。

同时核查 [仓库 Actions Secrets](https://github.com/decentralized-usd/docs/settings/secrets/actions)、
[组织 Actions Secrets](https://github.com/organizations/decentralized-usd/settings/secrets/actions) 和
[仓库 Runner 设置](https://github.com/decentralized-usd/docs/settings/actions/runners)：
确保文档仓库不继承业务生产凭据、不使用能访问生产内网的共享 Runner。
优先移除不应授予 docs 的访问范围，不要误删其他业务仍在使用的组织级密钥。

## 7. 验证规则生效（Alice）

使用测试 PR 留存以下结果，不在正式分支做破坏性测试：

- Alice 提交普通文档测试 PR，检查全部通过后，无需他人 Approve 即可合并；不为测试修改正式站点内容。
- 另一个测试 PR 新增非白名单外链，预期 `docs-security` 失败并阻止合并；测试内容不合入正式分支。
- PR 有新提交后，确认新版本重新运行检查，不能沿用旧版本的绿色结果；未成功时不能合并。
- 保存或导出规则配置，确认 master 要求 PR、安全检查且审批人数为 0；不通过实际直推 master 验证。
- 确认普通账号和 GitBook App 均不在 Bypass list；关闭未合并的负向测试 PR，清理对应测试分支。

GitBook 发布权限由其管理员另行一次性配置给 Alice 的实名账号，
验证 Alice 可完成编辑→复核→发布→线上复核，其他普通编辑者不能管理权限或直接发布。
套餐不支持的控制须记录缺口。GitHub Write 不会自动赋予 GitBook 发布权限，仓库检查也不能保护被供应商直接篡改的托管页面。

## 交由日常团队跟进

- Alice、研发和运维负责本次事件排查、凭据轮换、GitBook 整改、上线复核、告警与回滚演练。
- 调整 App 授权前保留原配置。2026-11-02 至 11-05 检查时刻的组织日志，若仅 Owner 可读，
  请一次性导出或配置合适的审计读取权限；团队负责分析，记录时区、覆盖范围与套餐造成的日志缺口。
- 独立静态站/CDN、受保护部署和监测由维护者与运维另提实施 PR，不作为领导日常审核任务。
- 若维护者调整或离职，另行更新授权、CODEOWNERS 与验证；单人维护仍不开放 App bypass。

单人模式没有第二人复核，不能阻止 Alice 账号失陷后修改工作流、策略或基线；CI 也不能保护被 GitBook 基础设施直接篡改的托管页面。

配置完成请回传：执行人 / 验证时间 / 配置截图 / 成功 CI 链接 / CI 放行与阻断验证结果 / 剩余缺口。

## 官方参考

- [成员权限管理](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-teams-and-people-with-access-to-your-repository)
- [Actions 配置](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- [Rulesets 配置](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- [Code Owners 权限与生效范围](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [手动运行工作流](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
- [GitHub App 授权范围](https://docs.github.com/en/apps/using-github-apps/reviewing-and-modifying-installed-github-apps)
