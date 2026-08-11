# Vault routing

## Configured operating Vault

安装后由用户在 `~/.codex/codex-self-growing-memory.json` 的
`vault_path` 字段配置唯一活动 Vault。示例：

`<YOUR_VAULT_ROOT>`

Use this Vault for:

- the user's stable work habits and product-manager preferences;
- five-role project decisions, evaluation cases, usage feedback, and future growth proposals;
- global control, lessons, and project records.

先从运行时配置读取路径，再读取该 Vault 根目录的 `AGENTS.md` 和控制文件；之后只读取最小相关项目子集。不得默认扫描整个 Vault。路径缺失或不可访问时，明确报告，不猜测其他目录。

## Optional external research Vault

Only use a separate industry or company research Vault when its path is explicitly configured or the user provides it. Use it for:

- industry research, durable domain knowledge, AI Native and market/project research;
- sources and research records governed by its own nearest `AGENTS.md`.

Do not migrate or duplicate its content into the operating Vault. If both are relevant, use the operating Vault for preferences and project state, and the external Vault for research evidence.

## Growth hook and current boundary

自动记忆只负责选择性检索和无正文审计，不会自动把候选晋升为规则。角色遗漏、有效质疑、路由错误和资源浪费写入当前项目或根目录全局日志的候选区；不得使用旧版 `06-Growth/` 平行结构。任何角色提示词修改仍需候选、回放测试、Human 批准和可回滚版本。
