from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class GenreBase(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class DirectorBase(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class RatingCreate(BaseModel):
    score: int

class MovieBase(BaseModel):
    title: str
    release_year: int
    cast: str

class MovieCreate(MovieBase):
    director_id: int
    genres: List[int]  

class MovieResponse(MovieBase):
    id: int
    director_id: int
    director: DirectorBase
    genres: List[GenreBase]
    average_rating: float = 0.0
    ratings_count: int = 0

    model_config = ConfigDict(from_attributes=True)