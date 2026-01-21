from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schema import UserCreate, UserResponse , UserUpadte
from app.db.session import get_db
from app.services.auth import sign_up, login, get_all_user, get_user_by_id, update_user, delete_user
from app.core.jwt import get_current_user
from app.services.auth import change_password
from app.schemas.schema import PasswordChange

router = APIRouter(prefix="/auth", tags=["Auth"])

# Signup endpoint
@router.post("/signup", response_model=UserResponse)
def signup_route(user: UserCreate, db: Session = Depends(get_db)):
    return sign_up(db, user)

# Login endpoint
@router.post("/login")
def login_route(user: UserCreate, db: Session = Depends(get_db)):
    return login(db, user.email, user.password)

@router.get("/",response_model=list[UserResponse])
def list_users(db:Session = Depends(get_db),
        current_user:int= Depends(get_current_user)):
    return get_all_user(db)

@router.get("/user_id/{user_id}",response_model=UserResponse)
def get_user(user_id:int , db:Session = Depends(get_db), current_user:int= Depends(get_current_user)):
    return get_user_by_id(db,user_id)

@router.put("/user_id/{user_id}",response_model=UserResponse)
def update_user_route(user_id:int, data:UserUpadte , db:Session = Depends(get_db), current_user:int= Depends(get_current_user)):
    return update_user(db,user_id,data)

@router.delete("/user_id/{user_id}")
def delete_user_route(user_id:int , db:Session = Depends(get_db), current_user:int= Depends(get_current_user)):
    return delete_user(db,user_id)

@router.put("/change-password")
def change_password_route(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return change_password(db, current_user, data.old_password, data.new_password)