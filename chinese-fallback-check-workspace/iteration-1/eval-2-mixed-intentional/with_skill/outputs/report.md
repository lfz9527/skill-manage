# 中文兜底检查报告

**检查范围**：`test-fixtures/mixedFile.js`
**检查时间**：2026-06-18 16:21

---

## 发现 2 处中文兜底

### 🔴 严重 -- 逻辑运算符兜底（P0，共 2 处）

| # | 文件:行号 | 代码片段 | 建议 |
|---|----------|---------|------|
| 1 | mixedFile.js:13 | `const command = input || '未识别命令'` | `|| '未识别命令'` 为中文硬编码兜底。应使用 i18n key（如 `language.unrecognizedCommand`）替代，并在 `LanguageList.json` 中补充 CN 翻译后移除兜底。 |
| 2 | mixedFile.js:14 | `return DEFAULT_COMMANDS[command] || '未知指令'` | `|| '未知指令'` 为中文硬编码兜底。应使用 i18n key（如 `language.unknownCommand`）替代，并在 `LanguageList.json` 中补充 CN 翻译后移除兜底。 |

---

## 排除项说明

以下中文文本经过上下文分析，被判定为**正常数据/配置，无需修改**：

| # | 文件:行号 | 代码片段 | 排除原因 |
|---|----------|---------|---------|
| 1 | mixedFile.js:5 | `forward: '前进'` | 该对象是 `DEFAULT_COMMANDS` 语音命令配置数据，第 3 行显式注释说明"中文是领域数据，非兜底"。属于领域数据映射，非 UI 文案兜底。 |
| 2 | mixedFile.js:6 | `backward: '后退'` | 同上，`DEFAULT_COMMANDS` 配置数据。 |
| 3 | mixedFile.js:7 | `left: '左转'` | 同上，`DEFAULT_COMMANDS` 配置数据。 |
| 4 | mixedFile.js:8 | `right: '右转'` | 同上，`DEFAULT_COMMANDS` 配置数据。 |

另外，第 19 行 `? cmd : 'Unknown'` 三元表达式的回退值是英文 `'Unknown'`，不含中文字符，不触发 P1 中文兜底检测。

---

## 修复优先级

1. 先修复 2 处 🔴 严重项（第 13、14 行）：在 `LanguageList.json` 中确认/添加 `unrecognizedCommand`、`unknownCommand` 对应的 CN 翻译后，将兜底改为 `language.xxx` 引用并移除 `|| '...'` 兜底。
2. `DEFAULT_COMMANDS` 对象中的中文（第 5-8 行）为语音命令领域数据，已由注释标明，无需处理。
