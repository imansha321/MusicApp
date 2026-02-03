from fastapi import FastAPI
from database import engine
from models.base import Base
from routes.auth import router as auth_router


app = FastAPI()

app.include_router(auth_router, prefix="/auth")


@app.post("/")
async def read_root():
    return {"Music API": "Welcome to the Music API!"}
    


Base.metadata.create_all(bind=engine)