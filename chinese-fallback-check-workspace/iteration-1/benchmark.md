# Benchmark: chinese-fallback-check — Iteration 1

## Summary

| Configuration | Pass Rate | Tokens (mean ± stddev) | Duration (mean ± stddev) |
|--------------|-----------|------------------------|--------------------------|
| **with_skill** | 100% (15/15) | 30511 ± 1025 | 70.9s ± 21.3s |
| **without_skill** | 100% (15/15) | 29070 ± 1347 | 70.6s ± 20.0s |

## Comparison

| Metric | Delta (with_skill - without_skill) |
|--------|-----------------------------------|
| Pass Rate | 0% (both perfect) |
| Tokens | +1441 (+5.0%) |
| Duration | +0.3s (+0.4%) |

## Per-Eval Breakdown

### Eval 0: logical-operator-fallback
| Config | Pass Rate | Tokens | Duration |
|--------|-----------|--------|----------|
| with_skill | 5/5 | 29,307 | 41.1s |
| without_skill | 5/5 | 28,202 | 43.5s |

### Eval 1: function-defaults
| Config | Pass Rate | Tokens | Duration |
|--------|-----------|--------|----------|
| with_skill | 5/5 | 30,417 | 81.9s |
| without_skill | 5/5 | 31,001 | 91.4s |

### Eval 2: mixed-intentional
| Config | Pass Rate | Tokens | Duration |
|--------|-----------|--------|----------|
| with_skill | 5/5 | 31,811 | 89.7s |
| without_skill | 5/5 | 28,008 | 76.9s |

## Analyst Observations

- Both configurations achieved 100% pass rate — the task is straightforward enough that the skill doesn't change detection accuracy
- Token overhead with skill is minimal (~5%), expected due to loading SKILL.md instructions
- Duration is comparable — the skill adds no meaningful latency
- The skill's primary value is in **consistency of report format** and **structured severity classification**, not in detection capability (both configs detect all patterns)
- For eval-2 (mixed-intentional), both configurations correctly distinguished intentional Chinese config data from fallback Chinese
