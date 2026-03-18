from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
import uvicorn

from database import get_db
from models import PerformanceData, SubmissionData, DashboardResponse, TaskScoreHistoryItem

# YOUR PERFORMANCE ENGINE
from performance_engine import calculate_performance


app = FastAPI(
    title="Analytics & Performance API Service",
    description="Microservice to provide analytics data and performance tracking",
    version="1.0.0"
)

# ------------------------------
# BASIC SERVICE CHECK
# ------------------------------
@app.get("/")
def home():
    return {"service": "Performance Tracking Engine Running"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Analytics API Service is running"}


# ------------------------------
# PERFORMANCE ENGINE API
# ------------------------------
@app.post("/update-performance/{student_id}")
def update_performance(student_id: str):

    result = calculate_performance(student_id)

    return {
        "message": "Performance updated",
        "data": result
    }


# ------------------------------
# ANALYTICS APIs
# ------------------------------

@app.get("/analytics/performance", response_model=List[PerformanceData])
async def get_performance_data(user_id: str = None, limit: int = 100, db: AsyncIOMotorDatabase = Depends(get_db)):
    query = {}
    if user_id:
        query["user_id"] = user_id
        
    try:
        cursor = db.performance.find(query).limit(limit)
        results = await cursor.to_list(length=limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/submissions", response_model=List[SubmissionData])
async def get_submission_data(user_id: str = None, status: str = None, limit: int = 100, db: AsyncIOMotorDatabase = Depends(get_db)):
    query = {}
    if user_id:
        query["user_id"] = user_id
    if status:
        query["status"] = status
        
    try:
        cursor = db.submissions.find(query).limit(limit)
        results = await cursor.to_list(length=limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/dashboard", response_model=DashboardResponse)
async def get_dashboard_data(user_id: Optional[str] = Query(None), db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        user_query = {"user_id": user_id} if user_id else {}

        performance_cursor = db.performance.find(user_query).sort("completed_at", 1)
        performance_records = await performance_cursor.to_list(length=None)

        submission_cursor = db.submissions.find(user_query)
        submission_records = await submission_cursor.to_list(length=None)

        total_assignments = len(submission_records)
        completed_assignments = sum(
            1 for sub in submission_records
            if sub.get("status") in ["completed", "graded"]
        )

        completion_percentage = (
            round((completed_assignments / total_assignments) * 100, 2)
            if total_assignments > 0 else 0.0
        )

        total_score = 0.0
        task_score_history = []

        for pref in performance_records:
            score = pref.get("score", 0)
            total_score += score

            completed_at = pref.get("completed_at")
            date_str = (
                completed_at.strftime("%Y-%m-%d")
                if isinstance(completed_at, datetime)
                else str(completed_at)
            )

            task_score_history.append(
                TaskScoreHistoryItem(
                    date=date_str,
                    score=score,
                    assessment_id=pref.get("assessment_id", "")
                )
            )

        average_score = (
            round(total_score / len(performance_records), 2)
            if performance_records else 0.0
        )

        if average_score >= 90:
            performance_level = "Excellent"
        elif average_score >= 75:
            performance_level = "Good"
        elif average_score >= 60:
            performance_level = "Average"
        else:
            performance_level = "Needs Improvement"

        return DashboardResponse(
            user_id=user_id,
            completion_percentage=completion_percentage,
            average_score=average_score,
            performance_level=performance_level,
            task_score_history=task_score_history
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to aggregate dashboard data: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)