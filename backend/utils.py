from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.auth import User
from schemas.agent_management import AgentCreateRequest


def validate_agent_creation(request: AgentCreateRequest, db: Session, VoiceAgent, user: User):
    """
    Checks if the agent name is already in use for the given user.
    
    Raises:
        ValueError: If the name is already associated with this user.
    """

    # Query for existing agent with same name for this user
    in_use = (
        db.query(VoiceAgent)
        .filter(
            VoiceAgent.user_id == user.id,
            VoiceAgent.name == request.name
        )
        .first()
    )

    if in_use:
        if in_use.name == request.name:
            raise ValueError("You already have an agent with this name")