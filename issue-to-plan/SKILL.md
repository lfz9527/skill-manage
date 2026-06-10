---
name: issue-to-plan
description: 根据 GitLab issue 链接自动生成开发计划。当用户提供 issue URL 并提到"生成开发计划"、"开发计划"、"实现计划"、"implementation plan"时使用。也适用于用户说"基于这个 issue 做计划"或类似表述。
---

# GitLab Issue → 开发计划

根据 GitLab issue 内容，自动探索相关代码并生成结构化开发计划。

## 工作流

### 第一步：解析 issue URL

从用户提供的 GitLab issue URL 中提取：

- `base_url`：如 `https://gitlab.example.com`
- `project_path`：如 `group/subgroup/project`（URL 中 `/issues/` 前面的部分去掉 `base_url` 前缀）
- `issue_iid`：URL 末尾的数字

### 第二步：通过 GitLab API 获取 issue

首先读取 `C:\Users\admin\.claude\settings.json`，提取 `env.GITLAB_TOKEN`。

然后用 Bash 调用 GitLab API（不要使用 WebFetch）：

```bash
curl -s -H "PRIVATE-TOKEN: <token>" "<base_url>/api/v4/projects/<URL编码的project_path>/issues/<issue_iid>"
```

注意：`project_path` 需要用 `jq` 的 `@uri` 或手动做 URL 编码（如 `group%2Fsubgroup%2Fproject`）。

**如果 API 调用成功（HTTP 200，返回 JSON 含 `title` 字段）**：
- 直接从 JSON 提取：标题、描述、labels、assignee、milestone 等信息
- 跳转到 **第四步**，跳过浏览器操作

**如果 API 调用失败（无 token、401、404、curl 报错等）**：
- 说明原因，降级到第三步（浏览器方式）

### 第三步（降级）：浏览器打开 issue

使用 Chrome DevTools MCP 打开用户提供的 issue URL：

```
new_page(url=<issue_url>)
```

如果超时，尝试 `navigate_page` 加长 timeout。

#### 检查登录状态

`take_snapshot` 检查页面内容：

- **如果页面 URL 已跳转到登录页**（URL 包含 `/login`、`/signin`、`/auth`，或页面快照中出现登录表单/按钮）→ **立即停止**，告知用户：「页面需要登录，请在浏览器中手动登录后告诉我，我再继续。」
- **如果页面正常显示 issue 内容** → 继续下一步。

#### 提取关键信息

从 issue 快照中提取：标题、描述、验收标准、依赖项。

### 第四步：探索代码库

并行探索以下内容：
- issue 中提到的所有文件（读取完整内容）
- 上游设计文档（如果路径存在）
- 相关组件的现有实现
- 涉及的常量、Redux 状态、API 端点、i18n 字符串

使用 Agent(Explore) 做一次性全面探索，并行读取所有相关文件。

### 第五步：输出开发计划

在对话中直接输出以下结构的开发计划，不需要写入文件：

```markdown
## 开发计划：[issue 标题]

### 概述
一段话概括要做什么。

### 涉及文件

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| ... | 新增/修改 | ... |

### 实现步骤

#### 步骤 1：[标题]
- **文件**：`path/to/file.js`
- **改动**：具体改动内容
- **验证**：如何验证改动正确

#### 步骤 2：...
（按依赖顺序排列，每一步都标注文件路径、具体改动、验证方式）

### 依赖与风险
- 依赖的外部组件 / 未就绪的接口
- 可能的风险点
```

## 原则

- **优先用 API**：有 GitLab token 就用 API，不做无意义的浏览器操作
- **先读后写**：必须完整读取所有相关文件后再生成计划，不臆测代码内容
- **引用真实路径**：计划中所有文件路径必须是探索后确认存在的
- **标注不存在的依赖**：issue 提到的依赖组件/文件如果不存在，在计划中明确标注
- **按依赖排序**：步骤按代码依赖关系排列，确保上一步完成后下一步可立即开始
- **对话中输出即可**：不要写入计划文件，除非用户额外要求
