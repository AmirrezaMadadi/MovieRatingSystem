import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.movie_service import MovieService
from app.schemas.schemas import MovieResponse, MovieCreate, RatingCreate
from typing import Optional, List, Any, Dict

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])

@router.get("/") 
def get_movies(
    page: int = 1,
    page_size: int = 10,
    title: Optional[str] = None,
    release_year: Optional[int] = None,
    genre: Optional[str] = None,
    db: Session = Depends(get_db)
):
    logger.info(f"Incoming GET request to /movies | Filters: title={title}, year={release_year}, genre={genre}, page={page}")
    
    service = MovieService(db)
    result = service.get_all_movies(page, page_size, title, release_year, genre)
    
    logger.info(f"Successfully returned movie list for page {page}")
    return {"status": "success", "data": result}

@router.get("/{movie_id}") 
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    logger.info(f"Incoming GET request for movie details | movie_id: {movie_id}")
    
    service = MovieService(db)
    movie = service.get_movie_detail(movie_id)
    
    logger.info(f"Successfully retrieved details for movie_id: {movie_id}")
    return {"status": "success", "data": MovieResponse.model_validate(movie)}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    logger.info(f"Incoming POST request to create movie: {movie.title}")
    
    service = MovieService(db)
    new_movie = service.create_new_movie(movie)
    
    logger.info(f"New movie created successfully via API | ID: {new_movie.id}")
    return {"status": "success", "data": MovieResponse.model_validate(new_movie)}

@router.post("/{movie_id}/ratings", status_code=status.HTTP_201_CREATED)
def rate_movie(movie_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    logger.info(f"Incoming POST request to rate movie_id {movie_id} with score {rating.score}")
    
    service = MovieService(db)
    result = service.add_rating_to_movie(movie_id, rating)
    
    logger.info(f"Rating submitted successfully for movie_id {movie_id}")
    return {"status": "success", "data": {"rating_id": result.id, "score": result.score}}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    service = MovieService(db)
    new_movie = service.create_new_movie(movie)
    return {"status": "success", "data": MovieResponse.model_validate(new_movie)}

@router.put("/{movie_id}")
def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    service = MovieService(db)
    updated = service.update_existing_movie(movie_id, movie)
    return {"status": "success", "data": MovieResponse.model_validate(updated)}

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    service.delete_movie(movie_id)
    return

@router.post("/{movie_id}/ratings", status_code=status.HTTP_201_CREATED)
def rate_movie(movie_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    service = MovieService(db)
    new_rating = service.add_rating_to_movie(movie_id, rating)
    return {"status": "success", "data": {"rating_id": new_rating.id, "score": new_rating.score}}