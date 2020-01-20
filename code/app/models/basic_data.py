# app/models/basic_data.py

from slimmyorm import BaseData


class BasicData(BaseData):
    def __init__(self, table=False, name=False, data=False):
        """Gets table name from param, if present """
        self._table = self._table if hasattr(self, '_table') else table
        super(BasicData, self).__init__(name, data)

    def setup(self):
        self.remove_attribute('id')
