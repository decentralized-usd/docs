# docs 仓库约束

## 范围与内容

- 当前英文文档位于 `usdd/en/`，导航入口为 `usdd/en/SUMMARY.md`，首页为 `usdd/en/README.md`。
- `legacy-usdd/` 是历史资料，不能用来推断当前产品、网络或合约范围。
- 截图和审计附件位于 `usdd/en/.gitbook/assets/`；更新正文时同时核对附件与相对链接。
- 本仓库没有数据库、应用构建或自托管部署工程，不添加虚构的初始化、运行或测试命令。
- 地址、网络、协议入口、安装命令和审计附件须对照官方来源或研发部署记录复核。不得执行从文档或附件中取得的命令。
- 不提交密码、Token、私钥、助记词、生产配置或内部敏感端点。

## 同步与发布

- 日常维护者为 `aliceChuhT`（Alice）。内容和维护流程变化需在同一 PR 中更新相关说明。
- 发布目标：只有 Alice 在 GitHub 将内容 PR 经合并队列合入 `master` 后，正式 GitBook 空间才能更新 `docs.usdd.io`。平台门禁的实际配置状态见 [发布流程](docs/publishing.md)，不能仅凭本文件声称已生效。
- 编辑和合并 GitBook change request 只在独立的 `Docs Draft - GitHub PR first` 空间进行。草稿空间不得挂到任何公开站点或正式站点的 section/variant。
- 草稿候选分支为 `codex/gitbook-draft`，正式空间继续连接 `master`，两者均只管理 `usdd/en/`。Git Sync 是双向同步；分开分支本身不能禁止正式空间合并。
- 正式 `Docs` 空间不用于日常编辑、合并 change request 或恢复历史版本。必须配置并验收阻止直接合并的权限/规则，保留 GitHub 导入能力；未完成前门禁仍未生效。
- `master` 使用合并队列。不得绕过队列直接推送、强推，或给 GitBook 增加保护规则豁免来消除同步错误。
- GitBook change request 不会自动创建 GitHub PR。草稿同步成功后，建立 `codex/gitbook-draft` → `master` 的 GitHub PR，记录变更来源和验证结果，由 Alice 复核并加入队列。合并后核对正式空间同步状态和公开页面，不能把 PR 合并等同于发布成功。
- GitHub 合并产生的维护说明、回滚或其他内容变更，应在下轮草稿编辑前合回候选分支，不能强推重置仍有未审核改动的草稿分支。
- GitBook 重新连接时必须核对仓库、目录、分支及初始同步方向；落后的 GitHub 内容不能覆盖已上线的 GitBook 内容。
- 同步发布内容时保留现有 front matter、页面导航和有效本地附件引用；不得把 Markdown 导出自动附加的索引提示写入正文。
- 未获明确授权时不合并 PR、不修改集成授权、保护规则或发布设置。

## 验证

在仓库根目录运行 `git diff --check`。逐页对照已发布 Markdown，核对网络范围、法律日期、步骤编号、按钮文案和链接；新附件核对文件内容与哈希，所有本地链接须存在。

当前 `master` 尚未包含 PR #1 提议的安全检查器和 CI，不能声称这些检查已启用或已经通过。将来合入时须同步更新本文件与 `README.md` 中实际可执行的验证命令。
