# Benchmarking

The integration path is deterministic and can be measured with `python -m timeit` or a project benchmark harness around `src.cli.main`. Capture wall-clock execution, Runtime stage timings from `SynchronousRuntimeResult`, provider latency at transport boundaries, graph node construction, and profile construction. External/live benchmarks are optional and must never be required for CI.
