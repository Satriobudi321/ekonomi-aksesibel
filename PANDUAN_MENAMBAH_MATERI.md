# Panduan Menambah Materi Baru

Materi pelajaran disimpan dalam format **Markdown (.md)** yang bisa diedit pakai **Notepad biasa**. Aplikasi otomatis membaca file baru — Anda **tidak perlu build ulang aplikasi**.

## Cara Menambah Bab Baru

### Langkah 1: Buka folder materi

Buka folder `data\materi\kelas_10\` (atau `kelas_11\`, `kelas_12\` sesuai kelas yang ingin ditambah).

### Langkah 2: Buat file baru

1. Klik kanan di folder, pilih **New → Text Document**
2. Beri nama file dengan format: `nomor_judul.md`

   Contoh nama yang benar:
   - `04_inflasi_dan_pengangguran.md`
   - `05_perdagangan_internasional.md`
   - `06_apbn.md`

   **Penting**: 
   - Awali dengan **angka 2 digit** (`04_`, `05_`, dst) untuk menentukan urutan bab
   - Akhiran harus **`.md`** (bukan `.txt`)
   - Jangan pakai spasi, ganti dengan garis bawah `_`

### Langkah 3: Isi materi

Buka file dengan **Notepad** (klik kanan → Open with → Notepad). Tulis dengan format:

```
# Judul Bab

Pengantar bab di sini. Boleh beberapa paragraf.
Tulis seperti menulis biasa.

## Sub-Bab Pertama

Isi sub-bab pertama di sini.

## Sub-Bab Kedua

Isi sub-bab kedua di sini.
```

### Langkah 4: Simpan

Tekan **Ctrl+S** untuk save. Pastikan saat simpan:
- File extension tetap `.md` (bukan berubah jadi `.md.txt`)
- Encoding: **UTF-8** (di Notepad, klik File → Save As → ubah Encoding ke "UTF-8" sebelum save)

### Langkah 5: Tes di aplikasi

Jalankan aplikasi `EkonomiAksesibel.exe`. Bab baru akan langsung muncul di daftar.

## Aturan Format Markdown

| Yang Ditulis | Hasilnya |
|---|---|
| `# Judul Bab` | Judul utama bab |
| `## Sub-Bab` | Judul sub-bab |
| Teks biasa | Paragraf konten |
| Baris kosong | Ganti paragraf |
| `[Video: Nama](https://youtube.com/...)` | Link video YouTube |

**Penting**: Harus ada **spasi** setelah `#` dan `##`. Tulis `# Judul`, bukan `#Judul`.

## Menambahkan Link Video YouTube

Anda bisa menambahkan link video YouTube atau link belajar lain di setiap bab. Siswa tinggal **tekan Enter** untuk membuka video di browser.

### Format Penulisan Link

```
[Video: Judul Video](https://www.youtube.com/watch?v=KODE_VIDEO)
```

**Contoh konkret:**

```
# Inflasi

Inflasi adalah kenaikan harga barang dan jasa secara umum.

## Penyebab Inflasi

Ada dua penyebab utama inflasi.

## Video Pembelajaran

[Video: Pengertian Inflasi oleh Pak Budi](https://www.youtube.com/watch?v=ABC123XYZ)
[Video: Contoh Kasus Inflasi di Indonesia](https://www.youtube.com/watch?v=DEF456UVW)
```

### Cara Mendapatkan Link YouTube

1. Buka video YouTube yang ingin ditambahkan
2. Klik tombol **"Bagikan"** di bawah video
3. Klik **"Salin"** untuk salin link
4. Paste link tersebut ke file `.md` Anda

Atau cara lebih cepat: copy URL dari address bar browser saat menonton video.

### Aturan Format Link

- **Wajib pakai tanda kurung siku dan kurung biasa**: `[Judul](URL)`
- **URL harus diawali `https://`** atau `http://`
- **Awali judul dengan kata `Video:`** agar terdeteksi sebagai video
- **Tidak boleh ada spasi di dalam URL**

### Tipe Link yang Dikenali

| Format Judul | Tipe |
|---|---|
| `[Video: ...]` | Video (akan tampil tanda [VIDEO] di aplikasi) |
| `[Audio: ...]` | Audio (akan tampil tanda [AUDIO]) |
| `[...]` | Link biasa (akan tampil tanda [LINK]) |

URL YouTube otomatis dikenali sebagai video meskipun tidak pakai prefix "Video:".

### Bagaimana Siswa Memakainya

1. Buka materi seperti biasa
2. Selain area teks materi, ada **daftar link** di bawah
3. Tekan **Tab** untuk berpindah ke daftar link
4. Pilih link dengan **panah atas/bawah** (NVDA bacakan judul setiap link)
5. Tekan **Enter** untuk membuka video di browser
6. Selesai nonton, **tutup browser**, kembali ke aplikasi (Alt+Tab)

### Tips Menambah Video untuk Tunanetra

- **Pilih video dengan narasi jelas** — siswa tunanetra mengandalkan suara
- **Hindari video yang banyak tulisan di layar tanpa narasi**
- **Beri judul deskriptif**: bukan "[Video: Materi 1]" tapi "[Video: Penjelasan Sistem Ekonomi Pancasila]"
- **Test dulu**: pastikan video YouTube memang ada dan tidak private

---



## Tips Menulis Materi untuk Tunanetra

Karena materi akan dibacakan oleh suara, perhatikan:

- **Hindari singkatan**. Tulis "dan seterusnya" daripada "dst".
- **Tulis angka dalam kalimat**. "lima ratus ribu rupiah" lebih jelas daripada "Rp 500.000".
- **Hindari simbol matematika**. Ganti `=` dengan "sama dengan", `+` dengan "ditambah".
- **Pakai titik dan koma** agar suara ada jeda alami.
- **Singkat dan jelas**. Kalimat panjang sulit diingat saat didengar.

## Contoh File Materi Lengkap

Buat file `04_inflasi.md`:

```
# Inflasi

Inflasi adalah kenaikan harga barang dan jasa secara umum 
dan terus menerus dalam suatu periode waktu.

## Penyebab Inflasi

Inflasi disebabkan oleh dua faktor utama. Pertama, kenaikan 
permintaan agregat yang melebihi penawaran. Kedua, kenaikan 
biaya produksi seperti upah dan bahan baku.

## Jenis Inflasi

Berdasarkan tingkat keparahannya, inflasi dibedakan menjadi 
empat jenis. Inflasi ringan di bawah sepuluh persen per tahun. 
Inflasi sedang antara sepuluh sampai tiga puluh persen. 
Inflasi berat antara tiga puluh sampai seratus persen. 
Hiperinflasi di atas seratus persen per tahun.

## Dampak Inflasi

Inflasi berdampak negatif pada masyarakat berpenghasilan 
tetap karena daya beli menurun. Namun bagi pengusaha, 
inflasi yang terkendali bisa mendorong produksi.
```

## Mengedit Materi yang Sudah Ada

1. Buka folder `data\materi\kelas_XX\`
2. Klik kanan file `.md` yang ingin diedit, pilih Open with → Notepad
3. Edit, simpan dengan Ctrl+S
4. Buka aplikasi, perubahan langsung terlihat

## Menghapus Bab

Cukup hapus file `.md`-nya dari folder. Bab langsung hilang dari aplikasi.

## Mengubah Urutan Bab

Ubah angka di awal nama file. Contoh:
- `01_konsep_dasar.md` → bab pertama
- `02_biaya_peluang.md` → bab kedua

Kalau ingin tukar urutan, rename:
- `01_konsep_dasar.md` jadi `02_konsep_dasar.md`
- `02_biaya_peluang.md` jadi `01_biaya_peluang.md`

---

## Untuk Soal Latihan

Soal sekarang juga pakai format Markdown, satu file per bab — sama seperti materi.

### Struktur Folder Soal

```
data\soal\kelas_10\
├── 01_konsep_dasar.md
├── 02_biaya_peluang.md
└── 03_sistem_ekonomi.md
```

Saat siswa pilih "Latihan Soal", aplikasi akan menampilkan daftar bab — siswa bisa memilih satu bab spesifik atau "Semua Bab" untuk gabungan.

### Format Penulisan Soal (.md)

Buat file misal `04_inflasi.md` dengan isi:

```
# Soal: Inflasi

## Soal 1

Apa yang dimaksud dengan inflasi?

- Penurunan harga barang
* Kenaikan harga barang dan jasa secara umum
- Stabilitas harga
- Penambahan jumlah uang

Pembahasan: Inflasi adalah kenaikan harga barang dan jasa secara umum dan terus menerus.

## Soal 2

Penyebab utama inflasi yang berasal dari sisi permintaan disebut...

* Demand-pull inflation
- Cost-push inflation
- Imported inflation
- Spiral inflation

Pembahasan: Demand-pull inflation terjadi ketika permintaan agregat melebihi penawaran agregat.
```

### Aturan Format Soal

| Yang Ditulis | Hasilnya |
|---|---|
| `# Soal: Judul Bab` | Judul bab soal |
| `## Soal 1` | Pemisah antar soal |
| Teks setelah `## Soal X` | Pertanyaan |
| `- Pilihan` | Pilihan jawaban biasa |
| `* Pilihan` | **Pilihan yang BENAR** (tanda bintang) |
| `Pembahasan: ...` | Penjelasan jawaban |

**Penting:**
- **Hanya satu pilihan** yang ditandai `*` (bintang) — itulah jawaban benar
- Pilihan lain pakai `-` (strip)
- Antara `*` atau `-` dengan teks pilihan harus ada **spasi**
- Pembahasan opsional (boleh ada boleh tidak)

### Tips Membuat Soal

- **Beri minimal 4 pilihan** (A, B, C, D) untuk pilihan ganda standar
- **Hindari pilihan "semua benar" / "tidak ada yang benar"** karena membingungkan
- **Pembahasan harus singkat dan jelas** — akan dibacakan TTS
- **Hindari soal yang butuh tabel atau gambar** — siswa tunanetra tidak bisa lihat
- **Test sendiri**: setelah edit, jalankan aplikasi dan coba kerjakan soal

### Cara Menambah Bab Soal Baru

1. Buka folder `data\soal\kelas_10\` (atau kelas lain)
2. Klik kanan → New → Text Document
3. Rename jadi `04_inflasi.md` (sesuai bab Anda)
4. Buka di Notepad, tulis sesuai format di atas
5. Save dengan encoding UTF-8
6. Buka aplikasi → Latihan Soal → kelas → bab baru langsung muncul

**Tidak perlu build ulang aplikasi.**
