from psycopg2 import connect
import re


def _clean(value: str) -> str:
    if not isinstance(value, str):
        return value
    return re.sub(r"[']", "''", value)


def tables(path_in: str, struct_file: dict, con: connect):
    try:
        cur = con.cursor()

        keys = struct_file.keys()
        for key in keys:
            print(f"[INFO] Creating table {key}")
            schema = struct_file[key]
            fields = schema.keys()

            SQL = f"CREATE TABLE {key} ("
            for field in fields:
                SQL += f"{field} {schema[field]}"
            SQL += ");\n"

            cur.execute(SQL)
        con.commit()

    except Exception as e:
        print(f"[ERROR] {e}")
        con.rollback()
        return e


def tuples(struct_file: dict, tuples: list, con: connect):
    try:
        cur = con.cursor()
        key = list(struct_file.keys())[0]

        print(f"[INFO] Iserting tuples in {key}")
        schema = struct_file[key]
        fields = schema.keys()
        len_fields = len(fields)

        for tuple in tuples:
            SQL = f"INSERT INTO {key} ("
            for idx, field in enumerate(fields):
                SQL += f"{field}," if idx < len_fields - 1 else f"{field}"
            SQL += ") "

            len_tuple = len(tuple)
            SQL += "VALUES ("
            for idx, value in enumerate(tuple):
                SQL += (
                    f"'{_clean(value)}',"
                    if idx < len_tuple - 1
                    else f"'{_clean(value)}'"
                )
            SQL += ")"

            cur.execute(SQL)
        con.commit()

    except Exception as e:
        print(f"[ERROR] {e}")
        con.rollback()
        return e
