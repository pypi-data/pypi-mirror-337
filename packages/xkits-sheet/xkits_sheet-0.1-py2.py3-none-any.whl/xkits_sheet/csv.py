# coding=utf-8

from csv import DictReader as csv_dist_reader
from csv import DictWriter as csv_dist_writer
from csv import reader as csv_reader
from csv import writer as csv_writer
from typing import Any

from xkits_file.safefile import SafeFile

from xkits_sheet.table import Form
from xkits_sheet.table import parse_table_name


class CSV():

    @classmethod
    def load(cls, filename: str,
             include_header: bool = True
             ) -> Form[str, str]:
        """Read .csv file
        """
        with SafeFile.lock(filename):
            SafeFile.restore(path=filename)
            table: Form[str, str] = Form(name=parse_table_name(filename))
            with open(filename, "r", encoding="utf-8") as rhdl:
                if include_header:
                    reader = csv_dist_reader(rhdl)
                    fields = reader.fieldnames
                    if fields is not None:
                        table.header = fields
                        for _row in reader:
                            table.append(table.reflection(_row))
                else:
                    reader = csv_reader(rhdl)
                    for _row in reader:
                        table.append(_row)
            return table

    @classmethod
    def dump(cls, filename: str, table: Form[Any, Any]) -> None:
        """Write .csv file
        """
        with SafeFile.lock(filename):
            SafeFile.create_backup(path=filename, copy=True)
            with open(filename, "w", encoding="utf-8") as whdl:
                if len(table.header) > 0:
                    writer = csv_dist_writer(whdl, fieldnames=table.header)
                    writer.writeheader()
                    writer.writerows(table.mappings)
                else:
                    writer = csv_writer(whdl)
                    writer.writerows(table.dump())
            SafeFile.delete_backup(path=filename)
