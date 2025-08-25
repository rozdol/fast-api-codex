from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """FastAPI dependency that provides a database session."""
    with Session(engine) as session:
        yield session
