from pydantic import BaseModel
from datetime import datetime

class Lead(BaseModel):
    conversation: str
    scheduled_time: datetime
    agent_id: str