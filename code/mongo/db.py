from pymongo import MongoClient
from typing import Optional
import atexit

class MongoDB:
    _connection_url = None
    _db = None
    _instance = None
    _client: Optional[MongoClient] = None
    
    def __new__(cls, connection_url: str = "", db_name: str = ""):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance._db = db_name
            cls._instance._connection_url = connection_url
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
        """Establish MongoDB connection"""
        if not self._client:
            try:
                self._client = MongoClient(self._connection_url)
                atexit.register(self._cleanup)
            except Exception as e:
                raise Exception(f"Failed to connect to MongoDB: {e}")
    
    def _cleanup(self):
        """Cleanup method to close connection"""
        if self._client:
            self._client.close()
            self._client = None
    
    @property
    def client(self) -> MongoClient:
        """Get MongoDB client instance"""
        return self._client
    
    @property
    def db(self):
        """Get default database instance"""
        return self._client[self._db]

    @property
    def user_collection(self):
        """Get reference to the user collection in the DB"""
        return self._client.DollarBot.users

    @property
    def spends_collection(self):
        """Get reference to the spends collection in the DB"""
        return self._client.DollarBot.spends
    
    def close(self):
        """Manually close the connection"""
        self._cleanup()