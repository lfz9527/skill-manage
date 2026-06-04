"""Aggregate grading results into benchmark.json."""
import json
import os

WORKSPACE = r"C:\Users\admin\.claude\skills\code-review-workspace\iteration-1"

def load_grading(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    evals = [
        {"id": 0, "name": "code-quality-naming"},
        {"id": 1, "name": "performance-n-plus-one"},
        {"id": 2, "name": "logic-null-boundary"},
    ]
    configs = ["with_skill", "without_skill"]

    runs = []
    all_with_pass = []
    all_without_pass = []

    for ev in evals:
        for config in configs:
            gpath = os.path.join(WORKSPACE, ev["name"], config, "grading.json")
            grading = load_grading(gpath)
            expectations = grading["expectations"]
            passed = sum(1 for e in expectations if e["passed"])
            total = len(expectations)
            pass_rate = passed / total if total > 0 else 0

            runs.append({
                "eval_id": ev["id"],
                "eval_name": ev["name"],
                "configuration": config,
                "run_number": 1,
                "result": {
                    "pass_rate": pass_rate,
                    "passed": passed,
                    "failed": total - passed,
                    "total": total,
                    "time_seconds": 0,
                    "tokens": 0,
                    "errors": 0
                },
                "expectations": expectations
            })

            if config == "with_skill":
                all_with_pass.append(pass_rate)
            else:
                all_without_pass.append(pass_rate)

    def stats(values):
        if not values:
            return {"mean": 0, "stddev": 0, "min": 0, "max": 0}
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return {
            "mean": round(mean, 2),
            "stddev": round(variance ** 0.5, 2),
            "min": min(values),
            "max": max(values)
        }

    ws_mean = sum(all_with_pass) / len(all_with_pass) if all_with_pass else 0
    wos_mean = sum(all_without_pass) / len(all_without_pass) if all_without_pass else 0

    benchmark = {
        "metadata": {
            "skill_name": "code-review",
            "timestamp": "2026-06-01T10:00:00Z",
            "evals_run": [0, 1, 2],
            "runs_per_configuration": 1
        },
        "runs": runs,
        "run_summary": {
            "with_skill": {
                "pass_rate": stats(all_with_pass),
                "time_seconds": {"mean": 0, "stddev": 0, "min": 0, "max": 0},
                "tokens": {"mean": 0, "stddev": 0, "min": 0, "max": 0}
            },
            "without_skill": {
                "pass_rate": stats(all_without_pass),
                "time_seconds": {"mean": 0, "stddev": 0, "min": 0, "max": 0},
                "tokens": {"mean": 0, "stddev": 0, "min": 0, "max": 0}
            },
            "delta": {
                "pass_rate": f"{ws_mean - wos_mean:+.2f}",
                "time_seconds": "N/A",
                "tokens": "N/A"
            }
        },
        "notes": [
            "With-skill reviews consistently follow structured format with file paths, line numbers, and fix suggestions",
            "Without-skill baseline catches similar issues but in less structured format",
            "code-quality-naming without_skill missed 'uses_structured_format' and 'includes_fix_suggestions' assertions (2/5 vs 5/5)"
        ]
    }

    outpath = os.path.join(WORKSPACE, "benchmark.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(benchmark, f, ensure_ascii=False, indent=2)

    print(f"Benchmark written to {outpath}")
    print(f"With skill avg pass rate: {ws_mean:.0%}")
    print(f"Without skill avg pass rate: {wos_mean:.0%}")

if __name__ == "__main__":
    main()
