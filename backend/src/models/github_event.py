from datetime import datetime
from typing import Optional, Dict, Any, List
from bson import ObjectId
from src.database import db

class GitHubEvent:
    """
    MongoDB Schema for GitHub Events:
    - _id: ObjectID – Auto-generated MongoDB ID
    - request_id: string – Git commit hash or PR ID
    - author: string – GitHub username
    - action: string (Enum) – One of "PUSH", "PULL_REQUEST", "MERGE"
    - from_branch: string – Source branch (for PRs and merges)
    - to_branch: string – Target branch
    - timestamp: string (datetime) – ISO-formatted UTC timestamp
    """
    
    VALID_ACTIONS = ["PUSH", "PULL_REQUEST", "MERGE"]
    COLLECTION_NAME = "github_events"
    
    def __init__(self, request_id: str, author: str, action: str, 
                 to_branch: str, from_branch: Optional[str] = None, 
                 timestamp: Optional[str] = None):
        
        if action not in self.VALID_ACTIONS:
            raise ValueError(f"Action must be one of {self.VALID_ACTIONS}")
        
        self.request_id = request_id
        self.author = author
        self.action = action
        self.from_branch = from_branch
        self.to_branch = to_branch
        self.timestamp = timestamp or datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary for MongoDB storage"""
        return {
            "request_id": self.request_id,
            "author": self.author,
            "action": self.action,
            "from_branch": self.from_branch,
            "to_branch": self.to_branch,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GitHubEvent':
        """Create a GitHubEvent instance from a dictionary"""
        return cls(
            request_id=data["request_id"],
            author=data["author"],
            action=data["action"],
            to_branch=data["to_branch"],
            from_branch=data.get("from_branch"),
            timestamp=data.get("timestamp")
        )
    
    def save(self) -> Optional[str]:
        """Save the event to MongoDB and return the inserted ID"""
        try:
            collection = db.get_collection(self.COLLECTION_NAME)
            if collection is not None:
                result = collection.insert_one(self.to_dict())
                return str(result.inserted_id)
            else:
                print("Database connection not available")
                return None
        except Exception as e:
            print(f"Error saving event: {e}")
            return None
    
    @classmethod
    def get_latest_events(cls, limit: int = 50) -> List[Dict[str, Any]]:
        """Get the latest events from MongoDB, sorted by timestamp descending"""
        try:
            collection = db.get_collection(cls.COLLECTION_NAME)
            if collection is not None:
                cursor = collection.find().sort("timestamp", -1).limit(limit)
                
                events = []
                for doc in cursor:
                    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
                    events.append(doc)
                
                return events
            else:
                print("Database connection not available")
                return []
        except Exception as e:
            print(f"Error fetching events: {e}")
            return []
    
    @classmethod
    def get_event_by_id(cls, event_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific event by its MongoDB ID"""
        try:
            collection = db.get_collection(cls.COLLECTION_NAME)
            if collection is not None:
                doc = collection.find_one({"_id": ObjectId(event_id)})
                
                if doc:
                    doc["_id"] = str(doc["_id"])
                    return doc
            return None
        except Exception as e:
            print(f"Error fetching event by ID: {e}")
            return None
    
    @classmethod
    def delete_all_events(cls) -> int:
        """Delete all events (useful for testing)"""
        try:
            collection = db.get_collection(cls.COLLECTION_NAME)
            if collection is not None:
                result = collection.delete_many({})
                return result.deleted_count
            return 0
        except Exception as e:
            print(f"Error deleting events: {e}")
            return 0
    
    @classmethod
    def create_sample_events(cls) -> List[str]:
        """Create sample events for testing"""
        sample_events = [
            cls("abc123", "john_doe", "PUSH", "main"),
            cls("def456", "jane_smith", "PULL_REQUEST", "main", "feature-branch"),
            cls("ghi789", "bob_wilson", "MERGE", "main", "develop"),
        ]
        
        inserted_ids = []
        for event in sample_events:
            event_id = event.save()
            if event_id:
                inserted_ids.append(event_id)
        
        return inserted_ids

