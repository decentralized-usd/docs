# GitHub 审核后发布

## 入口与责任

Alice（`aliceChuhT`）复核内容并将 GitHub PR 加入 `master` 合并队列。GitBook 仅负责编辑草稿、
渲染与托管；公开站点只连接正式空间。

| 用途 | GitBook 空间 | GitHub 分支 | 发布状态 |
| --- | --- | --- | --- |
| 编辑、评审草稿 | [Docs Draft - GitHub PR first](https://app.gitbook.com/o/SPOgHkiPCdlz2pdsJ32q/s/XQLoeyDuqEliLwaPC4Rn/) | `codex/gitbook-draft`（分支已创建，同步待连接） | 不连接公开站点 |
| 正式发布 | [Docs](https://app.gitbook.com/o/SPOgHkiPCdlz2pdsJ32q/sites/site_KNAO8/s/ARwMu8GsAubRHTakjdxU/) | `master` | [docs.usdd.io](https://docs.usdd.io/) |

两边仓库均为 `decentralized-usd/docs`，同步目录均为 `./usdd/en`。GitBook 旧连接可能显示
仓库旧名 `usdd-network/docs`，GitHub 已重定向到上述仓库。根目录维护文档不属于发布内容。

## 当前状态与未完成配置（2026-11-20）

- GitBook #63 已发布；Alice 合并的 [GitHub PR #3](https://github.com/decentralized-usd/docs/pull/3)
  已于 15:22（UTC+8）被正式空间导入，说明 GitHub → GitBook 链路正常。
- 独立草稿空间从当前正式内容复制；候选分支从同一版本 `0a4d738` 建立。
- 草稿 Git Sync 的设置页要求 Authenticate，目前未连接。既有正式同步连接继续保留。
- 正式空间只锁定了 live edits，仍可合并 change request。组织当前可见成员只有 Larry 管理员；
  普通空间角色不能限制组织管理员。Merge rules 页面提示需要升级套餐，尚未配置。
- GitHub `master` 已有合并队列、禁止删除和强推的规则；未配置必需安全检查。
  Alice 当前有 Write、没有 Admin。PR #1 的检查器和 CI 仍未合入。

**因此尚未满足“GitHub PR 合并前绝不发布”。仓库 PR 合并本身无法完成 GitBook 的授权或权限配置。**

## 完成配置的顺序

1. 为草稿空间完成 GitHub 连接授权，选 `codex/gitbook-draft` 和 `./usdd/en`。
   不修改正式连接，不授权 GitBook 绕过 `master` 保护。此前未同意新增 Alice OAuth；
   必须由账号负责人完成已有授权账号的连接，或另行明确确认新授权。
   初始同步前重新对比两端；仅在内容一致时从 GitHub 导入。存在未审核草稿时先保留差异。
2. 正式空间必须禁止日常账号合并 CR，同时允许 `master` 导入。
   可使用非管理员日常账号（正式空间只读，草稿空间有编辑/评审权限），管理员仅保留维护用途；
   或在支持 Merge rules 的套餐上设置正式空间拒绝直接 CR 合并，并实测 Git Sync 导入不受影响。
   继续使用 Larry 管理员日常编辑、仅降低默认空间角色，不能达到这个要求。
   新成员授权、付费升级均需另行确认，不能从仓库文件推断已经完成。
3. 如需由平台限制只有 Alice 能发起合并，仓库管理员须核对写权限及 ruleset：保持合并队列，
   不给 GitBook 或日常其他账号绕过权限。安全 CI 合入并验证后再设置准确的 required checks；
   CI 必须处理 `merge_group`，避免队列永远等待检查。Alice 的 Write 权限不能替代管理员配置。
4. 完成下述验收，记录验证 PR、合并 SHA、同步历史及公开页结果，再将 README 与本节状态更新为已启用。

## 日常操作

1. 在独立草稿空间编辑并合并 GitBook CR；确认候选分支同步成功，正式站点无变化。
2. 从 [候选分支对比页](https://github.com/decentralized-usd/docs/compare/master...codex/gitbook-draft?expand=1)
   创建到 `master` 的 PR，附草稿 CR 链接、页面范围、来源依据和附件验证。GitBook 不会自动创建该 PR。
3. Alice 核对差异和检查结果，加入合并队列。检查最终合并的提交，不能用旧预览代替最终内容审核。
4. 等待正式空间显示同步成功，在版本历史核对合并提交；检查对应公开页面与附件，确认发布完成。
5. 下轮编辑前将 `master` 的维护说明、回滚或其他直接 GitHub 变更合回候选分支，处理冲突后再编辑。
   保留尚未审核的草稿，不强推、不删除长期候选分支。

## 验收与故障处理

- 合并前：草稿空间不在任何公开站点结构中；草稿变更只到候选分支；GitHub PR 未合并时官网保持旧内容。
- 权限：日常账号不能在正式空间直接编辑、合并 CR 或恢复旧版本；如采用 Merge rules，确认规则确实阻止 CR。
  管理员可重新配置权限是管理边界，不能声称账号失陷后仍无法绕过。
- 合并后：由 Alice 合入一个实际审核过的内容 PR，核对 `master` SHA、GitBook 同步历史和公开页更新。
  不往官网加入测试占位文案来验收。
- 同步失败：保留当前线上版本，检查配置、账号权限和 GitBook 错误；不要在正式空间手工合并作为补救。
  PR 已合并但公开页未更新时，状态应报告为“已合入，发布待确认”。
- 回滚：基于 `master` 创建 revert PR，经 Alice 审核和队列合入，再验证正式空间同步与公开页恢复。
  随后同步回候选分支，避免下次草稿重带入已撤销内容。

机制依据：[GitBook 发布行为](https://gitbook.com/docs/getting-started/quickstart)、
[CR 与 GitHub PR 独立](https://gitbook.com/docs/docs-as-code/git-sync/troubleshooting)、
[角色权限](https://gitbook.com/docs/collaborate/member-management/roles)、
[管理员与权限继承](https://gitbook.com/docs/collaborate/member-management/permissions-and-inheritance)、
[Merge rules](https://gitbook.com/docs/collaborate/merge-rules)。
