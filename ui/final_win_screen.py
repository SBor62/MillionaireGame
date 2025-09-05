import tkinter as tk
from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from PIL import Image, ImageTk
import os


class FinalWinScreen(tk.Frame):
    def __init__(self, master, app, total_prize):
        super().__init__(master)
        self.master = master
        self.app = app
        self.total_prize = total_prize
        self.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.bg_image = None

        self.load_background()
        self.create_widgets()
        self.play_win_end_sound()

    def load_background(self):
        """Загружает фоновую картинку win_out.png"""
        image_path = "assets/backgrounds/win_out.png"
        if os.path.exists(image_path):
            self.master.update_idletasks()
            width = self.master.winfo_width() or WINDOW_WIDTH
            height = self.master.winfo_height() or WINDOW_HEIGHT
            self.canvas.config(width=width, height=height)

            img = Image.open(image_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        else:
            # Fallback на обычный win.png
            fallback_path = "assets/backgrounds/win.png"
            if os.path.exists(fallback_path):
                img = Image.open(fallback_path)
                img = img.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def play_win_end_sound(self):
        """Воспроизводит звук победы - сначала win_end, потом через 2 секунду win"""
        self.app.sound_manager.stop_all_sounds()
        self.app.sound_manager.play_sound("win_end", loop=False)
        # Откладываем запуск фоновой музыки на 3 секунды
        self.after(3000, lambda: self.app.sound_manager.play_sound("win", loop=True))

    def create_widgets(self):
        """Создает элементы интерфейса с кнопкой ВЫХОД"""
        # Основной контейнер
        main_frame = tk.Frame(self.canvas, bg="#120A2F", relief="raised", bd=5)
        self.canvas.create_window(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                  window=main_frame, anchor="center")

        # Заголовок
        title_font = ("Arial", 36, "bold")
        title_label = tk.Label(
            main_frame,
            text="ВЫ ВЫИГРАЛИ ВСЕ ИГРЫ!",
            font=title_font,
            fg="#FFD700",
            bg="#120A2F",
            pady=20
        )
        title_label.pack()

        # Выигрыш
        prize_font = ("Arial", 28)
        prize_label = tk.Label(
            main_frame,
            text=f"ВАШ ВЫИГРЫШ: {self.total_prize:,} руб.",
            font=prize_font,
            fg="white",
            bg="#120A2F",
            pady=15
        )
        prize_label.pack()

        # Сообщение о конце игры
        end_font = ("Arial", 24)
        end_label = tk.Label(
            main_frame,
            text="КОНЕЦ ИГРЫ",
            font=end_font,
            fg="#FFD700",
            bg="#120A2F",
            pady=20
        )
        end_label.pack()

        # Кнопка ВЫХОД
        exit_btn = tk.Button(
            main_frame,
            text="ВЫХОД",
            font=("Arial", 22, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            height=2,
            command=self.ask_player_name_before_exit,
            cursor="hand2"
        )
        exit_btn.pack(pady=30)

    def ask_player_name_before_exit(self):
        """Запрашивает имя игрока перед выходом"""
        from ui.dialog import ask_string

        player_name = ask_string(self.master, "Рекорд", "Введите ваше имя:")
        if player_name:
            # Сохраняем рекорд с общей суммой выигрыша
            self.app.settings.add_record(player_name, self.total_prize)

        # Переходим к экрану завершения
        self.exit_to_end_screen()

    def exit_to_end_screen(self):
        """Переходит к экрану завершения игры"""
        self.app.sound_manager.stop_all_sounds()
        # Правильный импорт - файл end_screens.py, класс EndScreen
        from ui.end_screen import EndScreen
        self.destroy()
        end_screen = EndScreen(self.master, self.app)
        end_screen.pack(fill=tk.BOTH, expand=True)
