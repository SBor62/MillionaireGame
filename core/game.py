from core.question_manager import QuestionManager


class Game:
    def __init__(self):
        self.question_manager = QuestionManager()
        self.current_question = None
        self.score = 0
        self.current_level = 1
        self.total_wins = 0
        self.total_prize = 0
        self.used_hints = {
            "50_50": False,
            "call_friend": False,
            "audience_help": False
        }

        # Несгораемые суммы после 5 и 10 вопросов
        self.safe_points = [5, 10]
        self.prize_levels = {
            1: 500, 2: 1000, 3: 2000, 4: 3000, 5: 5000,
            6: 10000, 7: 20000, 8: 30000, 9: 40000, 10: 50000,
            11: 100000, 12: 200000, 13: 300000, 14: 500000, 15: 1000000
        }

    def start_new_game(self, reset_questions=True, is_new_session=True):
        """Начинает новую игру"""
        # Сбрасываем только уровень и подсказки, НО НЕ набор вопросов!
        self.current_level = 1
        self.used_hints = {
            "50_50": False,
            "call_friend": False,
            "audience_help": False
        }

        if is_new_session:
            # Полный сброс только для новой сессии
            self.total_wins = 0
            self.total_prize = 0
            self.question_manager.reset_to_first_set()
            print("Новая игровая сессия")
        else:
            # Продолжение - сохраняем прогресс наборов
            print(f"Продолжение игры. Текущий набор: {self.question_manager.current_set_index + 1}")

        if reset_questions:
            self.question_manager.reset_current_set()

    def handle_level_completion(self):
        """Обрабатывает завершение уровня (15 вопросов) и возвращает True если есть следующий набор"""
        self.total_wins += 1
        self.total_prize += 1000000

        # Пытаемся перейти к следующему набору
        if self.question_manager.load_next_set():
            print(f"Успешно перешли к набору {self.question_manager.current_set_index + 1}")
            self.current_level = 1
            return True
        else:
            print("Все наборы пройдены - финальная победа!")
            return False

    def load_question(self):
        """Загружает следующий вопрос"""
        self.current_question = self.question_manager.get_question()
        return self.current_question

    def check_answer(self, answer_index):
        """Проверяет правильность ответа"""
        if not self.current_question:
            return False
        return self.current_question["correct_answer"] == answer_index

    def get_guaranteed_prize(self):
        """Возвращает несгораемую сумму"""
        if self.current_level >= 10:
            return self.prize_levels[10]
        elif self.current_level >= 5:
            return self.prize_levels[5]
        return 0

    def get_last_safe_sum(self):
        """Возвращает последнюю несгораемую сумму"""
        return self.get_guaranteed_prize()

    def get_current_question_set(self):
        """Возвращает номер текущего набора вопросов (1-7)"""
        return self.question_manager.current_set_index + 1

    def get_total_prize(self):
        """Возвращает общий выигрыш за все пройденные наборы"""
        return self.total_prize

    def get_current_set_prize(self):
        """Возвращает выигрыш за текущий набор"""
        return self.get_current_question_set() * 1000000

    def advance_to_next_set(self):
        """Переходит к следующему набору вопросов (альтернативный метод)"""
        return self.handle_level_completion()

    def is_final_win(self):
        """Проверяет, достигнут ли финальный выигрыш (все 7 наборов)"""
        return self.question_manager.current_set_index >= 6  # 0-based index, 6 = 7й набор

    def has_more_questions(self):
        """Проверяет, есть ли еще вопросы в текущем наборе"""
        return self.question_manager.has_more_questions()

    def is_last_set(self):
        """Проверяет, является ли текущий набор последним"""
        return self.question_manager.is_last_set()

    def get_question_set_info(self):
        """Возвращает информацию о текущем наборе"""
        return {
            'current_set': self.get_current_question_set(),
            'total_sets': self.question_manager.get_total_sets(),
            'set_name': self.question_manager.get_current_set_name(),
            'set_prize': self.get_current_set_prize()
        }
