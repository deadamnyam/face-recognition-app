import tkinter as tk
from tkinter import messagebox


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
