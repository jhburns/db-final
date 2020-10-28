# Modified from: https://www.sqlitetutorial.net/sqlite-python/create-tables/

from sqlite3 import Error, connect, Connection
from typing import Optional


def create_connection(db_file: str) -> Optional[Connection]:
    """ Create a database connection to the SQLite database specified by db_file.

        Parameters
        ----------
        db_file
            The file to connect to.

        Returns
        -------
        A connection, if it was possible.
    """
    try:
        connection = connect(db_file)
        return connection
    except Error as e:
        print("Error! creating connection failed.")
        print(e)
        return None


def create_tables(connection: Connection, create_tables_sql: str) -> None:
    """ Execute an SQL script in order to make tables if they don't already exist.

        Parameters
        ----------
        connection
            The database to create tables in.
        create_tables_sql
            The script to run.
    """
    cursor = connection.cursor()
    cursor.executescript(create_tables_sql)
    connection.commit()


def initialize_db() -> Optional[Connection]:
    """ Create a connection to the database and create tables in it.

        Returns
        -------
        A connection, if initialization was successful.
    """
    connection = create_connection("./airline.db")

    if connection is not None:
        try:
            # read sql statements
            path = "./burns_schema.sql"
            sql_file = open(path, 'r')

            # create tables
            sql = sql_file.read()
            create_tables(connection, sql)
        except Error as e:
            print("Error! cannot create tables.")
            print(e)
            return None

    return connection
