from schemas.outbound import Lead
from models.auth import User
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def qualify_and_schedule_lead(request: Lead, user: User, db: Session):

    # Lead Qualification

    # Schedule Lead
    ...


def qualification(conversation):
    ...