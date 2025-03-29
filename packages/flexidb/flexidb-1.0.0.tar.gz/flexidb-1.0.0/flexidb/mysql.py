"""
MySQL connector implementation.
"""

from typing import Dict, Any, List, Optional, Union
import mysql.connector
from .interface import DatabaseInterface


class MySQLConnector(DatabaseInterface):
    """MySQL implementation of the database interface."""
    
    def __init__(self, 
                host: str = "localhost", 
                port: int = 3306, 
                user: str = "root", 
                password: str = "", 
                database: str = "mysql",
                **kwargs):
        """
        Initialize MySQL connector.
        
        Args:
            host: Database server host
            port: Database server port
            user: Username for authentication
            password: Password for authentication
            database: Name of the database to use
            **kwargs: Additional connection parameters
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection_params = kwargs
        self.conn = None
        self.cursor = None
        
    def connect(self) -> None:
        """Establish connection to MySQL."""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                **self.connection_params
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MySQL: {str(e)}")
    
    def disconnect(self) -> None:
        """Close MySQL connection."""
        if self.conn:
            try:
                if self.cursor:
                    self.cursor.close()
                self.conn.close()
                self.conn = None
                self.cursor = None
            except Exception as e:
                raise ConnectionError(f"Failed to disconnect from MySQL: {str(e)}")
    
    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """
        Insert a record into a MySQL table.
        
        Args:
            collection: Table name
            data: Record to insert
            
        Returns:
            ID of the inserted record (assumes an auto-increment 'id' field)
        """
        if not self.conn:
            self.connect()
            
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            values = list(data.values())
            
            query = f"INSERT INTO {collection} ({columns}) VALUES ({placeholders})"
            
            self.cursor.execute(query, values)
            self.conn.commit()
            
            # Return the last insert id
            return str(self.cursor.lastrowid)
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Failed to insert record: {str(e)}")
    
    def select(self, collection: str, query: Dict[str, Any], limit: Optional[int] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Query records from a MySQL table.
        
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
                conditions.append(f"{key} = %s")
                values.append(value)
                
            where_clause = " AND ".join(conditions) if conditions else "TRUE"
            limit_clause = f"LIMIT {limit}" if limit else ""
            
            sql = f"SELECT * FROM {collection} WHERE {where_clause} {limit_clause}"
            
            self.cursor.execute(sql, values)
            
            if limit == 1:
                # Return a single record
                result = self.cursor.fetchone()
                return result if result else {}
            else:
                # Return a list of records
                results = self.cursor.fetchall()
                return results
        except Exception as e:
            raise ValueError(f"Failed to query records: {str(e)}")
    
    def update(self, collection: str, query: Dict[str, Any], data: Dict[str, Any]) -> int:
        """
        Update records in a MySQL table.
        
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
                set_items.append(f"{key} = %s")
                set_values.append(value)
                
            set_clause = ", ".join(set_items)
            
            # Build WHERE clause
            where_items = []
            where_values = []
            
            for key, value in query.items():
                where_items.append(f"{key} = %s")
                where_values.append(value)
                
            where_clause = " AND ".join(where_items) if where_items else "TRUE"
            
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
        Delete records from a MySQL table.
        
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
                conditions.append(f"{key} = %s")
                values.append(value)
                
            where_clause = " AND ".join(conditions) if conditions else "TRUE"
            
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
            self.cursor.execute("SHOW TABLES")
            results = self.cursor.fetchall()
            # The column name is the first key in the dictionary
            first_key = list(results[0].keys())[0] if results else None
            return [row[first_key] for row in results]
        except Exception as e:
            raise ConnectionError(f"Failed to list tables: {str(e)}")
