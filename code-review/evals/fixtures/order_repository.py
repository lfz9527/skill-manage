"""Order data module - 性能问题审查测试用例."""


class OrderRepository:
    """订单数据访问层."""

    def __init__(self, db_connection):
        self.db = db_connection

    def get_orders_with_users(self, order_ids):
        """获取订单及关联用户 —— 存在 N+1 查询."""
        orders = []
        for oid in order_ids:
            order = self.db.query("SELECT * FROM orders WHERE id = ?", oid)
            if order:
                user = self.db.query("SELECT * FROM users WHERE id = ?", order["user_id"])
                order["user"] = user
                orders.append(order)
        return orders

    def batch_update_status(self, orders, new_status):
        """批量更新订单状态 —— 逐条更新而非批量."""
        for order in orders:
            self.db.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                new_status, order["id"]
            )

    def filter_and_sort_orders(self, orders, keyword):
        """过滤并排序订单."""
        result = []
        for o in orders:
            result.append(o)
        filtered = []
        for o in result:
            if keyword in o["description"]:
                filtered.append(o)
        # 不必要的多次遍历
        sorted_orders = sorted(filtered, key=lambda x: x["created_at"])
        reversed_orders = list(reversed(list(sorted_orders)))
        return reversed_orders

    def get_order_summary(self, order_id):
        """获取订单摘要 —— 本地计算却放到循环里多次查询."""
        order = self.db.query("SELECT * FROM orders WHERE id = ?", order_id)
        items = self.db.query("SELECT * FROM order_items WHERE order_id = ?", order_id)
        total = 0
        for item in items:
            product = self.db.query("SELECT * FROM products WHERE id = ?", item["product_id"])
            total += item["quantity"] * product["price"]
        return {
            "order": order,
            "item_count": len(items),
            "total": total,
        }
