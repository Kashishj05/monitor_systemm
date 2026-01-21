from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.services.task import (
    create_task, get_all_tasks, get_task_by_id,
    get_users_task, update_task, update_status,
    reassign_task, delete_task, get_filtered_task
)
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskStatus, TaskResponse, TaskListResponse
from app.core.jwt import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/",response_model=TaskResponse)
def post_task(data:TaskCreate, db:Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    
    task = create_task(db, data,current_user)
    return task

@router.get("/",response_model=List[TaskResponse])
def fetch_all_task(db:Session =Depends(get_db)):
    return get_all_tasks(db)

@router.get("/{task_id}", response_model = TaskResponse)
def fetch_task(task_id :int, db:Session=Depends(get_db)):
    return get_task_by_id(db,task_id)

@router.get("/my",response_model=List[TaskResponse])
def fetch_my_tasks(db:Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    return get_users_task(db, current_user)

@router.put("/{task_id}",response_model=TaskResponse)
def put_task(task_id:int, data:TaskUpdate, db:Session=Depends(get_db)):
    return update_task(db, data, task_id)

@router.patch("/{task_id}/status",response_model=TaskResponse)
def patch_task_status(task_id:int,status:TaskStatus, db:Session=Depends(get_db)):
    return update_status(db, task_id, status)

@router.patch("/{task_id}/assign",response_model=TaskResponse)
def patch_task_assign(task_id:int ,new_user_id:int=Query(...), db:Session= Depends(get_db),current_user: int = Depends(get_current_user)):
    return reassign_task(db , task_id,new_user_id, current_user)

@router.delete("/{task_id}")
def delete_task_api(task_id:int, db:Session=Depends(get_db)):
    return delete_task(db,task_id)

@router.get("/filter",response_model=TaskListResponse)
def filter_tasks(
    status:Optional[str]= None,
    priority:Optional[str]= None,
    assigned_to_id: Optional[int] = None,
    sort_by: str = "created_at",
    order: str = "desc",
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return get_filtered_task(db, status= status, priority=priority,assigned_to_id=assigned_to_id, sort_by=sort_by, order=order, page=page, page_size=page_size)
