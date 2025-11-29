import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import random


class ModernFaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FaceFlow • AI Recognition")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0F0F23")
        self.root.resizable(True, True)

        # Современная цветовая палитра
        self.colors = {
            "dark_bg": "#0F0F23",
            "card_bg": "#1A1A2E",
            "accent": "#6C63FF",
            "accent_hover": "#7D76FF",
            "success": "#00D4AA",
            "warning": "#FF6B6B",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B0B0CC",
            "border": "#2D2D4D",
        }

        self.is_camera_active = False
        self.camera = None

        self.setup_styles()
        self.show_welcome_screen()

    def setup_styles(self):
        """Настраивает современные стили"""
        style = ttk.Style()
        style.theme_use("clam")

        # Настраиваем цвета для виджетов ttk
        style.configure("Modern.TFrame", background=self.colors["dark_bg"])
        style.configure(
            "Card.TFrame",
            background=self.colors["card_bg"],
            borderwidth=2,
            relief="flat",
        )

    def create_modern_button(self, parent, text, command, style="primary"):
        """Создает современную кнопку"""
        if style == "primary":
            bg = self.colors["accent"]
            hover_bg = self.colors["accent_hover"]
        else:
            bg = self.colors["card_bg"]
            hover_bg = self.colors["border"]

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            bg=bg,
            fg=self.colors["text_primary"],
            border=0,
            padx=30,
            pady=15,
            cursor="hand2",
            relief="flat",
        )

        # Анимация при наведении
        def on_enter(e):
            btn["bg"] = hover_bg

        def on_leave(e):
            btn["bg"] = bg

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def create_animated_card(self, parent, text, icon, command):
        """Создает анимированную карточку"""
        card = tk.Frame(parent, bg=self.colors["card_bg"], relief="flat", borderwidth=1)

        # Иконка
        icon_label = tk.Label(
            card,
            text=icon,
            font=("Arial", 24),
            bg=self.colors["card_bg"],
            fg=self.colors["accent"],
        )
        icon_label.pack(pady=(20, 10))

        # Текст
        text_label = tk.Label(
            card,
            text=text,
            font=("Arial", 11, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"],
            wraplength=150,
        )
        text_label.pack(pady=(0, 20))

        # Анимация при наведении
        def on_enter(e):
            card.configure(bg=self.colors["border"])
            for widget in card.winfo_children():
                widget.configure(bg=self.colors["border"])

        def on_leave(e):
            card.configure(bg=self.colors["card_bg"])
            for widget in card.winfo_children():
                widget.configure(bg=self.colors["card_bg"])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e: command())

        return card

    def show_welcome_screen(self):
        """Современный стартовый экран"""
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()

        # Основной контейнер с фоном
        main_container = tk.Frame(self.root, bg=self.colors["dark_bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Контент по центру
        content_frame = tk.Frame(main_container, bg=self.colors["dark_bg"])
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Логотип и заголовок
        logo_label = tk.Label(
            content_frame,
            text="🧠",
            font=("Arial", 48),
            bg=self.colors["dark_bg"],
            fg=self.colors["accent"],
        )
        logo_label.pack(pady=(0, 20))

        title_label = tk.Label(
            content_frame,
            text="FaceFlow AI",
            font=("Arial", 32, "bold"),
            bg=self.colors["dark_bg"],
            fg=self.colors["text_primary"],
        )
        title_label.pack(pady=(0, 15))

        subtitle_label = tk.Label(
            content_frame,
            text="Интеллектуальная система распознавания лиц",
            font=("Arial", 14),
            bg=self.colors["dark_bg"],
            fg=self.colors["text_secondary"],
        )
        subtitle_label.pack(pady=(0, 40))

        # Карточки возможностей
        features_frame = tk.Frame(content_frame, bg=self.colors["dark_bg"])
        features_frame.pack(pady=(0, 40))

        features = [
            ("🚀", "Мгновенное\nраспознавание"),
            ("👥", "Работа в\nреальном времени"),
            ("🔒", "Защита\nконфиденциальности"),
        ]

        for icon, text in features:
            card = self.create_animated_card(features_frame, text, icon, lambda: None)
            card.pack(side=tk.LEFT, padx=15)

        # Кнопка запуска
        start_btn = self.create_modern_button(
            content_frame, "🎭 Начать идентификацию", self.show_camera_screen
        )
        start_btn.pack(pady=20)

        # Футер
        footer_label = tk.Label(
            content_frame,
            text="Разработано с ❤️ Анной, Марией и Полиной",
            font=("Arial", 10),
            bg=self.colors["dark_bg"],
            fg=self.colors["text_secondary"],
        )
        footer_label.pack(pady=(40, 0))

    def show_camera_screen(self):
        """Современный экран камеры"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Верхняя панель
        header_frame = tk.Frame(self.root, bg=self.colors["card_bg"], height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        header_frame.pack_propagate(False)

        # Логотип и навигация
        back_btn = self.create_modern_button(
            header_frame, "← Назад", self.show_welcome_screen, style="secondary"
        )
        back_btn.pack(side=tk.LEFT, padx=10, pady=20)

        title_label = tk.Label(
            header_frame,
            text="🔍 Режим идентификации",
            font=("Arial", 18, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"],
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)

        # Основной контент
        main_frame = tk.Frame(self.root, bg=self.colors["dark_bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Левая панель - видео
        left_frame = tk.Frame(main_frame, bg=self.colors["card_bg"], relief="flat")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        video_header = tk.Label(
            left_frame,
            text="ВИДЕОПОТОК",
            font=("Arial", 12, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            pady=15,
        )
        video_header.pack(fill=tk.X)

        self.video_container = tk.Frame(
            left_frame, bg=self.colors["dark_bg"], height=500
        )
        self.video_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.video_label = tk.Label(self.video_container, bg=self.colors["dark_bg"])
        self.video_label.pack(expand=True)

        # Правая панель - управление
        right_frame = tk.Frame(main_frame, bg=self.colors["card_bg"], width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)

        # Панель управления
        control_header = tk.Label(
            right_frame,
            text="УПРАВЛЕНИЕ",
            font=("Arial", 12, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            pady=15,
        )
        control_header.pack(fill=tk.X)

        control_content = tk.Frame(right_frame, bg=self.colors["card_bg"])
        control_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.start_btn = self.create_modern_button(
            control_content, "▶️ Запуск камеры", self.start_camera
        )
        self.start_btn.pack(fill=tk.X, pady=5)

        self.stop_btn = self.create_modern_button(
            control_content, "⏹️ Остановить", self.stop_camera
        )
        self.stop_btn.pack(fill=tk.X, pady=5)
        self.stop_btn.config(state=tk.DISABLED)

        # Статус система
        status_frame = tk.Frame(control_content, bg=self.colors["card_bg"])
        status_frame.pack(fill=tk.X, pady=20)

        status_label = tk.Label(
            status_frame,
            text="СТАТУС СИСТЕМЫ:",
            font=("Arial", 10, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
        )
        status_label.pack(anchor=tk.W)

        self.status_indicator = tk.Label(
            status_frame,
            text="● Ожидание",
            font=("Arial", 10),
            bg=self.colors["card_bg"],
            fg=self.colors["warning"],
        )
        self.status_indicator.pack(anchor=tk.W, pady=(5, 0))

        # Информационная панель
        info_header = tk.Label(
            right_frame,
            text="ЛОГ СИСТЕМЫ",
            font=("Arial", 12, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            pady=15,
        )
        info_header.pack(fill=tk.X)

        info_container = tk.Frame(right_frame, bg=self.colors["card_bg"])
        info_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Стилизованное текстовое поле
        text_frame = tk.Frame(info_container, bg=self.colors["dark_bg"], relief="flat")
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.info_text = tk.Text(
            text_frame,
            height=10,
            font=("Consolas", 9),
            bg=self.colors["dark_bg"],
            fg=self.colors["text_primary"],
            wrap=tk.WORD,
            border=0,
            padx=10,
            pady=10,
        )

        scrollbar = tk.Scrollbar(text_frame, command=self.info_text.yview)
        self.info_text.config(yscrollcommand=scrollbar.set)

        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_info("🟢 Система инициализирована")
        self.add_info("📋 Готов к распознаванию лиц")
        self.add_info("💡 Нажмите 'Запуск камеры' для начала")

    def add_info(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.NORMAL)

    def start_camera(self):
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                messagebox.showerror("Ошибка", "Не удалось подключиться к камере!")
                return

            self.is_camera_active = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_indicator.config(text="● Активен", fg=self.colors["success"])
            self.add_info("🎥 Видеопоток активирован")
            self.add_info("👁️ Система анализирует изображение...")

            self.update_video()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при запуске камеры: {str(e)}")

    def stop_camera(self):
        self.is_camera_active = False
        if self.camera:
            self.camera.release()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_indicator.config(text="● Ожидание", fg=self.colors["warning"])
        self.add_info("⏹️ Видеопоток остановлен")

    def update_video(self):
        if self.is_camera_active:
            ret, frame = self.camera.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                img = img.resize((640, 480), Image.Resampling.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)

                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

            self.root.after(15, self.update_video)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernFaceRecognitionApp(root)
    root.mainloop()
