"""
ui/materi_window.py

Materi window dengan tema modern.
Tetap mendukung daftar link video yang bisa di-Enter.
"""

import wx
import webbrowser
from core.content_loader import list_kelas, load_materi, get_materi_info
from ui.theme import Theme


class MateriWindow(wx.Dialog):
    def __init__(self, parent, settings, tts, progress):
        super().__init__(parent, title="Pilih Materi",
                         size=(950, 750),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.settings = settings
        self.tts = tts
        self.progress = progress
        self.theme = Theme(settings)

        self.kelas_terpilih = None
        self.bab_terpilih = None
        self.materi_list = []
        self.links_bab = []

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
        """Helper menambahkan header standar."""
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

        # Garis pemisah
        vbox.AddSpacer(10)
        line = wx.StaticLine(self)
        vbox.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 60)
        vbox.AddSpacer(15)

    def _add_button(self, parent_sizer, label, handler, primary=False):
        """Helper menambahkan tombol dengan style konsisten."""
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
            "Gunakan panah atas dan bawah untuk memilih kelas, lalu tekan Enter."
        )

        self.list_kelas = wx.ListBox(self, style=wx.LB_SINGLE)
        self.theme.style_listbox(self.list_kelas)
        for kelas in list_kelas():
            info_kelas = get_materi_info(kelas)
            self.list_kelas.Append(
                f"  Kelas {kelas} - {info_kelas['judul']}  ({info_kelas['deskripsi']})"
            )
        self.list_kelas.SetSelection(0)
        vbox.Add(self.list_kelas, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 60)

        vbox.AddSpacer(15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        self._add_button(hbox, "&Buka Materi Kelas Ini",
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
        self.materi_list = load_materi(kelas)
        if not self.materi_list:
            wx.MessageBox(
                f"Materi kelas {kelas} belum tersedia.",
                "Materi Belum Tersedia", wx.OK | wx.ICON_WARNING
            )
            return
        self._build_pilih_bab()

    # ---------- TAHAP 2: PILIH BAB ----------
    def _build_pilih_bab(self):
        self._clear()

        vbox = wx.BoxSizer(wx.VERTICAL)
        self._add_header(
            vbox, f"Kelas {self.kelas_terpilih} - Daftar Bab",
            "Pilih bab dengan panah atas-bawah, tekan Enter untuk membuka."
        )

        self.list_bab = wx.ListBox(self, style=wx.LB_SINGLE)
        self.theme.style_listbox(self.list_bab)
        for i, bab in enumerate(self.materi_list):
            sudah = self.progress.sudah_dibaca(
                self.kelas_terpilih, bab.get("id", i)
            )
            check_mark = "[V] " if sudah else "[  ] "
            jumlah_video = len(
                [l for l in bab.get("links", []) if l.get("tipe") == "video"]
            )
            video_info = f"  ({jumlah_video} video)" if jumlah_video > 0 else ""
            self.list_bab.Append(
                f"  {check_mark}Bab {i+1}: {bab.get('judul', '?')}{video_info}"
            )
        self.list_bab.SetSelection(0)
        vbox.Add(self.list_bab, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 60)

        vbox.AddSpacer(15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        self._add_button(hbox, "&Buka Bab Ini",
                         self._on_buka_bab, primary=True)
        self._add_button(hbox, "&Kembali ke Pilih Kelas",
                         lambda e: self._build_pilih_kelas())
        hbox.AddStretchSpacer()
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        vbox.AddSpacer(15)

        self.SetSizer(vbox)
        self.Layout()

        self.list_bab.Bind(wx.EVT_LISTBOX_DCLICK, self._on_buka_bab)
        wx.CallAfter(self.list_bab.SetFocus)

    def _on_buka_bab(self, event):
        sel = self.list_bab.GetSelection()
        if sel == wx.NOT_FOUND:
            return
        self.bab_terpilih = sel
        self._build_baca_materi()

    # ---------- TAHAP 3: BACA MATERI ----------
    def _build_baca_materi(self):
        self._clear()
        bab = self.materi_list[self.bab_terpilih]
        self.links_bab = bab.get("links", [])

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(15)

        # Judul bab dengan styling
        judul = wx.StaticText(self, label=bab.get("judul", "Materi"))
        judul.SetFont(self.theme.get_font_judul())
        self.theme.style_label(judul, "primary")
        judul.Wrap(900)
        vbox.Add(judul, 0, wx.LEFT | wx.RIGHT | wx.TOP, 30)

        # Info kecil
        info_meta = wx.StaticText(
            self,
            label=f"Bab {bab.get('id', '?')} dari Kelas {self.kelas_terpilih}"
        )
        info_meta.SetFont(self.theme.get_font_normal(size_offset=-1))
        self.theme.style_label(info_meta, "muted")
        vbox.Add(info_meta, 0, wx.LEFT | wx.RIGHT, 30)

        vbox.AddSpacer(10)
        line = wx.StaticLine(self)
        vbox.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        vbox.AddSpacer(10)

        # Susun konten teks
        konten = bab.get("konten", "")
        sub_bab = bab.get("sub_bab", [])
        teks_lengkap = f"{bab.get('judul', '')}\n\n{konten}\n\n"
        for sub in sub_bab:
            teks_lengkap += f"{sub.get('judul', '')}\n\n{sub.get('isi', '')}\n\n"

        label_teks = wx.StaticText(self, label="ISI MATERI")
        label_teks.SetFont(self.theme.get_font_bold())
        self.theme.style_label(label_teks, "muted")
        vbox.Add(label_teks, 0, wx.LEFT | wx.RIGHT, 30)
        vbox.AddSpacer(5)

        self.text_area = wx.TextCtrl(
            self,
            value=teks_lengkap,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.HSCROLL | wx.BORDER_SIMPLE
        )
        self.theme.style_textbox(self.text_area)
        self.text_area.SetName(f"Isi materi bab {bab.get('judul', '')}")
        # Tinggi teks lebih besar daripada bagian video
        vbox.Add(self.text_area, 3, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)

        self.teks_materi = teks_lengkap

        # ----- BAGIAN LINK VIDEO -----
        if self.links_bab:
            vbox.AddSpacer(15)
            label_video = wx.StaticText(
                self,
                label=f"VIDEO DAN LINK TAMBAHAN ({len(self.links_bab)})"
            )
            label_video.SetFont(self.theme.get_font_bold())
            self.theme.style_label(label_video, "muted")
            vbox.Add(label_video, 0, wx.LEFT | wx.RIGHT, 30)

            info_video = wx.StaticText(
                self,
                label="Pilih dengan panah, tekan Enter untuk membuka di browser."
            )
            info_video.SetFont(self.theme.get_font_normal(size_offset=-1))
            self.theme.style_label(info_video, "secondary")
            vbox.Add(info_video, 0, wx.LEFT | wx.RIGHT, 30)
            vbox.AddSpacer(5)

            self.list_link = wx.ListBox(self, style=wx.LB_SINGLE)
            self.theme.style_listbox(self.list_link)
            for link in self.links_bab:
                tipe_label = {
                    "video": "[VIDEO]",
                    "audio": "[AUDIO]",
                    "link": "[LINK]",
                }.get(link.get("tipe", "link"), "[LINK]")
                self.list_link.Append(f"  {tipe_label} {link['label']}")

            self.list_link.SetName("Daftar video dan link tambahan")
            vbox.Add(self.list_link, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)

            self.list_link.Bind(wx.EVT_LISTBOX_DCLICK, self._on_buka_link)
            self.list_link.Bind(wx.EVT_KEY_DOWN, self._on_link_key)

        # ----- TOMBOL KONTROL -----
        vbox.AddSpacer(15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddSpacer(20)
        self._add_button(hbox, "&Putar Pembacaan", self._on_putar, primary=True)
        self._add_button(hbox, "&Hentikan",
                         lambda e: self.tts.stop())
        if self.links_bab:
            self._add_button(hbox, "Buka &Video Pertama",
                             self._on_video_pertama)
        hbox.AddStretchSpacer()
        self._add_button(hbox, "Tandai &Selesai", self._on_tandai_selesai)
        self._add_button(hbox, "&Kembali",
                         lambda e: self._build_pilih_bab())
        hbox.AddSpacer(20)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        vbox.AddSpacer(10)

        self.SetSizer(vbox)
        self.Layout()

        wx.CallAfter(self.text_area.SetFocus)

    def _on_link_key(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self._on_buka_link(event)
        else:
            event.Skip()

    def _on_buka_link(self, event):
        sel = self.list_link.GetSelection()
        if sel == wx.NOT_FOUND or sel >= len(self.links_bab):
            return
        link = self.links_bab[sel]
        try:
            self.tts.stop()
            webbrowser.open(link["url"])
        except Exception as e:
            wx.MessageBox(
                f"Gagal membuka link:\n{link['url']}\n\nError: {e}",
                "Error", wx.OK | wx.ICON_ERROR
            )

    def _on_video_pertama(self, event):
        if not self.links_bab:
            return
        for link in self.links_bab:
            if link.get("tipe") == "video":
                try:
                    self.tts.stop()
                    webbrowser.open(link["url"])
                except Exception:
                    pass
                return
        try:
            self.tts.stop()
            webbrowser.open(self.links_bab[0]["url"])
        except Exception:
            pass

    def _on_putar(self, event):
        if hasattr(self, "teks_materi"):
            self.tts.speak(self.teks_materi)

    def _on_tandai_selesai(self, event):
        bab = self.materi_list[self.bab_terpilih]
        self.progress.tandai_materi_dibaca(
            self.kelas_terpilih, bab.get("id", self.bab_terpilih)
        )
        wx.MessageBox(
            "Bab ini telah ditandai selesai.",
            "Tersimpan", wx.OK | wx.ICON_INFORMATION
        )
