import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Connect to MongoDB Atlas"""
        try:
            mongodb_uri = os.getenv('MONGODB_URI')
            database_name = os.getenv('DATABASE_NAME', 'gitping')
            
            if not mongodb_uri:
                # For development/testing, use a default connection string
                print("Warning: MONGODB_URI not found in environment variables")
                print("Please set up your MongoDB Atlas connection string in .env file")
                return
            
            self._client = MongoClient(mongodb_uri)
            self._db = self._client[database_name]
            
            # Test the connection
            self._client.admin.command('ping')
            print(f"Successfully connected to MongoDB Atlas - Database: {database_name}")
            
        except Exception as e:
            print(f"Failed to connect to MongoDB Atlas: {e}")
            print("Please check your MongoDB Atlas connection string and network access")
    
    def get_database(self):
        """Get the database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def get_collection(self, collection_name):
        """Get a specific collection"""
        db = self.get_database()
        if db is not None:
            return db[collection_name]
        return None
    
    def close_connection(self):
        """Close the database connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

# Global database instance
db = Database()

