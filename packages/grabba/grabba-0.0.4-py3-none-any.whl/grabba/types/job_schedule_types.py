from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .enums import JobSchedulePolicy

class OneTimeSchedule(BaseModel):
    timezone: str
    timestamp: datetime  # Automatically converts from string to datetime

class JobSchedule(BaseModel):
    policy: JobSchedulePolicy
    specification: Optional[OneTimeSchedule] = None 

    class Config:
        json_encoders = {JobSchedulePolicy: lambda v: v.value}


