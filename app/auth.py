"""Authentication utilities and routes."""

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlmodel import Session, select

from . import models, schemas
from .database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register", response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, session: Session = Depends(get_session)):
    if session.exec(select(models.User).where(models.User.email == user_in.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        email=user_in.email,
        phone_number=user_in.phone_number,
        hashed_password=get_password_hash(user_in.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    # TODO: send email/phone verification
    return user


@router.post("/login")
def login():
    """Placeholder for user login."""
    return {"message": "Implement login"}


# OAuth placeholders for Google and Apple
@router.get("/oauth/{provider}")
def oauth_login(provider: str):
    """Redirect user to external OAuth provider."""
    return {"message": f"Redirecting to {provider} OAuth"}


@router.get("/oauth/{provider}/callback")
def oauth_callback(provider: str):
    """Handle OAuth callback."""
    return {"message": f"Handle {provider} OAuth callback"}
