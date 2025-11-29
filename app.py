import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

from config.ui_config import UIConfig
from screens.welcome_screen import WelcomeScreen
from screens.camera_screen import CameraScreen
from screens.meet_dialog import MeetDialog


class FaceRecognitionApp:
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
