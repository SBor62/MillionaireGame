import tkinter as tk
from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class EndScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.master = master
        self.app = app
        self.bg_image = None
        self.pack(expand=True, fill=tk.BOTH)

        # Создаем Canvas с явными размерами
        self.canvas = tk.Canvas(self, highlightthickness=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_background()
        self.schedule_close()
        self.play_end_sound()

    def load_background(self):
        """Загружает фоновую картинку"""
        from PIL import Image, ImageTk
        import os

        image_path = "assets/backgrounds/end.png"
        if os.path.exists(image_path):
            # Ждем обновления размеров
            self.master.update_idletasks()

            # Получаем актуальные размеры
            width = self.master.winfo_width() or WINDOW_WIDTH
            height = self.master.winfo_height() or WINDOW_HEIGHT

            # Устанавливаем размер Canvas
            self.canvas.config(width=width, height=height)

            img = Image.open(image_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def play_end_sound(self):
        """Воспроизводит звук конца игры"""
        self.app.sound_manager.stop_all_sounds()
        self.app.sound_manager.play_sound("end", loop=True)

    def schedule_close(self):
        """Закрывает окно через 3 секунды"""
        self.after(3000, self.close_screen)

    def close_screen(self):
        """Полностью закрывает приложение"""
        self.master.destroy()
