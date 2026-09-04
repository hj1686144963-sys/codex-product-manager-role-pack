# Codex 产品经理公共能力包

这是一个可公开安装的 Codex 产品经理岗位包。它把产品工作方法、五角色审议、设计规范、常用 Skill、按需知识检索和环境重建能力放进同一个版本化插件中。安装后可直接在新任务和新项目中使用，不要求反复输入触发词。

> 当前版本：`0.5.0-beta.1`。本包保留经过脱敏的决策、踩坑和运行规则，但尚未经过多人、跨项目验证；个人习惯不会自动晋升为公共规则。

本包复刻的是可迁移的工作方式兼容性，不是身份克隆。它刻意排除真实姓名、组织、客户、同事、账号、私人项目、原始对话和本地路径；其他人安装后会获得接近的判断、表达、证据与验收习惯，但不会获得维护者的私人事实或权限。

## 包含的能力

- 中枢任务判断：每条任务先判断主责岗位、权限、验收与升级条件。
- 产品主岗位：Product Manager Specialist 对产品目标、范围、交互政策和验收负责。
- 按需岗位支持：产品经理可申请 UI、AI Agent 架构师或导演支持；独立专业任务也可由中枢直接路由。
- 五角色审议：Coordinator、Researcher、Product Strategist、System Strategist、Red Team Editor。
- 产品工作法：需求收口、方案评审、简明 PRD、交互状态、模型评测、Agent 与部门提效。
- 设计规范：内置 `product-ui-design-baseline`，项目既有系统优先，无既有系统时使用 Arco 主基线。
- 高频 Skill：`product-manager-core`、`five-role-deliberation`、`codex-auto-memory`、`product-ui-design-baseline`。
- 实例日志：包含已脱敏的决策、踩坑和研究日志，不再只提供空模板。
- 本地知识库：按标题、路径、元数据和相关度检索少量内容，不全库逐篇扫描。
- 上下文补全：小片段命中后自动带回标题路径和上级摘要，减少“命中了但理解错”的情况。
- 增量去重：用 `source_id + content_hash` 跳过未变化文件、识别更新、移动与重复内容。
- 岗位评测：在 Skill 新增、替换、合并、废弃前运行岗位回归集。
- 行为保真评测：公开 approved 行为记忆以 P0/P1 回放，P0 必须逐例 100%，P1 必须达到 95%。
- 环境重建：安装清单、依赖说明、验证脚本和回滚脚本均在本仓库内，不另建第三个包。

## 目录分类

```text
codex-product-manager-role-pack/
├── agents/                         # 产品主岗位、支持岗位与共享五角色
├── skills/                         # 产品经理高频 Skill
├── assets/knowledge-base/
│   ├── 01-Role/                    # 产品经理岗位画像
│   ├── 04-Methods/                 # 产品方法与设计规范
│   ├── 06-Growth/                  # 个人、岗位、公共候选分层
│   └── 08-System/                  # 决策、防踩坑和研究日志
├── environment/                    # 环境重建清单与依赖
├── knowledge/                      # GitHub 可直接读取的岗位共享知识
├── evaluations/                    # 产品经理岗位回归评测集
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

完整步骤见 [环境重建清单](REBUILD-CHECKLIST.md)；同一文件也包含在 ZIP 的 `environment/` 目录中。不熟悉终端时，可把 [SHARE-PROMPT.md](SHARE-PROMPT.md) 全文发给 Codex 辅助安装。

GitHub 上的文件夹是日常阅读和 AI 调用源，ZIP 只是下载/安装产物。多人共享方式见 [多岗位、多人员知识共享](docs/MULTI-USER-KNOWLEDGE.md)，Skill 替换与合并规则见 [Skill 生命周期](docs/SKILL-LIFECYCLE.md)。

路由协议见 [中枢与产品岗位路由协议](docs/ROUTING-PROTOCOL.md)。本包仍是产品岗位能力包：中枢只负责判岗与控制，其他岗位只提供必要专业支持，不会替代产品经理的主责。

## 多人加入方式

- 新增同岗位人员：安装同一产品经理岗位包，读取共同的 `knowledge/roles/product-manager/approved/`，同时建立自己的私人状态包。
- 新增岗位：增加一份岗位目录、岗位配置和岗位评测集，例如 `roles/director/`；不是给每位导演复制整套知识库。
- 个人经验先进入 candidates；每周审查并经负责人确认后，才进入 approved 供所有同岗位人员使用。

## 公共能力发布规则

日常使用产生的 Goodcase、Badcase、踩坑和偏好只进入个人或岗位候选区。每周可以自动生成候选摘要，但**不能自动改写或发布公共能力**；只有维护者人工确认后，才允许合并到公开版本并发布新版本。

## 安全与隐私

- 本仓库只包含可公开的岗位方法、模板和代码，不包含私人 Vault、聊天全文、账号信息或公司机密。
- 不保存密码、Token、Cookie、私钥和浏览器登录态。
- 外部写入、发布、删除和权限扩张仍遵循正常授权。
- 五角色负责监督和形成决策报告，Human 保留最终判断。
- `evaluations/fixtures/unsafe-private-sample.txt` 仅是固定 SHA-256 的合成负向自测样例；树和 ZIP 扫描只对此精确文件例外，内容或路径变化都会重新拦截。

## 行为保真验证

```bash
python3 scripts/run_behavior_eval.py
python3 scripts/scan_public_release.py --self-test
python3 scripts/scan_public_release.py codex-product-manager-role-pack-0.5.0-beta.1.zip
```

公开来源和排除范围见 [`PUBLIC-SOURCES.json`](PUBLIC-SOURCES.json)。

## 回滚

```bash
python3 scripts/rollback.py --latest
```

## 许可

MIT License。任何人都可以安装、修改和再分发，但请自行检查组织内的数据与权限规则。
