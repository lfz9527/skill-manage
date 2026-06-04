"""Grade each run's output against assertions."""
import json
import os
import re

WORKSPACE = r"C:\Users\admin\.claude\skills\code-review-workspace\iteration-1"

# Define checks as (assertion_name, keywords list, pattern regex)
# Each check returns (passed, evidence) for a given report text

EVAL_CHECKS = {
    "code-quality-naming": [
        ("identifies_poor_naming", ["命名", "变量", "单字母", "无意义", "d", "res", "tmp", "flag"]),
        ("identifies_duplicate_logic", ["重复", "process_data", "status", "role"]),
        ("identifies_complex_condition", ["复杂", "calculate_discount", "条件", "and", "or", "优先级"]),
        ("uses_structured_format", ["文件", "行号", "审查概览"]),
        ("includes_fix_suggestions", ["修复前", "修复后", "```"]),
    ],
    "performance-n-plus-one": [
        ("identifies_n_plus_one_orders", ["N+1", "get_orders_with_users", "订单"]),
        ("identifies_n_plus_one_products", ["N+1", "get_order_summary", "products", "产品"]),
        ("identifies_batch_update_issue", ["batch_update", "逐条", "批量"]),
        ("identifies_unnecessary_iterations", ["filter_and_sort", "列表", "转换", "遍历", "sorted", "reversed"]),
        ("includes_performance_fix_suggestions", ["修复前", "修复后", "```", "IN"]),
    ],
    "logic-null-boundary": [
        ("identifies_null_user_in_login", ["null", "login", "user.password", "findUserByEmail"]),
        ("identifies_null_currentUser_permission", ["null", "hasPermission", "currentUser", "permissions"]),
        ("identifies_silent_exception_swallow", ["异常", "吞", "getDashboardData", "catch", "{}"]),
        ("identifies_race_condition", ["竞态", "refreshToken", "并发", "race"]),
        ("identifies_null_in_getActiveUserRole", ["null", "getActiveUserRole", "currentUser", "user.role"]),
    ],
}

def grade_report(report_text, checks):
    """Grade a report against checks. Returns list of {text, passed, evidence}."""
    results = []
    report_lower = report_text.lower()
    report_normal = report_text

    for name, keywords in checks:
        # Match: at least 2 keywords must appear in the report
        matched = []
        for kw in keywords:
            if kw.lower() in report_lower or kw in report_normal:
                matched.append(kw)

        passed = len(matched) >= 2
        evidence = f"Matched keywords: {matched}" if matched else "No keywords matched"
        results.append({
            "text": name,
            "passed": passed,
            "evidence": evidence
        })

    return results

def main():
    evals = ["code-quality-naming", "performance-n-plus-one", "logic-null-boundary"]
    configs = ["with_skill", "without_skill"]

    for eval_name in evals:
        checks = EVAL_CHECKS[eval_name]
        for config in configs:
            report_path = os.path.join(WORKSPACE, eval_name, config, "outputs", "review_report.md")
            if not os.path.exists(report_path):
                print(f"MISSING: {report_path}")
                continue

            with open(report_path, "r", encoding="utf-8") as f:
                report_text = f.read()

            grading = grade_report(report_text, checks)
            grading_path = os.path.join(WORKSPACE, eval_name, config, "grading.json")

            with open(grading_path, "w", encoding="utf-8") as f:
                json.dump({"expectations": grading}, f, ensure_ascii=False, indent=2)

            passed = sum(1 for g in grading if g["passed"])
            total = len(grading)
            print(f"{eval_name}/{config}: {passed}/{total} passed")

if __name__ == "__main__":
    main()
