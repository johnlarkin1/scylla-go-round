from scylla_go_round.common import TableDefinition
from scylla_go_round.scylla import parse_schema

import re


def format_go_identifier(identifier):
    # Define a set of common initialisms that should remain in uppercase
    common_initialisms = {"id", "http", "api", "url"}
    parts = identifier.split("_")
    # More or less, let's convert to camel case
    formatted_parts = [
        part.upper() if part in common_initialisms else part.capitalize()
        for part in parts
    ]
    return "".join(formatted_parts)


def generate_entities_go(tables: list[TableDefinition], filename="entities.go") -> None:
    table_list = parse_schema(tables)
    with open(filename, "w") as file:
        file.write("package scylladb\n\n")
        # Just assume we're going to want `inf` and `time`
        file.write(
            'import (\n\t"time"\n\t"gopkg.in/inf.v0"\n\t"github.com/google/uuid"\n)\n\n'
        )
        for table in table_list:
            # Let's skip any table with `test` in it
            if "test" in table.name.lower():
                continue

            file.write(f"type {format_go_identifier(table.name)} struct {{\n")

            for column in table.columns:
                go_type = map_cql_type_to_go(column.col_type)
                go_identifier = format_go_identifier(column.name)
                pk_tag = ' cql_pk:"true"' if column.primary else ""
                file.write(
                    f'    {go_identifier} {go_type} `cql:"{column.name}"{pk_tag}`\n'
                )
            file.write("}\n\n")
    print(f"Go types created at {filename}")


def map_cql_type_to_go(cql_type):
    """
    Map CQL types to Go types with support for nested map types and sets.
    For example:
    - "map<text, decimal>" becomes "map[string]*inf.Dec" in Go.
    - "set<text>" becomes "[]string" in Go.
    - "list<map<text, decimal>" recurses back to the map case
    """
    # Cleanse our cql_type... this type:
    #   Set(TEXT, frozen) NOT NULL,
    # goes to this
    #   frozen<set<text>>
    # So let's remove that frozen keyword
    frozen_pattern = re.compile(r"frozen<(.+)>")
    frozen_match = frozen_pattern.match(cql_type)
    if frozen_match:
        cql_type = frozen_match.group(1)

    base_type_mapping = {
        "text": "string",
        "int": "int",
        "uuid": "uuid.UUID",
        "float": "float32",
        "double": "float64",
        "bigint": "int64",
        "decimal": "*inf.Dec",
        "timestamp": "time.Time",
        "boolean": "bool",
        "timeuuid": "uuid.UUID",
    }

    complex_type_pattern = re.compile(r"^(map|set|list)<(.+)>$", re.IGNORECASE)

    def handle_complex_type(cql_subtype):
        sub_type_match = complex_type_pattern.match(cql_subtype)
        if sub_type_match:
            collection_type, inner_types = sub_type_match.groups()
            inner_types = split_complex_types(inner_types)
            if collection_type.lower() == "map":
                go_key_type = map_cql_type_to_go(inner_types[0])
                go_value_type = map_cql_type_to_go(inner_types[1])
                return f"map[{go_key_type}]{go_value_type}"
            elif collection_type.lower() == "set":
                go_value_type = map_cql_type_to_go(inner_types[0])
                return f"[]{go_value_type}"
            elif collection_type.lower() == "list":
                go_value_type = map_cql_type_to_go(inner_types[0])
                return f"[]{go_value_type}"
        return base_type_mapping.get(cql_subtype, "interface{}")

    def split_complex_types(types_string):
        depth = 0
        types = []
        start = 0
        for i, char in enumerate(types_string):
            if char == "<":
                depth += 1
            elif char == ">":
                depth -= 1
            elif char == "," and depth == 0:
                types.append(types_string[start:i].strip())
                start = i + 1
        types.append(types_string[start:].strip())
        return types

    return handle_complex_type(cql_type)
