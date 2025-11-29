import tkinter as tk

class WelcomeScreen:
    """Класс для стартового экрана"""
    def __init__(self, root, ui_config, app):
        self.root = root
        self.ui_config = ui_config
        self.app = app
        
    def show(self):
        """Показывает стартовый экран"""
        for widget in self.root.winfo_children():
            widget.destroy()

        main_container = tk.Frame(self.root, bg=self.ui_config.colors["dark_bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        content_frame = tk.Frame(main_container, bg=self.ui_config.colors["dark_bg"])
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Логотип и заголовок
        logo_label = tk.Label(
            content_frame,
            text="🧠",
            font=("Arial", 48),
            bg=self.ui_config.colors["dark_bg"],
            fg=self.ui_config.colors["accent"],
        )
        logo_label.pack(pady=(0, 20))

        title_label = tk.Label(
            content_frame,
            text="FaceFlow AI",
            font=("Arial", 32, "bold"),
            bg=self.ui_config.colors["dark_bg"],
            fg=self.ui_config.colors["text_primary"],
        )
        title_label.pack(pady=(0, 15))

        subtitle_label = tk.Label(
            content_frame,
            text="Интеллектуальная система распознавания лиц",
            font=("Arial", 14),
            bg=self.ui_config.colors["dark_bg"],
            fg=self.ui_config.colors["text_secondary"],
        )
        subtitle_label.pack(pady=(0, 40))

        # Кнопка запуска
        start_btn = self.app.create_rounded_button(
            content_frame, "🎭 Начать идентификацию", self.app.show_camera_screen
        )
        start_btn.pack(pady=20)

        # Футер
        footer_label = tk.Label(
            content_frame,
            text="Разработано с ❤️ Анной, Марией и Полиной",
            font=("Arial", 10),
            bg=self.ui_config.colors["dark_bg"],
            fg=self.ui_config.colors["text_secondary"],
        )
        footer_label.pack(pady=(40, 0))