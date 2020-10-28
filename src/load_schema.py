# From: https://www.sqlitetutorial.net/sqlite-python/create-tables/

import sqlite3
from sqlite3 import Error
from typing import Optional


def create_connection(db_file: str) -> Optional[sqlite3.Connection]:
    """ create a database connection to the SQLite database
    specified by db_file
    :param db_file: database file
    :return: connection object if it succeeds
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print("Error! creating connection failed.")
        print(e)
        return None


def create_tables(
        connection: sqlite3.Connection, create_table_sql: str
        ) -> None:
    """ create tables
    :param connection: connection object
    :param create_table_sql: an SQL script
    :return:
    """
    cursor = connection.cursor()
    cursor.executescript(create_table_sql)
    connection.commit()


def initialize_db() -> Optional[sqlite3.Connection]:
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
