"""
core/tts.py

Mesin Text-to-Speech untuk membaca materi pelajaran panjang.

PENTING: Untuk navigasi tombol, kita TIDAK pakai TTS ini.
NVDA atau screen reader Windows akan otomatis membaca tombol wxPython
karena wxPython mendukung accessibility tree Windows.

TTS internal hanya untuk:
- Membaca isi materi panjang (dengan kontrol Putar/Stop)
- Membaca pertanyaan soal saat siswa menekan tombol "Dengar Soal"
- Membaca feedback jawaban
"""

import threading

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


class TTSEngine:
    def __init__(self, rate=180, volume=1.0):
        self.rate = rate
        self.volume = volume
        self._engine = None
        self._thread = None
        self._available = TTS_AVAILABLE

        if self._available:
            try:
                self._engine = pyttsx3.init()
                self._engine.setProperty("rate", self.rate)
                self._engine.setProperty("volume", self.volume)
                self._set_indonesian_voice()
            except Exception as e:
                print(f"Peringatan: Gagal inisialisasi TTS: {e}")
                self._available = False

    def _set_indonesian_voice(self):
        if not self._engine:
            return
        try:
            voices = self._engine.getProperty("voices")
            for voice in voices:
                name = (voice.name or "").lower()
                vid = (voice.id or "").lower()
                if "indonesian" in name or "indonesia" in name or "id-id" in vid:
                    self._engine.setProperty("voice", voice.id)
                    return
        except Exception:
            pass

    def speak(self, text):
        """Ucapkan teks (non-blocking)."""
        if not self._available or not text:
            return
        self.stop()
        self._thread = threading.Thread(
            target=self._speak_worker, args=(text,), daemon=True
        )
        self._thread.start()

    def _speak_worker(self, text):
        try:
            if self._engine is None:
                return
            self._engine.setProperty("rate", self.rate)
            self._engine.setProperty("volume", self.volume)
            self._engine.say(text)
            self._engine.runAndWait()
        except RuntimeError:
            pass
        except Exception as e:
            print(f"TTS error: {e}")

    def stop(self):
        if not self._available:
            return
        try:
            if self._engine:
                self._engine.stop()
        except Exception:
            pass

    def set_rate(self, rate):
        self.rate = max(50, min(400, int(rate)))
        if self._engine:
            try:
                self._engine.setProperty("rate", self.rate)
            except Exception:
                pass

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, float(volume)))
        if self._engine:
            try:
                self._engine.setProperty("volume", self.volume)
            except Exception:
                pass

    def is_available(self):
        return self._available
