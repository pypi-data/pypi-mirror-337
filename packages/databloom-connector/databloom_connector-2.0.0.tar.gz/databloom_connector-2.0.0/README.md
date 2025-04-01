# DataBloom SDK Client

A Python SDK client for establishing connections to various data sources and integrating with data warehouses.

## Project Structure

```
databloom/                      # Main package
├── api/                       # API modules
│   ├── credentials.py         # Credentials management
│   ├── db_connector.py        # Database connection handling
│   └── nessie_metadata.py     # Nessie metadata client
├── core/                      # Core functionality
│   ├── connector/             # Database connectors
│   │   ├── postgresql.py      # PostgreSQL connector
│   │   └── mysql.py          # MySQL connector
│   └── spark/                # Spark integration
│       └── session.py        # Spark session management
└── datasets/                 # Dataset operations
    └── dataset.py           # Dataset management
```

## Installation

### Development Installation

1. Create and activate a conda environment:
```bash
conda create -n databloom python=3.11
conda activate databloom
```

2. Install the package dependencies:
```bash
# Install core dependencies
make install

# Install development dependencies (includes testing and code quality tools)
make dev
```

## Development

### Code Quality

```bash
# Format code
make format

# Run linter
make lint

# Run type checker
make type-check
```

### Testing

The project uses pytest for testing. Tests are organized into categories:
- Unit tests
- Integration tests (connectors)
- Dataset tests

Run tests using make commands:

```bash
# Run all tests
make test

# Run specific test categories
make test-unit
make test-integration
make test-dataset

# Run from tests directory
cd tests
make all
make unit
make integration
make dataset
make connector-postgresql  # Run specific connector test
```

### Environment Variables

Required environment variables:
```bash
# S3 Configuration
S3_ENDPOINT=localhost:9000
S3_ACCESS_KEY_ID=admin
S3_SECRET_ACCESS_KEY=password

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DBNAME=postgres

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password

# Nessie Configuration
NESSIE_URI=http://localhost:19120/api/v1
NESSIE_REF=main
NESSIE_WAREHOUSE=s3a://nessie/
NESSIE_IO_IMPL=org.apache.iceberg.hadoop.HadoopFileIO
```

## Usage Example

```python
from databloom import DataBloomContext

# Create context
ctx = DataBloomContext()

# Attach source
ctx.attach_source(source="postgresql/postgres_source", dbname="mktvng", dest="source_mktvng")

# Query using DuckDB
duckdb_con = ctx.get_duck_con()
df_1 = duckdb_con.sql("""
    select * from source_mktvng.category_table_v2
""")

# Work with local data
import pandas as pd
dataframe_local = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"]
})

# Query in data warehouse
df_1 = ctx.duckdb_sql("""
    select * from source_mktvng.category_table_v2
    join on {{dataset.category_table_v2}}
    join on dataframe_local
""")
```

## Dependencies

Core dependencies (requirements.txt):
- pandas>=2.2.3
- pyspark==3.4.2
- duckdb>=0.10.0
- sqlalchemy>=2.0.38
- psycopg2-binary>=2.9.10
- mysql-connector-python>=8.0.0
- findspark>=2.0.1
- requests>=2.31.0
- python-dotenv>=0.19.0
- trino>=0.333.0

Development dependencies (requirements-dev.txt):
- pytest>=8.0.0
- pytest-cov>=4.1.0
- black>=24.0.0
- isort>=5.13.0
- flake8>=7.0.0
- mypy>=1.8.0

## License

MIT License 