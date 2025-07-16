from typing import Dict, List

from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse

from src.models.movies import Movie, MovieCreate, MovieUpdate


movies: List[Movie] = []
movie_router = APIRouter()


@movie_router.get("", tags=("Movies",), status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(content=[movie.model_dump() for movie in movies], status_code=200)


@movie_router.get("/{id}", tags=("Movies",))
def get_movie(id: int = Path(gt=0)) -> Movie | Dict:
    movie = filter(lambda movie: movie.id == id, movies)
    # movie = [movie for movie in movies if movie.get("id") == id]
    movies_found: Movie = list(movie)

    if not movies_found: return JSONResponse(content={})

    return movies_found[0].model_dump()


@movie_router.get("/", tags=("Movies",))
def get_movie_by_category(category: str = Query(min_length=3, max_length=20)) -> List[Movie]:
    movies_filtered = filter(
        lambda movie: movie.category == category, movies
    )
    movies_found: Movie = list(movies_filtered)
    return [movie_found.model_dump() for movie_found in movies_found]


@movie_router.post("", tags=("Movies",), status_code=201, response_description="Movie created")
def create_movie(movie: MovieCreate) -> List[Movie]:
    # movies.append(movie.model_dump())
    movies.append(movie)
    return JSONResponse([movie.model_dump() for movie in movies], status_code=201)


@movie_router.put("/{id}", tags=("Movies",))
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
            break

    return [movie.model_dump() for movie in movies]


@movie_router.delete("/{id}", tags=("Movies",))
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
            break

    return [movie.model_dump() for movie in movies]
