# POST /tasks	Task create
# GET /tasks	All tasks
# GET /tasks/{id}	Task detail
# GET /tasks/my	Logged-in user tasks
# PUT /tasks/{id}	Update task
# PATCH /tasks/{id}/status	Update status
# PATCH /tasks/{id}/assign	Reassign
# DELETE /tasks/{id}	Delete

# pending
# GET /tasks?filters	Filtering
# GET /tasks/{id}/activity	Audit log



from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.task_db import Task
from app.schemas.task_schema import TaskCreate,TaskUpdate, TaskStatus
from app.models.user import User
from datetime import datetime
from typing import Optional

# Constants
DEFAULT_STATUS = "pending"
DEFAULT_PRIORITY = "medium"
ALLOWED_SORT_FIELDS = {"created_at", "title", "priority", "status", "due_date"}
MAX_PAGE_SIZE = 100

# POST /tasks	Task create
def create_task(db:Session, data:TaskCreate ,current_user:int)->Task:
   try:
    if not data.title:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="task title is required")
    
    if not data.assigned_to_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="assigned user id is required")
    
    assigned_user = db.query(User).filter(User.id == data.assigned_to_id).first()
    if not assigned_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="assigned user not found")

    new_task= Task(
        title= data.title,
        description= data.description,
        assigned_to_id= data.assigned_to_id,
        created_by_id =current_user,
        status=DEFAULT_STATUS,
        priority=data.priority or DEFAULT_PRIORITY,
        due_date= data.due_date,
        created_at = datetime.utcnow()
    )
   
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
   except Exception as e:
        raise HTTPException(status_code= 500, detail=f"Internal server error: {str(e)}")
    
    

# GET /tasks	All tasks
def get_all_tasks(db:Session):

    try:
        tasks=db.query(Task).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code= 500, detail=f"Internal server err:{str(e)}")
    

def get_task_by_id(db:Session, task_id:int):
    try:
        task= db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404,detail=f"task not found for id {task_id}")
        return task
    except Exception as e:
        raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")
    
# GET /tasks/my	Logged-in user tasks


def get_users_task(db:Session, assigned_to_id:int):
    try:
        tasks= db.query(Task).filter(Task.assigned_to_id == assigned_to_id).all()
        return tasks
    except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")

def update_task(db:Session, data:TaskUpdate, task_id:int):
    try:
        task = get_task_by_id(db,task_id)
        if not task:
             raise HTTPException(status_code=404,detail=f"task not found for id")
        
        update_data = data.dict(exclude_unset=True)

# setattr(object, attribute_name, value)
        for key, value  in update_data.items():
            setattr(task,key, value)

        db.commit()
        db.refresh(task)
        return task
    
    except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")
    
def update_status(db:Session, task_id:int , new_status:TaskStatus):
    try:
        task = get_task_by_id(db, task_id)
        if not task:
         raise HTTPException(status_code=404,detail=f"task not found for id")
    
        task.status = new_status.value

        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")



def reassign_task(db:Session,  task_id:int,new_user_id:int,current_user_id:int ):
        try:
            task= get_task_by_id(db, task_id)
            if not task:
                 raise HTTPException(status_code=404, detail="Task not found")
            
            new_user = db.query(User).filter(User.id == new_user_id).first()
            if not new_user:
                raise HTTPException(status_code=404, detail="user not found")
            
            if task.assigned_to_id == new_user_id:
                raise HTTPException(
            status_code=400,
            detail="Task is already assigned to this user"
        )
            if task.status == "completed":
                  raise HTTPException(
            status_code=400,
            detail="Completed task cannot be reassigned"
        )
            
            old_assignee = task.assigned_to_id
            task.assigned_to_id = new_user_id

            db.commit()
            db.refresh(task)

            return task


        except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")



# DELETE /tasks/{id}	Delete
def delete_task(db:Session, task_id:int):
    try:
        task= get_task_by_id(db,task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        return {"message":"task deleted successfully"}

    except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")


# GET /tasks?filters	Filtering


def get_filtered_task(db:Session,
                      status:Optional[str]=None,
                      priority:Optional[str]=None,
                      assigned_to_id:Optional[int]=None,
                      sort_by:str ="created_at",
                      order:str="desc",
                      page:int=1,
                      page_size:int=10):
    query = db.query(Task)
    # filter
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_to_id:
        query = query.filter(Task.assigned_to_id == assigned_to_id)

    # sorting
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    sort_column = getattr(Task, sort_by)
    query = query.order_by(
        sort_column.asc() if order == "asc" else sort_column.desc()
    )

    # pagination
    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE
    offset = (page - 1) * page_size
    total = query.count()
    tasks = query.offset(offset).limit(page_size).all()
    
    return {
        "tasks": tasks,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }