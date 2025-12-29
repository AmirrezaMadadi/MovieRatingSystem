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

    def create_movie(self, movie_data, genres: list[Genre]):
        db_movie = Movie(**movie_data)
        db_movie.genres = genres
        self.db.add(db_movie)
        self.db.commit()
        self.db.refresh(db_movie)
        return db_movie

    def update_movie(self, movie: Movie, update_data: dict, new_genres: list[Genre] = None):
        for key, value in update_data.items():
            setattr(movie, key, value)

        if new_genres is not None:
            movie.genres = new_genres

        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete_movie(self, movie: Movie):
        self.db.delete(movie)
        self.db.commit()

    def add_rating(self, movie_id: int, score: int):
        rating = Rating(movie_id=movie_id, score=score)
        self.db.add(rating)
        self.db.commit()
        return rating

    def get_genres_by_ids(self, genre_ids: list[int]):
        return self.db.query(Genre).filter(Genre.id.in_(genre_ids)).all()