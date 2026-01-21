from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services.role_service import get_roles, get_role_by_id, get_role_by_name
from app.schemas.role_schema import RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=List[RoleResponse])
def fetch_all_roles(db: Session = Depends(get_db)):
    return get_roles(db)

@router.get("/id/{role_id}", response_model=RoleResponse)
def fetch_role_by_id(role_id: int, db: Session = Depends(get_db)):
    return get_role_by_id(db, role_id)

@router.get("/name/{role_name}", response_model=RoleResponse)
def fetch_role_by_name(role_name: str, db: Session = Depends(get_db)):
    return get_role_by_name(db, role_name)
