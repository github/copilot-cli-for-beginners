import statistics
import time

from books import Book, BookCollection


def run_benchmark(iterations: int = 10000, book_count: int = 1000) -> dict[str, float]:
    collection = BookCollection()
    collection.books = [
        Book(title=f"Book {index}", author="Benchmark Author", year=2000 + (index % 20))
        for index in range(book_count)
    ]

    samples = []
    for _ in range(iterations):
        start = time.perf_counter()
        collection.list_books()
        samples.append((time.perf_counter() - start) * 1_000_000)

    return {
        "iterations": iterations,
        "book_count": book_count,
        "mean_us": statistics.mean(samples),
        "median_us": statistics.median(samples),
        "min_us": min(samples),
        "max_us": max(samples),
    }


if __name__ == "__main__":
    results = run_benchmark()
    print("Benchmark: list_books")
    print(f"Iterations: {results['iterations']}")
    print(f"Book count: {results['book_count']}")
    print(f"Mean: {results['mean_us']:.3f} us")
    print(f"Median: {results['median_us']:.3f} us")
    print(f"Min: {results['min_us']:.3f} us")
    print(f"Max: {results['max_us']:.3f} us")