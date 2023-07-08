# OData query
from typing import List
from enum import Enum

class Query:
    def __init__(self):
        self.options = dict()
        self.options['top'] = 30
        self.options['format'] = 'JSON'

    def select(self, columns:List[Enum]):
        columns = list(map(lambda x: x.value, columns))
        self.options['select'] = ','.join(columns)

    def filter(self, filter):
        self.options['filter'] = filter

    def top(self, top: int):
        self.options['top'] = top
    
    def format(self, format: str):
        self.options['format'] = format
    
    def complete(self):
        option_list = list(map(lambda x: self.__as_string(x[0], x[1]), self.options.items()))
        return '&'.join(option_list)

    def __as_string(self, key, value):
        return f'${key}={value}'
        