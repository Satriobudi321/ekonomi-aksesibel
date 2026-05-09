# Ekonomi Aksesibel V2

**Aplikasi Belajar Ekonomi SMA untuk Siswa Tunanetra - Versi Ramah NVDA**

Aplikasi desktop Windows yang dibangun dari nol dengan fokus pada kompatibilitas penuh dengan screen reader **NVDA**, **JAWS**, dan **Narrator**. Menggunakan library wxPython yang mendukung accessibility tree Windows.

---

## Apa yang Berubah dari Versi 1?

| Aspek | V1 (Tkinter) | V2 (wxPython) |
|---|---|---|
| Library GUI | Tkinter | **wxPython** |
| NVDA membaca tombol | Tidak | **Ya, otomatis** |
| NVDA membaca menu | Tidak | **Ya** |
| Pengucapan saat Tab | Manual via TTS | **Otomatis oleh NVDA** |
| Komponen | Custom | **Native Windows** |

V2 dibuat dari nol di folder `EkonomiAksesibelV2/`. **Versi V1 tidak diubah** dan tetap bisa dijalankan jika diperlukan.

---

## 1. Persyaratan Sistem

- **Sistem Operasi**: Windows 10 atau yang lebih baru
- **Python**: versi 3.9 sampai 3.12 (saat dijalankan dari source code)
- **NVDA** (opsional tapi sangat direkomendasikan): [nvaccess.org/download](https://www.nvaccess.org/download/)

> **Catatan**: wxPython belum sepenuhnya kompatibel dengan Python 3.13+. Jika Anda pakai Python 3.14, pertimbangkan downgrade ke Python 3.12.

---

## 2. Instalasi (untuk Pengembang)

### Langkah 1: Pasang Python 3.12

1. Download Python 3.12 dari [python.org/downloads/release/python-31210/](https://www.python.org/downloads/release/python-31210/)
2. Saat instalasi, **centang "Add Python to PATH"**
3. Klik "Install Now"

### Langkah 2: Pasang Library

Buka Command Prompt di folder aplikasi:

```
cd C:\EkonomiAksesibelV2
python -m pip install -r requirements.txt
```

Tunggu sampai semua library terpasang. Proses ini bisa makan 5-10 menit karena wxPython cukup besar.

### Langkah 3: Jalankan Aplikasi

```
python main.py
```

---

## 3. Cara Pakai Bersama NVDA

### Untuk Siswa Tunanetra

1. **Pasang NVDA** dari [nvaccess.org/download](https://www.nvaccess.org/download/) (gratis)
2. **Jalankan NVDA dulu** sebelum buka aplikasi (icon NVDA di desktop atau start menu)
3. **Jalankan aplikasi Ekonomi Aksesibel**
4. NVDA akan otomatis membacakan setiap tombol saat Anda menekan **Tab**

### Yang Akan Dibacakan NVDA Otomatis

| Aksi | Yang NVDA Bacakan |
|---|---|
| Tab ke tombol | "Pilih Materi Pelajaran, Alt 1, button" |
| Panah di list | "Kelas 10 Ekonomi Kelas 10, 1 dari 3" |
| Panah di radio button soal | "A. Aturan, radio button, 1 dari 4" |
| Geser slider font | "Ukuran font 16" |
| Centang checkbox | "Mode kontras tinggi, dicentang" |
| Buka menu bar | "Berkas menu" |

### Yang Dibacakan TTS Internal Aplikasi

Hanya untuk konten panjang yang butuh tombol Putar/Stop:
- Isi materi pelajaran (saat tekan tombol "Putar Pembacaan")
- Pertanyaan soal saat tekan "Dengar Pertanyaan"
- Hasil akhir latihan soal

### Tombol Penting NVDA

| Tombol | Fungsi |
|---|---|
| `Insert + Q` | Keluar dari NVDA |
| `Ctrl` | Hentikan suara NVDA |
| `Insert + Tab` | Baca ulang elemen yang fokus |
| `Insert + Panah Atas` | Baca baris yang fokus |
| `Insert + Spasi` | Toggle mode browse/focus |

---

## 4. Build ke File .exe

### Langkah 1: Pastikan PyInstaller Terpasang

```
python -m pip install pyinstaller
```

### Langkah 2: Build

Di Command Prompt, dalam folder `EkonomiAksesibelV2`:

```
pyinstaller --name "EkonomiAksesibel" --onefile --windowed --add-data "data;data" main.py
```

### Langkah 3: Ambil Hasil

File `.exe` ada di folder `dist/EkonomiAksesibel.exe`. File inilah yang dibagikan ke sekolah.

> **Tip**: File hasil build akan cukup besar (50-80 MB) karena wxPython dibundel di dalamnya. Ini normal.

---

## 5. Struktur Folder

```
EkonomiAksesibelV2/
├── main.py                      # Entry point
├── requirements.txt
├── README.md
├── core/
│   ├── __init__.py
│   ├── tts.py                   # TTS untuk membaca materi panjang
│   ├── settings.py
│   ├── content_loader.py
│   └── progress.py
├── ui/
│   ├── __init__.py
│   ├── main_window.py           # Frame utama dengan menu bar
│   ├── materi_window.py         # Dialog 3-tahap baca materi
│   ├── soal_window.py           # Dialog latihan dengan RadioBox
│   ├── progress_window.py
│   └── pengaturan_window.py     # Slider untuk font/suara/volume
└── data/
    ├── materi/
    │   ├── kelas_10.json
    │   ├── kelas_11.json
    │   └── kelas_12.json
    ├── soal/
    │   ├── kelas_10.json
    │   ├── kelas_11.json
    │   └── kelas_12.json
    └── progress/                # otomatis dibuat
```

---

## 6. Shortcut Keyboard

### Menu Utama

| Tombol | Fungsi |
|---|---|
| `Tab` / `Shift+Tab` | Pindah tombol |
| `Enter` / `Spasi` | Aktifkan tombol |
| `Alt + 1` | Pilih Materi |
| `Alt + 2` | Latihan Soal |
| `Alt + 3` | Lihat Progress |
| `Alt + 4` | Pengaturan |
| `F1` | Bantuan |
| `Ctrl + Q` | Keluar |
| `Escape` | Keluar |

### Di Halaman Materi

| Tombol | Fungsi |
|---|---|
| `Panah Atas/Bawah` (di list kelas/bab) | Pilih kelas/bab |
| `Enter` | Buka pilihan |
| `Alt + P` | Putar pembacaan |
| `Alt + H` | Hentikan |
| `Alt + S` | Tandai selesai |
| `Alt + K` | Kembali |

### Di Halaman Soal

| Tombol | Fungsi |
|---|---|
| `Panah` (di radio button) | Pilih jawaban A-D |
| `Alt + J` | Submit jawaban |
| `Alt + D` | Dengar pertanyaan |
| `Alt + B` | Berhenti |

---

## 7. Troubleshooting

### Error saat install wxPython

wxPython belum mendukung Python 3.13+. Solusinya:

1. Uninstall Python 3.13/3.14
2. Install Python 3.12 dari [python.org](https://www.python.org/downloads/release/python-31210/)
3. Coba install ulang: `python -m pip install wxPython`

### NVDA tidak baca tombol

1. Pastikan NVDA dijalankan **sebelum** aplikasi dibuka
2. Restart NVDA: `Insert + Q` lalu jalankan ulang
3. Cek setting NVDA: `Insert + N` → Preferences → Settings → Object Presentation → pastikan "Report tooltips" aktif

### Suara TTS tidak keluar saat tekan "Putar Pembacaan"

1. Install pywin32: `python -m pip install pywin32`
2. Cek volume sistem
3. Tes di Pengaturan → tombol "Coba Suara"

### Aplikasi tidak terbuka

Jalankan dari Command Prompt untuk lihat error:
```
python main.py
```
Pesan error akan muncul di Command Prompt.

---

## 8. Format Data (untuk Edit Materi/Soal)

Sama seperti V1 — file JSON di `data/materi/` dan `data/soal/`. Format dan strukturnya identik dengan V1, jadi kalau Anda sudah punya materi tambahan dari V1, bisa langsung copy ke V2.

### Materi (`data/materi/kelas_XX.json`)

```json
{
  "judul": "Ekonomi Kelas 10",
  "deskripsi": "Deskripsi singkat",
  "bab": [
    {
      "id": 1,
      "judul": "Judul Bab",
      "konten": "Pengantar bab...",
      "sub_bab": [
        {"judul": "Sub-bab", "isi": "Isi sub-bab..."}
      ]
    }
  ]
}
```

### Soal (`data/soal/kelas_XX.json`)

```json
{
  "judul": "Soal Latihan",
  "soal": [
    {
      "pertanyaan": "Pertanyaan?",
      "pilihan": ["A", "B", "C", "D"],
      "jawaban": 2,
      "pembahasan": "Penjelasan..."
    }
  ]
}
```

`"jawaban"` adalah index, mulai dari 0 (A=0, B=1, C=2, D=3).

---

## 9. Argumen untuk Skripsi

V2 menggunakan **wxPython** yang membungkus komponen native Windows. Ini penting karena:

1. **Standar WCAG terpenuhi**: NVDA, JAWS, Narrator semuanya bisa membaca aplikasi karena memakai Microsoft UI Automation API
2. **Tidak butuh konfigurasi khusus**: Siswa cukup install NVDA standar tanpa ada plugin tambahan
3. **Konsisten dengan aplikasi Windows lain**: Pengguna NVDA sudah terbiasa dengan pola navigasi yang sama
4. **Self-contained**: Aplikasi tetap punya TTS sendiri untuk siswa yang belum sempat install NVDA

---

## 10. Saran Pengujian untuk Skripsi

1. Uji dengan NVDA + minimal 3 siswa tunanetra
2. Catat waktu untuk:
   - Menyelesaikan satu bab dari awal sampai tandai selesai
   - Mengerjakan satu sesi latihan soal
3. Wawancara siswa: apakah suara NVDA cukup jelas? Apakah tombol mudah ditemukan?
4. Bandingkan dengan aplikasi lama (V1) sebagai data pembanding

---

## Kontak

Aplikasi ini dibuat sebagai project akhir studi mahasiswa Pendidikan Ekonomi.
