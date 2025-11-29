import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import random


class UIConfig:
    """Класс для хранения конфигурации UI"""

    def __init__(self):
        self.colors = {
            "dark_bg": "#F0F8F0",
            "card_bg": "#E8F5E8",
            "accent": "#22C55E",
            "accent_hover": "#16A34A",
            "success": "#22C55E",
            "warning": "#EF4444",
            "text_primary": "#1F2937",
            "text_secondary": "#6B7280",
            "border": "#D1D5DB",
        }


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

        # Кнопки
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


class MeetDialog:
    """Класс для диалога знакомства"""

    def __init__(self, root, ui_config, app):
        self.root = root
        self.ui_config = ui_config
        self.app = app

    def show(self):
        """Показывает диалог знакомства"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Знакомство")
        dialog.geometry("400x300")
        dialog.configure(bg=self.ui_config.colors["dark_bg"])
        dialog.resizable(False, False)

        dialog.transient(self.root)
        dialog.grab_set()

        self._create_dialog_content(dialog)

    def _create_dialog_content(self, dialog):
        """Создает содержимое диалога"""
        title_label = tk.Label(
            dialog,
            text="👋 Давайте познакомимся!",
            font=("Arial", 16, "bold"),
            bg=self.ui_config.colors["dark_bg"],
            fg=self.ui_config.colors["text_primary"],
            pady=20,
        )
        title_label.pack()

        # Поле для имени
        name_label = tk.Label(
            dialog,
            text="Как вас зовут?",
            font=("Arial", 11),
            bg=self.ui_config.colors["dark_bg"],
            fg=self.ui_config.colors["text_secondary"],
        )
        name_label.pack(pady=(10, 5))

        name_entry = tk.Entry(dialog, font=("Arial", 12), width=30)
        name_entry.pack(pady=5)
        name_entry.focus()

        # Поле для информации о себе
        info_label = tk.Label(
            dialog,
            text="Расскажите о себе (не обязательно):",
            font=("Arial", 11),
            bg=self.ui_config.colors["dark_bg"],
            fg=self.ui_config.colors["text_secondary"],
        )
        info_label.pack(pady=(20, 5))

        info_text = tk.Text(
            dialog, font=("Arial", 11), width=35, height=6, wrap=tk.WORD
        )
        info_text.pack(pady=5)

        def save_info():
            name = name_entry.get().strip()
            info = info_text.get("1.0", tk.END).strip()

            if name:
                self.app.add_info(f"👤 Пользователь: {name}")
                if info:
                    self.app.add_info(f"📝 Информация: {info}")
                messagebox.showinfo(
                    "Успех", f"Приятно познакомиться, {name}!", parent=dialog
                )
                dialog.destroy()
            else:
                messagebox.showwarning(
                    "Внимание", "Пожалуйста, введите имя", parent=dialog
                )

        save_btn = self.app.create_rounded_button(dialog, "💾 Сохранить", save_info)
        save_btn.pack(pady=20)

        def on_enter(event):
            save_info()

        name_entry.bind("<Return>", on_enter)


class ModernFaceRecognitionApp:
    """Главный класс приложения"""

    def __init__(self, root):
        self.root = root
        self.root.title("FaceFlow • AI Recognition")
        self.root.geometry("1000x700")

        self.ui_config = UIConfig()
        self.root.configure(bg=self.ui_config.colors["dark_bg"])
        self.root.resizable(True, True)

        self.is_camera_active = False
        self.camera = None

        # Создаем экземпляры классов экранов
        self.welcome_screen = WelcomeScreen(root, self.ui_config, self)
        self.camera_screen = CameraScreen(root, self.ui_config, self)
        self.meet_dialog = MeetDialog(root, self.ui_config, self)

        self.welcome_screen.show()

    def create_rounded_button(self, parent, text, command, style="primary"):
        """Создает кнопку со скруглёнными углами"""
        if style == "primary":
            bg = self.ui_config.colors["accent"]
            hover_bg = self.ui_config.colors["accent_hover"]
            fg = "#FFFFFF"
        else:
            bg = self.ui_config.colors["card_bg"]
            hover_bg = self.ui_config.colors["border"]
            fg = self.ui_config.colors["text_primary"]

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            bg=bg,
            fg=fg,
            border=0,
            padx=30,
            pady=12,
            cursor="hand2",
            relief="flat",
            bd=0,
        )

        def on_enter(e):
            btn["bg"] = hover_bg

        def on_leave(e):
            btn["bg"] = bg

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def show_welcome_screen(self):
        """Показывает стартовый экран"""
        self.welcome_screen.show()

    def show_camera_screen(self):
        """Показывает экран камеры"""
        self.camera_screen.show()

    def show_meet_dialog(self):
        """Показывает диалог знакомства"""
        self.meet_dialog.show()

    def add_info(self, message):
        """Добавляет сообщение в лог"""
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)

    def start_camera(self):
        """Запускает камеру"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                messagebox.showerror("Ошибка", "Не удалось подключиться к камере!")
                return

            self.is_camera_active = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_indicator.config(
                text="● Активен", fg=self.ui_config.colors["success"]
            )
            self.add_info("🎥 Камера запущена")
            self.add_info("👁️ Анализ изображения...")

            self.update_video()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при запуске камеры: {str(e)}")

    def stop_camera(self):
        """Останавливает камеру"""
        self.is_camera_active = False
        if self.camera:
            self.camera.release()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_indicator.config(
            text="● Ожидание", fg=self.ui_config.colors["warning"]
        )
        self.add_info("⏹️ Камера остановлена")

        # Очищаем изображение камеры
        self.camera_screen.video_label.configure(image="")
        self.camera_screen.video_label.config(bg="#1F2937")

    def update_video(self):
        """Обновляет видео с камеры"""
        if self.is_camera_active:
            ret, frame = self.camera.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                img = img.resize((640, 480), Image.Resampling.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)

                self.camera_screen.video_label.imgtk = imgtk
                self.camera_screen.video_label.configure(image=imgtk)

            self.root.after(15, self.update_video)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernFaceRecognitionApp(root)
    root.mainloop()
