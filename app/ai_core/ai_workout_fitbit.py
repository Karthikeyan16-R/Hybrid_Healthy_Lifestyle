import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

from google import genai
from app.ai_core.data_loader_workout import load_workout_dataset


class FitbitWorkoutRecommender:
    """
    🚀 HYBRID Workout Recommender combining:
    - Dataset Analysis (Fitbit data patterns)
    - Gemini AI (Personalized explanations & adaptations)
    """

    def __init__(self):
        # Load Fitbit dataset
        self.df = load_workout_dataset()
        self.activity_thresholds = self._analyze_dataset()
        
        # Initialize Gemini client
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self.gemini_available = True
            print("✅ Workout Recommender initialized with Gemini AI")
        else:
            self.gemini_available = False
            print("⚠️ Workout Recommender initialized (Gemini unavailable)")

    # =============== DATASET ANALYSIS ===============

    def _analyze_dataset(self) -> Dict:
        """
        Analyze Fitbit dataset to derive evidence-based activity thresholds
        """
        if self.df.empty:
            return {
                "low": {"active_min": 10, "steps": 3000},
                "medium": {"active_min": 30, "steps": 7000},
                "high": {"active_min": 60, "steps": 10000}
            }

        try:
            # Calculate percentiles from dataset
            percentiles = self.df["veryactiveminutes"].quantile([0.25, 0.50, 0.75])
            steps_percentiles = self.df["totalsteps"].quantile([0.25, 0.50, 0.75]) if "totalsteps" in self.df.columns else None
            
            thresholds = {
                "low": {
                    "active_min": round(percentiles[0.25], 1),
                    "steps": round(steps_percentiles[0.25], 0) if steps_percentiles is not None else 3000
                },
                "medium": {
                    "active_min": round(percentiles[0.50], 1),
                    "steps": round(steps_percentiles[0.50], 0) if steps_percentiles is not None else 7000
                },
                "high": {
                    "active_min": round(percentiles[0.75], 1),
                    "steps": round(steps_percentiles[0.75], 0) if steps_percentiles is not None else 10000
                }
            }
            
            print(f"📊 Dataset Analysis Complete:")
            print(f"   Low Activity: {thresholds['low']['active_min']} min, {thresholds['low']['steps']} steps")
            print(f"   Medium Activity: {thresholds['medium']['active_min']} min, {thresholds['medium']['steps']} steps")
            print(f"   High Activity: {thresholds['high']['active_min']} min, {thresholds['high']['steps']} steps")
            
            return thresholds
            
        except Exception as e:
            print(f"⚠️ Error analyzing dataset: {e}")
            return {
                "low": {"active_min": 10, "steps": 3000},
                "medium": {"active_min": 30, "steps": 7000},
                "high": {"active_min": 60, "steps": 10000}
            }

    # =============== BODY METRICS ===============

    def calculate_bmi(self, height: float, weight: float) -> float:
        """Calculate BMI (kg/m²)"""
        if height <= 0 or weight <= 0:
            raise ValueError("Height and weight must be positive")
        return round(weight / ((height / 100) ** 2), 2)

    def get_bmi_category(self, bmi: float) -> str:
        """Classify BMI into health categories"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def calculate_target_heart_rate(self, age: int, intensity: str = "moderate") -> Dict:
        """Calculate target heart rate zones"""
        max_hr = 220 - age
        
        zones = {
            "light": (0.50, 0.60),      # 50-60% max HR
            "moderate": (0.60, 0.70),   # 60-70% max HR
            "vigorous": (0.70, 0.85),   # 70-85% max HR
            "maximum": (0.85, 0.95)     # 85-95% max HR
        }
        
        intensity = intensity.lower()
        min_pct, max_pct = zones.get(intensity, zones["moderate"])
        
        return {
            "max_hr": max_hr,
            "target_min": round(max_hr * min_pct),
            "target_max": round(max_hr * max_pct),
            "zone": intensity.capitalize()
        }

    # =============== WORKOUT TIER LOGIC ===============

    def determine_workout_tier(self, user: Dict) -> Dict:
        """
        Determine workout tier based on multiple factors:
        - BMI & health status
        - Activity level & fitness
        - Goals & constraints
        """
        bmi = self.calculate_bmi(user["height"], user["weight"])
        bmi_category = self.get_bmi_category(bmi)
        activity = user.get("activity_level", "medium").lower()
        goal = user.get("goal", "maintain").lower()
        age = user.get("age", 30)
        
        # Safety checks
        has_injury = user.get("has_injury", False)
        is_beginner = user.get("is_beginner", False)
        
        # Determine base tier
        if has_injury or bmi > 35:
            tier = "Recovery"
            intensity = "light"
        elif is_beginner or bmi > 30 or activity == "low":
            tier = "Foundation"
            intensity = "light"
        elif activity == "medium" or (25 <= bmi <= 30):
            tier = "Progression"
            intensity = "moderate"
        elif activity == "high" and bmi < 25:
            tier = "Performance"
            intensity = "vigorous"
        else:
            tier = "Progression"
            intensity = "moderate"
        
        # Adjust for age
        if age > 50:
            if tier == "Performance":
                tier = "Progression"
            intensity = "moderate" if intensity == "vigorous" else intensity
        
        # Calculate targets
        hr_zone = self.calculate_target_heart_rate(age, intensity)
        activity_target = self.activity_thresholds.get(activity, self.activity_thresholds["medium"])
        
        return {
            "tier": tier,
            "intensity": intensity,
            "bmi": bmi,
            "bmi_category": bmi_category,
            "heart_rate_zone": hr_zone,
            "daily_targets": {
                "active_minutes": activity_target["active_min"],
                "steps": activity_target["steps"],
                "workouts_per_week": 3 if tier == "Recovery" else 4 if tier == "Foundation" else 5
            }
        }

    # =============== STRUCTURED WORKOUT PLANS ===============

    def get_structured_workout_plan(self, tier: str, goal: str) -> Dict:
        """
        Evidence-based workout plans from dataset insights
        """
        goal = goal.lower()
        
        workout_library = {
            "Recovery": {
                "focus": "Gentle movement, mobility, healing",
                "exercises": [
                    {"name": "Gentle Walking", "duration": "10-15 min", "intensity": "Light", "calories": 50},
                    {"name": "Stretching Routine", "duration": "10 min", "intensity": "Light", "calories": 30},
                    {"name": "Chair Yoga", "duration": "15 min", "intensity": "Light", "calories": 40},
                    {"name": "Breathing Exercises", "duration": "5 min", "intensity": "Light", "calories": 10}
                ],
                "weekly_schedule": "3 days/week, rest days in between",
                "progression": "Focus on consistency, gradually increase walking duration"
            },
            
            "Foundation": {
                "focus": "Build basic strength and cardiovascular base",
                "exercises": [
                    {"name": "Bodyweight Squats", "sets": "3x10", "intensity": "Moderate", "calories": 60},
                    {"name": "Wall Push-ups", "sets": "3x8", "intensity": "Moderate", "calories": 40},
                    {"name": "Plank Hold", "duration": "20-30 sec", "intensity": "Moderate", "calories": 20},
                    {"name": "Brisk Walking", "duration": "20 min", "intensity": "Moderate", "calories": 100},
                    {"name": "Step-ups", "sets": "2x10 each leg", "intensity": "Moderate", "calories": 50}
                ],
                "weekly_schedule": "4 days/week (2 strength, 2 cardio)",
                "progression": "Increase reps by 2-3 each week, add more sets"
            },
            
            "Progression": {
                "focus": "Increase strength, endurance, and intensity",
                "exercises": [
                    {"name": "Goblet Squats", "sets": "4x12", "intensity": "Moderate-High", "calories": 80},
                    {"name": "Push-ups", "sets": "3x12", "intensity": "Moderate-High", "calories": 60},
                    {"name": "Walking Lunges", "sets": "3x10 each leg", "intensity": "Moderate-High", "calories": 70},
                    {"name": "Plank", "duration": "45-60 sec", "intensity": "Moderate-High", "calories": 30},
                    {"name": "Jogging/Running", "duration": "25-30 min", "intensity": "Moderate-High", "calories": 250},
                    {"name": "Mountain Climbers", "sets": "3x15", "intensity": "High", "calories": 50}
                ],
                "weekly_schedule": "5 days/week (3 strength, 2 cardio, 2 rest)",
                "progression": "Increase weight, reduce rest time, add explosive movements"
            },
            
            "Performance": {
                "focus": "Maximum strength, power, and athletic performance",
                "exercises": [
                    {"name": "Barbell Squats", "sets": "4x8", "intensity": "High", "calories": 120},
                    {"name": "Deadlifts", "sets": "4x6", "intensity": "High", "calories": 130},
                    {"name": "Bench Press", "sets": "4x8", "intensity": "High", "calories": 100},
                    {"name": "Pull-ups", "sets": "3x8", "intensity": "High", "calories": 70},
                    {"name": "HIIT Sprints", "duration": "20 min", "intensity": "Maximum", "calories": 300},
                    {"name": "Box Jumps", "sets": "3x10", "intensity": "High", "calories": 80},
                    {"name": "Burpees", "sets": "3x12", "intensity": "Maximum", "calories": 90}
                ],
                "weekly_schedule": "6 days/week (4 strength, 2 HIIT, 1 rest)",
                "progression": "Progressive overload, periodization, track 1RM improvements"
            }
        }
        
        base_plan = workout_library.get(tier, workout_library["Foundation"])
        
        # Adjust for specific goals
        if goal == "weight_loss":
            base_plan["goal_focus"] = "High-calorie burn exercises, longer cardio sessions"
            base_plan["nutrition_note"] = "Maintain calorie deficit while preserving muscle"
        elif goal == "muscle_gain":
            base_plan["goal_focus"] = "Progressive overload, compound movements, adequate rest"
            base_plan["nutrition_note"] = "Ensure calorie surplus and high protein intake"
        elif goal == "endurance":
            base_plan["goal_focus"] = "Longer duration cardio, circuit training, stamina building"
            base_plan["nutrition_note"] = "Adequate carbohydrate intake for sustained energy"
        else:
            base_plan["goal_focus"] = "Balanced approach for overall fitness"
            base_plan["nutrition_note"] = "Maintain balanced nutrition for steady progress"
        
        # Calculate total estimated calories
        total_calories = sum(ex.get("calories", 0) for ex in base_plan["exercises"])
        base_plan["estimated_calories_per_session"] = total_calories
        
        return base_plan

    # =============== GEMINI AI ENHANCEMENT ===============

    def _generate_ai_insights(self, user: Dict, tier_info: Dict, workout_plan: Dict) -> Dict:
        """
        Use Gemini AI to generate personalized insights, tips, and adaptations
        """
        if not self.gemini_available:
            return {
                "personalized_message": "Stay consistent and listen to your body!",
                "tips": ["Focus on proper form", "Stay hydrated", "Get adequate rest"],
                "motivation": "You've got this! Every workout counts."
            }
        
        try:
            # Build context prompt
            prompt = f"""You are a professional fitness coach analyzing a client's workout plan.

CLIENT PROFILE:
- Age: {user.get('age', 'N/A')}
- Height: {user.get('height', 'N/A')} cm
- Weight: {user.get('weight', 'N/A')} kg
- BMI: {tier_info['bmi']} ({tier_info['bmi_category']})
- Activity Level: {user.get('activity_level', 'N/A')}
- Fitness Goal: {user.get('goal', 'maintain')}
- Has Injury: {user.get('has_injury', False)}
- Is Beginner: {user.get('is_beginner', False)}

ASSIGNED WORKOUT TIER: {tier_info['tier']}
INTENSITY: {tier_info['intensity']}
TARGET HEART RATE: {tier_info['heart_rate_zone']['target_min']}-{tier_info['heart_rate_zone']['target_max']} bpm

WORKOUT PLAN FOCUS: {workout_plan.get('focus', 'General fitness')}
EXERCISES: {len(workout_plan.get('exercises', []))} exercises planned

Generate a JSON response with:
1. "personalized_message": A 2-3 sentence motivating message tailored to their profile and goals
2. "tips": Array of 5 specific, actionable tips for THIS person (consider their BMI, age, goals, limitations)
3. "motivation": One powerful motivational quote or statement
4. "exercise_modifications": Array of 2-3 modifications if they have injuries or limitations
5. "nutrition_tip": One specific nutrition tip aligned with their goal

IMPORTANT: Return ONLY valid JSON, no markdown, no explanation."""

            # Call Gemini
            models_to_try = ['models/gemini-2.5-flash', 'models/gemini-2.0-flash-exp', 'models/gemini-1.5-flash']
            
            for model_name in models_to_try:
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    
                    # Parse response
                    response_text = response.text.strip()
                    
                    # Remove markdown fences if present
                    if response_text.startswith('```'):
                        response_text = response_text.split('```')[1]
                        if response_text.startswith('json'):
                            response_text = response_text[4:]
                        response_text = response_text.strip()
                    
                    import json
                    ai_insights = json.loads(response_text)
                    
                    print(f"✅ Gemini AI insights generated with {model_name}")
                    return ai_insights
                    
                except Exception as e:
                    print(f"⚠️ Model {model_name} failed: {str(e)[:100]}")
                    continue
            
            # Fallback if all models fail
            return self._fallback_insights(user, tier_info)
            
        except Exception as e:
            print(f"❌ Gemini AI error: {e}")
            return self._fallback_insights(user, tier_info)

    def _fallback_insights(self, user: Dict, tier_info: Dict) -> Dict:
        """Fallback insights when AI is unavailable"""
        goal = user.get('goal', 'maintain').lower()
        tier = tier_info['tier']
        
        messages = {
            "Recovery": "Focus on gentle movement and healing. Your body needs time to recover and rebuild.",
            "Foundation": "You're building a strong foundation! Consistency is more important than intensity right now.",
            "Progression": "Great progress! You're ready to challenge yourself with more intensity and variety.",
            "Performance": "You're at peak performance level! Focus on optimization and preventing overtraining."
        }
        
        goal_tips = {
            "weight_loss": ["Create a calorie deficit", "Focus on compound movements", "Add cardio 3-4x/week"],
            "muscle_gain": ["Eat in calorie surplus", "Progressive overload each week", "Get 7-9 hours sleep"],
            "maintain": ["Stay consistent", "Balance strength and cardio", "Listen to your body"]
        }
        
        return {
            "personalized_message": messages.get(tier, "Stay consistent!"),
            "tips": goal_tips.get(goal, ["Focus on form", "Stay hydrated", "Rest adequately"]),
            "motivation": "Your only limit is you!",
            "exercise_modifications": [],
            "nutrition_tip": "Fuel your workouts with balanced nutrition"
        }

    # =============== MAIN RECOMMENDATION METHOD ===============

    def recommend_workout(self, user: Dict) -> Dict:
        """
        🚀 MAIN METHOD: Generate comprehensive workout recommendation
        
        Args:
            user: Dict with keys:
                - height (cm)
                - weight (kg)
                - age (int)
                - activity_level (str): 'low', 'medium', 'high'
                - goal (str): 'weight_loss', 'muscle_gain', 'maintain', 'endurance'
                - has_injury (bool, optional)
                - is_beginner (bool, optional)
        
        Returns:
            Comprehensive workout plan with AI insights
        """
        try:
            print("\n=== 🏋️ ENHANCED WORKOUT RECOMMENDER START ===")
            
            # Validate inputs
            required_fields = ['height', 'weight', 'age', 'activity_level', 'goal']
            missing = [f for f in required_fields if f not in user]
            if missing:
                raise ValueError(f"Missing required fields: {missing}")
            
            # Step 1: Determine workout tier
            tier_info = self.determine_workout_tier(user)
            print(f"✅ Tier: {tier_info['tier']} | Intensity: {tier_info['intensity']}")
            
            # Step 2: Get structured workout plan
            workout_plan = self.get_structured_workout_plan(
                tier_info['tier'], 
                user.get('goal', 'maintain')
            )
            print(f"✅ Generated {len(workout_plan['exercises'])} exercises")
            
            # Step 3: Get AI insights (if available)
            ai_insights = self._generate_ai_insights(user, tier_info, workout_plan)
            print(f"✅ AI insights generated")
            
            # Step 4: Compile final recommendation
            recommendation = {
                "success": True,
                "user_profile": {
                    "age": user.get('age'),
                    "bmi": tier_info['bmi'],
                    "bmi_category": tier_info['bmi_category'],
                    "activity_level": user.get('activity_level'),
                    "goal": user.get('goal')
                },
                "workout_tier": tier_info['tier'],
                "intensity_level": tier_info['intensity'],
                "heart_rate_zone": tier_info['heart_rate_zone'],
                "daily_targets": tier_info['daily_targets'],
                "workout_plan": {
                    "focus": workout_plan['focus'],
                    "exercises": workout_plan['exercises'],
                    "weekly_schedule": workout_plan['weekly_schedule'],
                    "progression_strategy": workout_plan['progression'],
                    "goal_specific_focus": workout_plan.get('goal_focus', ''),
                    "nutrition_note": workout_plan.get('nutrition_note', ''),
                    "estimated_calories_burned": workout_plan.get('estimated_calories_per_session', 0)
                },
                "ai_insights": ai_insights,
                "dataset_source": f"Based on analysis of {len(self.df)} Fitbit activity records",
                "timestamp": datetime.now().isoformat()
            }
            
            print("=== ✅ WORKOUT RECOMMENDATION COMPLETE ===\n")
            return recommendation
            
        except Exception as e:
            print(f"❌ Error generating workout recommendation: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate workout recommendation"
            }


# =============== GLOBAL INSTANCE ===============

workout_recommender = FitbitWorkoutRecommender()


# =============== USAGE EXAMPLE ===============

def example_usage():
    """
    Example of how to use the Enhanced Workout Recommender
    """
    try:
        # Example user profile
        user = {
            "age": 28,
            "height": 175,  # cm
            "weight": 75,   # kg
            "activity_level": "medium",
            "goal": "muscle_gain",
            "has_injury": False,
            "is_beginner": False
        }
        
        # Get recommendation
        result = workout_recommender.recommend_workout(user)
        
        if result.get("success"):
            print("\n" + "="*70)
            print("🎯 WORKOUT RECOMMENDATION GENERATED!")
            print("="*70)
            
            print(f"\n📊 USER PROFILE:")
            print(f"   BMI: {result['user_profile']['bmi']} ({result['user_profile']['bmi_category']})")
            print(f"   Goal: {result['user_profile']['goal']}")
            
            print(f"\n🏋️ WORKOUT TIER: {result['workout_tier']}")
            print(f"   Intensity: {result['intensity_level']}")
            print(f"   Heart Rate Zone: {result['heart_rate_zone']['target_min']}-{result['heart_rate_zone']['target_max']} bpm")
            
            print(f"\n🎯 DAILY TARGETS:")
            targets = result['daily_targets']
            print(f"   Active Minutes: {targets['active_minutes']} min")
            print(f"   Steps: {targets['steps']}")
            print(f"   Workouts/Week: {targets['workouts_per_week']}")
            
            print(f"\n💪 WORKOUT PLAN:")
            plan = result['workout_plan']
            print(f"   Focus: {plan['focus']}")
            print(f"   Schedule: {plan['weekly_schedule']}")
            print(f"   Estimated Calories: {plan['estimated_calories_burned']} per session")
            
            print(f"\n🏃 EXERCISES:")
            for i, ex in enumerate(plan['exercises'][:5], 1):  # Show first 5
                print(f"   {i}. {ex['name']}")
                if 'sets' in ex:
                    print(f"      Sets: {ex['sets']} | Intensity: {ex['intensity']}")
                elif 'duration' in ex:
                    print(f"      Duration: {ex['duration']} | Intensity: {ex['intensity']}")
            
            print(f"\n🤖 AI INSIGHTS:")
            insights = result['ai_insights']
            print(f"   💬 {insights.get('personalized_message', '')}")
            print(f"\n   💡 Tips:")
            for tip in insights.get('tips', [])[:3]:
                print(f"      • {tip}")
            
            print(f"\n   🔥 Motivation: {insights.get('motivation', '')}")
            
            print("\n" + "="*70)
        else:
            print(f"❌ Error: {result.get('error')}")
            
    except Exception as e:
        print(f"Error in example: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    example_usage()