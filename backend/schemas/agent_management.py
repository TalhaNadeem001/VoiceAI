from pydantic import BaseModel
from typing import Optional

class AgentCreateRequest(BaseModel):
    name: str
    phone_number: Optional[str] = None
    system_prompt: str