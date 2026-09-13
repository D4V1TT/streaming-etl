from collections.abc import Iterable, Iterator
from typing import overload

EMPLOYEES = [
    {"emp_id": 1, "name": "Nino",   "dept": "IT",      "salary": 4200},
    {"emp_id": 2, "name": "Giorgi", "dept": "IT",      "salary": 3800},
    {"emp_id": 3, "name": "Ana",    "dept": "Finance", "salary": 5100},
    {"emp_id": 4, "name": "Luka",   "dept": "Finance", "salary": 2900},
    {"emp_id": 5, "name": "Mari",   "dept": "IT",      "salary": 6100},
]


class EmployeeTable:
    def __init__(self, rows: Iterable[dict]) -> None:
        self._rows = list(rows)

    def __len__(self) -> int:
        return len(self._rows)

    @overload
    def __getitem__(self, key: int) -> dict: ...

    @overload
    def __getitem__(self, key: slice) -> "EmployeeTable": ...

    def __getitem__(self, key: int | slice) -> "dict | EmployeeTable":
        if isinstance(key, slice):
            data = self._rows[key]
            return EmployeeTable(data)
        return self._rows[key]

    def __iter__(self) -> Iterator:
        return EmployeeIterator(self._rows)

    """
    def __iter__(self):
        yield from self._rows
    """

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EmployeeTable):
            return NotImplemented
        return self._rows == other._rows

    __hash__ = None

    def __repr__(self) -> str:
        columns = list(self._rows[0]) if self._rows else []
        return f"{self.__class__.__name__}(rows={len(self._rows)}, columns=[{columns!r}])"

class EmployeeIterator:

    def __init__(self, rows: Iterable[dict]) -> None:
        self._rows = list(rows)
        self._pos = 0

    def __iter__(self) -> "EmployeeIterator":
        return self

    def __next__(self) -> dict:
        if self._pos < len(self._rows):
            row = self._rows[self._pos]
            self._pos += 1
            return row
        else:
            raise StopIteration


if __name__ == "__main__":
    employee_table = EmployeeTable(EMPLOYEES)
    print(len(employee_table))
    print(employee_table[1])
    print(employee_table[1:3])
    print(max(employee_table, key=lambda r: r["salary"]))
    print(sorted(employee_table, key=lambda r: r["name"]))
    print(sum(r["salary"] for r in employee_table))
    first, *rest = employee_table
    print(first, rest)
    my_iter = EmployeeIterator(EMPLOYEES)
    print(sum(1 for _ in my_iter))  # 5
    print(sum(1 for _ in my_iter))  # 0  ← exhausted
    itr = EmployeeTable(EMPLOYEES)
    print(sum(1 for _ in itr))  # 5
    print(sum(1 for _ in itr))  # 5  ← fresh iterator each time
    print(5 in employee_table)