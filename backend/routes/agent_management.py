from fastapi import APIRouter, Depends, HTTPException
from schemas.agent_management import AgentCreateRequest
from services.agent_management import create_agent_service, delete_agent_service, get_all_agents
from models.auth import User
from services.auth import get_current_user
from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/agents")
async def get_agents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all voice agents for the authenticated user from the local database.
    """
    try:
        return get_all_agents(current_user, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents")
async def create_agent(
    request: AgentCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return create_agent_service(request, current_user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/agents/{agent_id}")
async def delete_agent(
    agent_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return delete_agent_service(agent_id, current_user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))