from typing import List, TypeVar, Generic, Union

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

customers: SchemaTypes = [
    PrimaryKey[int]("customer_id", "customer ID"),
    Attribute[str]("first_name", "first name"),
    Attribute[str]("last_name", "last name"),
    Attribute[int]("weight_kg", "weight in kilograms"),
]

planes: SchemaTypes = [
    PrimaryKey[str]("serial_number", "serial number"),
    Attribute[int]("seat_count_row", "seat count in a row"),
    Attribute[int]("seat_count_column", "seat count in a column"),
    Attribute[int]("max_load_kg", "maximum load, kg"),
]

inventory: SchemaTypes = [
    PrimaryKey[int]("inventory_id", "inventory ID"),
    Attribute[int]("plane_id", "plane ID"),
]

flights: SchemaTypes = [
    PrimaryKey[int]("flight_id", "flight ID"),
    Attribute[str]("departure_datetime", "seat count in a row"),
    Attribute[int]("i_id", "seat count in a column"),
]

passengers: SchemaTypes = [
    PrimaryKey[int]("passenger_id", "customer ID"),
    Attribute[int]("f_id", "flight ID"),
]

schemas = [customers, planes, inventory, flights, passengers]
