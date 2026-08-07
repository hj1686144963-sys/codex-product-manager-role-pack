# 雷鸟 UI 设计基线

## 默认结论

- Semi Design 是颜色、字体、间距、圆角、阴影、密度、组件状态和整体视觉气质的唯一主视觉基线。
- 项目已有品牌规范、Design Token 和组件库优先；当前任务中的明确要求优先级最高。
- Arco、Ant Design、Carbon、Fluent 2、Material Design 3 和 Apple HIG 只补充专项交互模式，不直接混搭视觉参数。

## 场景路由

- 主题与 Token：参考 Arco 的组织方式。
- 账单、权限、复杂表格与批量操作：参考 Ant Design 的交互模式。
- 数据与无障碍：参考 Carbon。
- AI 输入、流式生成、引用和建议指令：参考 Fluent 2 Copilot。
- Android / Apple 平台：分别遵循 Material Design 3 / Apple HIG 的平台交互规则。

## Figma 与实现检查

1. 先读取现有变量、组件、样式、Auto Layout 和断点，不重复造组件。
2. 覆盖默认、悬停、按下、聚焦、禁用、加载、空态、错误和成功状态。
3. 图标使用一致的纯矢量资源；图标加文字使用水平 Auto Layout 和稳定间距，不用彩色 Emoji 代替。
4. 实现时复用主题变量和组件，完成响应式、键盘操作、焦点、对比度和错误状态。
5. 输出前检查层级、密度、对齐、可读性和设计到开发的还原成本。

完整可执行版本同时安装为 `leiniao-ui-design-baseline` Skill。
