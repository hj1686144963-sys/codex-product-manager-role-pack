<!-- GENERATED FILE. DO NOT EDIT. Source: skills/REGISTRY.json -->
# Skill 能力说明：codex-auto-memory

- 版本：`2.0.0`
- 生命周期：`active`
- 主分类：`knowledge.memory`
- 风险级别：`local-write`
- 执行定义：`skills/codex-auto-memory/SKILL.md`
- 内容哈希：`3b2ac2edb42b473b3c1331d97c7c0a3fa8c05cef3313033e401c2db07f5deae8`

## 一句话机器路由

当任务依赖历史项目、稳定规则、复盘或跨会话连续性时，按需检索并安全回写本地记忆；不把记忆作为最新外部事实的证明。

## Codex 实际触发描述

Automatically continue work across Codex chats by using local Memories, selectively retrieving a configured Markdown or Obsidian knowledge base, and safely writing back durable decisions, methods, project state, Goodcase, Badcase, and anti-regression lessons. Use when a task refers to prior work, an existing project, remembered preferences, a knowledge base, repeated mistakes, role growth, postmortems, self-growing knowledge, cross-chat continuity, memory setup, memory diagnosis, or plugin installation and verification.

## 核心能力

- 跨会话检索
- Obsidian 记忆路由
- 增量回写
- 重复与冲突治理
- 安装验证

## 来源与版本证据

- 来源类型：local-adapted
- 来源路径：`skills/codex-auto-memory`
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