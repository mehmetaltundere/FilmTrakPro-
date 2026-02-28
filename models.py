from dataclasses import dataclass

@dataclass
class Movie:
    # [EN] Core data model for a movie entity
    # [TR] Film varlığı için temel veri modeli
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
