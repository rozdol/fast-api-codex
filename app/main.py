from fastapi import FastAPI

from .auth import router as auth_router
from .database import init_db
from .routers.offers import router as offers_router
from .routers.users import router as users_router

app = FastAPI(title="Offer Swipe API")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(offers_router)
