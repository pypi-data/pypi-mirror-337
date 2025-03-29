# FlexiDB

A flexible Python database connector that provides a consistent API across multiple database types.

## Features

- Simple and consistent API for database operations
- Support for multiple database types:
  - MongoDB
  - PostgreSQL
  - MySQL
  - SQLite
  - Redis
- Easy switching between database backends
- Minimal configuration required

## Installation

```bash
pip install flexidb
```

## Basic Usage

```python
from flexidb import get_database

# Connect to a MongoDB database
db = get_database("mongodb", uri="mongodb://localhost:27017", database="test_db")

# Insert data
db.create("users", {"name": "John", "email": "john@example.com"})

# Find data
user = db.read("users", {"name": "John"})

# Update data
db.update("users", {"name": "John"}, {"email": "john.doe@example.com"})

# Delete data
db.delete("users", {"name": "John"})

# Close connection
db.disconnect()
```

## Supported Databases

- MongoDB: `get_database("mongodb", ...)`
- PostgreSQL: `get_database("postgresql", ...)`
- MySQL: `get_database("mysql", ...)`
- SQLite: `get_database("sqlite", ...)`
- Redis: `get_database("redis", ...)`
```
