from database import get_db

def calculate_performance(student_id):

    db = get_db()

    performance_data = list(db.performance.find({"user_id": student_id}))
    
    total_score = 0
    total_tasks = len(performance_data)

    for item in performance_data:
        total_score += item.get("score", 0)

    average_score = total_score / total_tasks if total_tasks > 0 else 0

    if average_score >= 90:
        level = "Excellent"
    elif average_score >= 75:
        level = "Good"
    elif average_score >= 60:
        level = "Average"
    else:
        level = "Needs Improvement"

    return {
        "student_id": student_id,
        "tasks_completed": total_tasks,
        "average_score": average_score,
        "performance_level": level
    }