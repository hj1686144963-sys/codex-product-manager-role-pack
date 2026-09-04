# 0.5.0-beta.1｜公开行为记忆版

## 目标

在不复制身份、私人事实和权限的前提下，提高产品经理工作方式的可迁移保真度。

## 新增

- `knowledge/roles/product-manager/approved/behavior-memory.md`：脱敏后的 P0/P1 行为记忆。
- `evaluations/behavior-memory.jsonl` 与 `scripts/run_behavior_eval.py`：P0 逐例 100%、P1 不低于 95% 的确定性回放。
- `PUBLIC-SOURCES.json`：来源、许可证依据、包含内容与排除范围。
- 树与 ZIP 递归安全扫描；负向 fixture 仅在固定路径和 SHA-256 同时匹配时例外。

## 安装与迁移

新安装会把公开行为记忆复制到本地知识库 `02-Knowledge/产品经理行为记忆.md`。已有同名文件不会被覆盖，避免覆盖使用者自己的内容。

## 边界

这是工作方式兼容包，不是身份克隆。它不包含私人 Vault、真实身份、组织与项目事实、聊天原文、截图、私链、本机绝对路径或凭据。

## 回滚

运行 `python3 scripts/rollback.py --latest` 恢复安装前的 Codex 配置、Agent、Skill、Hook 与插件；知识库按既有策略保留，不自动删除用户资料。
