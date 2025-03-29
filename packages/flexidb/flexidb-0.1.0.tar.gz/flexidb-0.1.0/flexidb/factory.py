"""
Factory module for creating database connections.
"""

from typing import Dict, Any, Optional

from .interface import DatabaseInterface
from .mongodb import MongoDBConnector
from .postgresql import PostgreSQLConnector
from .mysql import MySQLConnector
from .sqlite import SQLiteConnector
from .redis import RedisConnector


def get_database(db_type: str, **kwargs) -> DatabaseInterface:
    """
    Factory function to get a database connection of the specified type.
    
    Args:
        db_type: The type of database to connect to ('mongodb', 'postgresql', 'mysql', 'sqlite', 'redis')
        **kwargs: Connection parameters specific to the database type
        
    Returns:
        A database connector instance that implements the DatabaseInterface
        
    Raises:
        ValueError: If the specified database type is not supported
    """
    db_types = {
        "mongodb": MongoDBConnector,
        "postgresql": PostgreSQLConnector,
        "mysql": MySQLConnector,
        "sqlite": SQLiteConnector,
        "redis": RedisConnector
    }
    
    if db_type.lower() not in db_types:
        supported = ", ".join(f"'{k}'" for k in db_types.keys())
        raise ValueError(f"Unsupported database type: '{db_type}'. Supported types are: {supported}")
    
    connector_class = db_types[db_type.lower()]
    return connector_class(**kwargs)
