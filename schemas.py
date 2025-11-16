from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Użytkownicy
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        from_attributes = True

# Zadania
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    class Config:
        from_attributes = True
