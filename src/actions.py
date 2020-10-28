from typing import List, Union, Optional
import models
import sqlite3


def execute(
        connection: sqlite3.Connection,
        sql: str,
        data: List[Union[str, int]],
) -> None:
    current = connection.cursor()
    current.execute(sql, data)
    connection.commit()


def prompt_insert(
        attributes: models.SchemaTypes,
) -> List[Union[str, int]]:
    """
    Ask for a value for each column
    :param attributes: The schema of the table being inserted into
    """
    row: List[Union[str, int]] = []

    for a in attributes:
        if a.ty is str:
            messsage = "Please enter a {} (string): "
            print(messsage.format(a.display_name), end='')
            row.append(input())
        elif a.ty is int:
            while True:
                messsage = "Please enter a {} (positive integer): "
                print(messsage.format(a.display_name), end='')

                try:
                    user_input = int(input())
                    if user_input <= 0:
                        raise TypeError

                    row.append(user_input)
                    break
                except ValueError:
                    print("Error: {} was not an integer.".format(
                        a.display_name))
                except TypeError:
                    print("Error: {} was not positive.".format(
                        a.display_name))

                print()
                print("Try again")

    return row


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
    CustomQuery("", "b", None),
]
