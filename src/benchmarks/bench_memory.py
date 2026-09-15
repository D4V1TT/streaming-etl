"""Peak memory of three ways to compute the same number."""

import time
import tracemalloc
from pathlib import Path

from streaming_etl.data import write_employees_csv
from streaming_etl.pipeline import parse_csv, read_lines


def eager_whole_file(path: Path) -> int:
    """Read the entire file into one string, then build a list of every row."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    header = lines[0].split(",")
    rows = [dict(zip(header, line.split(","))) for line in lines[1:]]
    return sum(int(r["salary"]) for r in rows if r["dept"] == "IT")


def eager_rows_only(path: Path) -> int:
    """Stream the file line by line, but materialize all rows as a list."""
    rows = list(parse_csv(read_lines(path)))
    return sum(int(r["salary"]) for r in rows if r["dept"] == "IT")


def lazy(path: Path) -> int:
    """Never hold more than one row at a time."""
    rows = parse_csv(read_lines(path))
    return sum(int(r["salary"]) for r in rows if r["dept"] == "IT")


def measure(fn, path: Path) -> tuple[int, float, float]:
    """Return (result, peak_MB, seconds). Peak is what decides if the process dies."""
    tracemalloc.start()
    start = time.perf_counter()
    result = fn(path)
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak / 1024**2, elapsed


if __name__ == "__main__":
    approaches = [eager_whole_file, eager_rows_only, lazy]

    print(f"{'rows':>10} | {'approach':<18} | {'peak MB':>9} | {'seconds':>8} | {'file MB':>8}")
    print("-" * 68)

    for n in (100_000, 500_000, 2_000_000):
        path = Path(f"data/employees_{n}.csv")
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            write_employees_csv(path, n)
        file_mb = path.stat().st_size / 1024**2

        answers = []
        for fn in approaches:
            result, peak, secs = measure(fn, path)
            answers.append(result)
            print(f"{n:>10,} | {fn.__name__:<18} | {peak:>9.1f} | {secs:>8.2f} | {file_mb:>8.1f}")

        assert len(set(answers)) == 1, f"approaches disagree: {answers}"
        print("-" * 68)