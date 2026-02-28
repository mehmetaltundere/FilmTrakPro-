from dataclasses import dataclass

@dataclass
class Movie:
    imdb_id: str
    title: str
    year: str
    poster_url: str
    genre: str
    director: str
    actors: str
    rating: str
    plot: str
    runtime: str = "0 min"
