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
from app.models.user import User
from app.core.role_core import require_roles
from fastapi import HTTPException, status

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# only admin or manager can post the task 
@router.post("/",response_model=TaskResponse)
def post_task(data:TaskCreate, db:Session = Depends(get_db),current_user: User = Depends(require_roles(["admin","manager"]))):
    
    task = create_task(db, data,current_user.id)
    return task

# only admin and manager 
@router.get("/",response_model=List[TaskResponse])
def fetch_all_task(db:Session =Depends(get_db), current_user:User= Depends(require_roles(["admin","manager"]))):
    return get_all_tasks(db)

# get my task all can access
@router.get("/my",response_model=List[TaskResponse])
def fetch_my_tasks(db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return get_users_task(db, current_user.id)

# get single task only admin and manager     # 
@router.get("/{task_id}", response_model = TaskResponse)
def fetch_task(task_id :int, db:Session=Depends(get_db),
               current_user:User= Depends(get_current_user)):
     task = get_task_by_id(db, task_id)
     if current_user.role not in ["admin", "manager"] and task.assigned_to_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this task"
        )
     return task

# update a task only admin and user doubt
@router.put("/{task_id}",response_model=TaskResponse)
def put_task(task_id:int, data:TaskUpdate, db:Session=Depends(get_db),current_user:User=Depends(require_roles(["admin"]))):
    return update_task(db, data, task_id, current_user)

# only owner manager and admin  doubt
@router.patch("/{task_id}/status",response_model=TaskResponse)
def patch_task_status(task_id:int,status:TaskStatus, db:Session=Depends(get_db), current_user:User= Depends(get_current_user)):
    return update_status(db, task_id, status, current_user)


# manager and admin only
@router.patch("/{task_id}/assign",response_model=TaskResponse)
def patch_task_assign(task_id:int ,new_user_id:int=Query(...), db:Session= Depends(get_db),current_user: User = Depends(require_roles(["admin","manager"]))):
    return reassign_task(db , task_id,new_user_id, current_user.id)


# manager and admin only
@router.delete("/{task_id}")
def delete_task_api(task_id:int, db:Session=Depends(get_db),
                    current_user:User= Depends(require_roles(["admin","manager"]))):
    return delete_task(db,task_id,current_user)

# filter only admin and manager
@router.get("/filter",response_model=TaskListResponse)
def filter_tasks(
    status:Optional[str]= None,
    priority:Optional[str]= None,
    assigned_to_id: Optional[int] = None,
    sort_by: str = "created_at",
    order: str = "desc",
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user:User=Depends(require_roles(["admin","manager"]))
):
    return get_filtered_task(db, status= status, priority=priority,assigned_to_id=assigned_to_id, sort_by=sort_by, order=order, page=page, page_size=page_size)
