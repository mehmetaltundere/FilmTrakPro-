import sqlite3
from typing import List, Tuple, Optional
from datetime import datetime
from models import Movie

class DatabaseManager:
    def __init__(self, db_name: str = "filmtrak_pro.db"):
        self.db_name = db_name
        self._initialize_db()

    def _initialize_db(self):
        # [EN] Initialize database tables if they do not exist
        # [TR] Veritabanı tabloları mevcut değilse oluştur
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # [EN] Search History table
            # [TR] Arama Geçmişi tablosu
            cursor.execute("CREATE TABLE IF NOT EXISTS Gecmis(Anahtar TEXT, Tarih TEXT)")
            # [EN] Movies table (Library)
            # [TR] Filmler tablosu (Kitaplık)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Filmler(
                    imdbID TEXT PRIMARY KEY, 
                    Ad TEXT, 
                    Yil TEXT, 
                    Afis TEXT,
                    Tur TEXT,
                    Yonetmen TEXT,
                    IMDbPuan TEXT,
                    Ozellik TEXT,
                    Sure TEXT
                )
            """)
            # [EN] Comments table
            # [TR] Yorumlar tablosu
            cursor.execute("CREATE TABLE IF NOT EXISTS Yorumlar(imdbID TEXT, Yorum TEXT)")
            # [EN] Watched items table with ratings
            # [TR] İzlenenler tablosu (Puanlı)
            cursor.execute("CREATE TABLE IF NOT EXISTS Izlenenler(imdbID TEXT PRIMARY KEY, Puan INTEGER)")
            # [EN] Collections table
            # [TR] Koleksiyonlar tablosu
            cursor.execute("CREATE TABLE IF NOT EXISTS Koleksiyonlar(imdbID TEXT, ListeAdi TEXT)")
            conn.commit()

    def gecmis_ekle(self, anahtar: str):
        # [EN] Add a search term to the history
        # [TR] Arama terimini geçmişe ekle
        zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO Gecmis VALUES(?,?)", [anahtar, zaman])
            conn.commit()

    def gecmis_getir(self) -> List[Tuple[str, str]]:
        # [EN] Retrieve recent search history
        # [TR] Son arama geçmişini getir
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("SELECT Anahtar, Tarih FROM Gecmis ORDER BY Tarih DESC LIMIT 50").fetchall()

    def film_kaydet(self, movie: Movie):
        # [EN] Save or update a movie in the library
        # [TR] Filmi kütüphaneye kaydet veya güncelle
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO Filmler VALUES(?,?,?,?,?,?,?,?,?)
            """, [
                movie.imdb_id, movie.title, movie.year, movie.poster_url, 
                movie.genre, movie.director, movie.rating, movie.plot, movie.runtime
            ])
            conn.commit()

    def izlenenlere_ekle(self, imdb_id: str, puan: int = 0):
        # [EN] Mark a movie as watched and assign a rating
        # [TR] Filmi izlenenlere ekle ve puan ver
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT OR REPLACE INTO Izlenenler VALUES(?,?)", [imdb_id, puan])
            conn.commit()

    def koleksiyon_ekle(self, imdb_id: str, liste_adi: str):
        # [EN] Add a movie to a specific collection/list
        # [TR] Filmi belirli bir koleksiyona/listeye ekle
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO Koleksiyonlar VALUES(?,?)", [imdb_id, liste_adi])
            conn.commit()

    def istatistik_getir(self):
        # [EN] Calculate and return application statistics
        # [TR] Uygulama istatistiklerini hesapla ve getir
        with sqlite3.connect(self.db_name) as conn:
            stats = {}
            stats['toplam_film'] = conn.execute("SELECT COUNT(*) FROM Filmler").fetchone()[0]
            stats['izlenen_film'] = conn.execute("SELECT COUNT(*) FROM Izlenenler").fetchone()[0]
            
            # [EN] Total runtime calculation (e.g., "148 min" -> 148)
            # [TR] Toplam süre hesaplama (Örn: "148 min" -> 148)
            filmler = conn.execute("SELECT Sure FROM Filmler WHERE imdbID IN (SELECT imdbID FROM Izlenenler)").fetchall()
            toplam_dakika = 0
            for f in filmler:
                try: toplam_dakika += int(f[0].split()[0])
                except: pass
            stats['toplam_sure'] = toplam_dakika
            
            # [EN] Most watched genre
            # [TR] En çok izlenen tür
            stats['favori_tur'] = conn.execute("""
                SELECT Tur, COUNT(*) as c FROM Filmler 
                WHERE imdbID IN (SELECT imdbID FROM Izlenenler)
                GROUP BY Tur ORDER BY c DESC LIMIT 1
            """).fetchone()
            
            return stats

    def filmleri_getir(self) -> List[Tuple[str, str]]:
        # [EN] Fetch all movies from the library
        # [TR] Kütüphanedeki tüm filmleri getir
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("SELECT imdbID, Ad FROM Filmler").fetchall()

    def izlenenleri_getir(self) -> List[str]:
        # [EN] Fetch names of watched movies
        # [TR] İzlenen filmlerin adlarını getir
        with sqlite3.connect(self.db_name) as conn:
            rows = conn.execute("""
                SELECT f.Ad FROM Izlenenler i 
                JOIN Filmler f ON i.imdbID = f.imdbID
            """).fetchall()
            return [row[0] for row in rows]

    def yorum_ekle(self, imdb_id: str, yorum: str):
        # [EN] Add a comment for a movie
        # [TR] Filmi için yorum ekle
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO Yorumlar VALUES(?,?)", [imdb_id, yorum])
            conn.commit()

    def yorumlari_getir(self) -> List[Tuple[str, str]]:
        # [EN] Fetch all movie comments
        # [TR] Tüm film yorumlarını getir
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("""
                SELECT f.Ad, y.Yorum FROM Yorumlar y 
                JOIN Filmler f ON y.imdbID = f.imdbID
            """).fetchall()

    def film_sil(self, imdb_id: str):
        # [EN] Remove a movie and related data from all records
        # [TR] Filmi ve ilgili tüm verileri kayıtlardan sil
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("DELETE FROM Filmler WHERE imdbID=?", [imdb_id])
            conn.execute("DELETE FROM Izlenenler WHERE imdbID=?", [imdb_id])
            conn.execute("DELETE FROM Yorumlar WHERE imdbID=?", [imdb_id])
            conn.commit()

    def film_ara_kutuphane(self, terim: str) -> List[Tuple[str, str]]:
        # [EN] Search the local library with locale-aware filtering
        # [TR] Yerel kütüphaneyi arama, Türkçe karakter uyumlu
        with sqlite3.connect(self.db_name) as conn:
            terim = terim.replace('İ', 'i').replace('I', 'ı').lower()
            query = "SELECT imdbID, Ad FROM Filmler WHERE LOWER(Ad) LIKE ?"
            return conn.execute(query, [f"%{terim}%"]).fetchall()

    def rastgele_film_oner(self) -> Optional[tuple]:
        # [EN] Suggest a random movie from the library
        # [TR] Kütüphaneden rastgele bir film öner
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("SELECT Ad FROM Filmler ORDER BY RANDOM() LIMIT 1").fetchone()
