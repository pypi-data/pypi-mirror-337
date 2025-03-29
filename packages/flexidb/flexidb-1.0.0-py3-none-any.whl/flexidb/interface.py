"""
Database interface module that defines the common API for all database connectors.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union


class DatabaseInterface(ABC):
    """
    Abstract base class that defines the common interface for all database connectors.
    All database implementations must inherit from this class and implement its methods.
    """
    
    @abstractmethod
    def connect(self) -> None:
        """
        Establish a connection to the database.
        
        Raises:
            ConnectionError: If connection fails
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """
        Close the connection to the database.
        
        Raises:
            ConnectionError: If disconnection fails
        """
        pass
    
    @abstractmethod
    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """
        Create a new record in the specified collection.
        
        Args:
            collection: The name of the collection or table
            data: The data to insert
            
        Returns:
            The ID of the newly created record
            
        Raises:
            ValueError: If the data is invalid
            ConnectionError: If database operation fails
        """
        pass
    
    @abstractmethod
    def select(self, collection: str, query: Dict[str, Any], limit: Optional[int] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Select record(s) from the specified collection.
        
        Args:
            collection: The name of the collection or table
            query: The query filter to apply
            limit: Maximum number of results to return (None means no limit)
            
        Returns:
            A single record or list of records matching the query
            
        Raises:
            ValueError: If the query is invalid
            ConnectionError: If database operation fails
        """
        pass
    
    @abstractmethod
    def update(self, collection: str, query: Dict[str, Any], data: Dict[str, Any]) -> int:
        """
        Update record(s) in the specified collection.
        
        Args:
            collection: The name of the collection or table
            query: The query filter to find records to update
            data: The new data to apply
            
        Returns:
            Number of records updated
            
        Raises:
            ValueError: If the query or data is invalid
            ConnectionError: If database operation fails
        """
        pass
    
    @abstractmethod
    def delete(self, collection: str, query: Dict[str, Any]) -> int:
        """
        Delete record(s) from the specified collection.
        
        Args:
            collection: The name of the collection or table
            query: The query filter to find records to delete
            
        Returns:
            Number of records deleted
            
        Raises:
            ValueError: If the query is invalid
            ConnectionError: If database operation fails
        """
        pass
    
    @abstractmethod
    def list_collections(self) -> List[str]:
        """
        List all collections (tables) in the database.
        
        Returns:
            List of collection names
            
        Raises:
            ConnectionError: If database operation fails
        """
        pass
