# � SentimentAI: Tokopedia Product Sentiment Comparator

SentimentAI adalah aplikasi berbasis web yang memungkinkan pengguna untuk membandingkan sentimen pembeli antara dua produk dari Tokopedia. Aplikasi ini menggunakan model **BERT-base Indonesian** yang dilatih khusus untuk analisis sentimen guna memberikan hasil yang akurat.

## ✨ Fitur Utama
- **Review Scraping**: Mengambil hingga 1000 ulasan per produk menggunakan pagination otomatis (50 ulasan per request).
- **Deep Learning Sentiment Analysis**: Menggunakan model `ayameRushia/bert-base-indonesian-1.5G-sentiment-analysis-smsa` via Hugging Face Inference API.
- **Visual Comparison**: Menampilkan perbandingan persentase sentimen (Positif, Netral, Negatif) dalam bentuk grafik donat yang interaktif.
- **Auto-pagination**: Looping pintar untuk mendapatkan data ulasan dalam jumlah besar secara otomatis.

## 🛠️ Persyaratan
- Python 3.8+
- Token Hugging Face (Gratis)
- Koneksi Internet

## 🚀 Instalasi & Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/MuhAsmann/sentiment-produk.git
   cd sentiment-produk
   ```

2. **Buat Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Environment**
   Buat file `.env` di root direktori dan tambahkan kredensial Anda:
   ```env
   HF_TOKEN=your_hugging_face_token_here
   HF_API_URL=https://router.huggingface.co/hf-inference/models/ayameRushia/bert-base-indonesian-1.5G-sentiment-analysis-smsa
   ```

## 💻 Cara Menjalankan

Jalankan aplikasi dengan perintah:
```bash
python run.py
```
Aplikasi akan berjalan di `http://127.0.0.1:5000`. Cukup masukkan dua URL produk Tokopedia dan klik **"Analisis Sekarang"**.

---

## 🤝 Kontribusi

Kami sangat menghargai kontribusi Anda! Jika Anda ingin membantu mengembangkan proyek ini, silakan ikuti langkah-langkah berikut:

1. **Fork** repository ini.
2. Buat **Branch** baru untuk fitur Anda (`git checkout -b feature/FiturKeren`).
3. **Commit** perubahan Anda (`git commit -m 'Menambahkan fitur keren'`).
4. **Push** ke branch tersebut (`git push origin feature/FiturKeren`).
5. Buat **Pull Request**.

### Area yang Bisa Ditingkatkan:
- [ ] Penambahan support untuk marketplace lain (Shopee, Lazada, dll).
- [ ] Implementasi caching hasil analisis untuk menghemat API rate limit.
- [ ] UI/UX yang lebih responsif untuk perangkat mobile.
- [ ] Export hasil analisis ke format PDF atau Excel.

---

## 📜 Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## 👨‍💻 Author
Dibuat oleh [MuhAsmann](https://github.com/MuhAsmann)