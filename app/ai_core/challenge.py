# app/ai_core/challenges_system.py
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass, asdict, field
import json
import copy

class ChallengeType(Enum):
    """Types of health challenges"""
    DIET = "diet"
    WORKOUT = "workout"
    HYDRATION = "hydration"
    SLEEP = "sleep"
    WEIGHT_LOSS = "weight_loss"
    STEP_COUNT = "step_count"
    MEDITATION = "meditation"
    CUSTOM = "custom"

class ChallengeDuration(Enum):
    """Challenge duration options"""
    SEVEN_DAYS = 7
    FIFTEEN_DAYS = 15
    THIRTY_DAYS = 30
    SIXTY_DAYS = 60
    NINETY_DAYS = 90

class ChallengeStatus(Enum):
    """Challenge completion status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"

@dataclass
class DailyProgress:
    """Daily progress tracking"""
    day_number: int
    date: str
    completed: bool
    value: Optional[float] = None
    notes: Optional[str] = None
    timestamp: Optional[str] = None

@dataclass
class Challenge:
    """Challenge model"""
    id: str
    user_id: str
    title: str
    description: str
    challenge_type: str
    duration_days: int
    target_value: Optional[float]
    unit: Optional[str]
    start_date: str
    end_date: str
    status: str
    current_streak: int = 0
    longest_streak: int = 0
    completion_percentage: float = 0.0
    days_completed: int = 0
    total_days: int = 0
    daily_progress: List[Dict] = field(default_factory=list)
    rewards_earned: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

@dataclass
class Badge:
    """Achievement badge model"""
    id: str
    name: str
    description: str
    icon: str
    category: str
    requirement: str
    points: int
    rarity: str
    earned_date: Optional[str] = None
    progress: float = 0.0

class ChallengeManager:
    """Manages health challenges and gamification"""
    
    # Pre-defined challenge templates
    CHALLENGE_TEMPLATES = {
        "30_day_diet": {
            "title": "30-Day Clean Eating Challenge",
            "description": "Stick to your personalized diet plan for 30 consecutive days",
            "challenge_type": "diet",
            "duration_days": 30,
            "target_value": 30,
            "unit": "days"
        },
        "60_day_fitness": {
            "title": "60-Day Fitness Transformation",
            "description": "Complete your workout plan 5 days a week for 60 days",
            "challenge_type": "workout",
            "duration_days": 60,
            "target_value": 40,
            "unit": "workouts"
        },
        "7_day_hydration": {
            "title": "7-Day Hydration Challenge",
            "description": "Drink 8 glasses of water every day for a week",
            "challenge_type": "hydration",
            "duration_days": 7,
            "target_value": 8,
            "unit": "glasses"
        },
        "30_day_10k_steps": {
            "title": "30-Day 10K Steps Challenge",
            "description": "Walk 10,000 steps every day for 30 days",
            "challenge_type": "step_count",
            "duration_days": 30,
            "target_value": 10000,
            "unit": "steps"
        },
        "60_day_weight_loss": {
            "title": "60-Day Weight Loss Journey",
            "description": "Lose 5-10 kg through consistent diet and exercise",
            "challenge_type": "weight_loss",
            "duration_days": 60,
            "target_value": 7.5,
            "unit": "kg"
        },
        "30_day_sleep": {
            "title": "30-Day Sleep Optimization",
            "description": "Get 7-8 hours of quality sleep every night",
            "challenge_type": "sleep",
            "duration_days": 30,
            "target_value": 7.5,
            "unit": "hours"
        },
        "15_day_meditation": {
            "title": "15-Day Mindfulness Journey",
            "description": "Meditate for 10 minutes daily for 15 days",
            "challenge_type": "meditation",
            "duration_days": 15,
            "target_value": 10,
            "unit": "minutes"
        }
    }
    
    def __init__(self):
        # In production, use a database
        self.challenges: Dict[str, Challenge] = {}
        self.user_badges: Dict[str, List[Badge]] = {}
        self.user_points: Dict[str, int] = {}
        
        # Badge definitions as instance variable
        self.BADGE_DEFINITIONS = {
            "first_challenge": Badge(
                id="badge_001",
                name="Challenger",
                description="Complete your first challenge",
                icon="🎯",
                category="milestone",
                requirement="Complete 1 challenge",
                points=50,
                rarity="common"
            ),
            "7_day_streak": Badge(
                id="badge_002",
                name="Week Warrior",
                description="Maintain a 7-day streak",
                icon="🔥",
                category="streak",
                requirement="7 consecutive days",
                points=100,
                rarity="common"
            ),
            "30_day_streak": Badge(
                id="badge_003",
                name="Month Master",
                description="Maintain a 30-day streak",
                icon="⭐",
                category="streak",
                requirement="30 consecutive days",
                points=300,
                rarity="rare"
            ),
            "60_day_streak": Badge(
                id="badge_004",
                name="Legend",
                description="Maintain a 60-day streak",
                icon="👑",
                category="streak",
                requirement="60 consecutive days",
                points=600,
                rarity="epic"
            ),
            "perfect_week": Badge(
                id="badge_005",
                name="Perfectionist",
                description="Complete all daily tasks for a week",
                icon="💎",
                category="achievement",
                requirement="100% completion for 7 days",
                points=150,
                rarity="rare"
            ),
            "early_bird": Badge(
                id="badge_006",
                name="Early Bird",
                description="Complete tasks before 8 AM for 7 days",
                icon="🌅",
                category="achievement",
                requirement="Early completion streak",
                points=100,
                rarity="common"
            ),
            "weight_loss_5kg": Badge(
                id="badge_007",
                name="5kg Warrior",
                description="Lose 5kg through healthy habits",
                icon="🏆",
                category="weight_loss",
                requirement="Lose 5kg",
                points=250,
                rarity="rare"
            ),
            "fitness_beast": Badge(
                id="badge_008",
                name="Fitness Beast",
                description="Complete 100 workouts",
                icon="💪",
                category="fitness",
                requirement="100 workouts completed",
                points=400,
                rarity="epic"
            ),
            "diet_master": Badge(
                id="badge_009",
                name="Nutrition Expert",
                description="Follow diet plan for 60 days",
                icon="🥗",
                category="diet",
                requirement="60 days diet adherence",
                points=500,
                rarity="epic"
            ),
            "centurion": Badge(
                id="badge_010",
                name="Centurion",
                description="Maintain a 100-day streak",
                icon="🌟",
                category="streak",
                requirement="100 consecutive days",
                points=1000,
                rarity="legendary"
            )
        }
    
    def create_challenge(
        self,
        user_id: str,
        template_key: Optional[str] = None,
        custom_title: Optional[str] = None,
        custom_description: Optional[str] = None,
        challenge_type: Optional[str] = None,
        duration_days: Optional[int] = None,
        target_value: Optional[float] = None,
        unit: Optional[str] = None
    ) -> Dict:
        """Create a new challenge for a user"""
        
        try:
            # Use template if provided
            if template_key and template_key in self.CHALLENGE_TEMPLATES:
                template = self.CHALLENGE_TEMPLATES[template_key]
                challenge_data = template.copy()
            else:
                # Custom challenge
                if not all([custom_title, challenge_type, duration_days]):
                    return {
                        "success": False,
                        "error": "Missing required fields for custom challenge"
                    }
                challenge_data = {
                    "title": custom_title,
                    "description": custom_description or "",
                    "challenge_type": challenge_type,
                    "duration_days": duration_days,
                    "target_value": target_value,
                    "unit": unit
                }
            
            # Generate challenge ID
            challenge_id = f"challenge_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Calculate dates
            start_date = datetime.now()
            end_date = start_date + timedelta(days=challenge_data["duration_days"])
            
            # Create challenge object
            challenge = Challenge(
                id=challenge_id,
                user_id=user_id,
                title=challenge_data["title"],
                description=challenge_data["description"],
                challenge_type=challenge_data["challenge_type"],
                duration_days=challenge_data["duration_days"],
                target_value=challenge_data["target_value"],
                unit=challenge_data["unit"],
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                status=ChallengeStatus.IN_PROGRESS.value,
                total_days=challenge_data["duration_days"]
            )
            
            # Store challenge
            self.challenges[challenge_id] = challenge
            
            return {
                "success": True,
                "challenge": asdict(challenge),
                "message": f"Challenge '{challenge.title}' created successfully!"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create challenge: {str(e)}"
            }
    
    def update_daily_progress(
        self,
        challenge_id: str,
        completed: bool,
        value: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Dict:
        """Update daily progress for a challenge"""
        
        try:
            if challenge_id not in self.challenges:
                return {"success": False, "error": "Challenge not found"}
            
            challenge = self.challenges[challenge_id]
            
            # Calculate current day
            start = datetime.fromisoformat(challenge.start_date)
            today = datetime.now()
            day_number = (today - start).days + 1
            
            if day_number > challenge.total_days:
                return {"success": False, "error": "Challenge period has ended"}
            
            if day_number < 1:
                return {"success": False, "error": "Challenge hasn't started yet"}
            
            # Create daily progress entry
            progress = DailyProgress(
                day_number=day_number,
                date=today.strftime("%Y-%m-%d"),
                completed=completed,
                value=value,
                notes=notes,
                timestamp=datetime.now().isoformat()
            )
            
            # Add to daily progress
            challenge.daily_progress.append(asdict(progress))
            
            # Update statistics
            if completed:
                challenge.days_completed += 1
                challenge.current_streak += 1
                challenge.longest_streak = max(challenge.longest_streak, challenge.current_streak)
            else:
                challenge.current_streak = 0
            
            challenge.completion_percentage = (challenge.days_completed / challenge.total_days) * 100
            
            # Check if challenge is completed
            if challenge.completion_percentage >= 100:
                challenge.status = ChallengeStatus.COMPLETED.value
                self._award_completion_rewards(challenge)
            
            # Check for streak badges
            self._check_streak_badges(challenge.user_id, challenge.current_streak)
            
            return {
                "success": True,
                "challenge_id": challenge_id,
                "day_number": day_number,
                "current_streak": challenge.current_streak,
                "completion_percentage": round(challenge.completion_percentage, 2),
                "message": "Progress updated successfully!",
                "new_badges": self._get_recently_earned_badges(challenge.user_id, minutes=1)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update progress: {str(e)}"
            }
    
    def get_challenge_progress(self, challenge_id: str) -> Dict:
        """Get detailed progress for a challenge"""
        
        if challenge_id not in self.challenges:
            return {"success": False, "error": "Challenge not found"}
        
        challenge = self.challenges[challenge_id]
        
        return {
            "success": True,
            "challenge": asdict(challenge),
            "progress_summary": {
                "total_days": challenge.total_days,
                "days_completed": challenge.days_completed,
                "days_remaining": challenge.total_days - challenge.days_completed,
                "completion_percentage": round(challenge.completion_percentage, 2),
                "current_streak": challenge.current_streak,
                "longest_streak": challenge.longest_streak,
                "status": challenge.status
            }
        }
    
    def get_user_challenges(self, user_id: str, status: Optional[str] = None) -> Dict:
        """Get all challenges for a user"""
        
        user_challenges = [
            asdict(c) for c in self.challenges.values()
            if c.user_id == user_id and (status is None or c.status == status)
        ]
        
        return {
            "success": True,
            "user_id": user_id,
            "total_challenges": len(user_challenges),
            "challenges": user_challenges
        }
    
    def _award_completion_rewards(self, challenge: Challenge):
        """Award badges and points for completing a challenge"""
        
        user_id = challenge.user_id
        
        # Initialize user data if needed
        if user_id not in self.user_badges:
            self.user_badges[user_id] = []
        if user_id not in self.user_points:
            self.user_points[user_id] = 0
        
        # Award points based on duration
        points = challenge.duration_days * 10
        self.user_points[user_id] += points
        
        # Check for first challenge badge
        completed_challenges = [
            c for c in self.challenges.values()
            if c.user_id == user_id and c.status == ChallengeStatus.COMPLETED.value
        ]
        
        if len(completed_challenges) == 1:
            self._award_badge(user_id, "first_challenge")
        
        # Duration-specific badges
        if challenge.duration_days >= 30:
            self._award_badge(user_id, "30_day_streak")
        if challenge.duration_days >= 60:
            self._award_badge(user_id, "60_day_streak")
    
    def _check_streak_badges(self, user_id: str, streak: int):
        """Check and award streak badges"""
        
        if streak >= 7:
            self._award_badge(user_id, "7_day_streak")
        if streak >= 30:
            self._award_badge(user_id, "30_day_streak")
        if streak >= 60:
            self._award_badge(user_id, "60_day_streak")
        if streak >= 100:
            self._award_badge(user_id, "centurion")
    
    def _award_badge(self, user_id: str, badge_key: str):
        """Award a badge to a user"""
        
        if user_id not in self.user_badges:
            self.user_badges[user_id] = []
        
        # Check if badge already earned
        if any(b.id == self.BADGE_DEFINITIONS[badge_key].id for b in self.user_badges[user_id]):
            return
        
        # Create a copy of the badge to avoid modifying the template
        badge = copy.deepcopy(self.BADGE_DEFINITIONS[badge_key])
        badge.earned_date = datetime.now().isoformat()
        
        self.user_badges[user_id].append(badge)
        
        # Award points
        if user_id not in self.user_points:
            self.user_points[user_id] = 0
        self.user_points[user_id] += badge.points
    
    def get_user_badges(self, user_id: str) -> Dict:
        """Get all badges earned by a user"""
        
        badges = self.user_badges.get(user_id, [])
        points = self.user_points.get(user_id, 0)
        
        return {
            "success": True,
            "user_id": user_id,
            "total_badges": len(badges),
            "total_points": points,
            "badges": [asdict(b) for b in badges],
            "available_badges": [
                asdict(b) for b in self.BADGE_DEFINITIONS.values()
                if b.id not in [earned.id for earned in badges]
            ]
        }
    
    def _get_recently_earned_badges(self, user_id: str, minutes: int = 5) -> List[Dict]:
        """Get badges earned in the last N minutes"""
        
        recent_time = datetime.now() - timedelta(minutes=minutes)
        badges = self.user_badges.get(user_id, [])
        
        recent_badges = [
            asdict(b) for b in badges
            if b.earned_date and datetime.fromisoformat(b.earned_date) > recent_time
        ]
        
        return recent_badges
    
    def get_leaderboard(self, limit: int = 10) -> Dict:
        """Get global leaderboard by points"""
        
        leaderboard = sorted(
            self.user_points.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return {
            "success": True,
            "leaderboard": [
                {
                    "rank": i + 1,
                    "user_id": user_id,
                    "points": points,
                    "badges_count": len(self.user_badges.get(user_id, []))
                }
                for i, (user_id, points) in enumerate(leaderboard)
            ]
        }
    
    def get_challenge_templates(self) -> Dict:
        """Get all available challenge templates"""
        
        return {
            "success": True,
            "templates": {
                key: {**value, "template_key": key}
                for key, value in self.CHALLENGE_TEMPLATES.items()
            }
        }


# Global instance
challenge_manager = ChallengeManager()


# Example usage
if __name__ == "__main__":
    print("🏆 Challenge System Test\n")
    
    # Create a 30-day challenge
    result = challenge_manager.create_challenge(
        user_id="user123",
        template_key="30_day_diet"
    )
    
    if result.get("success"):
        print(f"✅ Challenge created: {result['challenge']['title']}")
        
        challenge_id = result['challenge']['id']
        
        # Simulate daily progress
        for day in range(7):
            progress = challenge_manager.update_daily_progress(
                challenge_id=challenge_id,
                completed=True,
                value=2000,
                notes=f"Day {day+1} completed!"
            )
            if progress.get("success"):
                print(f"Day {day+1}: Streak {progress['current_streak']}, Progress {progress['completion_percentage']}%")
        
        # Get badges
        badges = challenge_manager.get_user_badges("user123")
        print(f"\n🎖️  Badges earned: {badges['total_badges']}")
        print(f"⭐ Total points: {badges['total_points']}")
    else:
        print(f"❌ Error: {result.get('error')}")