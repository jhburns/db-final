from typing import Union, Optional, Tuple
import models
import sqlite3


def execute(
        connection: sqlite3.Connection,
        sql: str,
        data: Tuple[Union[str, int], ...],
) -> None:
    current = connection.cursor()
    current.execute(sql, data)
    connection.commit()


def fetch(
        connection: sqlite3.Connection,
        sql: str,
        data: Optional[Tuple[int, int]],
) -> str:
    current = connection.cursor()

    if data is None:
        current.execute(sql)
    else:
        current.execute(sql, data)

    return str(current.fetchone()[0])


def generate_insert(
        table_name: str,
        schema: models.SchemaTypes,
) -> str:
    """
    Generate the sql for inserting a record into the given table
    :param table_name: table being inserted into
    :param schema:
    :return:
    """
    return ''' INSERT INTO {}({})
        VALUES({}) '''.format(
        table_name,
        ", ".join(map(lambda a: a.identifier, schema)),
        ("?, " * len(schema))[:-2])


def generate_delete(
        table_name: str,
        schema: models.Attribute
) -> str:
    """
    Generate the sql for by primary key
    :param table_name: table being deleted from
    :param schema:
    :return:
    """
    return ''' DELETE FROM {} WHERE {}=? '''.format(
        table_name, schema.identifier)


class CustomQuery:
    sql: str
    description: str
    prompt: Optional[str]

    def __init__(self, s, d, p) -> None:
        self.sql = s
        self.description = d
        self.prompt = p


custom_queries = [
    CustomQuery("SELECT AVG(weight_kg) FROM customers",
                "Find the average weight of customers.", None),
    CustomQuery('''SELECT MAX(plane_id), plane_id FROM (SELECT COUNT(plane_id),
                 plane_id FROM inventory GROUP BY plane_id)''',
                '''Find the serial number and count of the most type of planes
           in inventory.''',
                None),
    CustomQuery("SELECT plane_id, count() FROM inventory GROUP BY plane_id",
                "Find the most common type of plane in inventory.", None),
    CustomQuery('''SELECT (seat_count_row * seat_count_column) < (SELECT COUNT(*)
                 FROM passengers WHERE f_id=?) FROM flights, inventory, planes
                WHERE flight_id=?''',
                "Find whether a flight is not full.", "Flight id (integer)"),
    CustomQuery('''SELECT max_load_kg < (SELECT COUNT(*) FROM passengers WHERE
                 f_id=?) FROM flights, inventory, planes WHERE flight_id=?''',
                "Find whether a flight is over its maximum weight.",
                "Flight id (integer)")
]
