from typing import List, Union, Mapping, Iterable, Type


class Attribute():
    identifier: str
    display_name: str
    is_primary: bool
    ty = Type

    def __init__(self, i, d, p, t) -> None:
        self.identifier = i
        self.display_name = d
        self.is_primary = p
        self.ty = t


# Schemas
SchemaTypes = List[Union[Attribute]]

tables: Mapping[str, SchemaTypes] = {
    "customers": [
        Attribute("customer_id", "customer ID", True, int),
        Attribute("first_name", "first name", False, str),
        Attribute("last_name", "last name", False, str),
        Attribute("weight_kg", "weight in kilograms", False, int),
    ],

    "planes": [
        Attribute("serial_number", "serial number", True, str),
        Attribute("seat_count_row", "seat count in a row", False, int),
        Attribute("seat_count_column",
                       "seat count in a column", False, int),
        Attribute("max_load_kg", "maximum load, kg", False, int),
    ],

    "inventory": [
        Attribute("inventory_id", "inventory ID", True, int),
        Attribute("plane_id", "plane ID", False, int),
    ],

    "flights": [
        Attribute("flight_id", "flight ID", True, int),
        Attribute("departure_datetime",
                       "seat count in a row", False, str),
        Attribute("i_id", "seat count in a column", False, int),
    ],

    "passengers": [
        Attribute("passenger_id", "customer ID", False, int),
        Attribute("f_id", "flight ID", False, int),
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
        if s.ty is str:
            new_schema.append(s)
        elif s.ty is int and not s.is_primary:
            new_schema.append(s)

    return new_schema
