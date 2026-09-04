# 产品经理公共能力包｜一次性安装指令

请安装当前文件夹中的「Codex 产品经理公共能力包 0.5.0-beta.1」。按下面顺序执行，不要让我手动选择 Agent、Skill、推理强度或知识库目录：

1. 先读取 `README.md`、`environment/REBUILD-CHECKLIST.md` 与 `.codex-plugin/plugin.json`。
2. 运行 `python3 scripts/verify_package.py` 检查包体；失败时先修复，不得跳过。
3. 运行 `python3 scripts/install.py --yes`。已有 Obsidian/Markdown 知识库时使用 `--vault PATH` 增量安装，不覆盖既有资料。
4. 合并当前 Codex 配置与生效的全局 AGENTS 文件，不删除第三方 Agent、Skill、Hook 或项目记录。
5. 安装产品经理主岗位、UI/AI Agent 架构师/导演支持岗位、共享五角色和四个 Skill：`product-manager-core`、`five-role-deliberation`、`codex-auto-memory`、`product-ui-design-baseline`。
6. 验证中枢 `TASK_JUDGE`、产品岗位 `SUPPORT_REQUEST` 与岗位 `ROUTE_BACK` 规则已进入全局 AGENTS。
6. 创建或补齐产品经理岗位画像，以及简明 PRD、模型评测、Agent 部门提效和 UI 设计方法。
7. 运行 `python3 scripts/verify.py`。只有 `status=pass`、`zero_trigger_ready=true` 且核心 Skill 全部通过，才能回复安装完成。
8. 运行 `python3 scripts/build_knowledge_index.py --root assets/knowledge-base`、`python3 scripts/run_role_eval.py`、`python3 scripts/run_routing_eval.py`、`python3 scripts/run_behavior_eval.py` 和 `python3 scripts/validate_skill_registry.py`。
9. 若失败，保留安装前备份并说明失败项，不得假装成功。
10. 安装完成后提醒我重启 Codex，并在首次 Hook 审核时点击信任。之后正常描述任务即可；复杂议题自动进入五角色审议，明确任务直接执行。
11. 日常经验只进入候选区；每周候选必须经维护者确认后才能合并进公共版本，禁止自动发布。
