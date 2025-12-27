from fastapi import FastAPI
from app.db.database import Base, engine
from app.controller import movie_controller
from app.core.logging_config import setup_logging

Base.metadata.create_all(bind=engine)
setup_logging()
app = FastAPI(title="Movie Rating System")

app.include_router(movie_controller.router)

@app.get("/")
def root():
    return {"message": "Welcome to Movie Rating API"}