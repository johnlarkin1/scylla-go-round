# Scylla-Go-Round

Welcome to Scylla-Go-Round! Spin up your ScyllaDB schemas into Go types with ease and style. This CLI tool is your handy companion in bridging the gap between schema design and Go implementation, ensuring your applications are running smoothly with the latest data structures.

## Features

- **Generate Go types** directly from your ScyllaDB or Cassandra schema.
- **Automatic connection** to your ScyllaDB instance.
- **Environment and CLI flexibility** for easy configuration.

## Getting Started

### Prerequisites

- Python 3.6+
- ScyllaDB or Cassandra setup

### Installation

Install `scylla-go-round` using pip:

```bash
pip install scylla-go-round
```

### Usage

Generate Go types by running:

```bash
scyllago --keyspace your_keyspace_name --host your_scylladb_host
```

### Configuration

You can configure `scylla-go-round` via environment variables or command line arguments:

- `SCYLLADB_DEV_HOST`: The host for your ScyllaDB instance.
- `SCYLLADB_DEV_ROLE`: Your ScyllaDB username.
- `SCYLLADB_DEV_PWD`: Your ScyllaDB password.

There is an example of what your `.env` file can look like in this current directory. You should rename that to be the `.env` file if you want it to be loaded in from this tool.

### Contributing

We love contributions! If you'd like to help improve Scylla-Go-Round, please follow these steps:

- Fork the repo on GitHub.
- Clone your fork locally.
- Create a new feature branch (git checkout -b my-new-feature).
- Make your changes.
- Push the branch to GitHub (git push origin my-new-feature).
- Submit a pull request.

### License

Scylla-Go-Round is released under the MIT License. See the LICENSE file for more details.

Happy Coding!
Thank you for using or contributing to Scylla-Go-Round. Have fun spinning your schemas into efficient Go types!
