from typing import Union, Optional, Tuple
import sqlite3
from models import SchemaTypes, Attribute


def execute(
        connection: sqlite3.Connection,
        sql: str,
        data: Tuple[Union[str, int], ...],
) -> None:
    """
        Parameters
        ----------
        connection
            The database to query.
        sql
            Prepared SQL, single statement.
        data
            Matching the prepared SQL.
    """
    current = connection.cursor()
    current.execute(sql, data)
    connection.commit()


def fetch(
        connection: sqlite3.Connection,
        sql: str,
        data: Optional[Tuple[int, int]],
) -> str:
    """ Select data from sqlite.

        Parameters
        ----------
        connection
            The database to query.
        sql
            Prepared SQL, using select.
        data
            Matching the prepared SQL.

        Returns
        -------
        The query response.
    """
    current = connection.cursor()

    if data is None:
        current.execute(sql)
    else:
        current.execute(sql, data)

    response = current.fetchone()
    print(str(response))

    return str(response[0])


def generate_insert(
        table_name: str,
        schema: SchemaTypes,
) -> str:
    """ Generate the sql for inserting a record into the given table.

        Parameters
        ----------
        table_name
            The table to insert into.
        schema
            The keys being used to insert.

        Returns
        -------
        An insert in SQL.
    """
    return ''' INSERT INTO {}({})
        VALUES({}) '''.format(
        table_name,
        ", ".join(map(lambda a: a.identifier, schema)),
        ("?, " * len(schema))[:-2])


def generate_delete(
        table_name: str,
        schema: Attribute
) -> str:
    """ Generate the sql by primary key.

        Parameters
        ----------
        table_name
            The table to delete from.
        schema
            The primary key of the row to delete.

        Returns
        -------
        A delete in SQL.
    """
    return ''' DELETE FROM {} WHERE {}=? '''.format(
        table_name, schema.identifier)


class CustomQuery:
    """ Make a built-in query.

        Attributes
        ----------
        sql
            The query.
        description
            Information presented to the user.
        prompt
            Optional, prompt the user to supply data.
    """
    sql: str
    description: str
    prompt: Optional[str]

    def __init__(self, s: str, d: str, p: Optional[str]) -> None:
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
