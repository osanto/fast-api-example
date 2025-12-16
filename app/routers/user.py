from fastapi import status, HTTPException, Depends, APIRouter
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from psycopg2.errors import UniqueViolation
from .. import models, schemas, utils
from .. database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,  db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)

    try:
        db.commit()
    except (IntegrityError, DBAPIError) as e:
        db.rollback()

        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        raise 

    db.refresh(new_user)
    return new_user

