from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.movie_service import MovieService
from app.schemas.schemas import MovieResponse, MovieCreate, RatingCreate
from typing import Optional

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])

@router.get("/", response_model=dict) # API 1 & 2
def get_movies(
    page: int = 1,
    page_size: int = 10,
    title: Optional[str] = None,
    release_year: Optional[int] = None,
    genre: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    result = service.get_all_movies(page, page_size, title, release_year, genre)
    return {"status": "success", "data": result}

@router.get("/{movie_id}", response_model=dict) # API 3
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    movie = service.get_movie_detail(movie_id)
    return {"status": "success", "data": movie}