# Codex 产品经理公共能力包

这是一个可公开安装的 Codex 产品经理岗位包。它把产品工作方法、五角色审议、设计规范、常用 Skill、按需知识检索和环境重建能力放进同一个版本化插件中。安装后可直接在新任务和新项目中使用，不要求反复输入触发词。

> 当前版本：`0.1.0 Beta`。本包来自一个已运行的个人产品经理系统，但尚未经过多人、跨项目验证；个人习惯不会自动晋升为公共规则。

## 包含的能力

- 五角色审议：Coordinator、Researcher、Product Strategist、System Strategist、Red Team Editor。
- 产品工作法：需求收口、方案评审、简明 PRD、交互状态、模型评测、Agent 与部门提效。
- 设计规范：内置 `leiniao-ui-design-baseline`，界面任务默认使用 Semi Design 主视觉基线。
- 高频 Skill：`product-manager-core`、`five-role-deliberation`、`codex-auto-memory`、`leiniao-ui-design-baseline`。
- 本地知识库：按标题、路径、元数据和相关度检索少量内容，不全库逐篇扫描。
- 环境重建：安装清单、依赖说明、验证脚本和回滚脚本均在本仓库内，不另建第三个包。

## 目录分类

```text
codex-product-manager-role-pack/
├── agents/                         # 五角色
├── skills/                         # 产品经理高频 Skill
├── assets/knowledge-base/
│   ├── 01-Role/                    # 产品经理岗位画像
│   ├── 04-Methods/                 # 产品方法与设计规范
│   ├── 06-Growth/                  # 个人、岗位、公共候选分层
│   └── 08-System/                  # 决策、防踩坑和研究日志
├── environment/                    # 环境重建清单与依赖
├── scripts/                        # 安装、验证、构建和回滚
└── SHARE-PROMPT.md                 # 给 Codex 的一次性安装指令
```

## 安装

需要 Python 3.9+ 和 Codex 桌面端或本地 Codex 工作环境。

```bash
python3 scripts/verify_package.py
python3 scripts/install.py --yes
python3 scripts/verify.py
```

默认创建 `~/Documents/Codex-Obsidian-Vault-Product-Manager`。已有 Markdown/Obsidian 知识库时可用 `--vault PATH` 增量安装，安装器会先备份并保留第三方配置。

安装后的验证结果必须包含：

```json
{
  "status": "pass",
  "zero_trigger_ready": true
}
```

完整步骤见 [环境重建清单](environment/REBUILD-CHECKLIST.md)。不熟悉终端时，可把 [SHARE-PROMPT.md](SHARE-PROMPT.md) 全文发给 Codex 辅助安装。

## 公共能力发布规则

日常使用产生的 Goodcase、Badcase、踩坑和偏好只进入个人或岗位候选区。每周可以自动生成候选摘要，但**不能自动改写或发布公共能力**；只有维护者人工确认后，才允许合并到公开版本并发布新版本。

## 安全与隐私

- 本仓库只包含可公开的岗位方法、模板和代码，不包含私人 Vault、聊天全文、账号信息或公司机密。
- 不保存密码、Token、Cookie、私钥和浏览器登录态。
- 外部写入、发布、删除和权限扩张仍遵循正常授权。
- 五角色负责监督和形成决策报告，Human 保留最终判断。

## 回滚

```bash
python3 scripts/rollback.py --latest
```

## 许可

MIT License。任何人都可以安装、修改和再分发，但请自行检查组织内的数据与权限规则。
