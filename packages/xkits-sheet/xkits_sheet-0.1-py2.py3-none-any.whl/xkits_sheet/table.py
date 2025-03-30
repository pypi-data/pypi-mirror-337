# coding=utf-8

import os
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

from tabulate import TableFormat
from tabulate import tabulate as __tabulate

FKT = TypeVar("FKT")
FVT = TypeVar("FVT")
RKT = TypeVar("RKT")
RVT = TypeVar("RVT")
CVT = TypeVar("CVT")


class Cell(Generic[CVT]):
    """Cell in the custom table

    Define cells to resolve the null value issue.
    """

    def __init__(self, value: Optional[CVT] = None):
        self.value = value

    def __str__(self) -> str:
        return str(self.value if self.value is not None else "")

    @property
    def empty(self) -> bool:
        return self.value is None

    @property
    def value(self) -> Optional[CVT]:
        return self.__value

    @value.setter
    def value(self, value: Optional[CVT]):
        self.__value = value


class Row(Generic[RKT, RVT]):
    """Row in the custom table
    """

    def __init__(self, values: Union[Iterable[Cell[RVT]],
                                     Iterable[Optional[RVT]]]):
        self.__cells = [self.new_cell(value=value) for value in values]

    def __len__(self) -> int:
        return len(self.__cells)

    def __iter__(self) -> Iterator[Cell[RVT]]:
        """all cells
        """
        return iter(self.__cells)

    def __getitem__(self, index: int) -> Cell[RVT]:
        return self.__cells[index]

    def __setitem__(self, index: int,
                    value: Union[Cell[RVT],
                                 Optional[RVT]]
                    ) -> None:
        self.__cells[index] = self.new_cell(value=value)

    @property
    def values(self) -> Tuple[Optional[RVT], ...]:
        """all cell values
        """
        return tuple(cell.value for cell in self)

    def append(self, value: Union[Cell[RVT], Optional[RVT]]) -> None:
        self.__cells.append(self.new_cell(value))

    def extend(self, values: Union[Iterable[Cell[RVT]],
                                   Iterable[Optional[RVT]]]) -> None:
        self.__cells.extend(self.new_cell(value) for value in values)

    def mapping(self, header: Tuple[RKT, ...]) -> Dict[RKT, RVT]:
        """Map the value of cells into dict
        """
        return {key: cell.value for key, cell in zip(header, self)
                if cell.value is not None}

    def new_cell(self, value: Union[Cell[RVT], Optional[RVT]]) -> Cell[RVT]:
        return value if isinstance(value, Cell) else Cell(value)


class Form(Generic[FKT, FVT]):
    """Custom table
    """

    def __init__(self, name: str, header: Optional[Iterable[FKT]] = None):
        self.__rows: List[Row[FKT, FVT]] = []
        self.__name: str = name
        self.header = header if header is not None else []

    def __len__(self) -> int:
        return len(self.__rows)

    def __iter__(self) -> Iterator[Row[FKT, FVT]]:
        """all rows
        """
        return iter(self.__rows)

    def __getitem__(self, index: int) -> Row[FKT, FVT]:
        return self.__rows[index]

    def __setitem__(self, index: int,
                    value: Union[Row[FKT, FVT],
                                 Iterable[Cell[FVT]],
                                 Iterable[FVT]]
                    ) -> None:
        self.__rows[index] = self.new_row(value)

    @property
    def name(self) -> str:
        """table name
        """
        return self.__name

    @property
    def header(self) -> Tuple[FKT, ...]:
        """table header (title line)
        """
        return self.__header

    @header.setter
    def header(self, value: Iterable[FKT]) -> None:
        self.__header: Tuple[FKT, ...] = tuple(i for i in value)

    @property
    def mappings(self) -> Iterator[Dict[FKT, FVT]]:
        return iter(row.mapping(self.header) for row in self)

    @property
    def values(self) -> Tuple[Tuple[Optional[FVT], ...], ...]:
        """all cell values (by row)
        """
        return tuple(row.values for row in self)

    def column_no(self, key: FKT) -> int:
        return self.header.index(key)

    def sort(self, fn: Callable[[Row[FKT, FVT]], Cell[FVT]],
             reverse: bool = False) -> None:
        """sort rows using a Lambda function as the key.
        """
        self.__rows.sort(key=lambda row: fn(row).value,  # type: ignore
                         reverse=reverse)

    def dump(self) -> Tuple[Tuple[Any, ...], ...]:
        """dump header and all rows
        """
        table: List[Tuple[Any, ...]] = [self.header]
        table.extend(self.values)
        return tuple(table)

    def reflection(self, cells: Dict[FKT, FVT],
                   default: Any = None) -> Row[FKT, FVT]:
        """Re-map the dict to new row object
        """
        return self.new_row(cells=tuple(cells.get(key, default)
                                        for key in self.header))

    def append(self, item: Union[Row[FKT, FVT],
                                 Iterable[Cell[FVT]],
                                 Iterable[FVT]]
               ) -> None:
        self.__rows.append(self.new_row(item))

    def extend(self, rows: Iterable[Union[Row[FKT, FVT],
                                          Iterable[Cell[FVT]],
                                          Iterable[FVT]]]) -> None:
        self.__rows.extend(self.new_row(row) for row in rows)

    def new_row(self, cells: Union[Row[FKT, FVT],
                                   Iterable[Cell[FVT]],
                                   Iterable[Optional[FVT]]]
                ) -> Row[FKT, FVT]:
        return cells if isinstance(cells, Row) else Row(values=cells)

    def new_map(self, default: Any = None) -> Dict[FKT, Any]:
        """Generate new mapping with default values
        """
        return {key: default for key in self.header}


def tabulate(table: Form[Any, Any],
             fmt: Union[str, TableFormat] = "simple") -> str:
    return __tabulate(tabular_data=table.values,
                      headers=table.header,
                      tablefmt=fmt)


def parse_table_name(filename: str) -> str:
    return os.path.splitext(os.path.basename(filename))[0]
