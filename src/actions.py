from typing import List, Union
from pytypes import is_of_type  # type: ignore
import models


def prompt_insert(
        attributes: models.SchemaTypes
) -> List[Union[str, int]]:
    """
    Ask for a value for each column
    :param attributes: The schema of the table being inserted into
    """
    row: List[Union[str, int]] = []

    for a in attributes:
        if is_of_type(a, models.Attribute[str]):
            messsage = "Please enter a {} (string): "
            print(messsage.format(a.display_name), end='')
            row.append(input())
        elif is_of_type(a, models.Attribute[int]):
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
