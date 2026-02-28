# 🎬 FilmTrak Pro

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**FilmTrak Pro** is a professional-grade movie tracking application featuring a modern interface and modular architecture. It leverages the OMDb API to provide real-time movie data and utilizes SQLite for secure local storage.

**FilmTrak Pro**, modern arayüzlü ve modüler mimariye sahip profesyonel bir film takip uygulamasıdır. OMDb API kullanarak gerçek zamanlı film verileri sağlar ve güvenli yerel depolama için SQLite kullanır.

---

## 🌍 Language Support / Dil Desteği

*   **English**: Documentation and Code Comments.
*   **Türkçe**: Dokümantasyon ve Kod Yorumları.

---

## ✨ Key Features / Temel Özellikler

### [EN] English
*   🔍 **Advanced Search**: Instant data retrieval via OMDb API.
*   📊 **Analytics Dashboard**: Track total watch time, movie counts, and favorite genres.
*   ⭐ **Interactive Rating**: Rate watched movies on a 1-5 scale.
*   📚 **Collection Management**: Organize movies into custom lists (Favorites, Watchlist, etc.).
*   🎲 **Recommendation Engine**: Get random movie suggestions from your local library.
*   🌑 **Premium UI**: Sleek Dark Mode design with Seoge UI typography.

### [TR] Türkçe
*   🔍 **Gelişmiş Arama**: OMDb API üzerinden anlık veri çekimi.
*   📊 **Analiz Paneli**: Toplam izleme süresi, film sayıları ve favori tür takibi.
*   ⭐ **Etkileşimli Puanlama**: İzlenen filmleri 1-5 ölçeğinde puanlayın.
*   📚 **Koleksiyon Yönetimi**: Filmleri özel listeler (Favoriler, İzlenecekler vb.) halinde düzenleyin.
*   🎲 **Öneri Motoru**: Yerel kütüphanenizden rastgele film önerileri alın.
*   🌑 **Premium Arayüz**: Segoe UI tipografisi ile şık Karanlık Tema tasarımı.

---

## �️ Installation / Kurulum

### [EN] English
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/mehmetaltundere/FilmTrakPro-.git
    cd FilmTrakPro-
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Key:**
    Set the `OMDB_API_KEY` environment variable or update `api.py`.
4.  **Run Application:**
    ```bash
    python main.py
    ```

### [TR] Türkçe
1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/mehmetaltundere/FilmTrakPro-.git
    cd FilmTrakPro-
    ```
2.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **API Anahtarını Yapılandırın:**
    `OMDB_API_KEY` ortam değişkenini tanımlayın veya `api.py` dosyasını güncelleyin.
4.  **Uygulamayı Çalıştırın:**
    ```bash
    python main.py
    ```

---

## 🏗️ Architecture / Mimari

*   `main.py`: Entry point and application lifecycle. / Giriş noktası ve uygulama yaşam döngüsü.
*   `ui.py`: Tkinter-based UI layer with custom styling. / Özel stillere sahip Tkinter tabanlı arayüz katmanı.
*   `database.py`: SQLite abstraction and data persistence. / SQLite soyutlama ve veri kalıcılığı.
*   `api.py`: External OMDb API integration services. / Harici OMDb API entegrasyon servisleri.
*   `models.py`: Core data structures and entities. / Temel veri yapıları ve varlıklar.

---

## 🤝 Contribution / Katkıda Bulunma

### [EN] English
Contributions are welcome. Please open an issue first to discuss major changes.
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

### [TR] Türkçe
Katkılarınızı bekliyoruz. Büyük değişiklikler için önce bir konu (issue) açmanızı rica ederiz.
1. Projeyi Fork'layın.
2. Özellik Dalınızı Oluşturun (`git checkout -b feature/YeniOzellik`).
3. Değişikliklerinizi Kaydedin (`git commit -m 'YeniÖzellik Eklendi'`).
4. Dalınıza İtin (`git push origin feature/YeniOzellik`).
5. Bir Çekme İsteği (Pull Request) Açın.

---
*Developed for professional portfolio and open-source contribution.* / *Profesyonel portfolyo ve açık kaynak katkısı için geliştirilmiştir.*
