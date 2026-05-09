"""
ui/pengaturan_window.py

Pengaturan dengan tampilan modern.
"""

import wx
from ui.theme import Theme


class PengaturanWindow(wx.Dialog):
    def __init__(self, parent, settings, tts, on_change=None):
        super().__init__(parent, title="Pengaturan",
                         size=(800, 700),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.settings = settings
        self.tts = tts
        self.on_change = on_change
        self.theme = Theme(settings)
        self.changed = False

        self.SetBackgroundColour(self.theme.BG_PRIMARY)
        self._build_ui()
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
        self.Centre()

    def _on_key(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self._on_tutup(None)
        else:
            event.Skip()

    def _add_section(self, vbox, title, builder_func):
        """Helper bikin section pengaturan dengan judul."""
        label = wx.StaticText(self, label=title.upper())
        label.SetFont(self.theme.get_font_bold())
        self.theme.style_label(label, "muted")
        vbox.Add(label, 0, wx.LEFT | wx.TOP, 30)
        vbox.AddSpacer(8)

        # Builder content
        builder_func(vbox)

        vbox.AddSpacer(15)
        line = wx.StaticLine(self)
        vbox.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        vbox.AddSpacer(10)

    def _build_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(20)

        # Header
        judul = wx.StaticText(self, label="Pengaturan")
        judul.SetFont(self.theme.get_font_judul())
        self.theme.style_label(judul, "primary")
        vbox.Add(judul, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        info = wx.StaticText(self, label="Perubahan langsung tersimpan otomatis.")
        info.SetFont(self.theme.get_font_normal())
        self.theme.style_label(info, "secondary")
        vbox.Add(info, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        vbox.AddSpacer(15)
        line = wx.StaticLine(self)
        vbox.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        vbox.AddSpacer(15)

        # ----- UKURAN FONT -----
        def build_font(vbox):
            self.label_font = wx.StaticText(
                self, label=f"Ukuran saat ini: {self.settings.get('font_size', 14)}"
            )
            self.label_font.SetFont(self.theme.get_font_normal())
            self.theme.style_label(self.label_font, "primary")
            vbox.Add(self.label_font, 0, wx.LEFT | wx.RIGHT, 30)
            vbox.AddSpacer(5)

            self.slider_font = wx.Slider(
                self, value=self.settings.get("font_size", 14),
                minValue=10, maxValue=32,
                style=wx.SL_HORIZONTAL | wx.SL_LABELS,
            )
            self.slider_font.SetName("Ukuran font, antara 10 sampai 32")
            self.slider_font.Bind(wx.EVT_SLIDER, self._on_font_change)
            vbox.Add(self.slider_font, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)

        self._add_section(vbox, "Ukuran Font", build_font)

        # ----- KECEPATAN TTS -----
        def build_rate(vbox):
            self.label_rate = wx.StaticText(
                self, label=f"Kecepatan saat ini: {self.settings.get('tts_rate', 180)} kata per menit"
            )
            self.label_rate.SetFont(self.theme.get_font_normal())
            self.theme.style_label(self.label_rate, "primary")
            vbox.Add(self.label_rate, 0, wx.LEFT | wx.RIGHT, 30)
            vbox.AddSpacer(5)

            self.slider_rate = wx.Slider(
                self, value=self.settings.get("tts_rate", 180),
                minValue=100, maxValue=300,
                style=wx.SL_HORIZONTAL | wx.SL_LABELS,
            )
            self.slider_rate.SetName("Kecepatan suara, antara 100 sampai 300")
            self.slider_rate.Bind(wx.EVT_SLIDER, self._on_rate_change)
            vbox.Add(self.slider_rate, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
            vbox.AddSpacer(8)

            btn_coba = wx.Button(self, label="&Coba Suara", size=(-1, 38))
            self.theme.style_button_primary(btn_coba)
            btn_coba.Bind(wx.EVT_BUTTON, self._on_coba_suara)
            vbox.Add(btn_coba, 0, wx.LEFT, 30)

        self._add_section(vbox, "Kecepatan Suara", build_rate)

        # ----- VOLUME -----
        def build_vol(vbox):
            self.label_vol = wx.StaticText(
                self,
                label=f"Volume saat ini: {int(self.settings.get('tts_volume', 1.0) * 100)} persen"
            )
            self.label_vol.SetFont(self.theme.get_font_normal())
            self.theme.style_label(self.label_vol, "primary")
            vbox.Add(self.label_vol, 0, wx.LEFT | wx.RIGHT, 30)
            vbox.AddSpacer(5)

            self.slider_vol = wx.Slider(
                self, value=int(self.settings.get("tts_volume", 1.0) * 100),
                minValue=10, maxValue=100,
                style=wx.SL_HORIZONTAL | wx.SL_LABELS,
            )
            self.slider_vol.SetName("Volume suara, dalam persen")
            self.slider_vol.Bind(wx.EVT_SLIDER, self._on_vol_change)
            vbox.Add(self.slider_vol, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)

        self._add_section(vbox, "Volume Suara", build_vol)

        # ----- KONTRAS TINGGI -----
        def build_kontras(vbox):
            self.cb_kontras = wx.CheckBox(
                self,
                label="&Mode Kontras Tinggi (latar hitam, teks putih)"
            )
            self.cb_kontras.SetFont(self.theme.get_font_normal())
            self.theme.style_label(self.cb_kontras, "primary")
            self.cb_kontras.SetValue(self.settings.get("high_contrast", False))
            self.cb_kontras.Bind(wx.EVT_CHECKBOX, self._on_kontras_change)
            vbox.Add(self.cb_kontras, 0, wx.LEFT | wx.RIGHT, 30)

            note = wx.StaticText(
                self,
                label="Catatan: perubahan kontras berlaku setelah Anda menutup pengaturan."
            )
            note.SetFont(self.theme.get_font_normal(size_offset=-2))
            self.theme.style_label(note, "muted")
            vbox.Add(note, 0, wx.LEFT | wx.RIGHT | wx.TOP, 30)

        self._add_section(vbox, "Tampilan", build_kontras)

        vbox.AddStretchSpacer()

        # Tombol
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        btn_tutup = wx.Button(self, label="&Simpan dan Tutup", size=(-1, 42))
        self.theme.style_button_primary(btn_tutup)
        btn_tutup.Bind(wx.EVT_BUTTON, self._on_tutup)
        hbox.Add(btn_tutup, 0, wx.ALL, 8)
        hbox.AddStretchSpacer()
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        vbox.AddSpacer(10)

        self.SetSizer(vbox)
        self.Layout()

        wx.CallAfter(self.slider_font.SetFocus)

    def _on_font_change(self, event):
        size = self.slider_font.GetValue()
        self.label_font.SetLabel(f"Ukuran saat ini: {size}")
        self.settings.set("font_size", size)
        self.changed = True

    def _on_rate_change(self, event):
        rate = self.slider_rate.GetValue()
        self.label_rate.SetLabel(f"Kecepatan saat ini: {rate} kata per menit")
        self.tts.set_rate(rate)
        self.settings.set("tts_rate", rate)

    def _on_vol_change(self, event):
        vol = self.slider_vol.GetValue() / 100.0
        self.label_vol.SetLabel(f"Volume saat ini: {int(vol * 100)} persen")
        self.tts.set_volume(vol)
        self.settings.set("tts_volume", vol)

    def _on_kontras_change(self, event):
        self.settings.set("high_contrast", self.cb_kontras.GetValue())
        self.changed = True

    def _on_coba_suara(self, event):
        self.tts.speak(
            f"Ini contoh suara pada kecepatan {self.slider_rate.GetValue()} "
            "kata per menit. Apakah suara ini terdengar nyaman?"
        )

    def _on_tutup(self, event):
        self.tts.stop()
        self.settings.save()
        if self.changed and self.on_change:
            self.on_change()
        self.EndModal(wx.ID_OK)
