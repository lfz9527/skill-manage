# 逻辑审查报告 — auth_handler.ts

## 发现的问题

### Bug: login 未处理 null 用户

`findUserByEmail` 可能返回 null（当邮箱不含 @ 时），但 `login` 直接访问 `user.password`。这是一个明确的 TypeError 崩溃路径。

修复：在访问 user 属性前添加 null 检查。

### Bug: hasPermission 未检查 currentUser

`currentUser` 初始值是 null，`hasPermission` 直接访问 `.permissions` 会崩溃。应该用可选链 `?.` 或提前返回 false。

### Bug: getActiveUserRole 未检查 currentUser

同样的问题模式——给 user 赋值后没有 null guard 就访问 `.role`。

### 异常处理: getDashboardData 吞异常

catch 块里直接 return {} 让调用方无法区分错误和空数据。至少应该打日志。

### 竞态条件: refreshToken

get 和 set 之间有 await，并发调用可能导致 token 错乱。

## 总结

这个模块的核心问题是**对 null 的乐观假设**——多个方法在使用 `currentUser` 和 `findUserByEmail` 的返回值时没有做空值防御。在 TypeScript 中 `User | null` 类型已经提示了可能为空，但代码没有根据类型约束做相应处理。
