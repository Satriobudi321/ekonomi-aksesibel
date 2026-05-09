"""
core/content_loader.py

Parser materi dan soal Markdown.

Struktur folder:
data/
├── materi/
│   ├── kelas_10/
│   │   ├── 01_konsep_dasar.md
│   │   └── 02_biaya_peluang.md
│   ├── kelas_11/
│   └── kelas_12/
└── soal/
    ├── kelas_10/
    │   ├── 01_konsep_dasar.md
    │   └── 02_biaya_peluang.md
    ├── kelas_11/
    └── kelas_12/

Materi mendukung link video markdown.
Soal pakai format ## Soal X dengan pilihan bertanda * untuk yang benar.
"""

import json
import os
import re
import sys


def _get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = _get_base_dir()
MATERI_DIR = os.path.join(BASE_DIR, "data", "materi")
SOAL_DIR = os.path.join(BASE_DIR, "data", "soal")


# Pattern untuk markdown link
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((https?://[^\s\)]+)\)")


def list_kelas():
    return ["10", "11", "12"]


# ==================== MATERI ====================

def _ekstrak_link(teks):
    """Ekstrak link markdown dari teks. Return (teks_bersih, list_links)."""
    links = []

    def _proses_match(match):
        label = match.group(1).strip()
        url = match.group(2).strip()
        tipe = "link"
        label_lower = label.lower()
        if (label_lower.startswith("video:") or "youtube.com" in url
                or "youtu.be" in url):
            tipe = "video"
        elif label_lower.startswith("audio:"):
            tipe = "audio"
        links.append({"label": label, "url": url, "tipe": tipe})
        return f"[{label}]"

    teks_bersih = LINK_PATTERN.sub(_proses_match, teks)
    return teks_bersih, links


def _parse_materi_md(content):
    """Parse file markdown materi."""
    lines = content.split("\n")
    judul = ""
    konten_lines = []
    sub_bab = []
    current_sub = None
    semua_links = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("# ") and not judul:
            judul = stripped[2:].strip()
        elif stripped.startswith("## "):
            if current_sub:
                isi_raw = "\n".join(current_sub["isi_lines"]).strip()
                isi_bersih, links = _ekstrak_link(isi_raw)
                current_sub["isi"] = isi_bersih
                current_sub["links"] = links
                semua_links.extend(links)
                del current_sub["isi_lines"]
                sub_bab.append(current_sub)
            current_sub = {"judul": stripped[3:].strip(), "isi_lines": []}
        elif current_sub is not None:
            current_sub["isi_lines"].append(line)
        elif judul:
            konten_lines.append(line)

    if current_sub:
        isi_raw = "\n".join(current_sub["isi_lines"]).strip()
        isi_bersih, links = _ekstrak_link(isi_raw)
        current_sub["isi"] = isi_bersih
        current_sub["links"] = links
        semua_links.extend(links)
        del current_sub["isi_lines"]
        sub_bab.append(current_sub)

    konten_raw = "\n".join(konten_lines).strip()
    konten_bersih, konten_links = _ekstrak_link(konten_raw)
    semua_links = konten_links + semua_links

    return {
        "judul": judul or "Tanpa Judul",
        "konten": konten_bersih,
        "sub_bab": sub_bab,
        "links": semua_links,
    }


def load_materi(kelas):
    """Muat semua bab materi .md untuk kelas."""
    folder = os.path.join(MATERI_DIR, f"kelas_{kelas}")
    bab_list = []

    if os.path.isdir(folder):
        try:
            files = sorted(
                f for f in os.listdir(folder)
                if f.lower().endswith(".md")
            )
            for i, fname in enumerate(files, start=1):
                filepath = os.path.join(folder, fname)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    parsed = _parse_materi_md(content)
                    parsed["id"] = i
                    parsed["filename"] = fname
                    bab_list.append(parsed)
                except IOError as e:
                    print(f"Error baca {filepath}: {e}")
        except OSError as e:
            print(f"Error akses folder {folder}: {e}")

    # Fallback ke format JSON lama
    if not bab_list:
        old_filepath = os.path.join(MATERI_DIR, f"kelas_{kelas}.json")
        if os.path.exists(old_filepath):
            try:
                with open(old_filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                bab_list = data.get("bab", [])
                for bab in bab_list:
                    bab.setdefault("links", [])
            except (json.JSONDecodeError, IOError):
                pass

    return bab_list


def get_materi_info(kelas):
    folder = os.path.join(MATERI_DIR, f"kelas_{kelas}")
    if os.path.isdir(folder):
        try:
            count = sum(
                1 for f in os.listdir(folder)
                if f.lower().endswith(".md")
            )
            return {
                "judul": f"Ekonomi Kelas {kelas}",
                "deskripsi": f"{count} bab tersedia",
            }
        except OSError:
            pass
    return {"judul": f"Ekonomi Kelas {kelas}", "deskripsi": ""}


# ==================== SOAL ====================

def _parse_soal_md(content):
    """
    Parse file markdown soal.

    Format:
        # Judul Bab Soal

        ## Soal 1
        Pertanyaan di sini?
        - Pilihan A
        * Pilihan B (yang benar)
        - Pilihan C
        - Pilihan D
        Pembahasan: penjelasan jawaban.

        ## Soal 2
        ...

    Return: {
        "judul": "...",
        "soal": [
            {
                "pertanyaan": "...",
                "pilihan": ["...", ...],
                "jawaban": index_int,
                "pembahasan": "..."
            }
        ]
    }
    """
    lines = content.split("\n")
    judul_bab = ""
    soal_list = []
    current_soal = None
    state = "header"  # header | pertanyaan | pilihan | pembahasan

    def _commit_soal():
        """Selesaikan soal yang sedang diparse."""
        if current_soal is None:
            return
        # Gabungkan baris pertanyaan
        current_soal["pertanyaan"] = " ".join(
            current_soal["pertanyaan_lines"]
        ).strip()
        del current_soal["pertanyaan_lines"]
        # Hanya commit kalau punya pertanyaan dan minimal 2 pilihan
        if current_soal["pertanyaan"] and len(current_soal["pilihan"]) >= 2:
            # Default jawaban ke 0 kalau tidak ada yang ditandai *
            if current_soal["jawaban"] is None:
                current_soal["jawaban"] = 0
            soal_list.append(current_soal)

    for line in lines:
        stripped = line.strip()

        # Header bab
        if stripped.startswith("# ") and not judul_bab:
            judul_bab = stripped[2:].strip()
            continue

        # Soal baru
        if stripped.startswith("## "):
            _commit_soal()
            current_soal = {
                "pertanyaan_lines": [],
                "pilihan": [],
                "jawaban": None,
                "pembahasan": "",
            }
            state = "pertanyaan"
            continue

        if current_soal is None:
            continue

        # Pembahasan (prefix "Pembahasan:" atau "pembahasan:")
        if stripped.lower().startswith("pembahasan:"):
            current_soal["pembahasan"] = stripped.split(":", 1)[1].strip()
            state = "pembahasan"
            continue

        # Pilihan jawaban (- atau *)
        if stripped.startswith("* "):
            # Pilihan yang BENAR
            pilihan_text = stripped[2:].strip()
            current_soal["jawaban"] = len(current_soal["pilihan"])
            current_soal["pilihan"].append(pilihan_text)
            state = "pilihan"
            continue
        if stripped.startswith("- "):
            # Pilihan biasa
            pilihan_text = stripped[2:].strip()
            current_soal["pilihan"].append(pilihan_text)
            state = "pilihan"
            continue

        # Lanjutan pertanyaan
        if state == "pertanyaan" and stripped:
            current_soal["pertanyaan_lines"].append(stripped)
        elif state == "pembahasan" and stripped:
            # Pembahasan multi-baris
            if current_soal["pembahasan"]:
                current_soal["pembahasan"] += " " + stripped
            else:
                current_soal["pembahasan"] = stripped

    # Commit soal terakhir
    _commit_soal()

    return {
        "judul": judul_bab or "Soal Latihan",
        "soal": soal_list,
    }


def load_soal_per_bab(kelas):
    """
    Muat semua bab soal untuk kelas tertentu.
    Return: list of dict, setiap dict adalah satu bab dengan list soalnya.
    """
    folder = os.path.join(SOAL_DIR, f"kelas_{kelas}")
    bab_soal_list = []

    if os.path.isdir(folder):
        try:
            files = sorted(
                f for f in os.listdir(folder)
                if f.lower().endswith(".md")
            )
            for i, fname in enumerate(files, start=1):
                filepath = os.path.join(folder, fname)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    parsed = _parse_soal_md(content)
                    parsed["id"] = i
                    parsed["filename"] = fname
                    if parsed["soal"]:  # hanya kalau ada soal valid
                        bab_soal_list.append(parsed)
                except IOError as e:
                    print(f"Error baca {filepath}: {e}")
        except OSError as e:
            print(f"Error akses folder {folder}: {e}")

    # Fallback ke format JSON lama (semua soal jadi 1 bab)
    if not bab_soal_list:
        old_filepath = os.path.join(SOAL_DIR, f"kelas_{kelas}.json")
        if os.path.exists(old_filepath):
            try:
                with open(old_filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                soal = data.get("soal", [])
                if soal:
                    bab_soal_list.append({
                        "id": 1,
                        "judul": data.get("judul", f"Soal Kelas {kelas}"),
                        "soal": soal,
                        "filename": f"kelas_{kelas}.json",
                    })
            except (json.JSONDecodeError, IOError):
                pass

    return bab_soal_list


def load_soal(kelas):
    """
    Untuk kompatibilitas: muat semua soal sekaligus dari semua bab.
    Dipakai oleh tombol "latihan semua bab".
    """
    bab_soal_list = load_soal_per_bab(kelas)
    semua_soal = []
    for bab in bab_soal_list:
        semua_soal.extend(bab["soal"])
    return semua_soal


def get_soal_info(kelas):
    """Info ringkas jumlah bab soal yang tersedia."""
    folder = os.path.join(SOAL_DIR, f"kelas_{kelas}")
    if os.path.isdir(folder):
        try:
            count = sum(
                1 for f in os.listdir(folder)
                if f.lower().endswith(".md")
            )
            return {"jumlah_bab": count}
        except OSError:
            pass
    return {"jumlah_bab": 0}
