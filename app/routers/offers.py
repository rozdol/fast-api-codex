from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .. import models, schemas
from ..database import get_session

router = APIRouter(prefix="/offers", tags=["offers"])


@router.post("/", response_model=schemas.OfferRead)
def create_offer(offer_in: schemas.OfferCreate, session: Session = Depends(get_session)):
    offer = models.Offer(**offer_in.model_dump())
    session.add(offer)
    session.commit()
    session.refresh(offer)
    return offer


@router.get("/next", response_model=schemas.OfferRead)
def get_next_offer(session: Session = Depends(get_session)):
    offer = session.exec(select(models.Offer).order_by(models.Offer.expires_at)).first()
    if not offer:
        raise HTTPException(status_code=404, detail="No offers available")
    return offer


@router.post("/{offer_id}/like", response_model=schemas.LikedOfferRead)
def like_offer(offer_id: int, user_id: int, session: Session = Depends(get_session)):
    offer = session.get(models.Offer, offer_id)
    user = session.get(models.User, user_id)
    if not offer or not user:
        raise HTTPException(status_code=404, detail="Offer or user not found")
    liked = models.LikedOffer(user_id=user_id, offer_id=offer_id)
    session.add(liked)
    session.commit()
    session.refresh(liked)
    return schemas.LikedOfferRead(offer=offer, liked_at=liked.liked_at)


@router.get("/liked/{user_id}", response_model=list[schemas.LikedOfferRead])
def liked_offers(user_id: int, session: Session = Depends(get_session)):
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        schemas.LikedOfferRead(offer=lo.offer, liked_at=lo.liked_at)
        for lo in user.liked_offers
    ]
