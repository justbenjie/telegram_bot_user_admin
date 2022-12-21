from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy import exc
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from typing import List


router = APIRouter(prefix="/admins", tags=["Admins"])


@router.get("/", response_model=List[schemas.AdminOut])
def get_admins(db: Session = Depends(get_db)):

    admins = db.query(models.Admin).all()

    return admins


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminOut)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):

    old_admin = (
        db.query(models.Admin).filter(models.Admin.user_id == admin.user_id).first()
    )

    if old_admin is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Admin with such id already exists",
        )

    new_admin = models.Admin(**admin.dict())

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int, db: Session = Depends(get_db)):

    admin_query = db.query(models.Admin).filter(models.Admin.user_id == id)

    if admin_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id: {id} doesn't exist",
        )

    admin_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
