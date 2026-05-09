"""
ui/progress_window.py

Tampilan ringkasan progress belajar dengan visualisasi yang lebih menarik.
"""

import wx
from ui.theme import Theme


class ProgressWindow(wx.Dialog):
    def __init__(self, parent, settings, tts, progress):
        super().__init__(parent, title="Progress Belajar",
                         size=(900, 700),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.settings = settings
        self.tts = tts
        self.progress = progress
        self.theme = Theme(settings)

        self.SetBackgroundColour(self.theme.BG_PRIMARY)
        self._build_ui()
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
        self.Centre()

    def _on_key(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        else:
            event.Skip()

    def _add_stat_card(self, parent_sizer, label_text, value_text, accent=False):
        """Bikin 'kartu' statistik visual."""
        card = wx.Panel(self)
        card.SetBackgroundColour(self.theme.BG_CARD)

        card_sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(card, label=label_text)
        label.SetFont(self.theme.get_font_bold(size_offset=-2))
        self.theme.style_label(label, "muted")
        card_sizer.Add(label, 0, wx.ALL, 12)

        value = wx.StaticText(card, label=value_text)
        value_font = wx.Font(
            self.settings.get("font_size", 14) + 12,
            wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
            faceName="Segoe UI"
        )
        value.SetFont(value_font)
        if accent:
            value.SetForegroundColour(self.theme.ACCENT)
        else:
            self.theme.style_label(value, "primary")
        card_sizer.Add(value, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        card.SetSizer(card_sizer)
        parent_sizer.Add(card, 1, wx.EXPAND | wx.ALL, 6)
        return card

    def _build_ui(self):
        r = self.progress.ringkasan()

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(20)

        # Header
        judul = wx.StaticText(self, label="Progress Belajar Anda")
        judul.SetFont(self.theme.get_font_judul())
        self.theme.style_label(judul, "primary")
        vbox.Add(judul, 0, wx.ALIGN_CENTER | wx.ALL, 8)

        info = wx.StaticText(self, label="Ringkasan kemajuan dari semua latihan")
        info.SetFont(self.theme.get_font_normal())
        self.theme.style_label(info, "secondary")
        vbox.Add(info, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        vbox.AddSpacer(15)
        line = wx.StaticLine(self)
        vbox.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 60)
        vbox.AddSpacer(20)

        # ----- KARTU STATISTIK -----
        # Baris 1: Materi & Sesi
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(30)
        self._add_stat_card(
            row1, "MATERI DIBACA",
            f"{r['jumlah_materi_dibaca']} bab"
        )
        self._add_stat_card(
            row1, "SESI LATIHAN",
            f"{r['jumlah_sesi_latihan']} sesi"
        )
        row1.AddSpacer(30)
        vbox.Add(row1, 0, wx.EXPAND)

        # Baris 2: Total soal & Persentase
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.AddSpacer(30)
        self._add_stat_card(
            row2, "SOAL DIKERJAKAN",
            f"{r['total_soal_dikerjakan']}"
        )
        self._add_stat_card(
            row2, "JAWABAN BENAR",
            f"{r['total_soal_benar']}"
        )
        self._add_stat_card(
            row2, "PERSENTASE BENAR",
            f"{r['persentase_benar']}%",
            accent=True
        )
        row2.AddSpacer(30)
        vbox.Add(row2, 0, wx.EXPAND)

        vbox.AddSpacer(20)

        # ----- RIWAYAT LATIHAN -----
        label_riwayat = wx.StaticText(self, label="5 LATIHAN TERAKHIR")
        label_riwayat.SetFont(self.theme.get_font_bold())
        self.theme.style_label(label_riwayat, "muted")
        vbox.Add(label_riwayat, 0, wx.LEFT, 40)
        vbox.AddSpacer(5)

        # TextCtrl untuk daftar riwayat (NVDA-friendly)
        riwayat_text = ""
        if r["riwayat_5_terakhir"]:
            for i, sesi in enumerate(reversed(r["riwayat_5_terakhir"]), 1):
                tanggal = sesi.get("tanggal", "")[:10]
                riwayat_text += (
                    f"{i}. {tanggal} - Kelas {sesi.get('kelas', '?')}: "
                    f"{sesi.get('benar', 0)} dari {sesi.get('total', 0)} benar "
                    f"({sesi.get('persentase', 0)}%)\n"
                )
        else:
            riwayat_text = "Belum ada riwayat latihan. Yuk mulai latihan soal!"

        text_riwayat = wx.TextCtrl(
            self, value=riwayat_text,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.BORDER_SIMPLE
        )
        self.theme.style_textbox(text_riwayat)
        text_riwayat.SetName("Daftar 5 latihan terakhir")
        vbox.Add(text_riwayat, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 40)

        vbox.AddSpacer(15)

        # Tombol
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()

        btn_baca = wx.Button(self, label="&Bacakan dengan Suara", size=(-1, 42))
        self.theme.style_button_secondary(btn_baca)
        btn_baca.Bind(wx.EVT_BUTTON, lambda e: self._bacakan(r))
        hbox.Add(btn_baca, 0, wx.ALL, 6)

        btn_reset = wx.Button(self, label="&Reset Progress", size=(-1, 42))
        self.theme.style_button_secondary(btn_reset)
        btn_reset.Bind(wx.EVT_BUTTON, self._on_reset)
        hbox.Add(btn_reset, 0, wx.ALL, 6)

        btn_tutup = wx.Button(self, label="&Tutup", size=(-1, 42))
        self.theme.style_button_primary(btn_tutup)
        btn_tutup.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_OK))
        hbox.Add(btn_tutup, 0, wx.ALL, 6)

        hbox.AddStretchSpacer()
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        vbox.AddSpacer(15)

        self.SetSizer(vbox)
        self.Layout()
        wx.CallAfter(text_riwayat.SetFocus)

    def _bacakan(self, r):
        teks = (
            f"Ringkasan progress Anda. "
            f"Materi dibaca {r['jumlah_materi_dibaca']} bab. "
            f"Sesi latihan {r['jumlah_sesi_latihan']} sesi. "
            f"Total soal dikerjakan {r['total_soal_dikerjakan']}. "
            f"Jawaban benar {r['total_soal_benar']}. "
            f"Persentase keseluruhan {r['persentase_benar']} persen."
        )
        self.tts.speak(teks)

    def _on_reset(self, event):
        dlg = wx.MessageDialog(
            self,
            "Yakin ingin menghapus semua data progress?\n"
            "Tindakan ini tidak dapat dibatalkan.",
            "Konfirmasi Reset", wx.YES_NO | wx.ICON_WARNING
        )
        if dlg.ShowModal() == wx.ID_YES:
            self.progress.reset()
            wx.MessageBox("Progress telah direset.",
                          "Selesai", wx.OK | wx.ICON_INFORMATION)
            # Rebuild UI
            if self.GetSizer():
                self.GetSizer().Clear(True)
                self.SetSizer(None)
            for child in list(self.GetChildren()):
                child.Destroy()
            self._build_ui()
        dlg.Destroy()
