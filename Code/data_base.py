import sqlite3
from contextlib import contextmanager
from typing import *


@contextmanager
def get_base(path: str, is_commit: bool = False):
    try:
        con = sqlite3.connect(path)
        sql = con.cursor()
        yield sql
    finally:
        if is_commit:
            con.commit()
        con.close()


def get_data_base(path: str, get_url: str, params: tuple or dict = None) -> list:
    """
    path: путь до базы данных sqlite3
    get_url: запрос к базе данных на языке SQLite
    params: словарь или кортеж с данными для запроса get_url
    return: list из базы данных по get_url с параметрами params
    """
    params = tuple() if params is None else params
    with get_base(path) as sql:
        return sql.execute(get_url, params).fetchall()


class Base:
    def __init__(self, path: str, get_url: str, params: tuple or dict = None, key: object = None) -> None:
        self.path = path
        self.get_url = get_url
        self.params = params
        self.key = key

    def __iter__(self) -> Generator[Tuple[Any, Any], Any, None]:
        data = get_data_base(self.path, self.get_url, self.params)
        if self.key:
            data.sort(key=self.key)
        return ((i[0], i[1]) for i in data)
