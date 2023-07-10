# OData query
from typing import List, Dict, Any
from enum import Enum

class Query:
    def __init__(self):
        self._options: Dict[str, Any] = dict()
        self._options['top'] = 30
        self._options['format'] = 'JSON'

    def select(self, columns:List[Enum]) -> None:
        columns = list(map(lambda x: x.value, columns))
        self._options['select'] = ','.join(columns)

    def filter(self, filter) -> None:
        self._options['filter'] = filter

    def top(self, top: int) -> None:
        self._options['top'] = top
    
    def format(self, format: str) -> None:
        self._options['format'] = format
    
    def complete(self) -> str:
        option_list = list(map(lambda x: self._as_string(x[0], x[1]), self._options.items()))
        return '&'.join(option_list)

    def _as_string(self, key, value) -> str:
        return f'${key}={value}'
        