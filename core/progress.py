"""
core/progress.py

Pencatatan progress belajar siswa.
"""

import json
import os
from datetime import datetime


def _get_progress_dir():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "data", "progress")


class ProgressTracker:
    def __init__(self, user_id="siswa"):
        self.user_id = user_id
        self.filepath = os.path.join(_get_progress_dir(), f"{user_id}_progress.json")
        self._data = {
            "materi_dibaca": [],
            "riwayat_latihan": [],
            "total_soal_benar": 0,
            "total_soal_dikerjakan": 0,
        }
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._data.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def tandai_materi_dibaca(self, kelas, bab_id):
        key = f"kelas_{kelas}_bab_{bab_id}"
        if key not in self._data["materi_dibaca"]:
            self._data["materi_dibaca"].append(key)
            self.save()

    def sudah_dibaca(self, kelas, bab_id):
        key = f"kelas_{kelas}_bab_{bab_id}"
        return key in self._data["materi_dibaca"]

    def catat_latihan(self, kelas, benar, total):
        self._data["riwayat_latihan"].append({
            "tanggal": datetime.now().isoformat(),
            "kelas": kelas,
            "benar": benar,
            "total": total,
            "persentase": round((benar / total) * 100, 1) if total > 0 else 0,
        })
        self._data["total_soal_benar"] += benar
        self._data["total_soal_dikerjakan"] += total
        self.save()

    def ringkasan(self):
        total_kerjakan = self._data["total_soal_dikerjakan"]
        total_benar = self._data["total_soal_benar"]
        persentase = round((total_benar / total_kerjakan) * 100, 1) if total_kerjakan > 0 else 0
        return {
            "jumlah_materi_dibaca": len(self._data["materi_dibaca"]),
            "jumlah_sesi_latihan": len(self._data["riwayat_latihan"]),
            "total_soal_dikerjakan": total_kerjakan,
            "total_soal_benar": total_benar,
            "persentase_benar": persentase,
            "riwayat_5_terakhir": self._data["riwayat_latihan"][-5:],
        }

    def reset(self):
        self._data = {
            "materi_dibaca": [],
            "riwayat_latihan": [],
            "total_soal_benar": 0,
            "total_soal_dikerjakan": 0,
        }
        self.save()
