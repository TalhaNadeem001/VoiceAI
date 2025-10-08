from fastapi import APIRouter, HTTPException, Depends
from schemas.outbound import Lead
from services.outbound import qualify_and_schedule_lead
from models.auth import User
from services.auth import get_current_user
from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/leads/analyze-and-schedule")
async def qualify_and_schedule_call(request: Lead, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = qualify_and_schedule_lead(request, current_user, db)
        return {"status": "success", "data": result}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in qualify_and_schedule_lead: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")