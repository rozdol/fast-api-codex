# Offer Swipe Application

A sample project demonstrating a Tinder-like experience for discount and promotion offers.
The backend is built with **FastAPI** and the frontend uses **React** with the Ionic
framework, optimised for mobile devices.

## Features
- Swipe left to dismiss an offer or right to like it.
- Each offer can contain a referral link or promo code and shows a countdown
  timer until expiration.
- Users must register with email and phone number; accounts become active only
  after both are verified.
- Users choose how to be notified about expiring offers: email, SMS, WhatsApp
  or Telegram.
- Liked offers are stored in the user profile for later reference.
- OAuth placeholders for Google and Apple sign-in are included.

## Backend

```bash
uvicorn app.main:app --reload
```

The backend uses SQLite via `sqlmodel` for simplicity.

## Frontend

The `frontend/` folder contains a minimal React + Ionic setup using Vite and
`react-tinder-card` for the swipe experience.

```bash
cd frontend
npm install
npm run dev
```

## Database Models

See `app/models.py` for the SQLModel definitions of `User`, `Offer` and
`LikedOffer` tables.
