import argparse
import os
from dotenv import load_dotenv

from scylla_go_round.go import generate_entities_go
from scylla_go_round.scylla import (
    connect_to_scylla,
    describe_keyspace,
    generate_schema_file,
)


def main():
    # Load environment variables from .env file if it exists
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)

    parser = argparse.ArgumentParser(
        description="Generate Go types from ScyllaDB schema."
    )
    parser.add_argument(
        "--keyspace", required=True, help="Keyspace to generate Go types for"
    )
    parser.add_argument(
        "--host", default=os.getenv("SCYLLADB_HOST"), help="ScyllaDB host"
    )
    parser.add_argument(
        "--username", default=os.getenv("SCYLLADB_ROLE"), help="ScyllaDB username"
    )
    parser.add_argument(
        "--password", default=os.getenv("SCYLLADB_PWD"), help="ScyllaDB password"
    )
    parser.add_argument(
        "--output-dir", default="output", help="Directory to output files"
    )

    args = parser.parse_args()

    session = connect_to_scylla(
        [args.host], args.keyspace, args.username, args.password
    )
    tables = describe_keyspace(session, args.keyspace)
    schema_file_dest = os.path.join(args.output_dir, "schema.cql")
    entities_file_dest = os.path.join(args.output_dir, f"{args.keyspace}_entities.go")

    generate_schema_file(tables, schema_file_dest)
    generate_entities_go(tables, entities_file_dest)


if __name__ == "__main__":
    main()
