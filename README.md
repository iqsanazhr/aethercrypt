# 🛡️ AetherCrypt: Multi-Stage Classical Cryptosystem & Cryptanalysis Workbench

> **Mata Kuliah:** Kriptografi (IF21A05)  
> **Program Studi:** Informatika, Fakultas Teknik, Universitas Jenderal Soedirman  
> **Dosen Pengampu:** Eddy Maryanto, Puteri Awaliatush Shofro, M.Kom  

---

## 🌟 1. Deskripsi Proyek
**AetherCrypt** adalah aplikasi web laboratorium kriptografi canggih yang mengimplementasikan **Super-Enkripsi 3 Lapis Berantai** dengan menggabungkan tiga algoritma klasik yang berbeda secara fundamental:
1. **Playfair Cipher** (Substitusi Poligram Bigram $5 \times 5$)
2. **Vigenère Cipher** (Substitusi Polialfabetik Modulo 26)
3. **Columnar Transposition** (Transposisi Geometris Kolom)

Dilengkapi dengan **3D Artifact Showcase interaktif (Da Vinci Cryptex, Mesin Enigma, dan Puzzle Box)** menggunakan **Three.js & React Three Fiber**, serta **Laboratorium Kriptanalisis Forensik** berbasis grafik distribusi frekuensi huruf dan skor *Index of Coincidence (IC)*.

Sesuai aturan mutlak penugasan, seluruh algoritma ditulis murni menggunakan **logika dasar matematika Python (Pure Math & Logic)** tanpa bergantung pada library kriptografi siap pakai.

---

## 🚀 2. Fitur Utama

- **Super-Enkripsi 3 Tahap**:
  $$\text{Plainteks} \longrightarrow [\text{Playfair 5×5}] \longrightarrow C_1 \longrightarrow [\text{Vigenère Mod 26}] \longrightarrow C_2 \longrightarrow [\text{Columnar Grid}] \longrightarrow C_{\text{Final}}$$
- **Uji Dekripsi & Validasi 100% Identik ($P \to C \to P' \equiv P$)**:
  Membuktikan secara otomatis bahwa proses dekripsi balik memulihkan pesan awal dengan akurasi 100%.
- **Interactive 3D Artifact Showcase**:
  - Model 3D **Da Vinci Cryptex** kuningan yang berputar saat proses enkripsi berlangsung.
  - Model 3D **Mesin Enigma 1934**.
  - Model 3D **Mechanical Puzzle Box** sebagai representasi status gembok keamanan.
- **Visualizer Interaktif Tiap Tahap**:
  - *Playfair 5×5*: Visualisasi matriks, pasangan bigram, dan aturan pergeseran (Baris Sama, Kolom Sama, Sudut Persegi).
  - *Vigenère*: Penyelarasan kunci periodik dan kalkulasi modulo per karakter.
  - *Columnar*: Visualisasi kisi baris/kolom dan pembacaan prioritas alfabetik kata kunci.
- **Laboratorium Kriptanalisis (Nilai Plus)**:
  - Grafik Histogram Frekuensi Huruf (Recharts) membandingkan teks asli vs super-cipherteks vs standar bahasa Indonesia.
  - Pengukur *Index of Coincidence (IC)* dan Entropi Informasi Shannon.
- **I/O Berkas**:
  - Upload berkas `.txt` langsung ke dalam plainteks.
  - Unduh hasil cipherteks sebagai `.txt` dan salin cepat ke clipboard.

---

## 💻 3. Struktur Direktori Proyek

```
D:\Kripto\
├── da_vinci_code_cryptex.glb       # Aset 3D Sketchfab
├── enigma_machine_1934.glb         # Aset 3D Sketchfab
├── puzzle_box_01.glb               # Aset 3D Sketchfab
├── run_app.bat                     # Peluncur otomatis backend & frontend
├── start_backend.bat               # Peluncur server FastAPI
├── start_frontend.bat              # Peluncur server Vite React
│
├── backend/
│   ├── main.py                     # Server FastAPI & endpoints REST API
│   ├── test_pipeline.py            # Skrip verifikasi unit test matematika
│   └── core/
│       ├── playfair.py             # Logika murni Playfair Cipher 5x5
│       ├── vigenere.py             # Logika murni Vigenère Cipher Modulo 26
│       ├── columnar.py             # Logika murni Columnar Transposition
│       ├── pipeline.py             # Orkestrasi rantai super-enkripsi/dekripsi
│       └── cryptanalysis.py        # Kalkulasi IC, Entropi, dan Frekuensi
│
└── frontend/
    ├── public/models/              # Berkas 3D GLB yang dimuat Three.js
    └── src/
        ├── components/
        │   ├── ThreeViewer.jsx     # Kanvas 3D Three.js & OrbitControls
        │   ├── PlayfairVisualizer.jsx
        │   ├── VigenereVisualizer.jsx
        │   ├── ColumnarVisualizer.jsx
        │   ├── CryptanalysisLab.jsx
        │   └── VerificationBadge.jsx
        ├── App.jsx                 # Halaman utama aplikasi
        ├── index.css               # Styling Tailwind CSS v4 & Glow
        └── main.jsx                # Entry point React
```

---

## 🛠️ 4. Cara Menjalankan Aplikasi

### Cara Termudah (Satu Klik):
Cukup klik ganda pada berkas:
```bash
D:\Kripto\run_app.bat
```
Skrip ini akan secara otomatis membuka jendela Backend FastAPI dan jendela Frontend Vite, lalu membuka browser pada alamat:
`http://localhost:5173`

### Cara Manual:
1. **Jalankan Backend (Terminal 1)**:
   ```bash
   cd D:\Kripto\backend
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```
   *Dokumentasi Swagger API aktif pada: `http://127.0.0.1:8000/docs`*

2. **Jalankan Frontend (Terminal 2)**:
   ```bash
   cd D:\Kripto\frontend
   npm run dev
   ```
   *Buka antarmuka web pada: `http://localhost:5173`*
