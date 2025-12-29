import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.movie_repository import MovieRepository
from app.schemas.schemas import MovieCreate, RatingCreate

logger = logging.getLogger(name)


class MovieService:
    def init(self, db: Session):
        self.repo = MovieRepository(db)

    def _attach_rating_stats(self, movie):
        if movie:
            try:
                avg, count = self.repo.get_rating_stats(movie.id)
                movie.average_rating = avg if avg else 0
                movie.ratings_count = count
            except Exception as e:
                logger.error(f"Error attaching rating stats for movie_id {movie.id}: {str(e)}", exc_info=True)
        return movie

    def get_all_movies(self, page: int, page_size: int, title: str, year: int, genre: str):
        logger.info(f"Fetching movies: page={page}, size={page_size}, filter_title='{title}'")

        try:
            skip = (page - 1) * page_size
            movies = self.repo.get_movies(skip, page_size, title, year, genre)
            total = self.repo.count_movies()

            for m in movies:
                self._attach_rating_stats(m)

            logger.info(f"Successfully retrieved {len(movies)} movies out of {total}")
            return {"items": movies, "total": total, "page": page, "page_size": page_size}
        except Exception as e:
            logger.error("Failed to retrieve movie list from database", exc_info=True)
            raise e

    def get_movie_detail(self, movie_id: int):
        logger.info(f"Detail request for movie_id: {movie_id}")

        movie = self.repo.get_movie_by_id(movie_id)
        if not movie:
            logger.warning(f"Movie with id {movie_id} not found in database")
            raise HTTPException(status_code=404, detail="Movie not found")

        return self._attach_rating_stats(movie)

    def create_new_movie(self, movie_data: MovieCreate):
        logger.info(f"Attempting to create a new movie: {movie_data.title}")
        try:
            new_movie = self.repo.create_movie(movie_data)
            logger.info(f"Movie created successfully with ID: {new_movie.id}")
            return new_movie
        except Exception as e:
            logger.error(f"Failed to create movie: {movie_data.title}", exc_info=True)
            raise e

    def add_rating_to_movie(self, movie_id: int, rating: RatingCreate):
        logger.info(f"User adding rating {rating.score} to movie_id {movie_id}")

        try:
            if rating.score < 1 or rating.score > 10:
                logger.warning(f"Invalid rating score attempted: {rating.score}")
                raise ValueError("Score must be between 1 and 10")

            new_rating = self.repo.add_rating(movie_id, rating.score)
            logger.info(f"Rating {rating.score} saved for movie {movie_id}")
            return new_rating
        except Exception as e:
            logger.error(f"Error adding rating to movie {movie_id}", exc_info=True)
            raise e