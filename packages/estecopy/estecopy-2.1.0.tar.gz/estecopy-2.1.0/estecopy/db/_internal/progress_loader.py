import math as _math
import sys as _sys
from estecopy._internal import _db
from estecopy.db._internal import attributes as _attributes


class _ProgressLoader:
    __PERCENT_INTERVAL = 5

    __METADATA_KEY = _attributes.METADATA_KEY
    __NAME_KEY = _attributes.NAME_KEY
    __ROWS_KEY = _attributes.ROWS_KEY

    def __init__(self, name):
        self.__name = name
        self.__tmp_data = []

    def load_table(self):
        self.__print("Loading '%s'" % (self.__name,))
        _db.supply_table_rows(self.__name, self.__append_row)
        data = {
            self.__NAME_KEY: self.__name,
            self.__METADATA_KEY: _db.get_table_metadata(self.__name),
            self.__ROWS_KEY: self.__tmp_data
        }
        self.__print("\rLoading 100%...")
        self.__print("Done.")
        return data

    def __print(self, string):
        print(string)

    def __append_row(self, count, row):
        interval = _math.ceil(count * self.__PERCENT_INTERVAL / 100)
        self.__tmp_data.append(row)
        if interval > 0 and len(self.__tmp_data) % interval == 0:
            current_percent = 100 * len(self.__tmp_data) / count
            _sys.stdout.write("\rLoading %d%%..." % current_percent)
