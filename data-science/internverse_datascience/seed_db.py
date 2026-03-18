import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "analytics_db")

def seed_data():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    try:
        client.admin.command('ping')
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return

    db = client[DB_NAME]
    
    now = datetime.utcnow()
    
    # Dummy Performance Data with historical trend
    performance_docs = [
        # User 123
        {"user_id": "user123", "assessment_id": "assess001", "score": 65.0, "time_taken": 1500, "completed_at": now - timedelta(days=5)},
        {"user_id": "user123", "assessment_id": "assess002", "score": 75.5, "time_taken": 1200, "completed_at": now - timedelta(days=3)},
        {"user_id": "user123", "assessment_id": "assess003", "score": 88.0, "time_taken": 1000, "completed_at": now - timedelta(days=1)},
        {"user_id": "user123", "assessment_id": "assess004", "score": 92.5, "time_taken": 900, "completed_at": now},
        
        # User 456
        {"user_id": "user456", "assessment_id": "assess001", "score": 50.0, "time_taken": 1800, "completed_at": now - timedelta(days=5)},
        {"user_id": "user456", "assessment_id": "assess002", "score": 60.0, "time_taken": 1700, "completed_at": now - timedelta(days=2)},
    ]
    
    # Dummy Submission Data
    submission_docs = [
        # User 123 (75% completion: 3/4 completed/graded)
        {"user_id": "user123", "assignment_id": "assign001", "status": "graded", "submitted_at": now - timedelta(days=5), "grade": 65.0},
        {"user_id": "user123", "assignment_id": "assign002", "status": "graded", "submitted_at": now - timedelta(days=3), "grade": 75.5},
        {"user_id": "user123", "assignment_id": "assign003", "status": "completed", "submitted_at": now - timedelta(days=1), "grade": None},
        {"user_id": "user123", "assignment_id": "assign004", "status": "pending", "submitted_at": now, "grade": None},
        
        # User 456 (33% completion: 1/3 completed/graded)
        {"user_id": "user456", "assignment_id": "assign001", "status": "graded", "submitted_at": now - timedelta(days=5), "grade": 50.0},
        {"user_id": "user456", "assignment_id": "assign002", "status": "pending", "submitted_at": now - timedelta(days=2), "grade": None},
        {"user_id": "user456", "assignment_id": "assign003", "status": "failed", "submitted_at": now, "grade": 40.0},
    ]
    
    db.performance.delete_many({})
    db.submissions.delete_many({})
    
    db.performance.insert_many(performance_docs)
    db.submissions.insert_many(submission_docs)
    
    print("Database seeded with richer dummy data for dashboard charting.")

if __name__ == "__main__":
    seed_data()
