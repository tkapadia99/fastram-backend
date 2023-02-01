import datetime
from typing import Optional
from pydantic import BaseModel
from fastapi_camelcase import CamelModel

class recordOut(CamelModel):

    id: str
    date: datetime.datetime
    workout_name: str
    duration: str
    exercise_name: str
    set_order: int
    weight: str
    reps: int
    distance: Optional[int]
    seconds: Optional[int]
    notes: Optional[str]
    workout_notes: Optional[str]
    rpe: Optional[str]