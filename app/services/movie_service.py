from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.movie_repository import MovieRepository
from app.schemas.schemas import MovieCreate, RatingCreate

class MovieService:
    def __init__(self, db: Session):
        self.repo = MovieRepository(db)

    def _attach_rating_stats(self, movie):
        if movie:
            avg, count = self.repo.get_rating_stats(movie.id)
            movie.average_rating = avg if avg else 0
            movie.ratings_count = count
        return movie

    def get_all_movies(self, page: int, page_size: int, title: str, year: int, genre: str):
        skip = (page - 1) * page_size
        movies = self.repo.get_movies(skip, page_size, title, year, genre)
        total = self.repo.count_movies()
        
        for m in movies:
            self._attach_rating_stats(m)
            
        return {"items": movies, "total": total, "page": page, "page_size": page_size}

    def get_movie_detail(self, movie_id: int):
        movie = self.repo.get_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return self._attach_rating_stats(movie)