# app/models.py
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base 

Base = declarative_base()

class Suggestion(Base):
    __tablename__ = "suggestion"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=False, index=True, nullable=False)
    suggestion = Column(String, unique=False, index=False, nullable=False)

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, unique=False, index=False, nullable=False)
