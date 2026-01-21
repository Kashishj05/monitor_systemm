from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.role_db import Role
from app.schemas.role_schema import RoleResponse

# ✅ Only fetch roles
def get_roles(db: Session):
    return db.query(Role).all()

def get_role_by_name(db: Session, name: str) -> Role:
    role = db.query(Role).filter(Role.name == name).first()
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{name}' not found")
    return role

def get_role_by_id(db: Session, role_id: int) -> Role:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
