import csv
import random
from collections.abc import Iterator
from pathlib import Path


def make_employees(n: int, seed: int = 42) -> Iterator[dict]:
    """Deterministic synthetic data for benchmarks and tests."""
    rng = random.Random(seed)
    depts = ["IT", "Finance", "Sales", "HR", "Ops"]
    
    for i in range(1, n + 1):
        yield {
                "emp_id": i,
                "name": f"emp_{i}",
                "dept": rng.choice(depts),
                "salary": rng.randrange(2000, 8000, 100),
                "hired": f"{rng.randint(2015, 2025)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
              }


def write_employees_csv(path: Path, n: int, seed: int=42) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["emp_id", "name", "dept", "salary", "hired"])

        writer.writeheader()

        for data in make_employees(n, seed=seed):
            writer.writerow(data)


if __name__ == "__main__":
    write_employees_csv(Path("employees.csv"), n=100)

