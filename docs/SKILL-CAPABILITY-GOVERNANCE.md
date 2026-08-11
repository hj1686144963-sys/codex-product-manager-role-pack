# Skill 能力说明与同类合并治理

本仓库中的每个受管 Skill 都必须同时具备可执行定义、机器路由短句和可追溯的能力说明。`SKILL.md` 是执行行为的唯一真相源，`skills/CATALOG.json` 是分类、来源、版本、风险和合并血缘的治理源；`skills/REGISTRY.json` 与 `docs/skill-capabilities/` 都由脚本生成，不得手工编辑。

## 分类体系

- `product.strategy`：产品价值、需求、交互状态与验收定义。
- `governance.decision`：高影响、多路径或证据冲突决策治理。
- `knowledge.memory`：本地知识检索、沉淀与跨会话连续性。
- `design.ui`：界面设计系统、视觉基线与体验约束。
- `engineering.motion`：Web 动效实现、框架集成与性能。
- `engineering.coding-efficiency`：需求锁定后的编码效率修饰。
- `productivity.task-management`：本地任务持久化、状态与协作关系。

分类只负责工作分工，不直接触发 Skill。Codex 的真实初筛仍依赖每个 `SKILL.md` 的 `name + description`；能力索引中的短句用于人和上层路由器快速扫描。

## 安装或下载 Skill

每次新增 Skill 必须在同一任务内完成：

1. 核验来源仓库、固定 commit 或版本、许可证和真实 Skill 路径。
2. 把源码放入 `skills/<name>/`，不得只登记名称。
3. 在 `skills/CATALOG.json` 登记：版本、状态、分类、风险、一句话能力、能力列表、来源和空的 `merged_from`。
4. 在 `evaluations/skill-routing-cases.json` 为它补齐正向、负向和近邻冲突用例。
5. 运行 `scripts/Generate-SkillRegistry.ps1` 与 `scripts/Generate-SkillCapabilityDocs.ps1`，生成 Registry、内容哈希、配套能力说明与索引。
6. 运行 Registry、路由夹具、Skill 结构、源与运行副本哈希核对。
7. 部署到官方用户级发现目录 `%USERPROFILE%\.agents\skills`；既有 `%USERPROFILE%\.codex\skills` 只作历史兼容。不得把备份或旧版本放在扫描目录内，也不得让两个同名副本同时被发现。
8. 把安装结果、验证证据和未验证事项写入当前项目与 Obsidian。

## 一句话机器路由

一句话必须说明：做什么、何时使用、何时不使用或应该转给哪个相邻 Skill。它不是宣传语，也不能只写“高效、专业、增强”等无法路由的词。

推荐格式：

> 当【可观察触发场景】时，执行【核心能力】并产出【结果】；不用于【相邻但不适用场景】。

## 同类 Skill 合并升级

合并产生的新 Skill 必须使用新名称或明确的新版本，并在 Catalog 中增加；Registry 随后自动生成：

- `merged_from`：所有来源 Skill 的名称和版本；
- `merge_notes`：保留、增强、删除和冲突处理；
- `successor`：旧 Skill 指向合并后的 Skill；
- 新的一句话能力、完整能力列表、分类、风险和来源；
- 正向、负向、近邻冲突和旧 Skill 回归测试。

旧 Skill 不立即删除。先标为 `deprecated`，验证新 Skill 能覆盖 Goodcase 且修复目标 Badcase 后，再由 Human 决定是否 `retired`。

## 自动生成

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Generate-SkillRegistry.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Generate-SkillCapabilityDocs.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Invoke-SkillGovernanceChecks.ps1
```

生成内容包括：分类、状态、风险、一句话路由、Codex 实际触发描述、核心能力、上游来源、固定版本、许可证、源码内容哈希、合并血缘、替代关系和完整 `SKILL.md` 位置。

路由用例校验只证明测试夹具完整，不等于模型命中率通过。真实上线前仍需在当前 Codex 版本上运行模型路由评测，并记录误触发、漏触发和近邻混淆。
