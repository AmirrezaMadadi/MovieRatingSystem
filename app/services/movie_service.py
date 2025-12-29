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

    def create_new_movie(self, movie_in: MovieCreate):
        genres = self.repo.get_genres_by_ids(movie_in.genres)
        if len(genres) != len(movie_in.genres):
            raise HTTPException(status_code=422, detail="Invalid genre IDs")

        movie_data = movie_in.dict(exclude={"genres"})
        return self.repo.create_movie(movie_data, genres)

    def update_existing_movie(self, movie_id: int, movie_in: MovieCreate):
        movie = self.repo.get_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        genres = self.repo.get_genres_by_ids(movie_in.genres)
        movie_data = movie_in.dict(exclude={"genres"})

        updated_movie = self.repo.update_movie(movie, movie_data, genres)
        return self._attach_rating_stats(updated_movie)

    def delete_movie(self, movie_id: int):
        movie = self.repo.get_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        self.repo.delete_movie(movie)

    def add_rating_to_movie(self, movie_id: int, rating_in: RatingCreate):
        if not (1 <= rating_in.score <= 10):
            raise HTTPException(status_code=422, detail="Score must be between 1 and 10")

        movie = self.repo.get_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        return self.repo.add_rating(movie_id, rating_in.score)