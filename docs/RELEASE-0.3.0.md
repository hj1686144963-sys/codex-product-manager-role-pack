# 0.3.0 发布说明

本版本把公共能力包从“文档声明可重建”推进到“目录、Manifest、打包边界和 Dashi 防复发规则可验证”。

## 新增

- 版本目录 `release/versions/v0.3.0/`。
- 幂等工作区目录初始化脚本。
- Dashi 同源镜像、SSE、首次安装、升级和回滚验收指南。
- 打包器的 `.git`、缓存、SQLite、WAL、SHM 排除规则。
- 发布前私人绝对路径检查。

## 不包含

- 私人 Vault、项目、任务、评论、踩坑日志与截图。
- 密码、Cookie、API Key、OAuth Token、浏览器或 Codex 登录态。
- Dashi 作者 UI、上游源码、派生 bundle 或运行数据库。

## 升级策略

0.2.0 用户可先运行 `scripts/verify_package.py`，再运行安装器。目录初始化脚本只创建缺失目录，不删除或覆盖现有内容。
