"""
SQLite connector implementation.
"""

from typing import Dict, Any, List, Optional, Union
import sqlite3
from pathlib import Path
from .interface import DatabaseInterface


class SQLiteConnector(DatabaseInterface):
    """SQLite implementation of the database interface."""
    
    def __init__(self, database: str = "database.db", **kwargs):
        """
        Initialize SQLite connector.
        
        Args:
            database: Path to SQLite database file
            **kwargs: Additional connection parameters
        """
        self.database = database
        self.connection_params = kwargs
        self.conn = None
        self.cursor = None
        
    def connect(self) -> None:
        """Establish connection to SQLite database."""
        try:
            # Ensure parent directory exists
            db_path = Path(self.database)
            if not db_path.parent.exists():
                db_path.parent.mkdir(parents=True, exist_ok=True)
                
            self.conn = sqlite3.connect(self.database, **self.connection_params)
            # Enable dictionary cursor
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SQLite: {str(e)}")
    
    def disconnect(self) -> None:
        """Close SQLite connection."""
        if self.conn:
            try:
                if self.cursor:
                    self.cursor.close()
                self.conn.close()
                self.conn = None
                self.cursor = None
            except Exception as e:
                raise ConnectionError(f"Failed to disconnect from SQLite: {str(e)}")
    
    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """
        Insert a record into a SQLite table.
        
        Args:
            collection: Table name
            data: Record to insert
            
        Returns:
            ID of the inserted record (assumes an auto-increment 'id' field or rowid)
        """
        if not self.conn:
            self.connect()
            
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            values = list(data.values())
            
            query = f"INSERT INTO {collection} ({columns}) VALUES ({placeholders})"
            
            self.cursor.execute(query, values)
            self.conn.commit()
            
            # Return the last insert rowid
            return str(self.cursor.lastrowid)
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Failed to insert record: {str(e)}")
    
    def read(self, collection: str, query: Dict[str, Any], limit: Optional[int] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Query records from a SQLite table.
        
        Args:
            collection: Table name
            query: Filter conditions
            limit: Maximum number of records to return
            
        Returns:
            Single record or list of records
        """
        if not self.conn:
            self.connect()
            
        try:
            conditions = []
            values = []
            
            for key, value in query.items():
                conditions.append(f"{key} = ?")
                values.append(value)
                
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            sql = f"SELECT * FROM {collection} WHERE {where_clause} {limit_clause}"
            
            self.cursor.execute(sql, values)
            
            if limit == 1:
                # Return a single record
                row = self.cursor.fetchone()
                if row:
                    return {key: row[key] for key in row.keys()}
                return {}
            else:
                # Return a list of records
                rows = self.cursor.fetchall()
                return [{key: row[key] for key in row.keys()} for row in rows]
        except Exception as e:
            raise ValueError(f"Failed to query records: {str(e)}")
    
    def update(self, collection: str, query: Dict[str, Any], data: Dict[str, Any]) -> int:
        """
        Update records in a SQLite table.
        
        Args:
            collection: Table name
            query: Filter conditions
            data: Updates to apply
            
        Returns:
            Number of records updated
        """
        if not self.conn:
            self.connect()
            
        try:
            # Build SET clause
            set_items = []
            set_values = []
            
            for key, value in data.items():
                set_items.append(f"{key} = ?")
                set_values.append(value)
                
            set_clause = ", ".join(set_items)
            
            # Build WHERE clause
            where_items = []
            where_values = []
            
            for key, value in query.items():
                where_items.append(f"{key} = ?")
                where_values.append(value)
                
            where_clause = " AND ".join(where_items) if where_items else "1=1"
            
            # Combine all values
            all_values = set_values + where_values
            
            # Execute update
            sql = f"UPDATE {collection} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(sql, all_values)
            row_count = self.cursor.rowcount
            self.conn.commit()
            
            return row_count
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Failed to update records: {str(e)}")
    
    def delete(self, collection: str, query: Dict[str, Any]) -> int:
        """
        Delete records from a SQLite table.
        
        Args:
            collection: Table name
            query: Filter conditions
            
        Returns:
            Number of records deleted
        """
        if not self.conn:
            self.connect()
            
        try:
            conditions = []
            values = []
            
            for key, value in query.items():
                conditions.append(f"{key} = ?")
                values.append(value)
                
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            sql = f"DELETE FROM {collection} WHERE {where_clause}"
            self.cursor.execute(sql, values)
            row_count = self.cursor.rowcount
            self.conn.commit()
            
            return row_count
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Failed to delete records: {str(e)}")
    
    def list_collections(self) -> List[str]:
        """
        List all tables in the database.
        
        Returns:
            List of table names
        """
        if not self.conn:
            self.connect()
            
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            results = self.cursor.fetchall()
            return [row['name'] for row in results]
        except Exception as e:
            raise ConnectionError(f"Failed to list tables: {str(e)}")
