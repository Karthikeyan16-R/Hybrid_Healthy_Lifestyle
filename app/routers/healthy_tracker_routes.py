# app/routers/health_tracking_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# Import managers (with error handling)
try:
    from app.ai_core.challenge import challenge_manager
    CHALLENGES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Challenges system not available: {e}")
    CHALLENGES_AVAILABLE = False

try:
    from app.ai_core.healthy_dashboard import HealthDashboard
    DASHBOARD_AVAILABLE = True
    dashboards = {}
    
    def get_or_create_dashboard(user_id: str) -> HealthDashboard:
        """Get or create dashboard for user"""
        if user_id not in dashboards:
            dashboards[user_id] = HealthDashboard(user_id)
        return dashboards[user_id]
except ImportError as e:
    print(f"⚠️  Health dashboard not available: {e}")
    DASHBOARD_AVAILABLE = False


# ==================== REQUEST MODELS ====================

class CreateChallengeRequest(BaseModel):
    template_key: Optional[str] = None
    custom_title: Optional[str] = None
    custom_description: Optional[str] = None
    challenge_type: Optional[str] = None
    duration_days: Optional[int] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None

class UpdateProgressRequest(BaseModel):
    completed: bool
    value: Optional[float] = None
    notes: Optional[str] = None

class LogWeightRequest(BaseModel):
    weight_kg: float
    notes: Optional[str] = None

class LogDietRequest(BaseModel):
    meal_type: str
    food_items: List[str]
    calories: float
    protein: float
    carbs: float
    fat: float
    notes: Optional[str] = None

class LogWorkoutRequest(BaseModel):
    workout_type: str
    duration_minutes: int
    exercises: List[str]
    calories_burned: float
    intensity: str = "medium"
    notes: Optional[str] = None

class LogSleepRequest(BaseModel):
    sleep_time: str
    wake_time: str
    quality_score: int
    interruptions: int = 0
    notes: Optional[str] = None

class LogStressRequest(BaseModel):
    stress_level: int
    mood: str
    stressors: List[str]
    coping_methods: Optional[List[str]] = None
    notes: Optional[str] = None

class SetGoalsRequest(BaseModel):
    weight_goal: Optional[float] = None
    calorie_target: Optional[int] = None
    protein_target: Optional[int] = None
    workout_days: Optional[int] = None
    sleep_hours: Optional[float] = None
    water_glasses: Optional[int] = None
    daily_steps: Optional[int] = None


# ==================== CHALLENGES ENDPOINTS ====================

@router.get("/challenges/templates")
async def get_challenge_templates():
    """Get all available challenge templates"""
    if not CHALLENGES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Challenges system not available")
    return challenge_manager.get_challenge_templates()

@router.post("/challenges/create/{user_id}")
async def create_challenge(user_id: str, request: CreateChallengeRequest):
    """Create a new challenge for user"""
    if not CHALLENGES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Challenges system not available")
    
    result = challenge_manager.create_challenge(
        user_id=user_id,
        template_key=request.template_key,
        custom_title=request.custom_title,
        custom_description=request.custom_description,
        challenge_type=request.challenge_type,
        duration_days=request.duration_days,
        target_value=request.target_value,
        unit=request.unit
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result

@router.post("/challenges/{challenge_id}/progress")
async def update_challenge_progress(challenge_id: str, request: UpdateProgressRequest):
    """Update daily progress for a challenge"""
    if not CHALLENGES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Challenges system not available")
    
    result = challenge_manager.update_daily_progress(
        challenge_id=challenge_id,
        completed=request.completed,
        value=request.value,
        notes=request.notes
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error"))
    
    return result

@router.get("/challenges/{challenge_id}")
async def get_challenge_progress(challenge_id: str):
    """Get detailed progress for a specific challenge"""
    if not CHALLENGES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Challenges system not available")
    
    result = challenge_manager.get_challenge_progress(challenge_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error"))
    
    return result

@router.get("/challenges/user/{user_id}")
async def get_user_challenges(
    user_id: str,
    status: Optional[str] = Query(None, description="Filter by status")
):
    """Get all challenges for a user"""
    if not CHALLENGES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Challenges system not available")
    
    return challenge_manager.get_user_challenges(user_id, status)

@router.get("/challenges/user/{user_id}/badges")
async def get_user_badges(user_id: str):
    """Get all badges and achievements for a user"""
    if not CHALLENGES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Challenges system not available")
    
    return challenge_manager.get_user_badges(user_id)

@router.get("/challenges/leaderboard")
async def get_leaderboard(limit: int = Query(10, ge=1, le=100)):
    """Get global leaderboard"""
    if not CHALLENGES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Challenges system not available")
    
    return challenge_manager.get_leaderboard(limit)


# ==================== HEALTH DASHBOARD ENDPOINTS ====================

@router.post("/dashboard/{user_id}/log/weight")
async def log_weight(user_id: str, request: LogWeightRequest):
    """Log daily weight"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.log_weight(request.weight_kg, request.notes)

@router.post("/dashboard/{user_id}/log/diet")
async def log_diet(user_id: str, request: LogDietRequest):
    """Log meal/diet entry"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.log_diet(
        meal_type=request.meal_type,
        food_items=request.food_items,
        calories=request.calories,
        protein=request.protein,
        carbs=request.carbs,
        fat=request.fat,
        notes=request.notes
    )

@router.post("/dashboard/{user_id}/log/workout")
async def log_workout(user_id: str, request: LogWorkoutRequest):
    """Log workout session"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.log_workout(
        workout_type=request.workout_type,
        duration_minutes=request.duration_minutes,
        exercises=request.exercises,
        calories_burned=request.calories_burned,
        intensity=request.intensity,
        notes=request.notes
    )

@router.post("/dashboard/{user_id}/log/sleep")
async def log_sleep(user_id: str, request: LogSleepRequest):
    """Log sleep data"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.log_sleep(
        sleep_time=request.sleep_time,
        wake_time=request.wake_time,
        quality_score=request.quality_score,
        interruptions=request.interruptions,
        notes=request.notes
    )

@router.post("/dashboard/{user_id}/log/stress")
async def log_stress(user_id: str, request: LogStressRequest):
    """Log stress and mood"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.log_stress(
        stress_level=request.stress_level,
        mood=request.mood,
        stressors=request.stressors,
        coping_methods=request.coping_methods,
        notes=request.notes
    )

@router.post("/dashboard/{user_id}/log/water")
async def log_water(user_id: str, glasses: int):
    """Log daily water intake"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.log_water(glasses)

@router.post("/dashboard/{user_id}/log/steps")
async def log_steps(user_id: str, steps: int):
    """Log daily step count"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.log_steps(steps)

@router.get("/dashboard/{user_id}/summary/daily")
async def get_daily_summary(user_id: str, date: Optional[str] = None):
    """Get daily health summary"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.get_daily_summary(date)

@router.get("/dashboard/{user_id}/summary/weekly")
async def get_weekly_summary(user_id: str, end_date: Optional[str] = None):
    """Get weekly health summary"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.get_weekly_summary(end_date)

@router.get("/dashboard/{user_id}/trends")
async def get_progress_trends(user_id: str, days: int = Query(30, ge=7, le=365)):
    """Get progress trends over time"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.get_progress_trends(days)

@router.get("/dashboard/{user_id}/achievements")
async def get_achievements(user_id: str):
    """Get user achievements and milestones"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.get_achievements()

@router.post("/dashboard/{user_id}/goals")
async def set_health_goals(user_id: str, request: SetGoalsRequest):
    """Set health and fitness goals"""
    if not DASHBOARD_AVAILABLE:
        raise HTTPException(status_code=503, detail="Dashboard system not available")
    
    dashboard = get_or_create_dashboard(user_id)
    return dashboard.set_goals(
        weight_goal=request.weight_goal,
        calorie_target=request.calorie_target,
        protein_target=request.protein_target,
        workout_days=request.workout_days,
        sleep_hours=request.sleep_hours,
        water_glasses=request.water_glasses,
        daily_steps=request.daily_steps
    )

@router.get("/dashboard/{user_id}/quick-stats")
async def get_quick_stats(user_id: str):
    """Get quick overview stats for dashboard widgets"""
    if not DASHBOARD_AVAILABLE or not CHALLENGES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Required systems not available")
    
    dashboard = get_or_create_dashboard(user_id)
    
    daily = dashboard.get_daily_summary()
    weekly = dashboard.get_weekly_summary()
    badges = challenge_manager.get_user_badges(user_id)
    challenges = challenge_manager.get_user_challenges(user_id, status="in_progress")
    
    return {
        "success": True,
        "user_id": user_id,
        "quick_stats": {
            "today": {
                "calories": daily['summary']['nutrition']['total_calories'],
                "workouts": daily['summary']['fitness']['workouts_completed'],
                "sleep_hours": daily['summary']['sleep']['hours_slept'],
                "steps": daily['summary']['activity']['steps']
            },
            "weekly": {
                "avg_calories": weekly['summary']['nutrition']['avg_daily_calories'],
                "total_workouts": weekly['summary']['fitness']['total_workouts'],
                "avg_sleep": weekly['summary']['sleep']['avg_hours']
            },
            "gamification": {
                "total_points": badges.get('total_points', 0),
                "total_badges": badges.get('total_badges', 0),
                "active_challenges": challenges.get('total_challenges', 0)
            }
        }
    }