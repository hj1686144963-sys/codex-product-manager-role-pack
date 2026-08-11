---
name: codex-auto-memory
description: Automatically continue work across Codex chats by using local Memories, selectively retrieving a configured Markdown or Obsidian knowledge base, and safely writing back durable decisions, methods, project state, Goodcase, Badcase, and anti-regression lessons. Use when a task refers to prior work, an existing project, remembered preferences, a knowledge base, repeated mistakes, role growth, postmortems, self-growing knowledge, cross-chat continuity, memory setup, memory diagnosis, or plugin installation and verification.
---

# Codex 自动记忆

## 核心流程

1. 读取 `~/.codex/codex-self-growing-memory.json`，确认知识库路径和检索上限。
2. 使用已注入的 Codex Memories 识别历史偏好、项目、决策、错误和未完成事项。
3. 先根据任务关键词、文件名、目录、元数据和更新时间筛选知识文件，再读取少量相关段落。
4. 当前用户指令、当前文件和可验证事实优先于历史记忆。
5. 任务产生稳定的新知识时，先查重，再更新原文件或正确的项目记录。
6. 只在本轮确有长期价值时写入；不要为普通问答制造知识垃圾。
7. 用户未确认的身份、岗位、工作、输出或偏好写为“待确认”或“未知”，禁止推断；个人与公共资产只生成候选，不自动晋升。

## 读取规则

- 优先读取 Vault 根目录的 `00_全局控制台.md`、就近的 `AGENTS.md`、相关索引和最近项目日志。
- 禁止一开始逐篇读取全部正文。
- 没有标题、路径、关键词或时间相关性的文件直接跳过。
- 对候选文件只读取完成任务所需的段落；需要追溯时再展开来源。
- 发现记忆与最新证据冲突时，保留冲突并采用较新、证据更强的内容。
- 涉及价格、法规、市场、产品能力或其他时效事实时重新核验。

## 写入规则

适合沉淀：

- 已确认的项目决策、架构选择与稳定偏好；
- 可复用的方法、模板、SOP、检查项和评估标准；
- 已验证的事实、来源、适用范围和置信度；
- 错误回复、失败原因、修复办法和防复发规则；
- Goodcase、Badcase、Skill 使用结果与同类 Skill 合并候选；
- 项目状态变化、完成事项、未完成事项和下一步。

默认不沉淀：寒暄、临时措辞、重复内容、未经证实的猜测、敏感凭据、口令、Token、个人隐私和无长期价值的信息。

写入前必须：

1. 搜索同主题记录并优先更新原文件。
2. 区分事实、推断、假设与建议。
3. 只记录增量，不复制整段对话。
4. 项目特有踩坑写入项目的 `04_项目踩坑.md`；跨项目候选写入根目录 `01_全局复利&踩坑日志.md`，详细证据索引写入 `90-System/03_详细踩坑证据索引.md`。
5. 将工作区结构和机制变更写入 `90-System/01_变更记录.md`，测试证据写入 `90-System/02_研究与测试证据索引.md`。

## 安装与诊断

当用户要求安装、迁移、修复或验证此机制时：

1. 先备份并合并现有 `config.toml`、全局 AGENTS、`hooks.json` 和运行时配置，不直接覆盖。
2. Windows 上必须使用实际存在且经过运行测试的 Python 绝对路径；不得假设 `python3`、`python` 或 `py` 可用。
3. 安装后分别模拟 `SessionStart`、`UserPromptSubmit` 和 `SessionEnd`，并解析其 JSON 输出。
4. 若验证失败，只修复失败项，不覆盖已有配置。
5. 提醒用户完全重启 Codex 并开启一个新对话；当前会话不能证明 Hook 已被应用加载。
6. 同时验证五个角色配置和 `five-role-deliberation` Skill 未被破坏。

安装或修复必须保留已有 `config.toml`、当前生效的全局 AGENTS 文件、用户级
`hooks.json` 与 Marketplace 内容，只更新本机制的配置和条目。若存在非空
`AGENTS.override.md`，必须先确认实际生效文件，不能假装更新成功。

## 权限边界

- 自动记忆不扩大文件、网络、外部应用或发布权限。
- 不自动删除知识文件，不静默覆盖冲突结论。
- 对外写入、发送、发布、删除和权限扩张仍需正常授权。
- 记忆用于召回，不作为最新外部事实的证据。

需要判断分类、过期、冲突、敏感信息或文件落点时，读取 [references/memory-policy.md](references/memory-policy.md)。
