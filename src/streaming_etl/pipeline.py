import logging
import csv
from collections.abc import Callable,Iterable, Iterator
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCHEMA: dict[str, Callable[[str], object]] = {
    "emp_id": int,
    "name": str,
    "dept": str,
    "salary": int,
    "hired": lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
}

def read_lines(path: Path) -> Iterator[str]:
    with open(path, encoding="utf-8", mode='r') as f:
        for line in f:
            yield line.rstrip("\n")

def parse_csv(lines: Iterable[str]) -> Iterator[dict]:
        it = iter(lines)
        title = next(it).strip().split(',')

        for line in it:
            data = line.strip().split(",")
            dict_data = dict(zip(title, data))
            yield dict_data

def parse_csv_stdlib(path: Path) -> Iterator[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        yield from csv.DictReader(f)

def coerce(rows: Iterable[dict], schema: dict[str, Callable]) -> Iterator[dict]:
    for row in rows:
        yield {**row, **{col: fn(row[col]) for col, fn in schema.items() if col in row}}

def filter_rows(rows: Iterable[dict], predicate: Callable[[dict], bool]) -> Iterator[dict]:
    for row in rows:
        if predicate(row):
            yield row

def add_column(rows: Iterable[dict], name: str, fn: Callable[[dict], object]) -> Iterator[dict]:
    for row in rows:
        res = row | {name: fn(row)}
        yield res

def take(rows: Iterable[dict], n: int) -> Iterator[dict]:
    for row, data in enumerate(rows, 1):
        if row > n:
            return
        yield data

def log_every(rows: Iterable[dict], n: int=100_000) ->Iterator[dict]:
    for i, row in enumerate(rows, 1):
        if i % n == 0:
            my_logger.info("processed %d rows", i)
        yield row


if __name__ == "__main__":
    path = Path("employees.csv")
    lines    = read_lines(path)
    rows     = parse_csv(lines)
    typed    = coerce(rows, SCHEMA)
    banded   = add_column(typed, "salary_band",
                          lambda r: "high" if r["salary"] > 4000 else "low")
    it_only  = filter_rows(banded, lambda r: r["dept"] == "IT")

    for row in it_only:      # ← nothing has been read until this line
        print(row)

