# coding=utf-8

import os
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from wcwidth import wcswidth
from xkits_file.safefile import SafeFile
import xlrd
import xlwt

from xkits_sheet.table import Form


class Reader():
    """Read .xls file
    """

    def __init__(self, filename: str):
        self.__file: str = filename
        SafeFile.restore(path=filename)
        self.__book: xlrd.Book = xlrd.open_workbook(filename)

    @property
    def file(self) -> str:
        return self.__file

    @property
    def book(self) -> xlrd.Book:
        return self.__book

    def load_sheet(self, sheet_name: Optional[str] = None) -> Form[str, str]:
        sheet_index: int = self.book.sheet_names().index(sheet_name)\
            if isinstance(sheet_name, str) else 0
        sheet: xlrd.sheet.Sheet = self.book.sheet_by_index(sheet_index)
        first: Iterable[str] = sheet.row_values(0)  # first line as header
        table: Form[str, Any] = Form(name=sheet.name, header=first)
        for i in range(1, sheet.nrows):
            table.append(sheet.row_values(i))
        return table

    def load_sheets(self) -> Tuple[Form[str, str], ...]:
        return tuple(self.load_sheet(name) for name in self.book.sheet_names())


class Writer():
    """Write .xls file
    """
    WIDTH = 325

    def __init__(self):
        self.__book: xlwt.Workbook = xlwt.Workbook(
            encoding="utf-8", style_compression=0)

    @property
    def book(self) -> xlwt.Workbook:
        return self.__book

    def save(self, filename: str) -> bool:
        abspath: str = os.path.abspath(filename)
        try:
            dirname: str = os.path.dirname(abspath)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            SafeFile.create_backup(path=abspath, copy=True)
            self.book.save(abspath)
            SafeFile.delete_backup(path=abspath)
            return True
        except Exception:  # pragma: no cover, pylint: disable=broad-except
            # f"failed to write file {abspath}"
            return False  # pragma: no cover

    def dump_sheet(self, table: Form[Any, Any]):
        sheet: xlwt.Worksheet = self.book.add_sheet(
            table.name, cell_overwrite_ok=True)
        widths: List[int] = []
        values: Tuple[Tuple[Any, ...], ...] = table.dump()
        for row_no, cells in enumerate(values):
            for col_no, _cell in enumerate(cells):
                value = str(_cell)
                sheet.write(row_no, col_no, value)
                width = wcswidth(value)
                if col_no >= len(widths):
                    sheet.col(col_no).width = self.WIDTH
                    widths.append(0)
                if width > widths[col_no]:
                    sheet.col(col_no).width = self.WIDTH * width
                    widths[col_no] = width

    def dump_sheets(self, tables: Iterable[Form[Any, Any]]):
        for table in tables:
            self.dump_sheet(table=table)
