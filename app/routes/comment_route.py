from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.jwt import get_current_user
from app.schemas.comment_schema import CommentCreate, CommentResponse, CommentUpdate
from app.services.comment_service import (
    create_comment,
    get_comment_by_task,
      update_comment, delete_comment
)
from app.models.user import User

router = APIRouter(
    prefix="/tasks/{task_id}/comments",
    tags=["Comments"]
)


@router.post("/",response_model=CommentResponse)
def add_comment(
    task_id:int,
    data:CommentCreate,
    db:Session=Depends(get_db),
    current_user :User= Depends(get_current_user)
):
    return create_comment(
        db=db,
        task_id=task_id,
        data= data.content,
        current_user=current_user
    )

@router.get("/",response_model=List[CommentResponse])
def list_comments(
    task_id:int,
    db:Session= Depends(get_db),
):
    return get_comment_by_task(db, task_id)

@router.put("/{comment_id}", response_model=CommentResponse)
def edit_comment(
    task_id: int,
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_comment(db, comment_id, data, task_id, current_user)


@router.delete("/{comment_id}")
def remove_comment(
    task_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_comment(db, comment_id,task_id, current_user)
