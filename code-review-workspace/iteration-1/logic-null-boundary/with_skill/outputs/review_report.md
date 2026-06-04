# Code Review 报告

## 审查概览
- 审查文件：1 个
- 严重问题：2 个
- 警告问题：3 个
- 建议：0 个

## 问题列表

### 严重 🔴 — 必须修复，会导致功能异常或严重性能问题

**[严重] login 方法直接访问可能为 null 的对象属性**
- 文件：`evals/fixtures/auth_handler.ts:20-29`
- 类型：逻辑正确性
- 描述：`findUserByEmail` 返回类型为 `User | null`，当邮箱格式不含 `@` 时返回 `null`。第 24 行 `user.password` 在 `user` 为 `null` 时会抛出 `TypeError: Cannot read properties of null`，导致登录接口 500 错误而非返回 `{ success: false, error: "..." }`。
- 修复建议：
```typescript
// 修复前
async login(email: string, password: string): Promise<AuthResult> {
    const user = await this.findUserByEmail(email);
    if (user.password === password) {

// 修复后
async login(email: string, password: string): Promise<AuthResult> {
    const user = await this.findUserByEmail(email);
    if (!user) {
        return { success: false, error: "用户不存在" };
    }
    if (user.password === password) {
```
- 影响范围：所有调用 login 的路径，传入无效邮箱格式时直接崩溃而非返回业务错误。

**[严重] hasPermission 未检查 currentUser 是否为 null**
- 文件：`evals/fixtures/auth_handler.ts:44-47`
- 类型：逻辑正确性
- 描述：`currentUser` 声明为 `User | null`，初始值为 `null`。在用户未登录时调用 `hasPermission`，`this.currentUser.permissions` 会抛出 TypeError。权限检查是最频繁调用的方法之一，这个崩溃会影响所有需要鉴权的页面或 API。
- 修复建议：
```typescript
// 修复前
hasPermission(permission: string): boolean {
    return this.currentUser.permissions.includes(permission);
}

// 修复后
hasPermission(permission: string): boolean {
    return this.currentUser?.permissions.includes(permission) ?? false;
}
```
- 影响范围：所有调用 hasPermission 的鉴权逻辑。未登录用户访问任何受保护资源时直接崩溃。

### 警告 🟡 — 建议修复，影响可维护性或轻微性能

**[警告] getDashboardData 静默吞掉所有异常**
- 文件：`evals/fixtures/auth_handler.ts:49-57`
- 类型：逻辑正确性
- 描述：`catch (e)` 捕获所有异常后仅返回 `{}`，不记录日志，不区分网络错误、权限错误、数据格式错误。调用方收到空对象 `{}` 无法判断是正常空数据还是发生了错误，可能导致界面显示空白而无任何错误提示。
- 修复建议：
```typescript
// 修复前
try {
    const data = await this.fetchDashboard();
    return data;
} catch (e) {
    return {};
}

// 修复后
try {
    const data = await this.fetchDashboard();
    return data;
} catch (e) {
    console.error("Failed to fetch dashboard:", e);
    throw e; // 让调用方决定如何处理
}
```
- 影响范围：所有调用 getDashboardData 的上层代码，错误被隐藏会导致问题排查困难。

**[警告] getActiveUserRole 未检查 currentUser 是否为 null**
- 文件：`evals/fixtures/auth_handler.ts:76-83`
- 类型：逻辑正确性
- 描述：虽然第 78 行将 `this.currentUser` 赋值给局部变量 `user`，但未对 `null` 做判断就直接访问 `user.role`。与 hasPermission 相同的问题模式。
- 修复建议：
```typescript
// 修复前
getActiveUserRole(): string {
    const user = this.currentUser;
    if (user.role === "admin") {
        return "管理员";
    }
    return "普通用户";
}

// 修复后
getActiveUserRole(): string {
    if (this.currentUser?.role === "admin") {
        return "管理员";
    }
    return this.currentUser ? "普通用户" : "未登录";
}
```
- 影响范围：在未登录状态下调用此方法会崩溃。

**[警告] refreshToken 存在竞态条件**
- 文件：`evals/fixtures/auth_handler.ts:63-69`
- 类型：逻辑正确性
- 描述：第 65 行读取 `this.activeTokens.get(token)` 和第 68 行 `this.activeTokens.set(token, newToken)` 之间存在 `await`。如果在 await 期间另一个调用也传入了相同的 token，两个调用都会读取到 `oldToken`，然后分别获取新 token 并覆盖写入，导致最终存储的 token 与服务器状态不一致。
- 修复建议：
```typescript
// 修复前
async refreshToken(token: string): Promise<void> {
    const oldToken = this.activeTokens.get(token);
    if (oldToken) {
        const newToken = await this.requestNewToken(oldToken);
        this.activeTokens.set(token, newToken);
    }
}

// 修复后 — 先标记再更新，防止并发写入
async refreshToken(token: string): Promise<void> {
    const oldToken = this.activeTokens.get(token);
    if (!oldToken) return;
    // 立即删除旧条目，防止并发重复刷新
    this.activeTokens.delete(token);
    const newToken = await this.requestNewToken(oldToken);
    this.activeTokens.set(token, newToken);
}
```
- 影响范围：在用户快速操作触发多次 token 刷新时（如页面快速切换），可能导致 token 映射错乱，后续请求使用过期 token。
