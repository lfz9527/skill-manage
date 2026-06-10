---
name: kpi-report
description: 根据 GitLab wiki 上的 KPI 工作记录生成周报/月报总结。当用户提到"生成周报"、"生成月报"、"周报总结"、"月报总结"、"KPI 总结"、"工作周报"时使用。也适用于用户说"总结本周工作"、"写周报"、"这周干了什么"等表述。
---

## 概述

从 GitLab wiki 读取 KPI 工作记录数据（JSON 格式），生成 50 字以内的简短周报/月报总结。

## 工作流程

### 1. 确定参数

人名固定为 **lifangzheng**，无需询问用户。

根据用户意图确定时间范围：
- **周报**：当前周的周一至周日
- **月报**：当前月份（YYYY-MM）

### 2. 构造 URL

URL 格式固定为：

```
https://www.lejuhub.com/carlos/softdev_doc/-/wikis/kpi_data/lifangzheng/{YYYY-MM}.md
```

其中 `{YYYY-MM}` 取当前年月（如 `2026-06`）。

### 3. 读取数据

#### 方式一：Chrome DevTools MCP（优先）

使用 `navigate_page` 导航到上述 URL。

**检查登录状态**：页面加载后用 `take_snapshot` 获取页面内容。如果页面是 GitLab 登录页（含 "Sign in" / "登录" / "Remember me" 等），**立即停止**并提醒用户：需要先在浏览器中登录 `lejuhub.com`，登录后再重试。

如果已登录正常显示，用 `evaluate_script` 提取内容：

```js
document.querySelector('pre')?.textContent || document.body.textContent
```

解析为 JSON。

#### 方式二：直接粘贴数据（备用）

如果 Chrome DevTools MCP 不可用，告知用户后，请用户直接将页面 JSON 内容贴入对话。

### 4. 输出总结

生成一句话总结（≤50 字），格式：

> 本周主要产出概括；需关注的问题

**写作原则：**
- 优先提炼 `#work` 和 `#good` 中的核心工作内容
- 如果延期标签 `#deldelay` 占比过高（>60%），点明延期问题
- 忽略具体条目细节，只概括趋势
- 使用简洁中文，严格控制在 50 字以内
