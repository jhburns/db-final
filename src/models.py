from typing import List, TypeVar, Generic, Union
from pytypes import is_of_type  # type: ignore

T = TypeVar('T', str, int)


class Attribute(Generic[T]):
    identifier: str
    display_name: str

    def __init__(self, i, d):
        self.identifier = i
        self.display_name = d


G = TypeVar('G', bound=Attribute)


class PrimaryKey(Generic[G]):
    pass


# Schemas
SchemaTypes = List[Union[
    Attribute[str],
    Attribute[int],
    PrimaryKey[Attribute[str]],
    PrimaryKey[Attribute[int]],
]]

customers: SchemaSchema = [
    Attribute[PrimaryKey[int]]("customer_id", "Customer id"),
    Attribute[str]("first_name", "first name"),
    Attribute[str]("last_name", "last name"),
    Attribute[int]("weight_kg", "weight in kilograms"),
]

schemas = [customers]


def prompt_insert(
        attributes: List[Union[Attribute[str], Attribute[int]]]
        ) -> List[Union[str, int]]:
    """
    Ask for a value for each column
    :param attributes: The schema of the table being inserted into
    """
    row: List[Union[str, int]] = []

    for a in attributes:
        if is_of_type(a, Attribute[str]):
            messsage = "Please enter a {} (string): "
            print(messsage.format(a.display_name), end='')
            row.append(input())
        elif is_of_type(a, Attribute[int]):
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


prompt_insert(customers)
