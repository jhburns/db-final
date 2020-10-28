from typing import List, TypeVar, Generic, Union, Mapping, Iterable
from pytypes import is_of_type  # type: ignore

T = TypeVar('T', str, int)


class Attribute(Generic[T]):
    identifier: str
    display_name: str

    def __init__(self, i, d) -> None:
        self.identifier = i
        self.display_name = d


# Due to issue with boxing and unions,
# This class has to reimplement Attribute
class PrimaryKey(Generic[T]):
    identifier: str
    display_name: str

    def __init__(self, i, d) -> None:
        self.identifier = i
        self.display_name = d


# Schemas
SchemaTypes = List[Union[
    Attribute[str],
    Attribute[int],
    PrimaryKey[str],
    PrimaryKey[int],
]]

PrimaryTypes = Union[
    PrimaryKey[str],
    PrimaryKey[int],
]

tables: Mapping[str, SchemaTypes] = {
    "customers": [
        PrimaryKey[int]("customer_id", "customer ID"),
        Attribute[str]("first_name", "first name"),
        Attribute[str]("last_name", "last name"),
        Attribute[int]("weight_kg", "weight in kilograms"),
    ],

    "planes": [
        PrimaryKey[str]("serial_number", "serial number"),
        Attribute[int]("seat_count_row", "seat count in a row"),
        Attribute[int]("seat_count_column", "seat count in a column"),
        Attribute[int]("max_load_kg", "maximum load, kg"),
    ],

    "inventory": [
        PrimaryKey[int]("inventory_id", "inventory ID"),
        Attribute[int]("plane_id", "plane ID"),
    ],

    "flights": [
        PrimaryKey[int]("flight_id", "flight ID"),
        Attribute[str]("departure_datetime", "seat count in a row"),
        Attribute[int]("i_id", "seat count in a column"),
    ],

    "passengers": [
        PrimaryKey[int]("passenger_id", "customer ID"),
        Attribute[int]("f_id", "flight ID"),
    ]
}


def iter_row(data: List[Union[str, int]]) -> Iterable[str]:
    row: List[str] = []

    for d in data:
        if isinstance(d, str):
            row.append(d)
        elif isinstance(d, int):
            row.append(str(d))

    return iter(row)


# Casts required because mypy can't understand the proper types
def remove_primary_int(schema: SchemaTypes) -> SchemaTypes:
    new_schema: SchemaTypes = []

    for s in schema:
        if is_of_type(s, Attribute[str]):
            new_schema.append(s)
        elif is_of_type(s, Attribute[int]):
            new_schema.append(s)
        elif is_of_type(s, PrimaryKey[str]):
            new_schema.append(s)

    return new_schema


