# Performance Baseline

## Function

- Module: `samples/book-app-project/books.py`
- Target: `BookCollection.list_books()`
- Measurement approach: standalone micro-benchmark in `samples/book-app-project/benchmark_list_books.py`

## Command

```bash
cd samples/book-app-project
python benchmark_list_books.py
```

## Baseline Results

Run 1

- Iterations: 10000
- Book count: 1000
- Mean: 0.122 us
- Median: 0.100 us
- Min: 0.000 us
- Max: 2.100 us

Run 2

- Iterations: 10000
- Book count: 1000
- Mean: 0.098 us
- Median: 0.100 us
- Min: 0.000 us
- Max: 3.700 us

## Variance Notes

- The median stayed at 0.100 us across both runs, which matches the simple in-memory return path.
- The mean moved from 0.122 us to 0.098 us and the max moved from 2.100 us to 3.700 us, which is consistent with small scheduler or interpreter noise.
- Re-run the benchmark from a quiet shell if you want to compare future changes against a cleaner baseline.