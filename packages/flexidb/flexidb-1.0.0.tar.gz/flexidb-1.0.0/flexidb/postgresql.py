"""
PostgreSQL connector implementation.
"""

from typing import Dict, Any, List, Optional, Union
import psycopg2
import psycopg2.extras
from .interface import DatabaseInterface


class PostgreSQLConnector(DatabaseInterface):
    """PostgreSQL implementation of the database interface."""
    
    def __init__(self, 
                host: str = "localhost", 
                port: int = 5432, 
                user: str = "postgres", 
                password: str = "", 
                database: str = "postgres",
                **kwargs):
        """
        Initialize PostgreSQL connector.
        
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
        """Establish connection to PostgreSQL."""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.database,
                **self.connection_params
            )
            # Use RealDictCursor to return results as dictionaries
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {str(e)}")
    
    def disconnect(self) -> None:
        """Close PostgreSQL connection."""
        if self.conn:
            try:
                if self.cursor:
                    self.cursor.close()
                self.conn.close()
                self.conn = None
                self.cursor = None
            except Exception as e:
                raise ConnectionError(f"Failed to disconnect from PostgreSQL: {str(e)}")
    
    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """
        Insert a record into a PostgreSQL table.
        
        Args:
            collection: Table name
            data: Record to insert
            
        Returns:
            ID of the inserted record (assumes an 'id' field)
        """
        if not self.conn:
            self.connect()
            
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            values = list(data.values())
            
            query = f"INSERT INTO {collection} ({columns}) VALUES ({placeholders}) RETURNING id"
            
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            self.conn.commit()
            
            # Return the id as a string
            return str(result['id'])
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Failed to insert record: {str(e)}")
    
    def select(self, collection: str, query: Dict[str, Any], limit: Optional[int] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Query records from a PostgreSQL table.
        
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
                return dict(result) if result else {}
            else:
                # Return a list of records
                results = self.cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            raise ValueError(f"Failed to query records: {str(e)}")
    
    def update(self, collection: str, query: Dict[str, Any], data: Dict[str, Any]) -> int:
        """
        Update records in a PostgreSQL table.
        
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
        Delete records from a PostgreSQL table.
        
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
            self.cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            results = self.cursor.fetchall()
            return [row['table_name'] for row in results]
        except Exception as e:
            raise ConnectionError(f"Failed to list tables: {str(e)}")
