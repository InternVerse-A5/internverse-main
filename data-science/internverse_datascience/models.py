from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PerformanceData(BaseModel):
    user_id: str
    assessment_id: str
    score: float
    time_taken: int  # in seconds
    completed_at: datetime
    
    class Config:
        populate_by_name = True

class SubmissionData(BaseModel):
    user_id: str
    assignment_id: str
    status: str
    submitted_at: datetime
    grade: Optional[float] = None

    class Config:
        populate_by_name = True

class TaskScoreHistoryItem(BaseModel):
    date: str
    score: float
    assessment_id: str

class DashboardResponse(BaseModel):
    user_id: Optional[str] = None
    completion_percentage: float
    average_score: float
    performance_level: str
    task_score_history: List[TaskScoreHistoryItem]
