# 中枢与产品岗位路由协议

## TASK_JUDGE

```text
original_request: 用户原始请求
primary_role: 主责岗位
route: CONTROL_DIRECT / JOB_SPECIALIST / DOMAIN_PANEL / HUMAN_CLARIFY
support_roles: 当前已知支持岗位，没有则为空
permission_scope: 允许读取、写入和外部动作的边界
acceptance: 完成标准
reason: 一句话理由
escalation_condition: 何时返回中枢、审议或 Human
```

## SUPPORT_REQUEST

```text
role: UI Designer / AI Agent Architect / Director
reason: 产品岗位为什么不能独立完成
scope: 支持岗位允许处理的对象与边界
inputs: 原始请求、产品结论、项目 SSOT 和必要资料
expected_output: 需要返回的专业交付物
acceptance: 可观察验收标准
```

产品经理负责识别专业缺口，中枢 Agent 负责实际调用和权限控制。支持岗位发现新的跨岗缺口时返回 `ROUTE_BACK`，不得继续递归调度。外部发布、删除、发送和权限扩大仍需正常授权。
