"""
MongoDB connector implementation.
"""

from typing import Dict, Any, List, Optional, Union
import pymongo
from .interface import DatabaseInterface


class MongoDBConnector(DatabaseInterface):
    """MongoDB implementation of the database interface."""
    
    def __init__(self, uri: str = "mongodb://localhost:27017", database: str = "default", **kwargs):
        """
        Initialize MongoDB connector.
        
        Args:
            uri: MongoDB connection string
            database: Name of the database to use
            **kwargs: Additional connection parameters
        """
        self.uri = uri
        self.database_name = database
        self.connection_params = kwargs
        self.client = None
        self.db = None
        
    def connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = pymongo.MongoClient(self.uri, **self.connection_params)
            self.db = self.client[self.database_name]
            # Test connection by making a simple query
            self.client.server_info()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")
    
    def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            try:
                self.client.close()
                self.client = None
                self.db = None
            except Exception as e:
                raise ConnectionError(f"Failed to disconnect from MongoDB: {str(e)}")
    
    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """
        Insert a document into a MongoDB collection.
        
        Args:
            collection: Collection name
            data: Document to insert
            
        Returns:
            ID of the inserted document
        """
        if not self.client:
            self.connect()
            
        try:
            result = self.db[collection].insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            raise ValueError(f"Failed to insert document: {str(e)}")
    
    def read(self, collection: str, query: Dict[str, Any], limit: Optional[int] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Query documents from a MongoDB collection.
        
        Args:
            collection: Collection name
            query: MongoDB query
            limit: Maximum number of documents to return
            
        Returns:
            Single document or list of documents
        """
        if not self.client:
            self.connect()
            
        try:
            cursor = self.db[collection].find(query)
            
            if limit == 1:
                # Return a single document
                result = self.db[collection].find_one(query)
                if result:
                    # Convert ObjectId to string for JSON serialization
                    if '_id' in result:
                        result['_id'] = str(result['_id'])
                    return result
                return {}
            else:
                # Return a list of documents
                if limit:
                    cursor = cursor.limit(limit)
                    
                results = []
                for doc in cursor:
                    # Convert ObjectId to string for JSON serialization
                    if '_id' in doc:
                        doc['_id'] = str(doc['_id'])
                    results.append(doc)
                return results
        except Exception as e:
            raise ValueError(f"Failed to query documents: {str(e)}")
    
    def update(self, collection: str, query: Dict[str, Any], data: Dict[str, Any]) -> int:
        """
        Update documents in a MongoDB collection.
        
        Args:
            collection: Collection name
            query: Query to find documents to update
            data: Update to apply
            
        Returns:
            Number of documents updated
        """
        if not self.client:
            self.connect()
            
        try:
            result = self.db[collection].update_many(query, {"$set": data})
            return result.modified_count
        except Exception as e:
            raise ValueError(f"Failed to update documents: {str(e)}")
    
    def delete(self, collection: str, query: Dict[str, Any]) -> int:
        """
        Delete documents from a MongoDB collection.
        
        Args:
            collection: Collection name
            query: Query to find documents to delete
            
        Returns:
            Number of documents deleted
        """
        if not self.client:
            self.connect()
            
        try:
            result = self.db[collection].delete_many(query)
            return result.deleted_count
        except Exception as e:
            raise ValueError(f"Failed to delete documents: {str(e)}")
    
    def list_collections(self) -> List[str]:
        """
        List all collections in the database.
        
        Returns:
            List of collection names
        """
        if not self.client:
            self.connect()
            
        try:
            return self.db.list_collection_names()
        except Exception as e:
            raise ConnectionError(f"Failed to list collections: {str(e)}")
