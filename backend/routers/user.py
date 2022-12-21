from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy import exc
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from typing import List


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist",
        )

    return user


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    old_user = db.query(models.User).filter(models.User.id == user.id).first()

    if old_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with such id already exists",
        )

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/{id}", response_model=schemas.UserOut)
def update_user(
    id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)
):

    user_query = db.query(models.User).filter(models.User.id == user.id)

    user = user_query.first()

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist",
        )

    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)

    if user_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist",
        )

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
