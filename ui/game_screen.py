import tkinter as tk
from tkinter import font as tkfont
import random


class GameScreen(tk.Frame):
    def __init__(self, master, game, app):
        super().__init__(master)
        self.master = master
        self.game = game
        self.app = app
        self.answer_clicked = False

        self.question_label = None
        self.answer_buttons = []

        # Центрирующий фрейм
        self.center_frame = tk.Frame(self, bg=self.get_theme_color('bg'))
        self.center_frame.place(relx=0.45, rely=0.5, anchor=tk.CENTER)

        # Шкала призов (правая панель)
        self.prize_scale = tk.Frame(self, bg="#120A2F", width=250)
        self.prize_scale.pack(side=tk.RIGHT, fill=tk.Y, padx=30, pady=30)
        self.create_prize_scale()

        # Основное содержимое
        self.configure(bg='')
        self.create_widgets()

    def get_theme_color(self, key):
        """Получает цвет из текущей темы"""
        try:
            app = self.master.winfo_toplevel().millionaire_app
            theme = app.theme_manager.themes.get(app.theme_manager.current_theme, {})
            return theme.get(key, {'bg': 'black', 'text': 'white', 'btn': '#3498db'}.get(key))
        except:
            return {'bg': 'black', 'text': 'white', 'btn': '#3498db'}.get(key)

    def create_prize_scale(self):
        """Создает шкалу призов"""
        tk.Label(
            self.prize_scale,
            text="ВАШ ВЫИГРЫШ",
            font=tkfont.Font(size=14, weight="bold"),
            bg="#120A2F",
            fg="#FFD700"
        ).pack(pady=7)

        prizes = [
            "     500", "    1 000", "    2 000", "    3 000", "    5 000",
            "   10 000", "   20 000", "   30 000", "   40 000", "  50 000",
            " 100 000", " 200 000", " 300 000", " 500 000", "1 000 000"
        ]

        for i, prize in enumerate(reversed(prizes)):
            bg = "#120A2F"
            fg = "#FFD700"
            if i in [4, 9]:  # Несгораемые суммы
                bg = "#8B4513"  # Коричневый
            tk.Label(
                self.prize_scale,
                text=f"{15 - i}. {prize} руб.",
                font=tkfont.Font(size=14),
                bg=bg,
                fg=fg,
                anchor="w",
                width=14
            ).pack(fill=tk.X, pady=6)

    def create_widgets(self):
        """Создает интерфейс вопроса"""
        # Вопрос
        self.question_label = tk.Label(
            self.center_frame,
            text="",
            font=tkfont.Font(size=24, weight="bold"),
            bg=self.get_theme_color('bg'),
            fg=self.get_theme_color('text'),
            wraplength=700,
            justify="center"
        )
        self.question_label.pack()

        # Кнопки ответов
        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.center_frame,
                text="",
                font=tkfont.Font(size=22),
                bg=self.get_theme_color('btn'),
                fg=self.get_theme_color('btn_text'),
                width=40,
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(pady=6)
            self.answer_buttons.append(btn)

        # Панель с подсказками
        hints_frame = tk.Frame(self.center_frame, bg=self.get_theme_color('bg'))
        hints_frame.pack(pady=10)

        hints = [
            (" 50  НА  50 ", self.fifty_fifty),
            ("ЗВОНОК ДРУГУ", self.call_friend),
            ("ПОМОЩЬ ЗАЛА ", self.audience_help)
        ]

        for text, command in hints:
            btn = tk.Button(
                hints_frame,
                text=text,
                font=tkfont.Font(size=20, weight="bold"),
                bg="#01e489",
                fg="#0404e7",
                command=command
            )
            btn.pack(side=tk.LEFT, padx=10)

        # Кнопка "Назад"
        tk.Button(
            self.center_frame,
            text="НАЗАД В МЕНЮ",
            font=tkfont.Font(size=16, weight="bold"),
            bg="#ad1400",
            fg="white",
            command=self.back_to_menu
        ).pack(pady=10)

        self.load_question()

    def load_question(self):
        """Загружает новый вопрос"""
        self.answer_clicked = False

        question = self.game.load_question()
        if not question:
            self.app.show_win_screen()
            return

        self.question_label.config(text=question["question"])
        for i, option in enumerate(question["options"]):
            if i < len(self.answer_buttons):
                self.answer_buttons[i].config(text=option, state=tk.NORMAL)

        self.update_prize_scale()

    def update_prize_scale(self):
        """Обновляет подсветку текущего уровня"""
        for i, widget in enumerate(self.prize_scale.winfo_children()[1:]):
            level = 15 - i

            if level == self.game.current_level:
                widget.config(bg="#3498db", fg="white")
            elif level in self.game.safe_points:
                widget.config(bg="#8B4513", fg="#FFD700")
            else:
                widget.config(bg="#120A2F", fg="#FFD700")

    def check_answer(self, answer_index):
        """Проверяет правильность ответа"""
        if self.answer_clicked:
            return False

        self.answer_clicked = True

        # Блокируем все кнопки
        for btn in self.answer_buttons:
            btn.config(state=tk.DISABLED)

        correct_index = self.game.current_question["correct_answer"]
        is_correct = (answer_index == correct_index)

        if is_correct:
            # Увеличиваем выигрыш текущей игры
            prize_won = self.game.add_current_prize()

            # Останавливаем фоновую музыку для правильного ответа
            self.app.sound_manager.stop_all_sounds()
            self.app.sound_manager.play_sound("correct")
            self.after(3000, self.handle_correct_answer)  # Ждем окончания звука
        else:
            self.app.sound_manager.stop_all_sounds()
            self.app.sound_manager.play_sound("wrong")
            self.after(8000, self.handle_wrong_answer)

        return is_correct

    def handle_correct_answer(self):
        """Обрабатывает правильный ответ"""
        self.game.current_level += 1

        if self.game.current_level > 15:
            # Завершили текущий набор - переходим к победе
            self.app.show_win_screen()
        else:
            self.app.sound_manager.play_sound("game", loop=True)
            self.load_question()

    def handle_wrong_answer(self):
        """Обрабатывает неправильный ответ"""
        self.app.show_lose_screen()

    def fifty_fifty(self):
        """Подсказка 50/50"""
        if self.game.used_hints.get("50_50", False):
            return

        question = self.game.current_question
        correct = question["correct_answer"]
        wrong_answers = [i for i in range(4) if i != correct]
        random.shuffle(wrong_answers)

        for i in wrong_answers[:2]:
            self.answer_buttons[i].config(state=tk.DISABLED)

        self.game.used_hints["50_50"] = True

    def call_friend(self):
        """Подсказка 'Звонок другу'"""
        if self.game.used_hints["call_friend"]:
            return

        question = self.game.current_question
        correct = question["correct_answer"]

        if random.random() < 0.8:
            message = f"Друг говорит: 'Я уверен, это вариант {correct + 1}!'"
        else:
            random_answer = random.choice([i for i in range(4) if i != correct])
            message = f"Друг говорит: 'Мне кажется, это вариант {random_answer + 1}...'"

        from ui.dialog import show_info
        show_info(self.master, message, "Звонок другу")

        self.game.used_hints["call_friend"] = True

    def audience_help(self):
        """Подсказка 'Помощь зала'"""
        if self.game.used_hints["audience_help"]:
            return

        question = self.game.current_question
        correct = question["correct_answer"]

        votes = [random.randint(5, 25) for _ in range(4)]
        votes[correct] += random.randint(30, 60)
        total = sum(votes)
        percentages = [round((v / total) * 100) for v in votes]

        message = "Зал голосует:\n\n"
        for i, percent in enumerate(percentages):
            bars = "█" * (percent // 5)
            message += f"{i + 1}: {bars} {percent}%\n"

        from ui.dialog import show_info
        show_info(self.master, message, "Помощь зала")

        self.game.used_hints["audience_help"] = True

    def back_to_menu(self):
        """Возвращает в главное меню"""
        # Сохраняем настройки перед выходом из игры
        self.app.settings.save_settings()
        self.app.sound_manager.stop_all_sounds()
        self.app.show_main_menu()
