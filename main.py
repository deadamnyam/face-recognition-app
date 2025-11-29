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
        self.root.configure(bg='#F0F8F0')  # Светло-зеленый нейтральный фон
        self.root.resizable(True, True)
        
        # Зелёная цветовая палитра
        self.colors = {
            'dark_bg': '#F0F8F0',  # Светло-зеленый нейтральный фон
            'card_bg': '#E8F5E8',  # Очень светлый зеленый для карточек
            'accent': '#22C55E',   # Насыщенный зеленый для кнопок
            'accent_hover': '#16A34A',  # Темно-зеленый при наведении
            'success': '#22C55E',
            'warning': '#EF4444',
            'text_primary': '#1F2937',  # Темно-серый для текста
            'text_secondary': '#6B7280',  # Серый для второстепенного текста
            'border': '#D1D5DB'  # Светло-серый для границ
        }
        
        self.is_camera_active = False
        self.camera = None
        
        self.show_welcome_screen()
    
    def create_rounded_button(self, parent, text, command, style='primary'):
        """Создает кнопку со скруглёнными углами"""
        if style == 'primary':
            bg = self.colors['accent']
            hover_bg = self.colors['accent_hover']
            fg = '#FFFFFF'  # Белый текст на зеленых кнопках
        else:
            bg = self.colors['card_bg']
            hover_bg = self.colors['border']
            fg = self.colors['text_primary']
        
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
            cursor='hand2',
            relief='flat',
            bd=0
        )
        
        # Анимация при наведении
        def on_enter(e):
            btn['bg'] = hover_bg
        def on_leave(e):
            btn['bg'] = bg
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def show_welcome_screen(self):
        """Стартовый экран с приветствием"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.colors['dark_bg'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Контент по центру
        content_frame = tk.Frame(main_container, bg=self.colors['dark_bg'])
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Логотип и заголовок
        logo_label = tk.Label(
            content_frame,
            text="🧠",
            font=("Arial", 48),
            bg=self.colors['dark_bg'],
            fg=self.colors['accent']  # Насыщенный зеленый для логотипа
        )
        logo_label.pack(pady=(0, 20))
        
        title_label = tk.Label(
            content_frame,
            text="FaceFlow AI",
            font=("Arial", 32, "bold"),
            bg=self.colors['dark_bg'],
            fg=self.colors['text_primary']
        )
        title_label.pack(pady=(0, 15))
        
        subtitle_label = tk.Label(
            content_frame,
            text="Интеллектуальная система распознавания лиц",
            font=("Arial", 14),
            bg=self.colors['dark_bg'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Кнопка запуска
        start_btn = self.create_rounded_button(
            content_frame,
            "🎭 Начать идентификацию",
            self.show_camera_screen
        )
        start_btn.pack(pady=20)
        
        # Футер
        footer_label = tk.Label(
            content_frame,
            text="Разработано с ❤️ Анной, Марией и Полиной",
            font=("Arial", 10),
            bg=self.colors['dark_bg'],
            fg=self.colors['text_secondary']
        )
        footer_label.pack(pady=(40, 0))
    
    def show_camera_screen(self):
        """Минималистичный экран камеры"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Основной контент
        main_frame = tk.Frame(self.root, bg=self.colors['dark_bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Левая панель - видео (без заголовка)
        left_frame = tk.Frame(main_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Контейнер для видео с отступами
        self.video_container = tk.Frame(left_frame, bg='#1F2937', height=500)  # Темный фон для видео
        self.video_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.video_label = tk.Label(self.video_container, bg='#1F2937')
        self.video_label.pack(expand=True)
        
        # Правая панель - управление
        right_frame = tk.Frame(main_frame, bg=self.colors['card_bg'], width=280)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        right_frame.pack_propagate(False)
        
        # Заголовок управления
        control_title = tk.Label(
            right_frame,
            text="Управление",
            font=("Arial", 14, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary'],
            pady=20
        )
        control_title.pack(fill=tk.X)
        
        # Контент управления
        control_content = tk.Frame(right_frame, bg=self.colors['card_bg'])
        control_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Кнопки управления
        self.start_btn = self.create_rounded_button(
            control_content,
            "▶️ Запуск камеры",
            self.start_camera
        )
        self.start_btn.pack(fill=tk.X, pady=8)
        
        self.stop_btn = self.create_rounded_button(
            control_content,
            "⏹️ Остановить",
            self.stop_camera
        )
        self.stop_btn.pack(fill=tk.X, pady=8)
        self.stop_btn.config(state=tk.DISABLED)
        
        # Разделитель
        separator = tk.Frame(control_content, height=2, bg=self.colors['border'])
        separator.pack(fill=tk.X, pady=20)
        
        # Статус системы
        status_title = tk.Label(
            control_content,
            text="Статус системы:",
            font=("Arial", 11, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_secondary']
        )
        status_title.pack(anchor=tk.W, pady=(0, 5))
        
        self.status_indicator = tk.Label(
            control_content,
            text="● Ожидание",
            font=("Arial", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['warning']
        )
        self.status_indicator.pack(anchor=tk.W)
        
        # Информационная панель
        info_title = tk.Label(
            control_content,
            text="Лог системы:",
            font=("Arial", 11, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_secondary'],
            pady=20
        )
        info_title.pack(anchor=tk.W)
        
        # Текстовое поле с прокруткой
        text_frame = tk.Frame(control_content, bg='#FFFFFF')  # Белый фон для текстового поля
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.info_text = tk.Text(
            text_frame,
            height=8,
            font=("Consolas", 9),
            bg='#FFFFFF',
            fg=self.colors['text_primary'],
            wrap=tk.WORD,
            border=0,
            padx=10,
            pady=10,
            relief='flat'
        )
        
        scrollbar = tk.Scrollbar(text_frame, command=self.info_text.yview)
        self.info_text.config(yscrollcommand=scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Начальные сообщения
        self.add_info("🟢 Система инициализирована")
        self.add_info("📷 Готов к работе с камерой")
        self.add_info("💚 Нажмите 'Запуск камеры'")
    
    def add_info(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)
    
    def start_camera(self):
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                messagebox.showerror("Ошибка", "Не удалось подключиться к камере!")
                return
            
            self.is_camera_active = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_indicator.config(text="● Активен", fg=self.colors['success'])
            self.add_info("🎥 Камера запущена")
            self.add_info("👁️ Анализ изображения...")
            
            self.update_video()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при запуске камеры: {str(e)}")
    
    def stop_camera(self):
        self.is_camera_active = False
        if self.camera:
            self.camera.release()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_indicator.config(text="● Ожидание", fg=self.colors['warning'])
        self.add_info("⏹️ Камера остановлена")
    
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


