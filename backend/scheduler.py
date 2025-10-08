from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

def create_scheduler(db_url: str):
    
    # APScheduler needs its own job table (it will auto-create)
    jobstores = {
        "default": SQLAlchemyJobStore(url=db_url)
    }

    scheduler = BackgroundScheduler(jobstores=jobstores)
    scheduler.start()
    return scheduler