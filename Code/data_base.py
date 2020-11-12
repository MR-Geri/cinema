import sqlite3


def get_data_base(path: str, get_url: str, params=None) -> list:
    params = tuple() if params is None else params
    con = sqlite3.connect(path)
    sql = con.cursor()
    result = sql.execute(get_url, params).fetchall()
    con.close()
    return result
