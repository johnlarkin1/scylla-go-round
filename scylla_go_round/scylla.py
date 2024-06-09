from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Session, ResultSet

from scylla_go_round.common import Column, Table, TableDefinition

import re


def connect_to_scylla(
    hosts: list[str], keyspace: str, username: str, password: str
) -> Session:
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster(hosts, auth_provider=auth_provider)
    session = cluster.connect(keyspace)
    return session


def parse_schema(tables: list[TableDefinition]) -> list[Table]:
    column_pattern = re.compile(
        r"^\s*(\w+)\s+((?:[\w\s]+<(?:[^<>]|<[^<>]*>)*>|[\w\s]+)(?:,|$))", re.MULTILINE
    )
    primary_key_pattern = re.compile(r"PRIMARY KEY\s*\(([^)]+)\)", re.IGNORECASE)

    results = []
    for table in tables:
        table_name = table.table_name
        columns_part = table.create_statement

        primary_keys = []
        pk_match = primary_key_pattern.search(columns_part)
        if pk_match:
            # Handle composite primary keys by splitting them carefully
            primary_keys = [
                pk.strip() for pk in re.split(r",\s*(?![^()]*\))", pk_match.group(1))
            ]

        columns = []
        # We split the columns part to safely process column definitions before PRIMARY KEY or WITH clauses
        columns_data = re.split(r"\bPRIMARY KEY\b|\bWITH\b", columns_part)[0]
        for column_match in column_pattern.finditer(columns_data):
            column_name = column_match.group(1)
            # Our regex pulls the comma, so let's cut that out
            column_type = column_match.group(2).strip()[:-1]
            primary = column_name in primary_keys
            columns.append(
                Column(name=column_name, col_type=column_type, primary=primary)
            )

        results.append(Table(name=table_name, columns=columns))

    return results


def generate_schema_file(tables: list[TableDefinition], filename="schema.cql") -> None:
    with open(filename, "w") as file:
        for table in tables:
            file.write(table.create_statement)
            file.write("\n\n")

    print(f"Schema file created at {filename}")


def describe_keyspace(session: Session, keyspace: str) -> list[TableDefinition]:
    result: ResultSet = session.execute(f"DESCRIBE KEYSPACE {keyspace}")
    data: list[TableDefinition] = [
        TableDefinition.from_row(row) for row in result.all()
    ]
    return [table for table in data if table.entity_type == "table"]
