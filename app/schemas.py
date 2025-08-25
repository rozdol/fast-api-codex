from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    phone_number: str
    notify_email: bool = True
    notify_sms: bool = False
    notify_whatsapp: bool = False
    notify_telegram: bool = False


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    is_verified_email: bool
    is_verified_phone: bool


class OfferBase(BaseModel):
    title: str
    description: str
    referral_link: Optional[str] = None
    promo_code: Optional[str] = None
    expires_at: datetime


class OfferCreate(OfferBase):
    pass


class OfferRead(OfferBase):
    id: int


class LikedOfferRead(BaseModel):
    offer: OfferRead
    liked_at: datetime
