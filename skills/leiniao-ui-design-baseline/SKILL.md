---
name: leiniao-ui-design-baseline
description: Apply the user's persistent UI design baseline to Figma designs and vibe-coding implementations for web pages, web apps, product interfaces, prototypes, dashboards, AIGC workbenches, billing, permissions, model management, data views, AI interactions, and mobile interfaces. Use by default whenever the user asks Codex to design, redesign, polish, or implement UI in Figma or code, unless the user explicitly selects another design system or an existing project has a confirmed incompatible visual system.
---

# 雷鸟 UI 设计基线

把 Semi Design 作为唯一主视觉规范，并按业务场景有限借鉴其他设计系统。开始产出前先读取 [references/ui-visual-design-baseline.md](references/ui-visual-design-baseline.md)。

## 适用优先级

按以下顺序处理冲突：

1. 当前任务中用户的明确要求；
2. 已有项目中确认生效的品牌规范、Design Token 和组件库；
3. 本技能的默认基线。

若前两项与本基线冲突，说明冲突并沿用更高优先级要求。不要为了套用本技能破坏现有项目的一致性。

## 统一视觉基准

- 只用 Semi Design 定义颜色、字体、间距、圆角、阴影、密度、组件状态和整体视觉气质。
- 不把其他设计系统的色值、圆角、阴影、字号或组件外观直接混入 Semi。
- 原始清单没有规定固定 token 数值。优先读取项目中的现有变量、样式和组件；没有现成数值时，采用与当前技术栈兼容的 Semi 官方实现，不凭空编造“已确认的规范值”。
- 需要当前官方组件、API、UI Kit、版本或 token 默认值时，只查官方资料并标明核验时间。

## 专项参考路由

| 场景 | 参考系统 | 只借鉴 |
|---|---|---|
| 主题定制、Design Token、业务物料复用 | Arco Design | 主题组织与工程化方法 |
| 账单、模型配置、成员权限、复杂表格、批量操作、筛选 | Ant Design | 复杂业务交互模式 |
| 图表、数据表达、无障碍 | Carbon | 数据呈现、对比度、键盘操作、焦点状态 |
| AI 输入、生成、流式输出、引用、建议指令、AI 标识 | Fluent 2 Copilot | AI 交互模式 |
| Android | Material Design 3 | 平台交互规则 |
| iOS、iPadOS、macOS | Apple HIG | 平台交互规则 |

这些系统只补充模式，不替换 Semi 的视觉参数。

## Figma 工作流

1. 检查现有页面、变量、文字样式、组件库、Auto Layout 和断点规则。
2. 先确认 Semi 主基线，再按专项路由补充业务交互。
3. 优先复用现有变量和组件；需要新增时保持命名、状态和属性体系一致。
4. 先搭结构与组件，再处理视觉细节；避免逐个图层写死同类参数。
5. 检查默认、悬停、按下、聚焦、禁用、加载、空态、错误和成功状态。
6. 对关键页面做局部与整页视觉验收，确认层级、密度、对齐、响应式与可读性。

## Vibe coding 工作流

1. 先检查仓库技术栈、现有依赖、Design Token、主题和组件封装。
2. 技术栈兼容且项目未选定其他系统时，优先使用 Semi 对应组件与语义。
3. 项目已有组件体系时，不擅自引入新的 UI 框架；把本基线翻译到现有组件和 token 中。
4. 用共享 token、主题变量和可复用组件实现，不在多个页面散落硬编码视觉值。
5. 完成响应式、键盘操作、焦点可见性、对比度、加载与错误状态。
6. 运行项目已有的 lint、类型检查和测试，并在浏览器中检查关键视口与交互状态。

## 输出前验收

- 是否仍只有一套主视觉语言；
- 是否覆盖创作工作台、上传、生成、结果、失败与重试等相关流程；
- 是否覆盖当前任务所需的账单、表格、筛选、批量操作、成员与权限；
- 是否使用可复用变量、组件属性和明暗主题能力；
- 是否符合当前前端技术栈且便于设计到开发还原；
- 是否具备响应式、国际化和无障碍所需状态；
- 是否明确区分源文件已确认内容、当前核验事实与设计推断。

若用户没有指定视觉方向，直接采用本基线，不重复询问是否使用 Semi。
