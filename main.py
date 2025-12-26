from fastapi import FastAPI
from app.db.database import Base, engine
from app.controller import movie_controller

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Rating System")

app.include_router(movie_controller.router)

@app.get("/")
def root():
    return {"message": "Welcome to Movie Rating API"}