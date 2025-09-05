import tkinter as tk
from tkinter import font as tkfont
from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from PIL import Image, ImageTk
import os


class LeaderboardScreen(tk.Frame):
    def __init__(self, master, settings):
        super().__init__(master)
        self.master = master
        self.settings = settings
        self.pack(expand=True, fill=tk.BOTH)
        self.bg_image = None

        # Создаем Canvas для фоновой картинки
        self.canvas = tk.Canvas(self, highlightthickness=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Загружаем фоновую картинку
        self.load_background()
        self.create_widgets()

    def load_background(self):
        """Загружает фоновую картинку"""
        image_path = "assets/backgrounds/record.png"
        if os.path.exists(image_path):
            # Ждем пока окно отобразится и получит правильные размеры
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

    def create_widgets(self):
        text_color = "white"  # Белый

        # Заголовок в первой четверти экрана
        title_font = tkfont.Font(size=48, weight="bold")
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 6,  # 1/6 высоты
            text="ТАБЛИЦА РЕКОРДОВ",
            font=title_font,
            fill="#FFD700",  # золотисто-желтого цвета
            anchor="center"
        )

        title_bg = self.canvas.create_rectangle(
            WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 6 - 25,
            WINDOW_WIDTH // 2 + 250, WINDOW_HEIGHT // 6 + 25,
            fill="#120A2F", outline=""
        )
        self.canvas.tag_lower(title_bg)  # Под текст

        # Получаем записи
        records = self.settings.get_records()
        y_position = WINDOW_HEIGHT // 4  # Начальная позиция для записей

        if not records:
            # Нет рекордов
            no_records_font = tkfont.Font(size=28)
            self.canvas.create_text(
                WINDOW_WIDTH // 2,
                y_position,
                text="РЕКОРДОВ ПОКА НЕТ",
                font=no_records_font,
                fill=text_color,
                anchor="center"
            )

        else:
            # Есть рекорды
            record_font = tkfont.Font(size=18)
            for i, record in enumerate(records, 1):
                record_text = f"{i}. {record['name']} - {record['score']} руб. (дата: {record.get('date', 'неизвестно')})"
                self.canvas.create_text(
                    WINDOW_WIDTH // 2,
                    y_position,
                    text=record_text,
                    font=record_font,
                    fill=text_color,
                    anchor="center"
                )
                y_position += 40  # Отступ между записями

        # Кнопка НАЗАД в нижней четверти экрана
        back_btn = tk.Button(
            self.canvas,
            text="НАЗАД",
            font=tkfont.Font(size=28, weight="bold"),
            bg="#e74c3c",  # Красный
            fg="white",
            width=17,
            height=1,
            command=self.back_to_menu
        )

        # Размещаем кнопку на 3/4 высоты экрана
        self.canvas.create_window(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT * 2 // 3,
            window=back_btn,
            anchor="center"
        )

    def back_to_menu(self):
        root = self.master.winfo_toplevel()
        app = root.millionaire_app
        app.show_main_menu()
