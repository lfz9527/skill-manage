# Code Review 报告

## 审查概览
- 审查文件：1 个
- 技术栈：javascript
- P0 致命：0 个
- P1 严重：3 个
- P2 一般：0 个
- P3 建议：0 个

## 合并建议

⏳ **修复后合并** — 存在 P1 严重问题，修复后方可合并

## 问题详情

### P0 致命 — 安全/数据损坏，阻塞合并

（无）

### P1 严重 — 合并前必须修复

---

**[P1] JS-A01 — Promise 未处理 rejection**
- 文件：`auth_handler.ts:20-29`
- 问题：`login()` 为 async 函数，内部无 try-catch。当 `findUserByEmail(email)` 返回 `null` 时（非邮箱格式输入），第 24 行 `user.password` 直接访问 null 对象的属性，抛出 TypeError 成为未处理的 Promise rejection，导致调用方无法正常捕获错误。
- 修复建议：在 `login()` 中添加 try-catch 包装异步操作；同时在对 `findUserByEmail` 结果使用前进行空值检查。

```typescript
async login(email: string, password: string): Promise<AuthResult> {
  try {
    const user = await this.findUserByEmail(email);
    if (!user) {
      return { success: false, error: "用户不存在" };
    }
    if (user.password === password) {
      this.currentUser = user;
      return { success: true, user };
    }
    return { success: false, error: "密码错误" };
  } catch (e) {
    return { success: false, error: "登录失败" };
  }
}
```
- 影响范围：JS-A02（async 函数无错误处理）

---

**[P1] JS-A04 — 竞态条件**
- 文件：`auth_handler.ts:63-70`
- 问题：`refreshToken()` 中两次快速调用共享可变状态 `this.activeTokens`。第一次调用的 `requestNewToken` 尚未完成时，第二次调用读取到旧 token 映射，导致 token 映射错乱，引发数据不一致。
- 修复建议：使用 AbortController 取消前一次未完成的请求，或加锁机制确保串行执行。

```typescript
private refreshLock: Promise<void> | null = null;

async refreshToken(token: string): Promise<void> {
  if (this.refreshLock) {
    await this.refreshLock;
  }
  this.refreshLock = this.doRefreshToken(token);
  await this.refreshLock;
  this.refreshLock = null;
}

private async doRefreshToken(token: string): Promise<void> {
  const oldToken = this.activeTokens.get(token);
  if (oldToken) {
    const newToken = await this.requestNewToken(oldToken);
    this.activeTokens.set(token, newToken);
  }
}
```

---

**[P1] JS-E01 — 空 catch 块（静默吞错）**
- 文件：`auth_handler.ts:51-56`
- 问题：`getDashboardData()` 中 `catch (e) { return {}; }` 静默吞掉所有异常并返回空对象 `{}`。调用方无法区分"正常返回空数据"与"网络异常导致无数据"，故障排查困难，且可能导致 UI 层展示空白而无提示。
- 修复建议：在 catch 中至少记录错误日志，或重新抛出错误交给上层处理。

```typescript
async getDashboardData(): Promise<object> {
  try {
    const data = await this.fetchDashboard();
    return data;
  } catch (e) {
    console.error("Dashboard fetch failed:", e);
    throw e; // 或返回含错误标识的结构
  }
}
```

---

### P2 一般 — 建议修复，可跟进

（无）

### P3 建议 — 优化建议

（无）

---

## 附：边界条件补充发现

以下为规则库未覆盖、但属于"逻辑正确性和边界条件处理"范畴的额外问题：

**1. `hasPermission()` — 空值解引用（auth_handler.ts:46）**
- `this.currentUser` 类型为 `User | null`，未登录状态下为 `null`。第 46 行直接访问 `this.currentUser.permissions` 将抛出 TypeError，导致程序崩溃。
- 修复：在使用前检查 `currentUser` 是否为 null。

```typescript
hasPermission(permission: string): boolean {
  if (!this.currentUser) {
    return false;
  }
  return this.currentUser.permissions.includes(permission);
}
```

**2. `getActiveUserRole()` — 空值解引用（auth_handler.ts:78-82）**
- 同样，`this.currentUser` 可能为 null。第 79 行 `user.role` 会抛出 TypeError。代码注释写"假设 user 一定存在"但这不成立。
- 修复：添加空值守卫。

```typescript
getActiveUserRole(): string {
  const user = this.currentUser;
  if (!user) {
    return "未登录";
  }
  if (user.role === "admin") {
    return "管理员";
  }
  return "普通用户";
}
```
