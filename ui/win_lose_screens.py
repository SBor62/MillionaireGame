import tkinter as tk
from tkinter import font as tkfont
from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class WinScreen(tk.Frame):
    def __init__(self, master, app, prize=0):
        super().__init__(master)
        self.master = master
        self.app = app
        self.prize = prize
        self.pack(expand=True, fill=tk.BOTH)

        # Создаем Canvas для фоновой картинки
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bg_image = None

        self.load_background()
        self.create_widgets()
        self.play_sounds()

    def load_background(self):
        """Загружает фоновую картинку"""
        from PIL import Image, ImageTk
        import os

        image_path = "assets/backgrounds/win.png"
        if os.path.exists(image_path):
            self.master.update_idletasks()
            width = self.master.winfo_width() or WINDOW_WIDTH
            height = self.master.winfo_height() or WINDOW_HEIGHT

            self.canvas.config(width=width, height=height)

            img = Image.open(image_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def play_sounds(self):
        """Воспроизводит звуки победы - сначала victory, потом через 3 секунды win"""
        self.app.sound_manager.stop_all_sounds()
        self.app.sound_manager.play_sound("victory", loop=False)
        # Откладываем запуск фоновой музыки на 3 секунды
        self.after(3000, lambda: self.app.sound_manager.play_sound("win", loop=True))

    def create_widgets(self):
        """Создает элементы интерфейса"""
        bg_color = "#120A2F"
        text_color = "white"
        title_color = "#27ae60"

        main_frame = tk.Frame(self.canvas, bg=bg_color, relief="raised", bd=5)
        self.canvas.create_window(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2.5, window=main_frame, anchor="center")

        # Заголовок
        title_font = tkfont.Font(size=38, weight="bold")
        tk.Label(
            main_frame,
            text="ВЫ ВЫИГРАЛИ!",
            font=title_font,
            fg=title_color,
            bg=bg_color,
            pady=20
        ).pack()

        # Выигрыш - используем переданный prize (уже правильный)
        prize_font = tkfont.Font(size=26)
        tk.Label(
            main_frame,
            text=f"Ваш выигрыш: {self.prize:,} руб.",
            font=prize_font,
            fg=text_color,
            bg=bg_color,
            pady=15
        ).pack()

        # Вопрос
        question_font = tkfont.Font(size=24)
        tk.Label(
            main_frame,
            text="Хотите сыграть еще раз?",
            font=question_font,
            fg=text_color,
            bg=bg_color,
            pady=20
        ).pack()

        # Кнопки
        btn_frame = tk.Frame(main_frame, bg=bg_color)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="ПРОДОЛЖИТЬ",
            font=tkfont.Font(size=22, weight="bold"),
            bg="#2ecc71",
            fg="white",
            width=14,
            height=2,
            command=self.new_game
        ).pack(side=tk.LEFT, padx=15)

        tk.Button(
            btn_frame,
            text="В МЕНЮ",
            font=tkfont.Font(size=22, weight="bold"),
            bg="#3498db",
            fg="white",
            width=14,
            height=2,
            command=self.to_menu
        ).pack(side=tk.RIGHT, padx=15)

    def new_game(self):
        """Начинает новую игру со СЛЕДУЮЩИМ набором вопросов"""
        self.app.sound_manager.stop_all_sounds()
        self.ask_player_name(self._start_next_set_game)

    def _start_next_set_game(self):
        """Запускает игру со СЛЕДУЮЩИМ набором вопросов"""
        # Переходим к следующему набору
        if self.app.game.handle_level_completion():
            print(f"Начинаем набор {self.app.game.get_current_question_set()}")
            self.app.start_game(is_new_session=False)
        else:
            # Все наборы пройдены - финальная победа
            total_prize = self.app.game.get_total_prize()
            self.app.show_final_win_screen(total_prize)

    def to_menu(self):
        """Возвращает в главное меню"""
        self.app.sound_manager.stop_all_sounds()
        self.ask_player_name(lambda: self.app.show_main_menu())

    def ask_player_name(self, callback):
        """Запрашивает имя игрока и выполняет callback"""
        from ui.dialog import ask_string

        # Используем главное окно для диалога
        player_name = ask_string(self.master, "Рекорд", "Введите ваше имя:")

        if player_name:
            # Используем ОБЩУЮ накопленную сумму для записи рекорда
            total_prize = self.app.game.get_total_prize()
            self.app.settings.add_record(player_name, total_prize)

        # Выполняем callback после диалога
        callback()


class LoseScreen(tk.Frame):
    def __init__(self, master, app, prize=0):
        super().__init__(master)
        self.master = master
        self.app = app
        self.prize = prize
        self.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.bg_image = None

        self.load_background()
        self.create_widgets()
        self.play_sounds()

    def load_background(self):
        """Загружает фоновую картинку"""
        from PIL import Image, ImageTk
        import os

        image_path = "assets/backgrounds/lose.png"
        if os.path.exists(image_path):
            self.master.update_idletasks()
            width = self.master.winfo_width() or WINDOW_WIDTH
            height = self.master.winfo_height() or WINDOW_HEIGHT

            self.canvas.config(width=width, height=height)

            img = Image.open(image_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def play_sounds(self):
        """Воспроизводит звуки проигрыша"""
        self.app.sound_manager.play_sound("lose", loop=True)

    def create_widgets(self):
        """Создает элементы интерфейса"""
        bg_color = "#120A2F"
        text_color = "white"
        title_color = "#e74c3c"

        main_frame = tk.Frame(self.canvas, bg=bg_color, relief="raised", bd=5)
        self.canvas.create_window(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2.5, window=main_frame, anchor="center")

        title_font = tkfont.Font(size=38, weight="bold")
        tk.Label(
            main_frame,
            text="ВЫ ПРОИГРАЛИ",
            font=title_font,
            fg=title_color,
            bg=bg_color,
            pady=20
        ).pack()

        # Используем переданный prize (несгораемую сумму)
        prize_font = tkfont.Font(size=26)
        if self.prize > 0:
            tk.Label(
                main_frame,
                text=f"Ваш выигрыш: {self.prize:,} руб.",
                font=prize_font,
                fg=text_color,
                bg=bg_color,
                pady=15
            ).pack()
        else:
            tk.Label(
                main_frame,
                text="ВЫ НИЧЕГО НЕ ВЫИГРАЛИ",
                font=prize_font,
                fg=text_color,
                bg=bg_color,
                pady=15
            ).pack()

        question_font = tkfont.Font(size=24)
        tk.Label(
            main_frame,
            text="Хотите переиграть?",
            font=question_font,
            fg=text_color,
            bg=bg_color,
            pady=20
        ).pack()

        btn_frame = tk.Frame(main_frame, bg=bg_color)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="ПЕРЕИГРАТЬ",
            font=tkfont.Font(size=22, weight="bold"),
            bg="#2ecc71",
            fg="white",
            width=14,
            height=2,
            command=self.retry_game
        ).pack(side=tk.LEFT, padx=15)

        tk.Button(
            btn_frame,
            text="В МЕНЮ",
            font=tkfont.Font(size=22, weight="bold"),
            bg="#3498db",
            fg="white",
            width=14,
            height=2,
            command=self.to_menu
        ).pack(side=tk.RIGHT, padx=15)

    def retry_game(self):
        """Повторяет игру с ТЕМ ЖЕ набором вопросов"""
        self.app.sound_manager.stop_all_sounds()

        # Сбрасываем выигрыш текущей игры при переигрыше
        self.app.game.current_game_winnings = 0

        # НЕ сбрасываем набор вопросов, только перезагружаем текущий
        self.app.game.question_manager.reset_current_set()
        self.app.game.current_level = 1
        self.app.game.used_hints = {
            "50_50": False,
            "call_friend": False,
            "audience_help": False
        }

        # Запускаем игру БЕЗ сброса сессии
        self.app.start_game(is_new_session=False)

    def to_menu(self):
        """Возвращает в главное меню с сохранением выигрыша"""
        self.app.sound_manager.stop_all_sounds()

        # ИСПРАВЛЕНИЕ: При проигрыше игрок получает последнюю несгораемую сумму
        safe_sum = self.app.game.get_last_safe_sum()
        total_prize = self.app.game.total_accumulated_winnings + safe_sum

        # Запрашиваем имя и переходим в меню
        self.ask_player_name(total_prize, lambda: self.app.show_main_menu())

    def ask_player_name(self, prize, callback):
        """Запрашивает имя игрока и выполняет callback"""
        from ui.dialog import ask_string

        player_name = ask_string(self.master, "Рекорд", "Введите ваше имя:")
        if player_name:
            self.app.settings.add_record(player_name, prize)

        callback()
