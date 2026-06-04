# Code Review 报告

## 审查概览
- 审查文件：1 个
- 严重问题：2 个
- 警告问题：2 个
- 建议：0 个

## 问题列表

### 严重 🔴 — 必须修复，会导致功能异常或严重性能问题

**[严重] get_orders_with_users 存在双重 N+1 查询**
- 文件：`evals/fixtures/order_repository.py:10-19`
- 类型：性能
- 描述：外层循环逐条查询 orders（第一个 N+1），内层又逐条查询 users（第二个 N+1）。假设有 100 个 order_ids，会产生 100 次 orders 查询 + 100 次 users 查询 = 200 次数据库往返。使用 SQL IN 子句只需 2 次查询。
- 修复建议：
```python
# 修复前
def get_orders_with_users(self, order_ids):
    orders = []
    for oid in order_ids:
        order = self.db.query("SELECT * FROM orders WHERE id = ?", oid)
        if order:
            user = self.db.query("SELECT * FROM users WHERE id = ?", order["user_id"])
            order["user"] = user
            orders.append(order)
    return orders

# 修复后
def get_orders_with_users(self, order_ids):
    if not order_ids:
        return []
    orders = self.db.query(
        "SELECT * FROM orders WHERE id IN (%s)" % ",".join("?" * len(order_ids)),
        order_ids
    )
    user_ids = [o["user_id"] for o in orders]
    users = self.db.query(
        "SELECT * FROM users WHERE id IN (%s)" % ",".join("?" * len(user_ids)),
        user_ids
    )
    user_map = {u["id"]: u for u in users}
    for order in orders:
        order["user"] = user_map.get(order["user_id"])
    return orders
```
- 影响范围：当 order_ids 数量较大时，当前实现会导致数据库连接池耗尽和响应严重延迟。

**[严重] get_order_summary 循环内逐条查询 products**
- 文件：`evals/fixtures/order_repository.py:43-55`
- 类型：性能
- 描述：在遍历 order_items 的循环内，对每个 item 单独查询 products 表。如果一个订单有 50 个 item，将产生 50 次数据库查询。应改为先收集所有 product_id，一次批量查询。
- 修复建议：
```python
# 修复前
total = 0
for item in items:
    product = self.db.query("SELECT * FROM products WHERE id = ?", item["product_id"])
    total += item["quantity"] * product["price"]

# 修复后
product_ids = [item["product_id"] for item in items]
products = self.db.query(
    "SELECT * FROM products WHERE id IN (%s)" % ",".join("?" * len(product_ids)),
    product_ids
)
price_map = {p["id"]: p["price"] for p in products}
total = sum(item["quantity"] * price_map[item["product_id"]] for item in items)
```
- 影响范围：每个调用此方法的请求都会产生大量数据库往返，在并发场景下会严重拖垮数据库性能。

### 警告 🟡 — 建议修复，影响可维护性或轻微性能

**[警告] batch_update_status 逐条执行 UPDATE**
- 文件：`evals/fixtures/order_repository.py:21-27`
- 类型：性能
- 描述：方法名为 batch_update 但实现是逐条 UPDATE。对于大量订单的状态更新，每条 SQL 都是一次数据库往返。
- 修复建议：
```python
# 修复前
for order in orders:
    self.db.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        new_status, order["id"]
    )

# 修复后 — 使用批量 UPDATE
ids = [o["id"] for o in orders]
self.db.execute(
    "UPDATE orders SET status = ? WHERE id IN (%s)" % ",".join("?" * len(ids)),
    [new_status] + ids
)
```
- 影响范围：在订单量较大时（如批量发货、批量退款），延迟线性增长。

**[警告] filter_and_sort_orders 多次不必要列表转换**
- 文件：`evals/fixtures/order_repository.py:29-41`
- 类型：性能
- 描述：函数内经历了 5 次列表遍历/拷贝：for 追加复制 → for 过滤 → sorted() 生成新列表 → list() 再包装 → reversed() 生成迭代器 → list() 最终转换。其中第 1 次复制完全多余，sorted() 结果无需再包 list()，反向排序直接用 `reverse=True` 即可。
- 修复建议：
```python
# 修复前
result = []
for o in orders:
    result.append(o)
filtered = []
for o in result:
    if keyword in o["description"]:
        filtered.append(o)
sorted_orders = sorted(filtered, key=lambda x: x["created_at"])
reversed_orders = list(reversed(list(sorted_orders)))
return reversed_orders

# 修复后
filtered = [o for o in orders if keyword in o["description"]]
return sorted(filtered, key=lambda x: x["created_at"], reverse=True)
```
- 影响范围：在 orders 列表较大的场景下造成不必要的内存分配和 CPU 消耗。
