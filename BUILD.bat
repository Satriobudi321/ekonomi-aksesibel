@echo off
REM Script otomatis build aplikasi EkonomiAksesibel
REM Klik dua kali file ini untuk build .exe

echo ============================================================
echo   Build Aplikasi Ekonomi Aksesibel
echo ============================================================
echo.

REM Pindah ke folder script ini
cd /d "%~dp0"

REM Hapus build lama
echo [1/4] Membersihkan build lama...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist EkonomiAksesibel.spec del /q EkonomiAksesibel.spec
echo      Selesai.
echo.

REM Jalankan PyInstaller dengan mode folder
echo [2/4] Membangun aplikasi (5-10 menit)...
echo      Jangan tutup jendela ini!
python -m PyInstaller --name "EkonomiAksesibel" --windowed --noconfirm main.py
if errorlevel 1 (
    echo.
    echo ERROR: Build gagal. Cek pesan error di atas.
    pause
    exit /b 1
)
echo.

REM Copy folder data ke hasil build
echo [3/4] Menyalin folder materi dan soal...
xcopy /E /I /Y data dist\EkonomiAksesibel\data >nul
echo      Selesai.
echo.

REM Copy panduan
echo [4/4] Menyalin panduan...
if exist PANDUAN_MENAMBAH_MATERI.md copy /Y PANDUAN_MENAMBAH_MATERI.md dist\EkonomiAksesibel\ >nul
echo      Selesai.
echo.

echo ============================================================
echo   BUILD BERHASIL
echo ============================================================
echo.
echo Aplikasi siap pakai ada di folder:
echo   %cd%\dist\EkonomiAksesibel\
echo.
echo File utama: EkonomiAksesibel.exe
echo.
echo Folder data\materi\ dan data\soal\ ada di samping .exe
echo Anda bisa edit materi langsung tanpa build ulang.
echo.
echo Untuk distribusi ke sekolah:
echo   1. Zip seluruh folder dist\EkonomiAksesibel\
echo   2. Kirim file zip
echo   3. Extract di komputer tujuan, klik EkonomiAksesibel.exe
echo.
pause
