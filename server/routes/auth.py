import uuid
import bcrypt
from fastapi import Depends, HTTPException , APIRouter
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import UserLogin
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/signup", status_code=201)
async def signup_user(user: UserCreate , db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="Email already registered") 
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(16))
    user_db = User(id = str(uuid.uuid4()), name=user.name, email=user.email, password=hashed_password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db


@router.post("/login")
async def login_user(user: UserLogin , db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid email or password") 
    
    if not bcrypt.checkpw(user.password.encode('utf-8'), user_db.password):
        raise HTTPException(status_code=400, detail="Invalid email or password") 
    
    return {"message": "Login successful"}