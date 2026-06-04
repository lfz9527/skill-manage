# 性能审查报告 — order_repository.py

分析了 `OrderRepository` 类的 4 个方法，以下按严重程度排列。

## 严重问题

### N+1 查询：get_orders_with_users

这个方法在循环内逐条查询 orders 和 users。如果传入 100 个 ID，就产生 200 次 DB 查询。应该用 IN 查询一次性拉取。

### N+1 查询：get_order_summary

在遍历 order_items 的循环内逐条查 products 表。每个 item 一次查询，应该先收集所有 product_id 然后批量查询。

## 中等问题

### batch_update_status 名不副实

方法名叫 batch 但实际是一条条 update，改成 IN 子句的批量更新会好很多。

### filter_and_sort_orders 多余的遍历

函数做了多次不必要的列表转换。开头那段 `for o in orders: result.append(o)` 完全没意义，直接遍历 orders 就行。后面的 sorted + reversed 也可以直接用 reverse=True。

## 建议

整体来看这个模块的性能问题集中在数据库访问模式上——习惯性地在循环内逐条查询。建议统一改为先收集 ID、批量查询、构建内存映射的模式。这样可以把 O(n) 次数据库往返降低到 O(1)。
