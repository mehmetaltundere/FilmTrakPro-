# 🎬 FilmTrak Pro

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**FilmTrak Pro**, modern arayüzlü, hızlı ve kullanıcı dostu bir film takip asistanıdır. OMDb API gücüyle film dünyasını parmaklarınızın ucuna getirir.

---

## ✨ Öne Çıkan Özellikler

*   🔍 **Akıllı Arama**: OMDb API ile anında binlerce film arasından seçim yapın.
*   📊 **Dashboard**: Toplam izleme süreniz ve favori türlerinizle kendi istatistiklerinizi tutun.
*   ⭐ **Puanlama Sistemi**: İzlediğiniz filmlere 1-5 arası puan verin.
*   📚 **Kişisel Koleksiyon**: Filmleri "İzlenecekler", "Favoriler" gibi özel listelere ayırın.
*   🎲 **Rastgele Öneri**: Ne izleyeceğinize karar veremiyor musunuz? Bırakın asistanınız seçsin!
*   🌑 **Modern Dark Mode**: Göz yormayan, şık ve ergonomik arayüz.

## 📸 Ekran Görüntüleri

> [!TIP]
> Buraya uygulamanızın bir ekran görüntüsünü eklemek projenizin güvenilirliğini artırır!

## 🛠️ Kurulum

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/KULLANICI_ADINIZ/FilmTrakPro.git
    cd FilmTrakPro
    ```

2.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **API Anahtarını Ayarlayın:**
    `.env` dosyası oluşturun veya sisteminize ekleyin:
    ```bash
    OMDB_API_KEY=your_api_key_here
    ```

4.  **Çalıştırın:**
    ```bash
    python main.py
    ```

## 🏗️ Proje Mimarısı

*   `main.py`: Uygulamanın kalbi ve giriş noktası.
*   `ui.py`: Tkinter tabanlı modern arayüz katmanı.
*   `database.py`: SQLite ile güvenli veri depolama.
*   `api.py`: OMDb ile yüksek performanslı veri çekme.

## 🤝 Katkıda Bulunma

Hataları bildirmek veya yeni özellikler eklemek için bir **Pull Request** açmaktan çekinmeyin!

1. 🍴 Projeyi Fork'layın
2. 🌿 Yeni bir Branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. 💾 Değişikliklerinizi Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. 🚀 Branch'inizi Push edin (`git push origin feature/AmazingFeature`)
5. 🔍 Bir Pull Request açın

---
*Bu proje bir film tutkunu tarafından, diğer film tutkunları için geliştirilmiştir.* 🍿
