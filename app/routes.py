import uuid
from . import models
from sqlalchemy.future import select
from pydantic import BaseModel,EmailStr
from .database import get_session,engine
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter,Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

class SuggestionValidator(BaseModel):
    email: EmailStr
    suggestion: str

class UserValidator(BaseModel):
    name: str
    email: EmailStr

@router.post('/')
async def server_check(request : Request):
    json_payload = request.json()
    return{
        "message" : f"{json_payload.message}We are live !"
    }

@router.post('/submit_suggestion')
async def submit_suggestion(suggestion_data : SuggestionValidator,session : AsyncSession = Depends(get_session)):
    new_suggestion = models.Suggestion(
        id=f"sgn{str(uuid.uuid4())}"[0:10],
        email=suggestion_data.email,
        suggestion=suggestion_data.suggestion
    )
    session.add(new_suggestion)
    await session.commit()
    await session.refresh(new_suggestion)
    return {
    "message" : "Your suggestion has been submitted successfully \U00002705"
    }

@router.post('/enroll')
async def enroll(user_data : UserValidator,session : AsyncSession = Depends(get_session)):
    new_user = models.User(
        id=f"usr{str(uuid.uuid4())}"[0:10],
        email=user_data.email,
        name=user_data.name
    )
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return {
        "message" : "You have been successfully enrolled to SubbedIn \U00002705"
    }
    except IntegrityError:
        await session.rollback()
        return {
        "message" : "A user is already enrolled with the email address !"
        }