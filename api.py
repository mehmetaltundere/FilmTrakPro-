import http.client
import json
import urllib.request
import urllib.parse
import webbrowser
import os
from typing import Optional
from models import Movie

class MovieAPI:
    def __init__(self, api_key: Optional[str] = None):
        # [EN] Check parameter first, then environment variable, finally default fallback
        # [TR] Önce parametreye, sonra ortam değişkenine, en son varsayılana bak
        self.api_key = api_key or os.getenv("OMDB_API_KEY") or "b20bde7"
        self.base_url = "www.omdbapi.com"

    def open_imdb_page(self, imdb_id: str):
        # [EN] Open movie detail page on IMDb
        # [TR] IMDb üzerinde film detay sayfasını aç
        if imdb_id:
            url = f"https://www.imdb.com/title/{imdb_id}/"
            webbrowser.open(url)

    def search_movie(self, title: str) -> Optional[Movie]:
        # [EN] Search for a movie by title and return a Movie object
        # [TR] Film adına göre arama yap ve bir Movie nesnesi döndür
        try:
            # [EN] Sanitize and prepare the search query
            # [TR] Arama terimini temizle ve hazırla
            clean_title = title.strip().replace(' ', '+')
            conn = http.client.HTTPSConnection(self.base_url)
            query = f"/?apikey={self.api_key}&t={urllib.parse.quote(clean_title)}"
            conn.request("GET", query)
            res = conn.getresponse()
            data = res.read()
            f = json.loads(data)
            
            if f.get("Response") == "True":
                return Movie(
                    imdb_id=f.get("imdbID", ""),
                    title=f.get("Title", ""),
                    year=f.get("Year", ""),
                    poster_url=f.get("Poster", ""),
                    genre=f.get("Genre", ""),
                    director=f.get("Director", ""),
                    actors=f.get("Actors", ""),
                    rating=f.get("imdbRating", ""),
                    plot=f.get("Plot", ""),
                    runtime=f.get("Runtime", "0 min")
                )
        except Exception as e:
            print(f"API Error: {e}")
        return None

    def get_poster_data(self, url: str) -> Optional[bytes]:
        # [EN] Download movie poster image data
        # [TR] Film afiş görsel verisini indir
        if not url or url == "N/A":
            return None
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except Exception as e:
            print(f"Poster Error: {e}")
            return None
