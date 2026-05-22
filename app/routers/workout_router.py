# app/routers/ai_routes.py
# Add this to your EXISTING ai_routes.py file

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import your workout recommender
from app.ai_core.workout_recommender import workout_recommender

router = APIRouter()

# ==================== WORKOUT RECOMMENDATION ====================

class WorkoutRequest(BaseModel):
    age: int
    height: float
    weight: float
    activity_level: str  # 'low', 'medium', 'high'
    goal: str  # 'weight_loss', 'muscle_gain', 'maintain', 'endurance'
    has_injury: bool = False
    is_beginner: bool = False

@router.post("/workout")
async def get_workout_recommendation(request: WorkoutRequest):
    """
    🏋️ Generate personalized workout recommendation
    
    **Input:**
    - age: User's age (15-100)
    - height: Height in cm (100-250)
    - weight: Weight in kg (30-300)
    - activity_level: 'low', 'medium', or 'high'
    - goal: 'weight_loss', 'muscle_gain', 'maintain', or 'endurance'
    - has_injury: Whether user has injury/limitation
    - is_beginner: Whether user is new to fitness
    
    **Returns:**
    - success: Boolean
    - user_profile: BMI, category, age, activity, goal
    - workout_tier: Recovery/Foundation/Progression/Performance
    - intensity_level: light/moderate/vigorous
    - heart_rate_zone: Target BPM range
    - daily_targets: Active minutes, steps, workouts per week
    - workout_plan: Exercises, schedule, progression
    - ai_insights: Personalized tips and motivation
    """
    try:
        # Convert request to dictionary
        user_data = {
            "age": request.age,
            "height": request.height,
            "weight": request.weight,
            "activity_level": request.activity_level,
            "goal": request.goal,
            "has_injury": request.has_injury,
            "is_beginner": request.is_beginner
        }
        
        # Generate workout recommendation
        result = workout_recommender.recommend_workout(user_data)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"❌ Workout recommendation error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate workout recommendation: {str(e)}"
        )

# ==================== EXISTING DIET ENDPOINT ====================
# (Keep your existing /diet endpoint here)

# Example if you don't have it yet:
"""
class DietRequest(BaseModel):
    age: int
    weight: float
    height: float
    gender: str
    activity_level: str
    goal: str
    cuisine_preference: Optional[str] = None

@router.post("/diet")
async def get_diet_plan(request: DietRequest):
    # Your diet logic here
    pass
"""