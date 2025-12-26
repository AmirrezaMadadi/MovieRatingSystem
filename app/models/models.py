from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

movie_genres = Table(
    'movie_genres', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")

class Director(Base):
    __tablename__ = 'directors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    movies = relationship("Movie", back_populates="director")

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    release_year = Column(Integer)
    cast = Column(String)
    director_id = Column(Integer, ForeignKey('directors.id'))
    
    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")

class Rating(Base):
    __tablename__ = 'movie_ratings'
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete="CASCADE"))
    
    movie = relationship("Movie", back_populates="ratings")