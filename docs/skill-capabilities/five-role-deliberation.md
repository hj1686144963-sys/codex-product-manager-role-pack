<!-- GENERATED FILE. DO NOT EDIT. Source: skills/REGISTRY.json -->
# Skill 能力说明：five-role-deliberation

- 版本：`2.2.0`
- 生命周期：`active`
- 主分类：`governance.decision`
- 风险级别：`read-only`
- 执行定义：`skills/five-role-deliberation/SKILL.md`
- 内容哈希：`1f1e56f69561a2e6fd69e7cd3fcabbca231b6836e5862703b4dd498ef1d8dea0`

## 一句话机器路由

当重要决策存在多条路径、证据冲突或高影响风险时，调用五角色独立审议并保留分歧；审议完成且用户授权后可生成只读 UI 设计交接，但不在面板内执行。

## Codex 实际触发描述

Use a fixed five-role review panel to challenge complex product, interaction, model-evaluation, Codex Agent, Skill, memory, automation, and department-efficiency decisions. Trigger when the user explicitly asks for 五角色审议、多角度讨论、反复讨论, or when a decision has multiple viable paths, material uncertainty, conflicting evidence, high impact, or repeated stalled reasoning. Do not invoke the full panel for clear low-risk execution, formatting, simple edits, or when the user says 直接执行.

## 核心能力

- 五角色独立审议
- 证据核验
- 系统与产品取舍
- 红队质疑
- 决策报告
- 审议后设计执行交接

## 来源与版本证据

- 来源类型：local-adapted
- 来源路径：`skills/five-role-deliberation`
- 许可证：repository-license

## 合并血缘

- 无；这是独立 Skill，不是同类 Skill 合并产物。

## 合并说明

不适用。

## 替代关系

- 后继 Skill：无

## 维护规则

- 本文由 `scripts/Generate-SkillCapabilityDocs.ps1` 生成，不得手工编辑。
- 行为变化先修改 `SKILL.md`；治理元数据先修改 `skills/CATALOG.json`，然后重新生成 Registry 和本文。
- 安装、合并、废弃或回滚必须保留来源版本、哈希和验证证据。