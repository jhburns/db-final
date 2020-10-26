# From: https://www.sqlitetutorial.net/sqlite-python/create-tables/

import sqlite3
from sqlite3 import Error
from typing import Optional


def create_connection(db_file: str) -> Optional[sqlite3.Connection]:
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return connection


def create_tables(connection: sqlite3.Connection, create_table_sql: str):
    """ create tables
    :param conn: Connection object
    :param create_table_sql: an SQL script
    :return:
    """
    try:
        cursor = connection.cursor()
        cursor.executescript(create_table_sql)
    except Error as e:
        print("Error! cannot create tables.")
        print(e)


def initialize_db():
    connection = create_connection(":memory:")

    if connection is not None:
        # create tables
        path = "./burns_schema.sql"
        sql_file = open(path, 'r')
        sql = sql_file.read()
        create_tables(connection, sql)
    else:
        print("Error! cannot create the database connection.")

