# app/routers/ai_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from app.ai_core.ai_recommender import recommend_from_dataset
from app.ai_core.ai_workout_fitbit import FitbitWorkoutRecommender
from app.ai_core.chatbot import chatbot
from app.ai_core.hospital_finder import hospital_finder

router = APIRouter()

# ==================== DIET PLANNING ====================

class DietRequest(BaseModel):
    age: int
    weight: float
    height: float
    gender: str
    activity_level: str
    goal: str
    cuisine_preference: Optional[str] = None

@router.post("/diet")
async def generate_diet(request: DietRequest):
    """Generate personalized AI diet plan"""
    try:
        plan = recommend_from_dataset(
            age=request.age,
            weight=request.weight,
            height=request.height,
            gender=request.gender,
            activity_level=request.activity_level,
            goal=request.goal,
            cuisine_preference=request.cuisine_preference
        )
        return {"success": True, "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== WORKOUT PLANNING ====================

class WorkoutRequest(BaseModel):
    """Workout recommendation request model"""
    age: int
    height: float
    weight: float
    activity_level: str  # 'low', 'medium', 'high'
    goal: str  # 'weight_loss', 'muscle_gain', 'maintain', 'endurance'
    has_injury: bool = False
    is_beginner: bool = False

@router.post("/workout")
async def generate_workout(request: WorkoutRequest):
    """
    🏋️ Generate personalized workout recommendation
    
    **Features:**
    - Fitbit data-driven recommendations
    - Personalized workout tiers (Recovery/Foundation/Progression/Performance)
    - Heart rate zone targeting
    - Exercise selection based on goals and limitations
    - AI-powered insights and tips
    
    **Input:**
    - age: User's age (15-100 years)
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
    - workout_plan: Exercises, schedule, progression strategy
    - ai_insights: Personalized tips and motivation
    - dataset_source: Data source information
    """
    try:
        recommender = FitbitWorkoutRecommender()
        
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
        result = recommender.recommend_workout(user_data)
        
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

# Keep the old endpoint for backward compatibility
@router.post("/workout-fitbit")
async def generate_workout_fitbit(request: WorkoutRequest):
    """
    ⚠️ DEPRECATED: Use /workout instead
    Generate Fitbit-based workout plan (legacy endpoint)
    """
    return await generate_workout(request)


# ==================== ADVANCED CHATBOT ====================

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default"

class ChatHistoryRequest(BaseModel):
    user_id: str

@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """
    Advanced AI health chatbot with context awareness
    
    Features:
    - Conversation memory
    - Symptom severity detection
    - Safety warnings
    - Context-aware responses
    """
    try:
        result = chatbot.chat(request.message, request.user_id)
        return {
            "success": True,
            "response": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/{user_id}")
async def get_chat_history(user_id: str):
    """Get conversation history for a user"""
    history = chatbot.get_conversation_history(user_id)
    return {
        "success": True,
        "user_id": user_id,
        "history": history,
        "message_count": len(history)
    }

@router.get("/chat/summary/{user_id}")
async def get_chat_summary(user_id: str):
    """Get conversation summary with topics and stats"""
    summary = chatbot.get_conversation_summary(user_id)
    return {
        "success": True,
        "user_id": user_id,
        "summary": summary
    }

@router.delete("/chat/history/{user_id}")
async def clear_chat_history(user_id: str):
    """Clear conversation history for a user"""
    success = chatbot.clear_conversation(user_id)
    return {
        "success": success,
        "message": "Conversation history cleared" if success else "No history found"
    }


# ==================== HOSPITAL FINDER ====================

class HospitalSearchRequest(BaseModel):
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    specialty: Optional[str] = None
    urgency: str = "routine"  # 'emergency', 'urgent', or 'routine'
    max_distance_km: float = 50.0
    max_results: int = 10

@router.post("/hospitals/search")
async def search_hospitals(request: HospitalSearchRequest):
    """
    Search for hospitals based on location and requirements
    
    Features:
    - Location-based search
    - Specialty filtering
    - Urgency routing
    - Distance calculation
    - Emergency service detection
    """
    try:
        result = hospital_finder.search_hospitals(
            location=request.location,
            latitude=request.latitude,
            longitude=request.longitude,
            specialty=request.specialty,
            urgency=request.urgency,
            max_distance_km=request.max_distance_km,
            max_results=request.max_results
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hospitals/{hospital_id}")
async def get_hospital_details(hospital_id: str):
    """Get detailed information for a specific hospital"""
    hospital = hospital_finder.get_hospital_by_id(hospital_id)
    if hospital:
        return {
            "success": True,
            "hospital": hospital
        }
    else:
        raise HTTPException(status_code=404, detail="Hospital not found")

@router.get("/hospitals/specialties")
async def get_specialties():
    """Get list of available medical specialties"""
    specialties = hospital_finder.get_specialties_list()
    return {
        "success": True,
        "specialties": specialties,
        "total": len(specialties)
    }


# ==================== HEALTH ASSESSMENT ====================

class SymptomCheckRequest(BaseModel):
    symptoms: List[str]
    severity: str  # 'mild', 'moderate', 'severe'
    duration_days: int
    age: int
    gender: str

@router.post("/symptom-check")
async def symptom_check(request: SymptomCheckRequest):
    """
    Quick symptom assessment with recommendations
    
    NOTE: This is advisory only, not a diagnosis
    """
    try:
        # Create symptom message for chatbot
        symptom_text = f"I am {request.age} year old {request.gender}. "
        symptom_text += f"I have been experiencing {', '.join(request.symptoms)} "
        symptom_text += f"for {request.duration_days} days with {request.severity} severity. "
        symptom_text += "What should I do?"
        
        # Get AI assessment
        result = chatbot.chat(symptom_text, user_id=f"symptom_check_{request.age}")
        
        # Determine if hospital search is needed
        requires_hospital = result.get("requires_doctor", False)
        
        response = {
            "success": True,
            "assessment": result,
            "requires_medical_attention": requires_hospital
        }
        
        # If urgent/critical, suggest nearby hospitals
        if requires_hospital:
            # This would use user's location in production
            hospitals = hospital_finder.search_hospitals(
                urgency="emergency" if result["severity"] == "critical" else "urgent",
                max_results=3
            )
            response["nearby_hospitals"] = hospitals.get("hospitals", [])
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== HEALTH TIPS ====================

@router.get("/health-tips")
async def get_health_tips(category: str = Query("general", description="Category: diet, fitness, mental_health, sleep")):
    """Get AI-generated health tips for different categories"""
    
    prompts = {
        "diet": "Give me 3 quick, practical nutrition tips for healthy eating",
        "fitness": "Give me 3 effective fitness tips for beginners",
        "mental_health": "Give me 3 tips for managing stress and improving mental wellbeing",
        "sleep": "Give me 3 tips for better sleep quality",
        "general": "Give me 3 general health and wellness tips"
    }
    
    prompt = prompts.get(category, prompts["general"])
    
    try:
        result = chatbot.chat(prompt, user_id=f"tips_{category}")
        return {
            "success": True,
            "category": category,
            "tips": result["reply"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))