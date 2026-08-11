# UI 视觉设计规范选型清单

| 字段       | 内容                       |
| ---------- | -------------------------- |
| 所属模块   | 跨模块                     |
| 作者       | 产品经理                   |
| 创建日期   | 2026-07-13                 |
| 最后更新   | 2026-07-13                 |
| 飞书链接   | _(如有)_                   |

---

## 1. 调研目的

- 保存成熟、可复用的 UI 设计规范，作为后续原型和视觉设计的基础参考。
- 支持 AIGC 创作工作台、计费、团队权限、模型管理等不同场景快速选型。
- 明确主规范与专项参考的边界，避免跨设计系统随意拼接导致视觉不一致。

## 2. 调研范围

- 对象：成熟企业开源设计系统、官方平台设计规范及配套 Figma/UI Kit。
- 重点：视觉基础、组件完整度、复杂后台能力、AI 交互、数据可视化、移动端和研发衔接。
- 调研时间：2026-07-13。

## 3. 设计规范概览

| 设计系统 | 所属公司 / 团队 | 核心定位 | 适合场景 | 资源入口 |
| -------- | --------------- | -------- | -------- | -------- |
| Semi Design | 字节跳动；抖音前端与 MED 产品设计团队 | 易定制的现代应用 UI 设计系统 | AIGC 创作平台、内容工具、现代中后台 | [官网](https://semi.design/zh-CN/) · [GitHub](https://github.com/DouyinFE/semi-design) |
| Arco Design | 字节跳动；GIP UED 与架构前端团队 | 企业级设计系统与主题定制工具链 | 创作工具、企业后台、品牌主题定制 | [官网](https://arco.design/) · [GitHub](https://github.com/arco-design/arco-design) |
| Ant Design | 蚂蚁集团 | 企业级产品设计语言与 React 组件库 | 计费、权限、配置、表格和复杂表单 | [官网](https://ant.design/docs/spec/introduce-cn) · [GitHub](https://github.com/ant-design/ant-design) |
| TDesign | 腾讯 | 跨技术栈、多端企业级设计系统 | Web、移动端、小程序多端统一 | [官网](https://tdesign.tencent.com/) · [GitHub](https://github.com/Tencent/tdesign) |
| Primer | GitHub | GitHub 产品设计系统 | 高信息密度 SaaS、开发者工具、导航与状态 | [官网](https://primer.style/) · [Figma 指南](https://primer.style/product/getting-started/figma/) |
| Carbon | IBM | 企业软件与数字体验设计系统 | 数据分析、运营后台、图表和无障碍 | [官网](https://carbondesignsystem.com/) · [设计资源](https://carbondesignsystem.com/designing/design-resources/) |
| Fluent 2 | Microsoft | 跨平台产品及 Copilot 设计系统 | AI 助手、Copilot、跨端应用、明暗主题 | [官网](https://fluent2.microsoft.design/) · [Figma 指南](https://fluent2.microsoft.design/get-started/design) |
| Material Design 3 | Google | Android 与跨平台产品设计规范 | Android、移动 Web、动态主题和无障碍 | [官网](https://m3.material.io/) |
| Apple HIG | Apple | Apple 平台人机界面规范 | iOS、iPadOS、macOS 等原生应用 | [规范](https://developer.apple.com/design/human-interface-guidelines/) · [设计资源](https://developer.apple.com/design/resources/) |

## 4. 字节系设计系统说明

### 4.1 Semi Design

- **明确属于字节系**：由抖音前端团队和 MED 产品设计团队设计、开发并维护。
- 从字节跳动不同业务线的复杂场景提炼，官方提供抖音、剪映、飞书、火山引擎等主题示例。
- 强项是内容优先、现代化视觉、主题定制、国际化、无障碍及 Figma 到代码衔接。
- 更适合作为雷鸟 AIGC 平台的**主视觉规范候选**。

### 4.2 Arco Design

- **同样属于字节系**：由字节跳动 GIP UED 团队与架构前端团队联合推出。
- 强项是企业级组件、Design Token、Design Lab、物料市场和品牌主题定制。
- 整体更偏企业中后台与工程化体系，视觉相较 Ant Design 更轻、更年轻。
- 适合作为雷鸟 AIGC 平台的**备选主规范或主题定制参考**。

### 4.3 两者选择建议

| 判断维度 | Semi Design | Arco Design |
| -------- | ----------- | ----------- |
| 团队来源 | 抖音前端、MED 产品设计 | GIP UED、架构前端 |
| 产品气质 | 内容优先、现代、人性化 | 清爽、企业级、工程化 |
| 优先场景 | 创作平台、内容工具、现代中后台 | 企业后台、主题定制、物料复用 |
| 对雷鸟平台的建议 | 优先作为主规范候选 | 作为第二候选和定制能力参考 |

## 5. 雷鸟 AIGC 平台已采用组合

- **选型状态：已接受，作为日常设计图默认基线（2026-07-13 起）**。
- **主规范：Semi Design**  
  统一颜色、字体、间距、圆角、阴影、组件状态和整体视觉气质。
- **主题定制参考：Arco Design**  
  参考 Design Token、主题配置和业务物料复用，不替换 Semi 的基础视觉参数。
- **复杂业务参考：Ant Design**  
  参考账单、模型配置、成员权限、复杂表格、批量操作和筛选模式。
- **数据与无障碍：Carbon**  
  参考图表、数据表达、对比度、键盘交互和焦点状态。
- **AI 交互：Fluent 2 Copilot UI Kit**  
  参考 AI 输入、生成状态、建议指令、引用、流式输出和 AI 标识。
- **移动端：Material Design 3 与 Apple HIG**  
  根据 Android、iOS 平台分别采用对应交互标准。

> 选型原则：可以参考多套设计系统，但正式项目只能确定一套视觉基准；其他系统只补充业务模式和专项规则，不直接混搭视觉参数。

## 6. 后续正式选型检查项

1. 是否覆盖创作工作台、素材上传、任务生成、生成结果和失败重试。
2. 是否覆盖计费账单、复杂表格、筛选、批量操作、成员与权限。
3. 是否提供 Figma UI Kit、变量、组件属性和明暗主题。
4. 是否能与当前前端技术栈对应，降低设计到开发的还原成本。
5. 是否支持品牌色、字体、圆角和密度的系统化定制。
6. 是否具备无障碍、国际化和响应式规范。
7. 官方文档、组件库和社区是否仍持续维护。

## 7. 参考资料

- [Semi Design 介绍](https://semi.design/zh-CN/start/introduction)
- [Arco Design GitHub 组织](https://github.com/arco-design)
- [Ant Design 设计语言](https://ant.design/docs/spec/introduce-cn)
- [TDesign GitHub](https://github.com/Tencent/tdesign)
- [GitHub Primer](https://primer.style/)
- [IBM Carbon Design System](https://carbondesignsystem.com/)
- [Microsoft Fluent 2](https://fluent2.microsoft.design/)
- [Material Design 3](https://m3.material.io/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Design Systems Repo](https://designsystemsrepo.com/design-systems-recent/)
- [Awesome Design Systems](https://github.com/alexpate/awesome-design-systems)

## 8. 变更记录

| 日期 | 变更内容 | 变更人 |
| ---- | -------- | ------ |
| 2026-07-13 | 首次建立 UI 视觉设计规范选型清单，补充字节系归属和雷鸟平台推荐组合 | 产品经理 |
| 2026-07-13 | 确认采用组合方案：Semi 为主规范，Arco、Ant、Carbon、Fluent 2 及移动端规范按专项补充 | 产品经理 |
