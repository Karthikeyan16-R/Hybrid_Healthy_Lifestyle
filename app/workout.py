from pydantic import BaseModel

class WorkoutRequest(BaseModel):
    age: int
    height: float
    weight: float
    goal: str
    activity_level: str
    time_available: int
