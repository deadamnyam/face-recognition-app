import tkinter as tk


class CameraScreen:
    """Класс для экрана камеры"""

    def __init__(self, root, ui_config, app):
        self.root = root
        self.ui_config = ui_config
        self.app = app

    def show(self):
        """Показывает экран камеры"""
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg=self.ui_config.colors["dark_bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Левая панель - видео
        left_frame = tk.Frame(
            main_frame, bg=self.ui_config.colors["card_bg"], relief="flat", bd=0
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        self.video_container = tk.Frame(left_frame, bg="#1F2937", height=500)
        self.video_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.video_label = tk.Label(self.video_container, bg="#1F2937")
        self.video_label.pack(expand=True)

        # Правая панель - управление
        self._create_control_panel(main_frame)

    def _create_control_panel(self, main_frame):
        """Создает панель управления"""
        right_frame = tk.Frame(
            main_frame, bg=self.ui_config.colors["card_bg"], width=280
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        right_frame.pack_propagate(False)

        control_title = tk.Label(
            right_frame,
            text="Управление",
            font=("Arial", 14, "bold"),
            bg=self.ui_config.colors["card_bg"],
            fg=self.ui_config.colors["text_primary"],
            pady=20,
        )
        control_title.pack(fill=tk.X)

        control_content = tk.Frame(right_frame, bg=self.ui_config.colors["card_bg"])
        control_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Кнопки управления
        self.app.start_btn = self.app.create_rounded_button(
            control_content, "▶️ Запуск камеры", self.app.start_camera
        )
        self.app.start_btn.pack(fill=tk.X, pady=8)

        self.app.stop_btn = self.app.create_rounded_button(
            control_content, "⏹️ Остановить", self.app.stop_camera
        )
        self.app.stop_btn.pack(fill=tk.X, pady=8)
        self.app.stop_btn.config(state=tk.DISABLED)

        # Кнопка "Познакомиться" под "Остановить"
        meet_btn = self.app.create_rounded_button(
            control_content,
            "👋 Познакомиться",
            self.app.show_meet_dialog,
            style="secondary",
        )
        meet_btn.pack(fill=tk.X, pady=8)

        separator = tk.Frame(
            control_content, height=2, bg=self.ui_config.colors["border"]
        )
        separator.pack(fill=tk.X, pady=20)

        self._create_status_panel(control_content)
        self._create_info_panel(control_content)

    def _create_status_panel(self, parent):
        """Создает панель статуса"""
        status_title = tk.Label(
            parent,
            text="Статус системы:",
            font=("Arial", 11, "bold"),
            bg=self.ui_config.colors["card_bg"],
            fg=self.ui_config.colors["text_secondary"],
        )
        status_title.pack(anchor=tk.W, pady=(0, 5))

        self.app.status_indicator = tk.Label(
            parent,
            text="● Ожидание",
            font=("Arial", 11),
            bg=self.ui_config.colors["card_bg"],
            fg=self.ui_config.colors["warning"],
        )
        self.app.status_indicator.pack(anchor=tk.W)

    def _create_info_panel(self, parent):
        """Создает информационную панель"""
        info_title = tk.Label(
            parent,
            text="Лог системы:",
            font=("Arial", 11, "bold"),
            bg=self.ui_config.colors["card_bg"],
            fg=self.ui_config.colors["text_secondary"],
            pady=20,
        )
        info_title.pack(anchor=tk.W)

        text_frame = tk.Frame(parent, bg="#FFFFFF")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.app.info_text = tk.Text(
            text_frame,
            height=8,
            font=("Consolas", 9),
            bg="#FFFFFF",
            fg=self.ui_config.colors["text_primary"],
            wrap=tk.WORD,
            border=0,
            padx=10,
            pady=10,
            relief="flat",
        )

        scrollbar = tk.Scrollbar(text_frame, command=self.app.info_text.yview)
        self.app.info_text.config(yscrollcommand=scrollbar.set)

        self.app.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.app.add_info("🟢 Система инициализирована")
        self.app.add_info("📷 Готов к работе с камерой")
        self.app.add_info("💚 Нажмите 'Запуск камеры'")
