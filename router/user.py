from typing import List
from fastapi import APIRouter, Depends
from schemas.schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

# Create user
@router.post("/", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)

# Read all user
@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db), 
                  current_user: UserBase = Depends(get_current_user)):
    return db_user.get_all_users(db)

# Read single user
@router.get("/{id}/", response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db), 
                  current_user: UserBase = Depends(get_current_user)):
    return db_user.get_user(db, id)

# Update user
@router.put("/{id}/update/", response_model=UserDisplay)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db), 
                  current_user: UserBase = Depends(get_current_user)):
    return db_user.update_user(db, id, request)

# Delete user
@router.delete("/{id}/delete/")
def delete_user(id: int, db: Session = Depends(get_db), 
                  current_user: UserBase = Depends(get_current_user)):
    return db_user.delete_user(db, id)