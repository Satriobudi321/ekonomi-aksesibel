"""
ui/theme.py

Tema visual aplikasi - terpusat untuk konsistensi.

Dirancang dengan prinsip:
- Kontras tinggi tapi tidak mata sakit (untuk siswa low-vision)
- Spacing lega (mudah dilihat dan diklik)
- Warna lembut yang nyaman dipandang lama
- Tetap kompatibel dengan mode kontras tinggi (Windows High Contrast)
"""

import wx


class Theme:
    """Tema visual yang konsisten untuk seluruh aplikasi."""

    def __init__(self, settings):
        self.settings = settings
        self.high_contrast = settings.get("high_contrast", False)
        self._setup_colors()

    def _setup_colors(self):
        if self.high_contrast:
            # Mode kontras tinggi: hitam + putih + kuning aksen
            self.BG_PRIMARY = wx.Colour(0, 0, 0)
            self.BG_SECONDARY = wx.Colour(20, 20, 20)
            self.BG_CARD = wx.Colour(30, 30, 30)
            self.FG_PRIMARY = wx.Colour(255, 255, 255)
            self.FG_SECONDARY = wx.Colour(220, 220, 220)
            self.FG_MUTED = wx.Colour(180, 180, 180)
            self.ACCENT = wx.Colour(255, 235, 60)  # kuning
            self.ACCENT_FG = wx.Colour(0, 0, 0)
            self.SUCCESS = wx.Colour(100, 255, 100)
            self.ERROR = wx.Colour(255, 100, 100)
            self.BORDER = wx.Colour(100, 100, 100)
        else:
            # Mode normal: warna lembut nyaman
            self.BG_PRIMARY = wx.Colour(248, 250, 253)    # putih kebiruan lembut
            self.BG_SECONDARY = wx.Colour(238, 242, 248)
            self.BG_CARD = wx.Colour(255, 255, 255)
            self.FG_PRIMARY = wx.Colour(28, 35, 50)        # navy gelap
            self.FG_SECONDARY = wx.Colour(64, 76, 100)
            self.FG_MUTED = wx.Colour(120, 132, 156)
            self.ACCENT = wx.Colour(45, 105, 195)          # biru sedang
            self.ACCENT_FG = wx.Colour(255, 255, 255)
            self.SUCCESS = wx.Colour(34, 130, 80)          # hijau
            self.ERROR = wx.Colour(200, 60, 60)            # merah
            self.BORDER = wx.Colour(210, 220, 232)

    def get_font_normal(self, size_offset=0):
        size = self.settings.get("font_size", 14) + size_offset
        return wx.Font(size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL, faceName="Segoe UI")

    def get_font_bold(self, size_offset=0):
        size = self.settings.get("font_size", 14) + size_offset
        return wx.Font(size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD, faceName="Segoe UI")

    def get_font_judul(self):
        size = self.settings.get("font_size", 14) + 8
        return wx.Font(size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD, faceName="Segoe UI")

    def get_font_subjudul(self):
        size = self.settings.get("font_size", 14) + 3
        return wx.Font(size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD, faceName="Segoe UI")

    def style_panel(self, panel):
        """Terapkan warna ke panel utama."""
        panel.SetBackgroundColour(self.BG_PRIMARY)

    def style_card(self, panel):
        """Terapkan warna untuk panel 'kartu' (background lebih terang)."""
        panel.SetBackgroundColour(self.BG_CARD)

    def style_label(self, label, level="primary"):
        """Style untuk wx.StaticText."""
        if level == "primary":
            label.SetForegroundColour(self.FG_PRIMARY)
        elif level == "secondary":
            label.SetForegroundColour(self.FG_SECONDARY)
        elif level == "muted":
            label.SetForegroundColour(self.FG_MUTED)
        elif level == "accent":
            label.SetForegroundColour(self.ACCENT)

    def style_button_primary(self, btn):
        """Tombol utama: warna aksen menonjol."""
        btn.SetBackgroundColour(self.ACCENT)
        btn.SetForegroundColour(self.ACCENT_FG)
        btn.SetFont(self.get_font_bold())

    def style_button_secondary(self, btn):
        """Tombol sekunder: warna lebih lembut."""
        btn.SetBackgroundColour(self.BG_SECONDARY)
        btn.SetForegroundColour(self.FG_PRIMARY)
        btn.SetFont(self.get_font_normal())

    def style_listbox(self, listbox):
        listbox.SetBackgroundColour(self.BG_CARD)
        listbox.SetForegroundColour(self.FG_PRIMARY)
        listbox.SetFont(self.get_font_normal())

    def style_textbox(self, textbox):
        textbox.SetBackgroundColour(self.BG_CARD)
        textbox.SetForegroundColour(self.FG_PRIMARY)
        textbox.SetFont(self.get_font_normal())
