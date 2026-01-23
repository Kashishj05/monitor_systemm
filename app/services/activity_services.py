# app/services/activity_service.py
from sqlalchemy.orm import Session
from app.models.activity_model import ActivityLog
from app.models.user import User

def log_activity(db: Session, actor_id: int, action: str,entity_type:str, entity_id: int , description:str | None = None):

    log = ActivityLog(  actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description)
    
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_all_tasks(db:Session):
    return db.query(ActivityLog).order_by(ActivityLog.created_at.desc()).all()


def get_activities_for_task(db: Session, task_id: int):
   return db.query(ActivityLog).filter(ActivityLog.entity_type == "TASK",ActivityLog.entity_id == task_id).order_by(ActivityLog.created_at.desc()).all()

def get_activities_for_user(db: Session,user_id: int):
 return (db.query(ActivityLog).filter(ActivityLog.actor_id == user_id).order_by(ActivityLog.created_at.desc())).all()
