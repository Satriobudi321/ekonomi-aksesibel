"""
ui/main_window.py

Window utama dengan tema modern yang lebih menarik.
Tetap ramah NVDA - menggunakan komponen wx native.
"""

import wx
from core.progress import ProgressTracker
from ui.theme import Theme


class MainWindow(wx.Frame):
    def __init__(self, parent, title, settings, tts):
        super().__init__(parent, title=title, size=(900, 700))
        self.settings = settings
        self.tts = tts
        self.theme = Theme(settings)
        self.progress = ProgressTracker(user_id=settings.get("current_user", "siswa"))

        # Set ikon dan ukuran minimum
        self.SetMinSize((700, 550))

        self._build_ui()
        self._bind_events()
        self.Centre()

        wx.CallAfter(self.btn_materi.SetFocus)

    def _build_ui(self):
        # Panel utama
        self.panel = wx.Panel(self)
        self.theme.style_panel(self.panel)

        # Sizer utama dengan padding besar
        outer = wx.BoxSizer(wx.VERTICAL)
        outer.AddSpacer(30)

        # ----- Header dengan judul besar dan subtitle -----
        header_box = wx.BoxSizer(wx.VERTICAL)

        judul = wx.StaticText(self.panel, label="Ekonomi Aksesibel")
        judul.SetFont(self.theme.get_font_judul())
        self.theme.style_label(judul, "primary")
        judul.SetName("Judul aplikasi: Ekonomi Aksesibel")
        header_box.Add(judul, 0, wx.ALIGN_CENTER)

        header_box.AddSpacer(8)

        subjudul = wx.StaticText(
            self.panel,
            label="Aplikasi Belajar Ekonomi SMA untuk Siswa Tunanetra"
        )
        subjudul.SetFont(self.theme.get_font_normal(size_offset=2))
        self.theme.style_label(subjudul, "secondary")
        header_box.Add(subjudul, 0, wx.ALIGN_CENTER)

        outer.Add(header_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 40)
        outer.AddSpacer(25)

        # ----- Garis pemisah -----
        line = wx.StaticLine(self.panel)
        outer.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 60)
        outer.AddSpacer(25)

        # ----- Instruksi navigasi -----
        instruksi = wx.StaticText(
            self.panel,
            label="MENU UTAMA"
        )
        instruksi.SetFont(self.theme.get_font_bold())
        self.theme.style_label(instruksi, "muted")
        outer.Add(instruksi, 0, wx.ALIGN_CENTER)

        outer.AddSpacer(5)

        info = wx.StaticText(
            self.panel,
            label="Tab untuk berpindah, Enter untuk memilih, F1 untuk bantuan"
        )
        info.SetFont(self.theme.get_font_normal(size_offset=-1))
        self.theme.style_label(info, "muted")
        outer.Add(info, 0, wx.ALIGN_CENTER)

        outer.AddSpacer(25)

        # ----- Tombol-tombol menu (lebih besar, lebih lega) -----
        button_grid = wx.BoxSizer(wx.VERTICAL)

        self.btn_materi = self._buat_tombol_menu(
            "1. Pilih Materi Pelajaran",
            "Buka materi ekonomi kelas 10, 11, atau 12",
            primary=True,
        )
        button_grid.Add(self.btn_materi, 0, wx.EXPAND | wx.BOTTOM, 12)

        self.btn_soal = self._buat_tombol_menu(
            "2. Latihan Soal",
            "Kerjakan soal pilihan ganda per bab",
            primary=True,
        )
        button_grid.Add(self.btn_soal, 0, wx.EXPAND | wx.BOTTOM, 12)

        self.btn_progress = self._buat_tombol_menu(
            "3. Lihat Progress Belajar",
            "Lihat ringkasan kemajuan belajar Anda",
        )
        button_grid.Add(self.btn_progress, 0, wx.EXPAND | wx.BOTTOM, 12)

        self.btn_pengaturan = self._buat_tombol_menu(
            "4. Pengaturan",
            "Atur ukuran font, kecepatan suara, dan tampilan",
        )
        button_grid.Add(self.btn_pengaturan, 0, wx.EXPAND | wx.BOTTOM, 12)

        self.btn_keluar = self._buat_tombol_menu(
            "5. Keluar",
            "Tutup aplikasi",
        )
        button_grid.Add(self.btn_keluar, 0, wx.EXPAND)

        outer.Add(button_grid, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 80)
        outer.AddSpacer(20)
        outer.AddStretchSpacer()

        # Status bar
        self.CreateStatusBar()
        self.SetStatusText("Siap. Tekan F1 untuk bantuan keyboard.")

        # Menu bar
        self._buat_menu_bar()

        self.panel.SetSizer(outer)
        self.panel.Layout()

    def _buat_tombol_menu(self, label, help_text, primary=False):
        """
        Buat tombol menu yang lebih besar dan menarik.
        Tetap pakai wx.Button standar agar NVDA bisa membacanya.
        """
        # Format label dengan accelerator pada angka pertama
        label_with_accel = "&" + label
        btn = wx.Button(self.panel, label=label_with_accel, size=(-1, 56))
        btn.SetFont(self.theme.get_font_bold(size_offset=2))

        if primary:
            self.theme.style_button_primary(btn)
        else:
            self.theme.style_button_secondary(btn)

        btn.SetHelpText(help_text)
        return btn

    def _buat_menu_bar(self):
        menubar = wx.MenuBar()

        menu_file = wx.Menu()
        item_keluar = menu_file.Append(wx.ID_EXIT, "&Keluar\tCtrl+Q",
                                       "Keluar dari aplikasi")
        self.Bind(wx.EVT_MENU, lambda e: self._keluar(), item_keluar)
        menubar.Append(menu_file, "&Berkas")

        menu_navigasi = wx.Menu()
        item_materi = menu_navigasi.Append(wx.ID_ANY, "Pilih &Materi\tAlt+1")
        item_soal = menu_navigasi.Append(wx.ID_ANY, "Latihan &Soal\tAlt+2")
        item_progress = menu_navigasi.Append(wx.ID_ANY, "Lihat &Progress\tAlt+3")
        item_pengaturan = menu_navigasi.Append(wx.ID_ANY, "Pen&gaturan\tAlt+4")
        self.Bind(wx.EVT_MENU, lambda e: self._buka_materi(), item_materi)
        self.Bind(wx.EVT_MENU, lambda e: self._buka_soal(), item_soal)
        self.Bind(wx.EVT_MENU, lambda e: self._buka_progress(), item_progress)
        self.Bind(wx.EVT_MENU, lambda e: self._buka_pengaturan(), item_pengaturan)
        menubar.Append(menu_navigasi, "&Navigasi")

        menu_bantuan = wx.Menu()
        item_bantuan = menu_bantuan.Append(wx.ID_HELP, "&Bantuan Keyboard\tF1")
        item_tentang = menu_bantuan.Append(wx.ID_ABOUT, "&Tentang Aplikasi")
        self.Bind(wx.EVT_MENU, lambda e: self._tampilkan_bantuan(), item_bantuan)
        self.Bind(wx.EVT_MENU, lambda e: self._tampilkan_tentang(), item_tentang)
        menubar.Append(menu_bantuan, "&Bantuan")

        self.SetMenuBar(menubar)

    def _bind_events(self):
        self.btn_materi.Bind(wx.EVT_BUTTON, lambda e: self._buka_materi())
        self.btn_soal.Bind(wx.EVT_BUTTON, lambda e: self._buka_soal())
        self.btn_progress.Bind(wx.EVT_BUTTON, lambda e: self._buka_progress())
        self.btn_pengaturan.Bind(wx.EVT_BUTTON, lambda e: self._buka_pengaturan())
        self.btn_keluar.Bind(wx.EVT_BUTTON, lambda e: self._keluar())

        self.btn_materi.Bind(wx.EVT_SET_FOCUS,
            lambda e: self._on_focus(e, "Pilih materi pelajaran ekonomi"))
        self.btn_soal.Bind(wx.EVT_SET_FOCUS,
            lambda e: self._on_focus(e, "Mulai latihan soal pilihan ganda"))
        self.btn_progress.Bind(wx.EVT_SET_FOCUS,
            lambda e: self._on_focus(e, "Lihat progress belajar Anda"))
        self.btn_pengaturan.Bind(wx.EVT_SET_FOCUS,
            lambda e: self._on_focus(e, "Atur ukuran font dan kecepatan suara"))
        self.btn_keluar.Bind(wx.EVT_SET_FOCUS,
            lambda e: self._on_focus(e, "Keluar dari aplikasi"))

        self.Bind(wx.EVT_CLOSE, lambda e: self._keluar())
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)

    def _on_focus(self, event, status_msg):
        self.SetStatusText(status_msg)
        event.Skip()

    def _on_key(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_F1:
            self._tampilkan_bantuan()
        elif keycode == wx.WXK_ESCAPE:
            self._keluar()
        else:
            event.Skip()

    def _tampilkan_bantuan(self):
        teks = (
            "BANTUAN KEYBOARD\n\n"
            "NAVIGASI DASAR:\n"
            "  Tab : Pindah ke tombol berikutnya\n"
            "  Shift+Tab : Pindah ke tombol sebelumnya\n"
            "  Enter atau Spasi : Pilih tombol\n"
            "  Escape : Kembali atau keluar\n"
            "  F1 : Tampilkan bantuan ini\n\n"
            "SHORTCUT MENU UTAMA:\n"
            "  Alt+1 : Pilih Materi\n"
            "  Alt+2 : Latihan Soal\n"
            "  Alt+3 : Lihat Progress\n"
            "  Alt+4 : Pengaturan\n"
            "  Ctrl+Q : Keluar\n\n"
            "DI HALAMAN MATERI:\n"
            "  Panah : Pilih kelas, bab, atau video\n"
            "  Enter : Buka pilihan / putar video\n"
            "  Tombol Putar : Bacakan materi dengan suara\n\n"
            "DI HALAMAN SOAL:\n"
            "  Panah : Pilih jawaban A sampai D\n"
            "  Tombol Jawab : Submit jawaban"
        )
        wx.MessageBox(teks, "Bantuan Keyboard", wx.OK | wx.ICON_INFORMATION)

    def _tampilkan_tentang(self):
        teks = (
            "Ekonomi Aksesibel\n\n"
            "Aplikasi belajar ekonomi SMA untuk siswa tunanetra.\n"
            "Dibuat sebagai project akhir studi mahasiswa Pendidikan Ekonomi.\n\n"
            "Versi 4.0 - Tampilan Modern, Soal per Bab, Mendukung Video"
        )
        wx.MessageBox(teks, "Tentang Aplikasi", wx.OK | wx.ICON_INFORMATION)

    def _buka_materi(self):
        from ui.materi_window import MateriWindow
        self.tts.stop()
        dlg = MateriWindow(self, self.settings, self.tts, self.progress)
        dlg.ShowModal()
        dlg.Destroy()
        self.btn_materi.SetFocus()

    def _buka_soal(self):
        from ui.soal_window import SoalWindow
        self.tts.stop()
        dlg = SoalWindow(self, self.settings, self.tts, self.progress)
        dlg.ShowModal()
        dlg.Destroy()
        self.btn_soal.SetFocus()

    def _buka_progress(self):
        from ui.progress_window import ProgressWindow
        self.tts.stop()
        dlg = ProgressWindow(self, self.settings, self.tts, self.progress)
        dlg.ShowModal()
        dlg.Destroy()
        self.btn_progress.SetFocus()

    def _buka_pengaturan(self):
        from ui.pengaturan_window import PengaturanWindow
        self.tts.stop()
        dlg = PengaturanWindow(self, self.settings, self.tts,
                               on_change=self._refresh_theme)
        dlg.ShowModal()
        dlg.Destroy()
        self.btn_pengaturan.SetFocus()

    def _refresh_theme(self):
        """Dipanggil saat pengaturan berubah - rebuild UI dengan tema baru."""
        self.theme = Theme(self.settings)
        # Hapus panel lama dan rebuild
        for child in list(self.GetChildren()):
            if isinstance(child, wx.Panel):
                child.Destroy()
        self._build_ui()
        self._bind_events()
        self.Layout()
        self.Refresh()
        wx.CallAfter(self.btn_materi.SetFocus)

    def _keluar(self):
        self.tts.stop()
        dlg = wx.MessageDialog(
            self, "Yakin ingin keluar dari aplikasi?",
            "Konfirmasi Keluar", wx.YES_NO | wx.ICON_QUESTION
        )
        if dlg.ShowModal() == wx.ID_YES:
            self.settings.save()
            self.progress.save()
            self.Destroy()
        dlg.Destroy()
