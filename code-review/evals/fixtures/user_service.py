"""User service module - 代码质量审查测试用例."""


def get_user_list(d):
    """获取用户列表."""
    res = []
    for i in d:
        u = fetch_user(i)
        res.append(u)
    return res


def fetch_user(uid):
    """从数据库获取单个用户."""
    # 模拟数据库查询
    return {"id": uid, "name": f"user_{uid}"}


def process_data(x):
    """处理用户数据."""
    tmp = x.get("name", "")
    flag = False
    if x.get("status") == 1:
        flag = True
    if x.get("role") == "admin":
        flag = True
    # 重复逻辑：下面这段和上面的 status/role 检查做的是同一件事
    if x["status"] == 1 or x["role"] == "admin":
        flag = True
    return {"name": tmp, "active": flag}


def format_user_names(users):
    """格式化用户名列表."""
    result = []
    for u in users:
        result.append(u["name"].strip().title())
    return result


def calculate_discount(price, user_type, years, coupon_code):
    """计算折扣 —— 逻辑复杂难以一眼看懂."""
    d = 0
    if user_type == "vip" and years > 5 or user_type == "svip" and years > 3 or user_type == "normal" and coupon_code:
        d = 0.2
    elif user_type == "vip" and years <= 5 or user_type == "svip" and years <= 3:
        d = 0.1
    elif user_type == "normal" and not coupon_code:
        d = 0
    else:
        d = 0.05
    return price * (1 - d)
