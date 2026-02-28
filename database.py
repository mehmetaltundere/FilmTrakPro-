import sqlite3
from typing import List, Tuple, Optional
from datetime import datetime
from models import Movie

class DatabaseManager:
    def __init__(self, db_name: str = "filmtrak_pro.db"):
        self.db_name = db_name
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Geçmiş tablosu
            cursor.execute("CREATE TABLE IF NOT EXISTS Gecmis(Anahtar TEXT, Tarih TEXT)")
            # Filmler tablosu (Kitaplık)
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
            # Yorumlar tablosu
            cursor.execute("CREATE TABLE IF NOT EXISTS Yorumlar(imdbID TEXT, Yorum TEXT)")
            # İzlenenler tablosu (Puan eklendi)
            cursor.execute("CREATE TABLE IF NOT EXISTS Izlenenler(imdbID TEXT PRIMARY KEY, Puan INTEGER)")
            # Koleksiyonlar tablosu
            cursor.execute("CREATE TABLE IF NOT EXISTS Koleksiyonlar(imdbID TEXT, ListeAdi TEXT)")
            conn.commit()

    def gecmis_ekle(self, anahtar: str):
        zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO Gecmis VALUES(?,?)", [anahtar, zaman])
            conn.commit()

    def gecmis_getir(self) -> List[Tuple[str, str]]:
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("SELECT Anahtar, Tarih FROM Gecmis ORDER BY Tarih DESC LIMIT 50").fetchall()

    def film_kaydet(self, movie: Movie):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO Filmler VALUES(?,?,?,?,?,?,?,?,?)
            """, [
                movie.imdb_id, movie.title, movie.year, movie.poster_url, 
                movie.genre, movie.director, movie.rating, movie.plot, movie.runtime
            ])
            conn.commit()

    def izlenenlere_ekle(self, imdb_id: str, puan: int = 0):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT OR REPLACE INTO Izlenenler VALUES(?,?)", [imdb_id, puan])
            conn.commit()

    def koleksiyon_ekle(self, imdb_id: str, liste_adi: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO Koleksiyonlar VALUES(?,?)", [imdb_id, liste_adi])
            conn.commit()

    def istatistik_getir(self):
        with sqlite3.connect(self.db_name) as conn:
            stats = {}
            stats['toplam_film'] = conn.execute("SELECT COUNT(*) FROM Filmler").fetchone()[0]
            stats['izlenen_film'] = conn.execute("SELECT COUNT(*) FROM Izlenenler").fetchone()[0]
            
            # Toplam süre hesaplama (Örn: "148 min" -> 148)
            filmler = conn.execute("SELECT Sure FROM Filmler WHERE imdbID IN (SELECT imdbID FROM Izlenenler)").fetchall()
            toplam_dakika = 0
            for f in filmler:
                try: toplam_dakika += int(f[0].split()[0])
                except: pass
            stats['toplam_sure'] = toplam_dakika
            
            # En çok izlenen tür
            stats['favori_tur'] = conn.execute("""
                SELECT Tur, COUNT(*) as c FROM Filmler 
                WHERE imdbID IN (SELECT imdbID FROM Izlenenler)
                GROUP BY Tur ORDER BY c DESC LIMIT 1
            """).fetchone()
            
            return stats

    def filmleri_getir(self) -> List[Tuple[str, str]]:
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("SELECT imdbID, Ad FROM Filmler").fetchall()

    def izlenenleri_getir(self) -> List[str]:
        with sqlite3.connect(self.db_name) as conn:
            rows = conn.execute("""
                SELECT f.Ad FROM Izlenenler i 
                JOIN Filmler f ON i.imdbID = f.imdbID
            """).fetchall()
            return [row[0] for row in rows]

    def yorum_ekle(self, imdb_id: str, yorum: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO Yorumlar VALUES(?,?)", [imdb_id, yorum])
            conn.commit()

    def yorumlari_getir(self) -> List[Tuple[str, str]]:
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("""
                SELECT f.Ad, y.Yorum FROM Yorumlar y 
                JOIN Filmler f ON y.imdbID = f.imdbID
            """).fetchall()

    def film_sil(self, imdb_id: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("DELETE FROM Filmler WHERE imdbID=?", [imdb_id])
            conn.execute("DELETE FROM Izlenenler WHERE imdbID=?", [imdb_id])
            conn.execute("DELETE FROM Yorumlar WHERE imdbID=?", [imdb_id])
            conn.commit()

    def film_ara_kutuphane(self, terim: str) -> List[Tuple[str, str]]:
        # SQLite LIKE varsayılan olarak ASCII uyumludur, Türkçe için LOWER kullanıyoruz.
        with sqlite3.connect(self.db_name) as conn:
            terim = terim.replace('İ', 'i').replace('I', 'ı').lower()
            query = "SELECT imdbID, Ad FROM Filmler WHERE LOWER(Ad) LIKE ?"
            return conn.execute(query, [f"%{terim}%"]).fetchall()

    def rastgele_film_oner(self) -> Optional[tuple]:
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("SELECT Ad FROM Filmler ORDER BY RANDOM() LIMIT 1").fetchone()
