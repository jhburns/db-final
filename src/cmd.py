from typing import List, Union, Mapping, Dict, Optional, Tuple
from load_schema import initialize_db
from models import SchemaTypes, Attribute, tables, remove_primary_int
from actions import (
    execute, generate_delete,
    generate_insert, custom_queries, fetch
)


def prompt_str(content: str) -> str:
    messsage = "\tPlease enter a {} (string): "
    print(messsage.format(content), end='')
    return input()


def prompt_int(content: str) -> int:
    while True:
        messsage = "\tPlease enter the {} (integer): "
        print(messsage.format(content), end='')

        try:
            user_input = int(input())
            if user_input <= 0:
                raise TypeError

            return user_input
        except ValueError:
            print("\tError: {} was not an integer.".format(messsage))
        except TypeError:
            print("\tError: {} was not positive.".format(messsage))

        print()
        print("\tTry again")


def prompt_insert(
        attributes: SchemaTypes,
) -> List[Union[str, int]]:
    """
    Ask for a value for each column
    :param attributes: The schema of the table being inserted into
    """
    row: List[Union[str, int]] = []

    for a in attributes:
        if a.ty is str:
            row.append(prompt_str(a.display_name))
        elif a.ty is int and not a.is_primary:
            row.append(prompt_int(a.display_name))

    return row


def primary_only(
    tables: Mapping[str, SchemaTypes]
) -> Dict[str, Attribute]:
    primary_only: Dict[str, Attribute] = {}

    for (name, attributes) in tables.items():
        for a in attributes:
            if a.is_primary:
                primary_only[name] = a

    return primary_only


print("Welcome to the airline manager 20000")
connection = initialize_db()

if connection is None:
    print("Error! initializing the db failed. Exiting.")
else:
    print("Connected to the database file: airline.db")
    print()

    while True:
        print('1. Insert, 2. Delete, 3. Predefined Query, 4. Quit')
        choice_input = input("Your choice: ")

        try:
            choice = int(choice_input)
            print("------------------")

            if choice == 1:
                print("Choose a table to insert into.")
                for (i, table) in enumerate(tables):
                    print("\t{}. {}".format(i, table))

                choice2 = int(input("\tYour choice: "))
                if choice2 < 0 or choice2 > len(tables) - 1:
                    raise ValueError
                print()

                table_name = list(tables.keys())[choice2]
                schema = tables[table_name]
                responce1 = tuple(prompt_insert(schema))

                execute(
                    connection,
                    generate_insert(
                        table_name,
                        remove_primary_int(schema)),
                    responce1)
            elif choice == 2:
                print("Choose a table to delete from.")

                primaries = primary_only(tables)
                for (i, table) in enumerate(primaries):
                    print("\t{}. {}".format(i, table))

                choice2 = int(input("\tYour choice: "))
                if choice2 < 0 or choice2 > len(primaries) - 1:
                    raise ValueError
                print()

                table_name = list(primaries.keys())[choice2]
                attribute = primaries[table_name]

                responce2: Tuple[Union[str, int]]
                if attribute.ty is str:
                    respone = prompt_str(attribute.display_name)
                elif attribute.ty is int:
                    responce2 = (prompt_int(attribute.display_name),)

                execute(
                    connection,
                    generate_delete(
                        table_name,
                        attribute),
                    responce2)
            elif choice == 3:
                print("Choose a predefined query.")

                for (i, q) in enumerate(custom_queries):
                    print("\t{}. {}".format(i, q.description))

                choice2 = int(input("\tYour choice: "))
                if choice2 < 0 or choice2 > len(custom_queries) - 1:
                    raise ValueError
                print()

                action = custom_queries[choice2]

                responce3: Optional[Tuple[int, int]] = None
                if action.prompt is not None:
                    mes = int(input("\t{}: ".format(action.prompt)))
                    responce3 = (mes, mes)

                result = fetch(
                    connection,
                    action.sql,
                    responce3)
                print("\tQuery result: {}".format(result))
            elif choice == 4:
                print("Quitting...")
                break
            else:
                raise ValueError

            print("\t--Done!--")
            print()
        except ValueError:
            print("Error! Try again, input the proper type.")
            print()
        except Exception as e:
            print("Error! " + str(e))
            print("An error unexpected has occurred, try again.")
            print()

    connection.close()
