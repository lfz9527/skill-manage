## 中文兜底检查报告

检查范围：`test-fixtures/utilsWithDefaults.js`
检查时间：2026-06-18

### 发现 6 处中文兜底

---

#### P1 — 三元表达式中文回退（共 2 处）

| # | 文件:行号 | 代码片段 | 建议 |
|---|----------|---------|------|
| 1 | utilsWithDefaults.js:16 | `user.nickname ? user.nickname : '匿名用户'` | 应使用 i18n key 替代硬编码中文 |
| 2 | utilsWithDefaults.js:20 | `code === 0 ? '成功' : '未知错误'` | 应使用 i18n key 替代硬编码中文 |

#### P2 — 函数默认参数中文（共 4 处）

| # | 文件:行号 | 代码片段 | 建议 |
|---|----------|---------|------|
| 1 | utilsWithDefaults.js:2 | `msg = '操作成功'` | 应考虑使用 i18n key 或由调用方传入 |
| 2 | utilsWithDefaults.js:6 | `name = '未命名用户'` | 同上 |
| 3 | utilsWithDefaults.js:6 | `role = '普通用户'` | 同上 |
| 4 | utilsWithDefaults.js:10 | `format = '默认格式'` | 同上 |

---

### 修复优先级

1. 先修复 P1 三元表达式（2 处）：三元表达式的分支均为硬编码中文，无 i18n 回退路径，最高优先级。
2. 再处理 P2 函数默认参数（4 处）：showMessage、createUser、formatDate 三个函数的默认参数值为中文硬编码。若为 UI 展示文案，应移除默认值由调用方传入翻译后文案。

注意：本文件未引入 i18n 模块，若需保留默认值，需先建立 i18n 依赖。更好的做法是将文案职责交给调用方，纯工具函数不携带默认中文文案。
