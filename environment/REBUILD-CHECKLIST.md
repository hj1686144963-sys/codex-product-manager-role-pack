# 环境重建清单

环境重建能力属于岗位包本体，不拆成独立仓库。

1. 下载本仓库并确认目录完整。
2. 检查 Python：`python3 --version`，要求 3.9+。
3. 运行 `python3 scripts/verify_package.py`。
4. 运行 `python3 scripts/install.py --yes`；已有知识库时追加 `--vault PATH`。
5. 重启 Codex，并在首次 Hook 审核时确认信任。
6. 运行 `python3 scripts/verify.py`，确认 `status=pass` 与 `zero_trigger_ready=true`。
7. 运行 `python3 scripts/build_knowledge_index.py --root assets/knowledge-base`。
8. 运行 `python3 scripts/run_role_eval.py` 和 `python3 scripts/validate_skill_registry.py`。
9. 新建一个任务，用正常语言提出产品问题，确认无需触发词即可路由产品方法。
10. 再新建一个项目，确认岗位画像、Skill、五角色和本地知识库仍可用。
11. 检查第三方 Skill、Hook 和已有项目未被覆盖。
12. 若失败，运行 `python3 scripts/rollback.py --latest` 并保留失败日志。

## 验收边界

- 安装脚本成功不等于闭环成功；必须完成跨新任务和新项目的实际验证。
- 没有权限或连接器时应明确报错，不得把“无法读取”写成“没有内容”。
- 公共包不包含个人状态；个人 Vault 的恢复需使用私人备份仓库。
