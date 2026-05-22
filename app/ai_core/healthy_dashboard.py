# app/ai_core/health_dashboard.py
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import statistics

@dataclass
class HealthMetric:
    """Base health metric tracking"""
    date: str
    value: float
    unit: str
    notes: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

@dataclass
class DietLog:
    """Daily diet logging"""
    date: str
    meal_type: str  # breakfast, lunch, dinner, snack
    food_items: List[str]
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: Optional[float] = None
    notes: Optional[str] = None
    adherence_score: float = 0.0  # 0-100%

@dataclass
class WorkoutLog:
    """Workout session tracking"""
    date: str
    workout_type: str  # cardio, strength, yoga, sports
    duration_minutes: int
    calories_burned: float
    exercises: List[str]
    intensity: str  # low, medium, high
    notes: Optional[str] = None

@dataclass
class SleepLog:
    """Sleep quality tracking"""
    date: str
    sleep_time: str  # HH:MM format
    wake_time: str
    duration_hours: float
    quality_score: int  # 1-10
    interruptions: int = 0
    notes: Optional[str] = None

@dataclass
class StressLog:
    """Stress and mood tracking"""
    date: str
    stress_level: int  # 1-10
    mood: str  # happy, neutral, sad, anxious, energetic
    stressors: List[str]
    coping_methods: Optional[List[str]] = None
    notes: Optional[str] = None

class HealthDashboard:
    """Comprehensive health tracking and analytics dashboard"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        
        # Storage (in production, use database)
        self.weight_logs: List[HealthMetric] = []
        self.diet_logs: List[DietLog] = []
        self.workout_logs: List[WorkoutLog] = []
        self.sleep_logs: List[SleepLog] = []
        self.stress_logs: List[StressLog] = []
        self.water_intake: List[HealthMetric] = []
        self.step_count: List[HealthMetric] = []
        
        # User profile
        self.user_profile = {
            "weight_goal": None,
            "calorie_target": None,
            "protein_target": None,
            "workout_goal_days": 5,
            "sleep_target_hours": 7.5,
            "water_target_glasses": 8,
            "step_target": 10000
        }
    
    # ==================== LOGGING METHODS ====================
    
    def log_weight(self, weight_kg: float, notes: Optional[str] = None) -> Dict:
        """Log daily weight"""
        metric = HealthMetric(
            date=datetime.now().strftime("%Y-%m-%d"),
            value=weight_kg,
            unit="kg",
            notes=notes
        )
        self.weight_logs.append(metric)
        
        return {
            "success": True,
            "message": "Weight logged successfully",
            "data": asdict(metric)
        }
    
    def log_diet(
        self,
        meal_type: str,
        food_items: List[str],
        calories: float,
        protein: float,
        carbs: float,
        fat: float,
        notes: Optional[str] = None
    ) -> Dict:
        """Log meal/diet entry"""
        
        # Calculate adherence score
        target_calories = self.user_profile.get("calorie_target", 2000)
        adherence = min(100, (calories / (target_calories / 4)) * 100)  # Per meal
        
        log = DietLog(
            date=datetime.now().strftime("%Y-%m-%d"),
            meal_type=meal_type,
            food_items=food_items,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            notes=notes,
            adherence_score=adherence
        )
        self.diet_logs.append(log)
        
        return {
            "success": True,
            "message": "Diet logged successfully",
            "data": asdict(log)
        }
    
    def log_workout(
        self,
        workout_type: str,
        duration_minutes: int,
        exercises: List[str],
        calories_burned: float,
        intensity: str = "medium",
        notes: Optional[str] = None
    ) -> Dict:
        """Log workout session"""
        
        log = WorkoutLog(
            date=datetime.now().strftime("%Y-%m-%d"),
            workout_type=workout_type,
            duration_minutes=duration_minutes,
            calories_burned=calories_burned,
            exercises=exercises,
            intensity=intensity,
            notes=notes
        )
        self.workout_logs.append(log)
        
        return {
            "success": True,
            "message": "Workout logged successfully",
            "data": asdict(log)
        }
    
    def log_sleep(
        self,
        sleep_time: str,
        wake_time: str,
        quality_score: int,
        interruptions: int = 0,
        notes: Optional[str] = None
    ) -> Dict:
        """Log sleep data"""
        
        # Calculate duration
        sleep_dt = datetime.strptime(sleep_time, "%H:%M")
        wake_dt = datetime.strptime(wake_time, "%H:%M")
        
        if wake_dt < sleep_dt:
            wake_dt += timedelta(days=1)
        
        duration = (wake_dt - sleep_dt).seconds / 3600
        
        log = SleepLog(
            date=datetime.now().strftime("%Y-%m-%d"),
            sleep_time=sleep_time,
            wake_time=wake_time,
            duration_hours=round(duration, 2),
            quality_score=quality_score,
            interruptions=interruptions,
            notes=notes
        )
        self.sleep_logs.append(log)
        
        return {
            "success": True,
            "message": "Sleep logged successfully",
            "data": asdict(log)
        }
    
    def log_stress(
        self,
        stress_level: int,
        mood: str,
        stressors: List[str],
        coping_methods: Optional[List[str]] = None,
        notes: Optional[str] = None
    ) -> Dict:
        """Log stress and mood"""
        
        log = StressLog(
            date=datetime.now().strftime("%Y-%m-%d"),
            stress_level=stress_level,
            mood=mood,
            stressors=stressors,
            coping_methods=coping_methods,
            notes=notes
        )
        self.stress_logs.append(log)
        
        return {
            "success": True,
            "message": "Stress logged successfully",
            "data": asdict(log)
        }
    
    def log_water(self, glasses: int) -> Dict:
        """Log daily water intake"""
        metric = HealthMetric(
            date=datetime.now().strftime("%Y-%m-%d"),
            value=glasses,
            unit="glasses"
        )
        self.water_intake.append(metric)
        
        return {
            "success": True,
            "message": "Water intake logged",
            "data": asdict(metric)
        }
    
    def log_steps(self, steps: int) -> Dict:
        """Log daily step count"""
        metric = HealthMetric(
            date=datetime.now().strftime("%Y-%m-%d"),
            value=steps,
            unit="steps"
        )
        self.step_count.append(metric)
        
        return {
            "success": True,
            "message": "Steps logged",
            "data": asdict(metric)
        }
    
    # ==================== ANALYTICS METHODS ====================
    
    def get_daily_summary(self, date: Optional[str] = None) -> Dict:
        """Get comprehensive summary for a specific day"""
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Filter logs for the date
        day_diet = [log for log in self.diet_logs if log.date == date]
        day_workouts = [log for log in self.workout_logs if log.date == date]
        day_sleep = [log for log in self.sleep_logs if log.date == date]
        day_stress = [log for log in self.stress_logs if log.date == date]
        day_water = [log for log in self.water_intake if log.date == date]
        day_steps = [log for log in self.step_count if log.date == date]
        
        # Calculate totals
        total_calories = sum(log.calories for log in day_diet)
        total_protein = sum(log.protein for log in day_diet)
        total_workout_mins = sum(log.duration_minutes for log in day_workouts)
        total_calories_burned = sum(log.calories_burned for log in day_workouts)
        
        return {
            "success": True,
            "date": date,
            "summary": {
                "nutrition": {
                    "total_calories": round(total_calories, 1),
                    "total_protein": round(total_protein, 1),
                    "meals_logged": len(day_diet),
                    "target_calories": self.user_profile.get("calorie_target", 2000),
                    "calorie_deficit": round(self.user_profile.get("calorie_target", 2000) - total_calories, 1)
                },
                "fitness": {
                    "workouts_completed": len(day_workouts),
                    "total_duration_minutes": total_workout_mins,
                    "calories_burned": round(total_calories_burned, 1),
                    "workout_types": list(set(log.workout_type for log in day_workouts))
                },
                "sleep": {
                    "hours_slept": day_sleep[0].duration_hours if day_sleep else 0,
                    "quality_score": day_sleep[0].quality_score if day_sleep else 0,
                    "target_hours": self.user_profile.get("sleep_target_hours", 7.5)
                },
                "hydration": {
                    "glasses": day_water[0].value if day_water else 0,
                    "target": self.user_profile.get("water_target_glasses", 8)
                },
                "activity": {
                    "steps": int(day_steps[0].value) if day_steps else 0,
                    "target": self.user_profile.get("step_target", 10000)
                },
                "wellness": {
                    "stress_level": day_stress[0].stress_level if day_stress else 0,
                    "mood": day_stress[0].mood if day_stress else "N/A"
                }
            }
        }
    
    def get_weekly_summary(self, end_date: Optional[str] = None) -> Dict:
        """Get summary for the past 7 days"""
        
        if end_date is None:
            end = datetime.now()
        else:
            end = datetime.strptime(end_date, "%Y-%m-%d")
        
        start = end - timedelta(days=7)
        
        # Collect data for date range
        week_diet = [log for log in self.diet_logs 
                    if start.strftime("%Y-%m-%d") <= log.date <= end.strftime("%Y-%m-%d")]
        week_workouts = [log for log in self.workout_logs 
                        if start.strftime("%Y-%m-%d") <= log.date <= end.strftime("%Y-%m-%d")]
        week_sleep = [log for log in self.sleep_logs 
                     if start.strftime("%Y-%m-%d") <= log.date <= end.strftime("%Y-%m-%d")]
        
        # Calculate averages
        avg_calories = statistics.mean([log.calories for log in week_diet]) if week_diet else 0
        avg_protein = statistics.mean([log.protein for log in week_diet]) if week_diet else 0
        avg_sleep = statistics.mean([log.duration_hours for log in week_sleep]) if week_sleep else 0
        
        return {
            "success": True,
            "period": f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}",
            "summary": {
                "nutrition": {
                    "avg_daily_calories": round(avg_calories, 1),
                    "avg_daily_protein": round(avg_protein, 1),
                    "days_tracked": len(set(log.date for log in week_diet))
                },
                "fitness": {
                    "total_workouts": len(week_workouts),
                    "total_duration_minutes": sum(log.duration_minutes for log in week_workouts),
                    "workout_frequency": len(week_workouts) / 7
                },
                "sleep": {
                    "avg_hours": round(avg_sleep, 2),
                    "days_tracked": len(week_sleep)
                }
            }
        }
    
    def get_progress_trends(self, days: int = 30) -> Dict:
        """Get trends and progress over time"""
        
        end = datetime.now()
        start = end - timedelta(days=days)
        
        # Weight trend
        recent_weights = [
            log for log in self.weight_logs
            if start.strftime("%Y-%m-%d") <= log.date <= end.strftime("%Y-%m-%d")
        ]
        
        weight_trend = {
            "data": [{"date": log.date, "weight": log.value} for log in recent_weights],
            "change": 0
        }
        
        if len(recent_weights) >= 2:
            weight_trend["change"] = round(recent_weights[-1].value - recent_weights[0].value, 2)
        
        return {
            "success": True,
            "period_days": days,
            "trends": {
                "weight": weight_trend,
                "total_data_points": len(recent_weights)
            }
        }
    
    def get_achievements(self) -> Dict:
        """Get user achievements and milestones"""
        
        achievements = []
        
        # Workout streaks
        workout_dates = sorted(set(log.date for log in self.workout_logs))
        current_streak = self._calculate_streak(workout_dates)
        
        if current_streak >= 7:
            achievements.append({
                "title": f"{current_streak}-Day Workout Streak",
                "icon": "🔥",
                "category": "fitness"
            })
        
        # Total workouts
        total_workouts = len(self.workout_logs)
        if total_workouts >= 50:
            achievements.append({
                "title": f"{total_workouts} Workouts Completed",
                "icon": "💪",
                "category": "fitness"
            })
        
        return {
            "success": True,
            "total_achievements": len(achievements),
            "achievements": achievements
        }
    
    def _calculate_streak(self, dates: List[str]) -> int:
        """Calculate current consecutive streak"""
        if not dates:
            return 0
        
        streak = 0
        today = datetime.now().date()
        
        for i in range(len(dates) - 1, -1, -1):
            date = datetime.strptime(dates[i], "%Y-%m-%d").date()
            expected = today - timedelta(days=streak)
            
            if date == expected:
                streak += 1
            else:
                break
        
        return streak
    
    def set_goals(
        self,
        weight_goal: Optional[float] = None,
        calorie_target: Optional[int] = None,
        protein_target: Optional[int] = None,
        workout_days: Optional[int] = None,
        sleep_hours: Optional[float] = None,
        water_glasses: Optional[int] = None,
        daily_steps: Optional[int] = None
    ) -> Dict:
        """Set health goals"""
        
        if weight_goal is not None:
            self.user_profile["weight_goal"] = weight_goal
        if calorie_target is not None:
            self.user_profile["calorie_target"] = calorie_target
        if protein_target is not None:
            self.user_profile["protein_target"] = protein_target
        if workout_days is not None:
            self.user_profile["workout_goal_days"] = workout_days
        if sleep_hours is not None:
            self.user_profile["sleep_target_hours"] = sleep_hours
        if water_glasses is not None:
            self.user_profile["water_target_glasses"] = water_glasses
        if daily_steps is not None:
            self.user_profile["step_target"] = daily_steps
        
        return {
            "success": True,
            "message": "Goals updated successfully",
            "goals": self.user_profile
        }


# Example usage
if __name__ == "__main__":
    print("📊 Health Dashboard Test\n")
    
    dashboard = HealthDashboard(user_id="user123")
    
    # Set goals
    dashboard.set_goals(
        weight_goal=70,
        calorie_target=2000,
        protein_target=150,
        workout_days=5
    )
    
    # Log sample data
    dashboard.log_weight(75.5, notes="Morning weight")
    dashboard.log_diet("breakfast", ["oatmeal", "banana", "milk"], 400, 15, 60, 10)
    dashboard.log_workout("cardio", 30, ["running"], 250, "medium")
    dashboard.log_sleep("23:00", "07:00", 8)
    dashboard.log_water(6)
    dashboard.log_steps(8500)
    
    # Get summary
    summary = dashboard.get_daily_summary()
    print(f"✅ Daily Summary:")
    print(f"Calories: {summary['summary']['nutrition']['total_calories']}")
    print(f"Workouts: {summary['summary']['fitness']['workouts_completed']}")
    print(f"Steps: {summary['summary']['activity']['steps']}")