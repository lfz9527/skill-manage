## 中文兜底检查报告

检查范围：test-fixtures/utilsWithDefaults.js
检查时间：2026-06-18 16:21

### 发现 6 处中文兜底

#### 严重 -- 三元表达式中文回退（共 3 处）

| # | 文件:行号 | 代码片段 | 建议 |
|---|----------|---------|------|
| 1 | utilsWithDefaults.js:16 | `user.nickname ? user.nickname : '匿名用户'` | 应使用 i18n key 替代三元表达式中的中文回退值，例如 `user.nickname || t('user.anonymous')` |
| 2 | utilsWithDefaults.js:20 | `code === 0 ? '成功' : '未知错误'` | `'成功'` 和 `'未知错误'` 均为中文硬编码，应替换为 i18n key 引用，例如 `t(code === 0 ? 'common.success' : 'common.unknownError')` |

#### 建议 -- 函数默认参数中文（共 4 处）

| # | 文件:行号 | 代码片段 | 建议 |
|---|----------|---------|------|
| 1 | utilsWithDefaults.js:2 | `msg = '操作成功'` | 函数 `showMessage` 的默认参数使用了中文硬编码，建议改为从 i18n 获取默认值，或由调用方显式传入 |
| 2 | utilsWithDefaults.js:6 | `name = '未命名用户'` | 函数 `createUser` 的默认参数使用了中文硬编码，建议改为 key 引用或调用方传入 |
| 3 | utilsWithDefaults.js:6 | `role = '普通用户'` | 同上，`createUser` 第二个默认参数也使用了中文硬编码 |
| 4 | utilsWithDefaults.js:10 | `format = '默认格式'` | 箭头函数 `formatDate` 的默认参数使用了中文硬编码，建议由调用方显式传入格式化字符串 |

### 修复优先级

1. 先修复所有 严重项（P1 三元表达式回退）：在 LanguageList.json 中确认对应 i18n key 已定义，然后将中文硬编码替换为 `language.xxx` 引用
2. 再处理 建议项（P2 函数默认参数）：评估这些工具函数是否需要 i18n 化 -- 若为纯工具函数，可考虑要求调用方传入文案；若需自行提供默认值，应使用 i18n key
3. 该文件当前未引入 i18n 模块，建议在修复时补充 `import { language } from '...'` 或 `useTranslation` 相关导入
