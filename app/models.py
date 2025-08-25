from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    phone_number: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_verified_email: bool = Field(default=False)
    is_verified_phone: bool = Field(default=False)
    notify_email: bool = Field(default=True)
    notify_sms: bool = Field(default=False)
    notify_whatsapp: bool = Field(default=False)
    notify_telegram: bool = Field(default=False)

    liked_offers: Mapped[list[LikedOffer]] = Relationship(back_populates="user")


class Offer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    referral_link: Optional[str] = None
    promo_code: Optional[str] = None
    expires_at: datetime

    liked_by: Mapped[list[LikedOffer]] = Relationship(back_populates="offer")


class LikedOffer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    offer_id: int = Field(foreign_key="offer.id")
    liked_at: datetime = Field(default_factory=datetime.utcnow)

    user: Mapped[User] = Relationship(back_populates="liked_offers")
    offer: Mapped[Offer] = Relationship(back_populates="liked_by")
