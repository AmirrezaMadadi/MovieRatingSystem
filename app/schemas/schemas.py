from pydantic import BaseModel
from typing import List, Optional

class GenreBase(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class DirectorBase(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

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
    director: DirectorBase
    genres: List[GenreBase]
    average_rating: Optional[float] = 0.0
    ratings_count: Optional[int] = 0

    class Config:
        orm_mode = True