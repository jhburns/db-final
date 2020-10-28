from typing import List, Mapping, Type, Dict


class Attribute():
    """ Schema definition for a column in SQL

        Attributes
        ----------
        identifier
            The SQL identifier.
        display_name
            The text to display when prompting for this value.
        is_primary
            If true, this attribute is a primary key.
        ty
            The type of the attribute, str or int only.
    """
    identifier: str
    display_name: str
    is_primary: bool
    ty: Type

    def __init__(self, i: str, d: str, p: bool, t: Type) -> None:
        self.identifier = i
        self.display_name = d
        self.is_primary = p
        self.ty = t


# Schemas
SchemaTypes = List[Attribute]

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
                  "the departure date", False, str),
        Attribute("i_id", "plane ID", False, int),
    ],

    "passengers": [
        Attribute("passenger_id", "customer ID", False, int),
        Attribute("f_id", "flight ID", False, int),
    ]
}


def remove_primary_int(schema: SchemaTypes) -> SchemaTypes:
    """ Remove any primary, int type attribute from a schema.
        Because those are set automatically by sqlite.

        Parameters
        ----------
        schema
            The schema to alter.

        Returns
        -------
        Schema without primary, int attributes.
    """
    new_schema: SchemaTypes = []

    for s in schema:
        if s.ty is str:
            new_schema.append(s)
        elif s.ty is int and not s.is_primary:
            new_schema.append(s)

    return new_schema


def primary_only(
    tables: Mapping[str, SchemaTypes]
) -> Dict[str, Attribute]:
    """ Remove any non primary key.

        Parameters
        ----------
        tables
            A description of all table schemas.

        Returns
        -------
        Tables without primary keys.
    """
    primary_only: Dict[str, Attribute] = {}

    for (name, attributes) in tables.items():
        for a in attributes:
            if a.is_primary:
                primary_only[name] = a

    return primary_only
