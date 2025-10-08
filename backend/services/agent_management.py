from schemas.agent_management import AgentCreateRequest
from utils import validate_agent_creation
from clients.elevenlabs_client import elevenlabs
from elevenlabs import ConversationalConfig
from models.auth import User
from models.voiceagents import VoiceAgent
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


def get_all_agents(user: User, db: Session):
    """
    Retrieve all voice agents belonging to the given user from the local database.

    Args:
        user (User): Authenticated user requesting their agents.
        db (Session): SQLAlchemy database session.

    Returns:
        list[dict]: List of agents with their details.
    """
    agents = (
        db.query(VoiceAgent)
        .filter(VoiceAgent.user_id == user.id)
        .all()
    )

    return [
        {
            "id": agent.id,
            "name": agent.name,
            "phone_number": agent.phone_number,
            "system_prompt": agent.system_prompt,
            "created_at": agent.created_at,
            "updated_at": agent.updated_at,
        }
        for agent in agents
    ]


def create_agent_service(request: AgentCreateRequest, user: User, db: Session):
    """
    Service function to create a new Voice Agent for a user.

    Steps:
        1. Validates that the agent name is unique for this user.
        2. Creates the agent in the ElevenLabs Conversational AI platform.
        3. Creates a corresponding entry in the local database using the ElevenLabs agent ID.
        4. Handles database integrity errors (e.g., duplicate agent name for the user).

    Args:
        request (AgentCreateRequest): Pydantic schema containing agent creation data.
            - name: Name of the agent.
            - System Prompt: How the Agent Should Act
        user (User): SQLAlchemy User model of the currently authenticated user.
        db (Session): SQLAlchemy database session.

    Raises:
        ValueError: If an agent with the same name already exists for the user.

    Returns:
        dict: Details of the newly created agent:
            - status: "success"
            - agent_id: The ElevenLabs agent ID (string)
            - name: Agent name
    """

    # 1️. Validate uniqueness of agent name for this user
    validate_agent_creation(request, db, VoiceAgent, user)

    # 2️. Create agent in ElevenLabs with required conversation_config
    conversation_config = ConversationalConfig(
    agent_config={
        "prompt": {
            "prompt": request.system_prompt
            }
        }   
    )

    # 2️. Create agent in ElevenLabs and store metadata
    agent = elevenlabs.conversational_ai.agents.create(
        name=request.name,
        conversation_config=conversation_config
    )

    # 3️. Create VoiceAgent database entry using the ElevenLabs agent ID
    voice_agent = VoiceAgent(
        id=agent.agent_id,  
        user_id=user.id,
        name=request.name,
        phone_number= request.phone_number,
        system_prompt=request.system_prompt,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # 4️. Add to DB and handle unique constraint violations
    try:
        db.add(voice_agent)
        db.commit()
        db.refresh(voice_agent)
    except IntegrityError:
        db.rollback()
        # Could happen if another request created the same agent concurrently
        raise ValueError("An agent with this name already exists for this user")

    # 5️. Return structured response
    return {
        "status": "success",
        "agent_id": voice_agent.id,
        "name": voice_agent.name,
    }

def delete_agent_service(agent_id: str, user: User, db: Session):
    """
    Delete a voice agent belonging to the given user.

    Steps:
        1. Look up the agent by ID and ensure it belongs to the user.
        2. Remove the agent from ElevenLabs.
        3. Delete the agent record from the local database.

    Args:
        agent_id (str): ElevenLabs agent ID to delete.
        user (User): Authenticated user requesting the deletion.
        db (Session): SQLAlchemy database session.

    Raises:
        ValueError: If the agent is not found or does not belong to the user.
        HTTPException: If deletion from DB fails.

    Returns:
        dict: Status and confirmation message.
    """
    # Find the agent for this user
    voice_agent = (
        db.query(VoiceAgent)
        .filter(VoiceAgent.id == agent_id, VoiceAgent.user_id == user.id)
        .first()
    )

    if not voice_agent:
        raise ValueError("Agent not found or does not belong to this user")

    try:
        # Remove agent from ElevenLabs
        elevenlabs.conversational_ai.agents.delete(agent_id=agent_id)

        # Delete agent from local DB
        db.delete(voice_agent)
        db.commit()

        return {"status": "success", "message": f"Agent {agent_id} deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete agent: {str(e)}")