import sqlite3
from contextlib import contextmanager


@contextmanager
def get_base(path: str, is_commit=False):
    try:
        con = sqlite3.connect(path)
        sql = con.cursor()
        yield sql
    finally:
        if is_commit:
            con.commit()
            con.close()
        else:
            con.close()


def get_data_base(path: str, get_url: str, params=None) -> list:
    params = tuple() if params is None else params
    with get_base(path) as sql:
        return sql.execute(get_url, params).fetchall()
