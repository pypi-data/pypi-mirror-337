"""
Redis connector implementation.
"""

from typing import Dict, Any, List, Optional, Union
import json
import redis
from .interface import DatabaseInterface


class RedisConnector(DatabaseInterface):
    """Redis implementation of the database interface."""
    
    def __init__(self, 
                host: str = "localhost", 
                port: int = 6379, 
                password: str = None, 
                db: int = 0,
                **kwargs):
        """
        Initialize Redis connector.
        
        Args:
            host: Redis server host
            port: Redis server port
            password: Password for authentication
            db: Redis database number
            **kwargs: Additional connection parameters
        """
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.connection_params = kwargs
        self.client = None
        
    def connect(self) -> None:
        """Establish connection to Redis."""
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                **self.connection_params
            )
            # Test connection
            self.client.ping()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
    
    def disconnect(self) -> None:
        """Close Redis connection."""
        if self.client:
            try:
                self.client.close()
                self.client = None
            except Exception as e:
                raise ConnectionError(f"Failed to disconnect from Redis: {str(e)}")
    
    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """
        Insert a record into Redis.
        For Redis, 'collection' is used as a namespace prefix for keys.
        The record must have an 'id' field or one will be generated.
        
        Args:
            collection: Namespace prefix for the record
            data: Record to insert
            
        Returns:
            ID of the inserted record
        """
        if not self.client:
            self.connect()
            
        try:
            # Check for id in data or generate one
            record_id = str(data.get('id', self.client.incr(f"{collection}:id_counter")))
            
            # Create a copy of data with id included
            record_data = data.copy()
            record_data['id'] = record_id
            
            # Convert data to JSON string
            json_data = json.dumps(record_data)
            
            # Store in Redis
            key = f"{collection}:{record_id}"
            self.client.set(key, json_data)
            
            # Add to collection set
            self.client.sadd(f"{collection}:all", record_id)
            
            return record_id
        except Exception as e:
            raise ValueError(f"Failed to insert record: {str(e)}")
    
    def read(self, collection: str, query: Dict[str, Any], limit: Optional[int] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Query records from Redis.
        
        For Redis:
        - If query contains 'id', retrieve the specific record
        - Otherwise, scan all records in the collection and filter
        
        Args:
            collection: Namespace prefix for records
            query: Filter conditions
            limit: Maximum number of records to return
            
        Returns:
            Single record or list of records
        """
        if not self.client:
            self.connect()
            
        try:
            # Direct lookup by ID
            if 'id' in query and len(query) == 1:
                record_id = query['id']
                key = f"{collection}:{record_id}"
                data = self.client.get(key)
                
                if data:
                    return json.loads(data)
                return {}
            
            # Need to scan and filter
            results = []
            member_count = 0
            
            # Get all IDs in this collection
            all_ids = self.client.smembers(f"{collection}:all")
            
            for record_id in all_ids:
                key = f"{collection}:{record_id.decode('utf-8')}"
                data = self.client.get(key)
                
                if data:
                    record = json.loads(data)
                    # Check if record matches query
                    matches = True
                    for k, v in query.items():
                        if k not in record or record[k] != v:
                            matches = False
                            break
                    
                    if matches:
                        if limit == 1:
                            return record
                        results.append(record)
                        member_count += 1
                        
                        if limit and member_count >= limit:
                            break
            
            return results
        except Exception as e:
            raise ValueError(f"Failed to query records: {str(e)}")
    
    def update(self, collection: str, query: Dict[str, Any], data: Dict[str, Any]) -> int:
        """
        Update records in Redis.
        
        Args:
            collection: Namespace prefix for records
            query: Filter conditions
            data: Updates to apply
            
        Returns:
            Number of records updated
        """
        if not self.client:
            self.connect()
            
        try:
            updated_count = 0
            
            # Direct update by ID
            if 'id' in query and len(query) == 1:
                record_id = query['id']
                key = f"{collection}:{record_id}"
                
                # Get existing data
                existing_data = self.client.get(key)
                if existing_data:
                    record = json.loads(existing_data)
                    # Update fields
                    record.update(data)
                    # Save back
                    self.client.set(key, json.dumps(record))
                    updated_count = 1
                
                return updated_count
            
            # Need to scan and update
            all_ids = self.client.smembers(f"{collection}:all")
            
            for record_id in all_ids:
                key = f"{collection}:{record_id.decode('utf-8')}"
                existing_data = self.client.get(key)
                
                if existing_data:
                    record = json.loads(existing_data)
                    # Check if record matches query
                    matches = True
                    for k, v in query.items():
                        if k not in record or record[k] != v:
                            matches = False
                            break
                    
                    if matches:
                        # Update fields
                        record.update(data)
                        # Save back
                        self.client.set(key, json.dumps(record))
                        updated_count += 1
            
            return updated_count
        except Exception as e:
            raise ValueError(f"Failed to update records: {str(e)}")
    
    def delete(self, collection: str, query: Dict[str, Any]) -> int:
        """
        Delete records from Redis.
        
        Args:
            collection: Namespace prefix for records
            query: Filter conditions
            
        Returns:
            Number of records deleted
        """
        if not self.client:
            self.connect()
            
        try:
            deleted_count = 0
            
            # Direct delete by ID
            if 'id' in query and len(query) == 1:
                record_id = query['id']
                key = f"{collection}:{record_id}"
                
                # Check if key exists
                if self.client.exists(key):
                    # Delete the key
                    self.client.delete(key)
                    # Remove from the collection set
                    self.client.srem(f"{collection}:all", record_id)
                    deleted_count = 1
                
                return deleted_count
            
            # Need to scan and delete
            all_ids = self.client.smembers(f"{collection}:all")
            to_delete = []
            
            for record_id in all_ids:
                str_id = record_id.decode('utf-8')
                key = f"{collection}:{str_id}"
                existing_data = self.client.get(key)
                
                if existing_data:
                    record = json.loads(existing_data)
                    # Check if record matches query
                    matches = True
                    for k, v in query.items():
                        if k not in record or record[k] != v:
                            matches = False
                            break
                    
                    if matches:
                        # Delete the key
                        self.client.delete(key)
                        to_delete.append(record_id)
                        deleted_count += 1
            
            # Remove from the collection set
            if to_delete:
                self.client.srem(f"{collection}:all", *to_delete)
            
            return deleted_count
        except Exception as e:
            raise ValueError(f"Failed to delete records: {str(e)}")
    
    def list_collections(self) -> List[str]:
        """
        List all collections in Redis.
        
        For Redis, collections are identified by keys ending with ':all'
        
        Returns:
            List of collection names
        """
        if not self.client:
            self.connect()
            
        try:
            collections = set()
            # Scan for keys ending with ':all'
            cursor = 0
            while True:
                cursor, keys = self.client.scan(cursor, match='*:all')
                for key in keys:
                    # Extract the collection name from the key
                    collection = key.decode('utf-8').replace(':all', '')
                    collections.add(collection)
                
                if cursor == 0:
                    break
            
            return list(collections)
        except Exception as e:
            raise ConnectionError(f"Failed to list collections: {str(e)}")
