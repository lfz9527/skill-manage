## 中文兜底检查报告

检查范围：`ComponentWithFallback.jsx`
检查时间：2026-06-18 16:21

### 发现 5 处中文兜底

#### 🔴 严重 -- 逻辑运算符兜底（共 4 处）

| # | 文件:行号 | 代码片段 | 建议 |
|---|----------|---------|------|
| 1 | ComponentWithFallback.jsx:6 | `language.pageTitle \|\| '页面标题'` | 在 LanguageList.json 中确认 pageTitle 的 CN 翻译已定义后，移除兜底 |
| 2 | ComponentWithFallback.jsx:7 | `language.subtitle ?? '默认副标题'` | 在 LanguageList.json 中确认 subtitle 的 CN 翻译已定义后，移除兜底 |
| 3 | ComponentWithFallback.jsx:14 | `language.description \|\| '这是默认描述文本'` | 在 LanguageList.json 中确认 description 的 CN 翻译已定义后，移除兜底 |
| 4 | ComponentWithFallback.jsx:16 | `language.confirm \|\| '确认'` | 在 LanguageList.json 中确认 confirm 的 CN 翻译已定义后，移除兜底 |

#### 🟢 提示 -- JSX 中文硬编码（共 1 处）

| # | 文件:行号 | 代码片段 | 建议 |
|---|----------|---------|------|
| 1 | ComponentWithFallback.jsx:15 | `<span>保存成功</span>` | 该文件已使用 i18n（`language.*`），建议改用 `language.saveSuccess` 并通过 LanguageList.json 配置翻译 |

### 修复优先级

1. 先修复所有 4 处 🔴 严重项：确认对应 i18n key（`pageTitle`、`subtitle`、`description`、`confirm`）在 LanguageList.json 中已定义 CN 翻译，然后移除兜底文本
2. 再处理 1 处 🟢 提示项：`<span>保存成功</span>` 为 JSX 中的纯中文硬编码，建议使用 i18n key 替代
