from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, LoginSchema, TokenSchema
from app.db.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,  # ✅ ADD THIS
)

router = APIRouter()  

@router.post("/signup", response_model=UserResponse)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(payload.password)
    user = User(email=payload.email, name=payload.name, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenSchema)
def login(form_data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
