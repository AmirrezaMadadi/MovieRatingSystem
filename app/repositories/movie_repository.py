from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Movie, Genre, Rating, movie_genres

class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_movies(self, skip: int = 0, limit: int = 10, title: str = None, year: int = None, genre_name: str = None):
        query = self.db.query(Movie)
        
        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if year:
            query = query.filter(Movie.release_year == year)
        if genre_name:
            query = query.join(Movie.genres).filter(Genre.name == genre_name)
            
        return query.offset(skip).limit(limit).all()

    def get_movie_by_id(self, movie_id: int):
        return self.db.query(Movie).filter(Movie.id == movie_id).first()
        
    def count_movies(self):
        return self.db.query(Movie).count()

    def get_rating_stats(self, movie_id: int):
        result = self.db.query(
            func.avg(Rating.score),
            func.count(Rating.id)
        ).filter(Rating.movie_id == movie_id).first()
        return result