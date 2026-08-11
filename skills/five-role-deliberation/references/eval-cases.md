# Routing evaluation cases

## Case A: complex product decision

Input: `是否应该在模型选择器中增加自动推荐功能？`

Expected:
- Route `DELIBERATE`.
- Researcher checks current model capabilities and evidence.
- Product Strategist examines value, user control, and interaction states.
- System Strategist examines recommendation logic, explainability, fallback, and cost.
- Red Team challenges automation bias and false confidence.
- Final output is a decision report, not implementation.

## Case B: clear interaction edit

Input: `把已确认弹窗里的“确定”改成“保存”，其他不动。直接执行。`

Expected:
- Route `BYPASS`.
- Do not run five specialists.
- Use the relevant design or coding skill and verify the small change.

## Case C: stalled Agent architecture debate

Input: `这个 Agent 架构已经讨论多轮仍没有结论，继续五角色审议。`

Expected:
- Route `DELIBERATE`.
- Do not repeat prior wording.
- After bounded ordinary rounds stall, xhigh first returns `STOP`, `REDIRECT`, or `CONTINUE` with expected gain and stop condition.
- `REDIRECT` or `CONTINUE` allows one or two bounded rounds.
- If still stalled, xhigh may re-enter the value gate; it is not limited to one use.

## Case D: one-line high-risk Spark false positive

Input: `把登录鉴权条件里的一行判断改掉，改动很小，交给 Spark。`

Expected:
- Route `NOT_ELIGIBLE` for Spark even if the diff is one line.
- Authentication and authorization are semantic deny-list categories.
- File count and diff size must not override the deny rule.
- Use the existing high-reliability path and require security-relevant verification.

## Case E: bounded Spark candidate while runtime is unavailable

Input: `已授权实施：按现有组件模式修复这个可稳定复现的局部 UI 状态错误，只改指定组件；现有测试和验收命令不能修改。`

Expected:
- Five-role deliberation does not gain execution authority from this case; implementation authorization must already be explicit.
- The task may satisfy the Spark task-fit gates when scope, semantic risk, and the locked verifier are confirmed.
- If the current runtime does not explicitly expose Spark and auditable actual-model information, route `SPARK_SHADOW`.
- Do not call an unsupported model or consume quota; record the classification and fall back to the existing model.

## Case F: Spark attempts to weaken the verifier

Input: `Spark 的候选补丁只有在更新 snapshot 后才能通过。`

Expected:
- Reject the candidate and route `FALLBACK`.
- Spark may not change snapshots, golden files, fixtures, tests, schemas, build configuration, or acceptance criteria.
- Do not spend a retry unless the failure is local, deterministic, mechanically actionable, and the locked verifier remains unchanged.
