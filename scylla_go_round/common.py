from dataclasses import dataclass, field


@dataclass
class Column:
    name: str
    col_type: str
    primary: bool = False


@dataclass
class Table:
    name: str
    columns: list[Column] = field(default_factory=list)


@dataclass
class TableDefinition:
    keyspace_name: str
    entity_type: str
    table_name: str
    create_statement: str

    @classmethod
    def from_row(cls, row):
        return cls(
            keyspace_name=row[0],
            entity_type=row[1],
            table_name=row[2],
            create_statement=row[3],
        )
