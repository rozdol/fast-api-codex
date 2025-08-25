from fastapi import APIRouter, Depends
from sqlmodel import Session

from .. import models, schemas
from ..database import get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    return session.get(models.User, user_id)


@router.put("/{user_id}", response_model=schemas.UserRead)
def update_user_settings(user_id: int, user_in: schemas.UserBase, session: Session = Depends(get_session)):
    user = session.get(models.User, user_id)
    for field, value in user_in.model_dump().items():
        setattr(user, field, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
