from models.base import Base
from sqlalchemy import Column, TEXT , VARCHAR, LargeBinary

class User(Base):
    __tablename__ = "users"

    id = Column(TEXT, primary_key=True, index=True)
    name = Column(VARCHAR(10))
    email = Column(VARCHAR(50), unique=True, index=True)
    password = Column(LargeBinary)