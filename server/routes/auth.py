import uuid
import bcrypt
from fastapi import Depends, HTTPException , APIRouter
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import UserLogin
from database import get_db
from sqlalchemy.orm import Session
import jwt 
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

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

    token = jwt.encode({"user_id": user_db.id}, SECRET_KEY, algorithm="HS256")

    return {"username": user_db.name, "email": user_db.email, "id": user_db.id, "token": token}


@router.post("/login")
async def login_user(user: UserLogin , db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid email or password") 
    
    if not bcrypt.checkpw(user.password.encode('utf-8'), user_db.password):
        raise HTTPException(status_code=400, detail="Invalid email or password") 
    
    token = jwt.encode({"user_id": user_db.id}, SECRET_KEY, algorithm="HS256")

    return {"username": user_db.name, "email": user_db.email, "id": user_db.id, "token": token}