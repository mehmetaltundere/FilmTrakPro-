import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import io
from models import Movie
from api import MovieAPI
from database import DatabaseManager

class FilmTrakUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("FilmTrak Pro")
        self.root.geometry("1000x850")
        self.root.configure(bg="#1e1e2e")

        self.api = MovieAPI()
        self.db = DatabaseManager()
        self.current_movie = None

        self._setup_styles()
        self._create_widgets()
        self._load_data()

    def _setup_styles(self):
        # [EN] Configure modern UI styles and colors
        # [TR] Modern arayüz stillerini ve renklerini yapılandır
        style = ttk.Style()
        style.theme_use("clam")
        
        bg_color = "#1e1e2e"
        fg_color = "#cdd6f4"
        accent_color = "#fab387"
        secondary_bg = "#313244"

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI Bold", 18), foreground=accent_color)
        
        style.configure("TButton", 
                        background=accent_color, 
                        foreground="#11111b", 
                        font=("Segoe UI Bold", 10),
                        borderwidth=0)
        style.map("TButton", background=[("active", "#f5c2e7")])
        style.configure("Action.TButton", background=secondary_bg, foreground=fg_color)
        style.configure("TEntry", fieldbackground=secondary_bg, foreground=fg_color, borderwidth=0)
        
    def _create_widgets(self):
        # [EN] Create and pack UI components
        # [TR] Arayüz bileşenlerini oluştur ve yerleştir

        # [EN] Upper Search Bar
        # [TR] Üst Arama Çubuğu
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill="x", padx=30, pady=20)

        self.search_entry = ttk.Entry(search_frame, font=("Segoe UI", 12), width=50)
        self.search_entry.pack(side="left", padx=(0, 10), ipady=5)
        self.search_entry.bind("<Return>", lambda e: self.search_movie())

        ttk.Button(search_frame, text="FİLM ARA", command=self.search_movie).pack(side="left")

        # [EN] Main Content Area
        # [TR] Ana İçerik Alanı
        main_content = ttk.Frame(self.root)
        main_content.pack(fill="both", expand=True, padx=30)

        # [EN] Left Panel: Movie Details
        # [TR] Sol Panel: Film Detayları
        left_panel = ttk.Frame(main_content)
        left_panel.pack(side="left", fill="both", expand=True)

        self.poster_label = tk.Label(left_panel, text="Afiş Yüklenecek", bg="#313244", fg="#cdd6f4", 
                                     width=30, height=20, font=("Segoe UI", 10))
        self.poster_label.pack(pady=10)

        self.title_label = ttk.Label(left_panel, text="Hoş Geldiniz!", style="Header.TLabel", wraplength=400)
        self.title_label.pack(pady=5)

        self.info_text = tk.Text(left_panel, height=8, width=50, bg="#1e1e2e", fg="#cdd6f4", 
                                 font=("Segoe UI", 10), relief="flat", wrap="word")
        self.info_text.pack(pady=5)
        self.info_text.config(state="disabled")

        # [EN] Action Buttons
        # [TR] İşlem Butonları
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Koleksiyona Ekle", command=self.save_movie).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="İzledim & Puanla", command=self.mark_as_watched).pack(side="left", padx=5)
        self.imdb_btn = ttk.Button(btn_frame, text="IMDb'de Gör", command=self.open_imdb)
        self.imdb_btn.pack(side="left", padx=5)
        self.imdb_btn.state(['disabled'])

        # [EN] Right Panel: Lists and Statistics
        # [TR] Sağ Panel: Listeler ve İstatistikler
        right_panel = ttk.Frame(main_content)
        right_panel.pack(side="right", fill="both", padx=(20, 0))

        # [EN] Library Listbox
        # [TR] Kitaplık Liste Kutusu
        ttk.Label(right_panel, text="Kitaplığım", font=("Segoe UI Bold", 12)).pack(anchor="w")
        self.lib_search = ttk.Entry(right_panel, font=("Segoe UI", 10))
        self.lib_search.pack(fill="x", pady=2)
        self.lib_search.bind("<KeyRelease>", lambda e: self.filter_library())

        self.library_list = tk.Listbox(right_panel, bg="#313244", fg="#cdd6f4", borderwidth=0, 
                                       highlightthickness=0, width=40, height=10)
        self.library_list.pack(pady=(2, 10))

        # [EN] Dashboard and Operations
        # [TR] Dashboard ve İşlemler
        stats_frame = ttk.Frame(right_panel)
        stats_frame.pack(fill="x", pady=5)
        
        ttk.Button(stats_frame, text="📊 Dashboard", 
                   style="Action.TButton", command=self.show_stats).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(stats_frame, text="🗑️ Sil", 
                   style="Action.TButton", command=self.delete_selected).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(stats_frame, text="🎲 Öneri", 
                   style="Action.TButton", command=self.suggest_random).pack(side="left", expand=True, fill="x", padx=2)

        # [EN] Recent Comments Section
        # [TR] Son Yorumlar Bölümü
        ttk.Label(right_panel, text="Son Yorumlar", font=("Segoe UI Bold", 12)).pack(anchor="w", pady=(10,0))
        self.comment_list = tk.Listbox(right_panel, bg="#313244", fg="#cdd6f4", borderwidth=0, 
                                        highlightthickness=0, width=40, height=5)
        self.comment_list.pack(pady=5)

        # [EN] Footer: Search History
        # [TR] Alt Bilgi: Arama Geçmişi
        history_frame = ttk.Frame(self.root)
        history_frame.pack(fill="x", side="bottom", padx=30, pady=10)
        ttk.Label(history_frame, text="Son Aramalar: ", font=("Segoe UI", 9, "italic")).pack(side="left")
        self.history_label = ttk.Label(history_frame, text="Veri yok", font=("Segoe UI", 9))
        self.history_label.pack(side="left")

    def search_movie(self):
        # [EN] Trigger movie search via API
        # [TR] API üzerinden film aramasını başlat
        query = self.search_entry.get().strip()
        if not query: return

        movie = self.api.search_movie(query)
        if movie:
            self.current_movie = movie
            self.db.gecmis_ekle(query)
            self._display_movie(movie)
            self.imdb_btn.state(['!disabled'])
            self._update_ui_lists()
        else:
            messagebox.showwarning("Hata", f"'{query}' bulunamadı!")

    def _display_movie(self, movie: Movie):
        # [EN] Render movie data to UI components
        # [TR] Film verilerini arayüz bileşenlerine aktar
        self.title_label.config(text=f"{movie.title} ({movie.year})")
        info = f"⭐ IMDb: {movie.rating}  |  ⏳ Süre: {movie.runtime}\n"
        info += f"🎬 Yönetmen: {movie.director}\n"
        info += f"🏷️ Tür: {movie.genre}\n\n"
        info += f"📝 Konu: {movie.plot}"
        
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state="disabled")

        poster_data = self.api.get_poster_data(movie.poster_url)
        if poster_data:
            img = Image.open(io.BytesIO(poster_data))
            img = img.resize((240, 360), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.poster_label.config(image=photo, text="")
            self.poster_label.image = photo
        else:
            self.poster_label.config(image="", text="Afiş Yok")

    def save_movie(self):
        # [EN] Add current movie to library and collection
        # [TR] Mevcut filmi kütüphaneye ve koleksiyona ekle
        if not self.current_movie: return
        liste = simpledialog.askstring("Liste", "Liste adı (Örn: Favoriler, Sonra İzle):")
        if liste:
            self.db.film_kaydet(self.current_movie)
            self.db.koleksiyon_ekle(self.current_movie.imdb_id, liste)
            messagebox.showinfo("Başarılı", f"'{liste}' listesine eklendi.")
            self._update_ui_lists()

    def mark_as_watched(self):
        # [EN] Mark movie as watched and save rating
        # [TR] Filmi izlenenlere işaretle ve puanı kaydet
        if not self.current_movie: return
        puan = simpledialog.askinteger("Puan", "Puanınız (1-5):", minvalue=1, maxvalue=5)
        if puan:
            self.db.film_kaydet(self.current_movie)
            self.db.izlenenlere_ekle(self.current_movie.imdb_id, puan)
            messagebox.showinfo("Harika!", f"{puan}/5 puan verildi.")
            self._update_ui_lists()

    def show_stats(self):
        # [EN] Display application analytics in a modal
        # [TR] Uygulama istatistiklerini bir pencerede göster
        s = self.db.istatistik_getir()
        msg = f"📊 İSTATİSTİKLER\n"
        msg += f"-------------------\n"
        msg += f"🎬 Toplam Film: {s['toplam_film']}\n"
        msg += f"✅ İzlenen: {s['izlenen_film']}\n"
        msg += f"⏳ İzleme Süresi: {s['toplam_sure'] // 60}sa {s['toplam_sure'] % 60}dk\n"
        if s['favori_tur']:
            msg += f"🌟 Favori Tür: {s['favori_tur'][0]} ({s['favori_tur'][1]} film)"
        messagebox.showinfo("Dashboard", msg)

    def open_imdb(self):
        # [EN] Redirect to IMDb web page
        # [TR] IMDb web sayfasına yönlendir
        if self.current_movie:
            self.api.open_imdb_page(self.current_movie.imdb_id)

    def delete_selected(self):
        # [EN] Delete the selected movie from library
        # [TR] Seçili filmi kütüphaneden sil
        sel = self.library_list.curselection()
        if not sel: return
        movies = self.db.filmleri_getir()
        id, title = movies[sel[0]]
        if messagebox.askyesno("Sil", f"'{title}' kütüphaneden silinsin mi?"):
            self.db.film_sil(id)
            self._update_ui_lists()

    def filter_library(self):
        # [EN] Live filter library list based on search term
        # [TR] Arama terimine göre kütüphane listesini anlık filtrele
        term = self.lib_search.get().strip()
        self.library_list.delete(0, tk.END)
        movies = self.db.film_ara_kutuphane(term) if term else self.db.filmleri_getir()
        for _, t in movies:
            self.library_list.insert(tk.END, f"• {t}")

    def suggest_random(self):
        # [EN] Show a random suggestion from library
        # [TR] Kütüphaneden rastgele bir öneri göster
        res = self.db.rastgele_film_oner()
        if res: messagebox.showinfo("Öneri", f"Şunu izleyebilirsin: {res[0]}")

    def _update_ui_lists(self):
        # [EN] Refresh all list components in the UI
        # [TR] Arayüzdeki tüm liste bileşenlerini yenile
        self.library_list.delete(0, tk.END)
        for _, t in self.db.filmleri_getir():
            self.library_list.insert(tk.END, f"• {t}")

        self.comment_list.delete(0, tk.END)
        for t, c in self.db.yorumlari_getir():
            self.comment_list.insert(tk.END, f"{t}: {c}")

        h = self.db.gecmis_getir()
        if h: self.history_label.config(text=", ".join([x[0] for x in h[:5]]))

    def _load_data(self):
        # [EN] Initial data load on startup
        # [TR] Açılışta ilk veri yüklemesi
        self._update_ui_lists()
