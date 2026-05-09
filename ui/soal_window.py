"""
ui/soal_window.py

Latihan soal pilihan ganda - sekarang dengan pemilihan bab.
Alur: Pilih kelas -> pilih bab -> kerjakan soal -> hasil.
"""

import wx
import random
from core.content_loader import list_kelas, load_soal_per_bab, get_soal_info
from ui.theme import Theme


class SoalWindow(wx.Dialog):
    def __init__(self, parent, settings, tts, progress):
        super().__init__(parent, title="Latihan Soal",
                         size=(950, 750),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.settings = settings
        self.tts = tts
        self.progress = progress
        self.theme = Theme(settings)

        self.kelas_terpilih = None
        self.bab_soal_list = []  # daftar bab soal untuk kelas terpilih
        self.bab_terpilih = None
        self.daftar_soal = []
        self.soal_sekarang = 0
        self.jumlah_benar = 0

        self.SetBackgroundColour(self.theme.BG_PRIMARY)
        self._build_pilih_kelas()
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
        self.Centre()

    def _on_key(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        else:
            event.Skip()

    def _clear(self):
        if self.GetSizer():
            self.GetSizer().Clear(True)
            self.SetSizer(None)
        for child in list(self.GetChildren()):
            child.Destroy()

    def _add_header(self, vbox, judul_text, info_text=None):
        vbox.AddSpacer(20)
        judul = wx.StaticText(self, label=judul_text)
        judul.SetFont(self.theme.get_font_judul())
        self.theme.style_label(judul, "primary")
        vbox.Add(judul, 0, wx.ALIGN_CENTER | wx.ALL, 8)

        if info_text:
            info = wx.StaticText(self, label=info_text)
            info.SetFont(self.theme.get_font_normal())
            self.theme.style_label(info, "secondary")
            info.Wrap(850)
            vbox.Add(info, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 30)

        vbox.AddSpacer(10)
        line = wx.StaticLine(self)
        vbox.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 60)
        vbox.AddSpacer(15)

    def _add_button(self, parent_sizer, label, handler, primary=False):
        btn = wx.Button(self, label=label, size=(-1, 42))
        if primary:
            self.theme.style_button_primary(btn)
        else:
            self.theme.style_button_secondary(btn)
        btn.Bind(wx.EVT_BUTTON, handler)
        parent_sizer.Add(btn, 0, wx.ALL, 6)
        return btn

    # ---------- TAHAP 1: PILIH KELAS ----------
    def _build_pilih_kelas(self):
        self._clear()

        vbox = wx.BoxSizer(wx.VERTICAL)
        self._add_header(
            vbox, "Pilih Kelas",
            "Pilih kelas untuk latihan soal. Tekan Enter untuk lanjut."
        )

        self.list_kelas = wx.ListBox(self, style=wx.LB_SINGLE)
        self.theme.style_listbox(self.list_kelas)
        for kelas in list_kelas():
            info = get_soal_info(kelas)
            jumlah = info["jumlah_bab"]
            ket = f"({jumlah} bab soal)" if jumlah > 0 else "(belum ada soal)"
            self.list_kelas.Append(f"  Soal Kelas {kelas}  {ket}")
        self.list_kelas.SetSelection(0)
        vbox.Add(self.list_kelas, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 60)
        vbox.AddSpacer(15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        self._add_button(hbox, "&Lanjut Pilih Bab",
                         self._on_pilih_kelas, primary=True)
        self._add_button(hbox, "&Tutup",
                         lambda e: self.EndModal(wx.ID_CANCEL))
        hbox.AddStretchSpacer()
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        vbox.AddSpacer(15)

        self.SetSizer(vbox)
        self.Layout()

        self.list_kelas.Bind(wx.EVT_LISTBOX_DCLICK, self._on_pilih_kelas)
        wx.CallAfter(self.list_kelas.SetFocus)

    def _on_pilih_kelas(self, event):
        sel = self.list_kelas.GetSelection()
        if sel == wx.NOT_FOUND:
            return
        kelas = list_kelas()[sel]
        self.kelas_terpilih = kelas
        self.bab_soal_list = load_soal_per_bab(kelas)
        if not self.bab_soal_list:
            wx.MessageBox(
                f"Soal kelas {kelas} belum tersedia.",
                "Belum Tersedia", wx.OK | wx.ICON_WARNING
            )
            return
        self._build_pilih_bab()

    # ---------- TAHAP 2: PILIH BAB SOAL ----------
    def _build_pilih_bab(self):
        self._clear()

        vbox = wx.BoxSizer(wx.VERTICAL)
        self._add_header(
            vbox, f"Kelas {self.kelas_terpilih} - Pilih Bab Soal",
            "Pilih bab yang ingin dilatih, atau pilih 'Semua Bab' untuk gabungan."
        )

        self.list_bab = wx.ListBox(self, style=wx.LB_SINGLE)
        self.theme.style_listbox(self.list_bab)

        # Opsi pertama: semua bab
        total_soal = sum(len(bab["soal"]) for bab in self.bab_soal_list)
        self.list_bab.Append(f"  [SEMUA] Latihan Semua Bab  ({total_soal} soal)")

        # Tiap bab
        for i, bab in enumerate(self.bab_soal_list):
            judul = bab.get("judul", f"Bab {i+1}")
            # Buang prefix "Soal: " kalau ada
            if judul.lower().startswith("soal:"):
                judul = judul[5:].strip()
            self.list_bab.Append(
                f"  Bab {i+1}: {judul}  ({len(bab['soal'])} soal)"
            )

        self.list_bab.SetSelection(0)
        vbox.Add(self.list_bab, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 60)
        vbox.AddSpacer(15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        self._add_button(hbox, "&Mulai Latihan",
                         self._on_mulai, primary=True)
        self._add_button(hbox, "&Kembali ke Pilih Kelas",
                         lambda e: self._build_pilih_kelas())
        hbox.AddStretchSpacer()
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        vbox.AddSpacer(15)

        self.SetSizer(vbox)
        self.Layout()

        self.list_bab.Bind(wx.EVT_LISTBOX_DCLICK, self._on_mulai)
        wx.CallAfter(self.list_bab.SetFocus)

    def _on_mulai(self, event):
        sel = self.list_bab.GetSelection()
        if sel == wx.NOT_FOUND:
            return

        if sel == 0:
            # Semua bab
            self.daftar_soal = []
            for bab in self.bab_soal_list:
                self.daftar_soal.extend(bab["soal"])
            self.bab_terpilih = "semua"
        else:
            # Bab spesifik
            bab_idx = sel - 1
            self.daftar_soal = list(self.bab_soal_list[bab_idx]["soal"])
            self.bab_terpilih = bab_idx

        if not self.daftar_soal:
            wx.MessageBox("Tidak ada soal di pilihan ini.",
                          "Kosong", wx.OK | wx.ICON_WARNING)
            return

        random.shuffle(self.daftar_soal)
        self.soal_sekarang = 0
        self.jumlah_benar = 0
        self._tampilkan_soal()

    # ---------- TAHAP 3: KERJAKAN SOAL ----------
    def _tampilkan_soal(self):
        self._clear()
        soal = self.daftar_soal[self.soal_sekarang]
        total = len(self.daftar_soal)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(20)

        # Progress soal
        progress_text = wx.StaticText(
            self, label=f"SOAL {self.soal_sekarang + 1} DARI {total}"
        )
        progress_text.SetFont(self.theme.get_font_bold(size_offset=2))
        self.theme.style_label(progress_text, "accent")
        vbox.Add(progress_text, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # Progress bar visual
        gauge = wx.Gauge(self, range=total, size=(-1, 12))
        gauge.SetValue(self.soal_sekarang + 1)
        vbox.Add(gauge, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 60)

        vbox.AddSpacer(20)

        # Pertanyaan dalam frame
        label_q = wx.StaticText(self, label="PERTANYAAN")
        label_q.SetFont(self.theme.get_font_bold())
        self.theme.style_label(label_q, "muted")
        vbox.Add(label_q, 0, wx.LEFT | wx.RIGHT, 40)
        vbox.AddSpacer(5)

        # TextCtrl read-only agar NVDA bisa fokus dan baca per kata/baris
        # dengan panah, sama seperti halaman materi.
        pertanyaan_text = wx.TextCtrl(
            self,
            value=soal.get("pertanyaan", ""),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.TE_NO_VSCROLL | wx.BORDER_SIMPLE,
            size=(-1, 100)
        )
        pertanyaan_text.SetFont(self.theme.get_font_normal(size_offset=2))
        self.theme.style_textbox(pertanyaan_text)
        pertanyaan_text.SetName(f"Pertanyaan soal {self.soal_sekarang + 1}")
        vbox.Add(pertanyaan_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 40)

        # Simpan referensi untuk fokus awal
        self.pertanyaan_ctrl = pertanyaan_text

        vbox.AddSpacer(20)

        # RadioBox jawaban
        pilihan = soal.get("pilihan", [])
        huruf = ["A", "B", "C", "D", "E"]
        labels = [f"{huruf[i]}. {p}" for i, p in enumerate(pilihan)]

        self.radio_jawaban = wx.RadioBox(
            self,
            label="  Pilih satu jawaban  ",
            choices=labels,
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS,
        )
        self.radio_jawaban.SetFont(self.theme.get_font_normal(size_offset=1))
        self.radio_jawaban.SetForegroundColour(self.theme.FG_PRIMARY)
        self.radio_jawaban.SetBackgroundColour(self.theme.BG_PRIMARY)
        vbox.Add(self.radio_jawaban, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 40)

        vbox.AddStretchSpacer()
        vbox.AddSpacer(15)

        # Tombol aksi
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddSpacer(20)
        self._add_button(hbox, "&Jawab", self._on_jawab, primary=True)
        self._add_button(hbox, "&Dengar Pertanyaan", self._on_dengar)
        hbox.AddStretchSpacer()
        self._add_button(hbox, "&Berhenti", self._on_berhenti)
        hbox.AddSpacer(20)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        vbox.AddSpacer(15)

        self.SetSizer(vbox)
        self.Layout()

        # Fokus awal ke pertanyaan agar NVDA langsung bacakan isinya
        wx.CallAfter(self.pertanyaan_ctrl.SetFocus)

    def _on_dengar(self, event):
        soal = self.daftar_soal[self.soal_sekarang]
        teks = f"Soal {self.soal_sekarang + 1}. {soal.get('pertanyaan', '')}"
        huruf = ["A", "B", "C", "D", "E"]
        for i, p in enumerate(soal.get("pilihan", [])):
            teks += f". Pilihan {huruf[i]}: {p}"
        self.tts.speak(teks)

    def _on_jawab(self, event):
        idx = self.radio_jawaban.GetSelection()
        soal = self.daftar_soal[self.soal_sekarang]
        jawaban_benar = soal.get("jawaban", 0)
        huruf = ["A", "B", "C", "D", "E"]

        benar = (idx == jawaban_benar)
        if benar:
            self.jumlah_benar += 1
            judul_dlg = "Jawaban Benar"
            ikon = wx.ICON_INFORMATION
            pesan = f"Benar! Jawaban Anda {huruf[idx]} adalah tepat."
        else:
            judul_dlg = "Jawaban Kurang Tepat"
            ikon = wx.ICON_WARNING
            pesan = (
                f"Jawaban kurang tepat. Anda memilih {huruf[idx]}. "
                f"Jawaban yang benar adalah {huruf[jawaban_benar]}."
            )

        pembahasan = soal.get("pembahasan", "")
        if pembahasan:
            pesan += f"\n\nPembahasan:\n{pembahasan}"

        wx.MessageBox(pesan, judul_dlg, wx.OK | ikon)

        self.soal_sekarang += 1
        if self.soal_sekarang >= len(self.daftar_soal):
            self._tampilkan_hasil()
        else:
            self._tampilkan_soal()

    def _on_berhenti(self, event):
        dlg = wx.MessageDialog(
            self,
            "Yakin berhenti? Progress soal ini tidak disimpan.",
            "Konfirmasi", wx.YES_NO | wx.ICON_QUESTION
        )
        if dlg.ShowModal() == wx.ID_YES:
            self.tts.stop()
            self.EndModal(wx.ID_CANCEL)
        dlg.Destroy()

    # ---------- TAHAP 4: HASIL ----------
    def _tampilkan_hasil(self):
        self._clear()
        total = len(self.daftar_soal)
        persen = round((self.jumlah_benar / total) * 100, 1) if total > 0 else 0

        # Catat ke progress
        self.progress.catat_latihan(self.kelas_terpilih, self.jumlah_benar, total)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(40)

        # Judul hasil
        judul = wx.StaticText(self, label="HASIL LATIHAN")
        judul.SetFont(self.theme.get_font_bold())
        self.theme.style_label(judul, "muted")
        vbox.Add(judul, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        vbox.AddSpacer(20)

        # Skor besar
        skor_text = wx.StaticText(self, label=f"{persen}")
        skor_font = wx.Font(
            self.settings.get("font_size", 14) + 30,
            wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
            faceName="Segoe UI"
        )
        skor_text.SetFont(skor_font)
        if persen >= 80:
            skor_text.SetForegroundColour(self.theme.SUCCESS)
        elif persen >= 60:
            skor_text.SetForegroundColour(self.theme.ACCENT)
        else:
            skor_text.SetForegroundColour(self.theme.ERROR)
        vbox.Add(skor_text, 0, wx.ALIGN_CENTER)

        persen_label = wx.StaticText(self, label="POIN DARI 100")
        persen_label.SetFont(self.theme.get_font_bold(size_offset=-1))
        self.theme.style_label(persen_label, "muted")
        vbox.Add(persen_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        vbox.AddSpacer(25)

        # Detail
        detail = wx.StaticText(
            self,
            label=f"Anda menjawab {self.jumlah_benar} dari {total} soal dengan benar."
        )
        detail.SetFont(self.theme.get_font_normal(size_offset=2))
        self.theme.style_label(detail, "primary")
        vbox.Add(detail, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # Komentar
        if persen >= 80:
            komentar = "Hebat! Anda sangat memahami materi."
        elif persen >= 60:
            komentar = "Bagus! Pertahankan dan terus berlatih."
        elif persen >= 40:
            komentar = "Lumayan. Pelajari kembali bagian yang belum dipahami."
        else:
            komentar = "Jangan menyerah. Baca ulang materi lalu coba lagi."

        komentar_text = wx.StaticText(self, label=komentar)
        komentar_text.SetFont(self.theme.get_font_normal(size_offset=1))
        self.theme.style_label(komentar_text, "secondary")
        komentar_text.Wrap(700)
        vbox.Add(komentar_text, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        vbox.AddStretchSpacer()

        # Tombol
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        self._add_button(hbox, "&Latihan Lagi",
                         lambda e: self._restart(), primary=True)
        self._add_button(hbox, "&Pilih Bab Lain",
                         lambda e: self._build_pilih_bab())
        self._add_button(hbox, "&Tutup",
                         lambda e: self.EndModal(wx.ID_OK))
        hbox.AddStretchSpacer()
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        vbox.AddSpacer(20)

        self.SetSizer(vbox)
        self.Layout()

        # Bacakan hasil
        hasil_audio = (
            f"Hasil latihan. Anda menjawab {self.jumlah_benar} dari {total} "
            f"soal dengan benar. Nilai Anda {persen} poin. {komentar}"
        )
        self.tts.speak(hasil_audio)

    def _restart(self):
        random.shuffle(self.daftar_soal)
        self.soal_sekarang = 0
        self.jumlah_benar = 0
        self._tampilkan_soal()
