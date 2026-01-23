# app/routes/activity_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.activity_schema import ActivityLogResponse
from app.services.activity_services import get_activities_for_user, get_all_tasks,get_activities_for_task
from app.models.user import User
from app.core.role_core import require_roles

router = APIRouter(prefix="/activities", tags=["Activity Logs"])

@router.get("/",response_model=List[ActivityLogResponse])
def fetch_all_logs(db:Session= Depends(get_db),current_user :User= Depends(require_roles(["admin"]))):
    return get_all_tasks(db)

@router.get("/task/{task_id}",response_model=List[ActivityLogResponse])
def fetch_task_activity_logs(task_id:int, db:Session = Depends(get_db),current_user:User= Depends(require_roles(["admin","manager"]))):
    return get_activities_for_task(db, task_id)


@router.get("/user/{user_id}",response_model=List[ActivityLogResponse])
def fetch_all_user_activity(user_id:int, db:Session= Depends(get_db),current_user:User = Depends(require_roles(["admin"]))):
    return get_activities_for_user(db, user_id)