import sqlite3
from contextlib import contextmanager


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


def get_data_base(path: str, get_url: str, params: tuple = None) -> list:
    params = tuple() if params is None else params
    with get_base(path) as sql:
        return sql.execute(get_url, params).fetchall()


class Base:
    def __init__(self, path: str, get_url: str, params: tuple = None) -> None:
        self.path = path
        self.get_url = get_url
        self.params = params

    def __iter__(self) -> object:
        return (i for i in get_data_base(self.path, self.get_url, self.params))
