"""
Ekonomi Aksesibel V2
Aplikasi pembelajaran ekonomi SMA untuk siswa tunanetra.
Versi 2 - menggunakan wxPython untuk kompatibilitas penuh dengan NVDA.

Dijalankan: python main.py
Windows 10 ke atas, Python 3.9+
"""

import sys
import os
import wx

# Tambahkan folder project ke path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from core.settings import Settings
from core.tts import TTSEngine


class EkonomiApp(wx.App):
    """Aplikasi utama wxPython."""

    def OnInit(self):
        # Muat pengaturan pengguna
        self.settings = Settings()

        # Inisialisasi TTS untuk membaca materi panjang
        self.tts = TTSEngine(
            rate=self.settings.get("tts_rate", 180),
            volume=self.settings.get("tts_volume", 1.0),
        )

        # Buat window utama
        self.frame = MainWindow(
            None,
            title="Ekonomi Aksesibel - Belajar Ekonomi SMA",
            settings=self.settings,
            tts=self.tts,
        )
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        try:
            self.tts.stop()
            self.settings.save()
        except Exception:
            pass
        return 0


def main():
    try:
        app = EkonomiApp()
        app.MainLoop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nError: {e}")
        print("Pastikan wxPython dan pyttsx3 sudah terpasang:")
        print("  python -m pip install wxPython pyttsx3 pywin32")
        input("Tekan Enter untuk keluar...")


if __name__ == "__main__":
    main()
