import json
from pathlib import Path


class QuestionManager:
    def __init__(self, questions_dir="data/questions"):
        self.questions_dir = Path(questions_dir)
        self.question_sets = []  # Все наборы вопросов
        self.current_set_index = 0  # Текущий набор (0 = set1)
        self.current_questions = []  # Вопросы текущего набора
        self.load_question_sets()

    def load_question_sets(self):
        """Загружает наборы вопросов СТРОГО ПО ПОРЯДКУ: set1.json -> set7.json"""
        # Жестко задаем порядок файлов
        question_files = [
            self.questions_dir / "set1.json",
            self.questions_dir / "set2.json",
            self.questions_dir / "set3.json",
            self.questions_dir / "set4.json",
            self.questions_dir / "set5.json",
            self.questions_dir / "set6.json",
            self.questions_dir / "set7.json"
        ]

        print("Загрузка наборов вопросов в строгом порядке:")

        for file in question_files:
            try:
                if file.exists():
                    with open(file, "r", encoding="utf-8") as f:
                        questions = json.load(f)
                        # Проверяем, что вопросы не пустые
                        if questions and len(questions) > 0:
                            self.question_sets.append({
                                'name': file.stem,
                                'questions': questions,
                                'file_path': file
                            })
                            print(f"  ✓ {file.stem} ({len(questions)} вопросов)")
                        else:
                            print(f"  ⚠ {file.stem} - пустой файл")
                else:
                    print(f"  ❌ {file.name} - файл не найден")

            except Exception as e:
                print(f"  ❌ Ошибка загрузки {file.name}: {e}")

        print(f"Всего загружено наборов: {len(self.question_sets)}")

        # Загружаем первый набор
        if self.question_sets:
            self.current_questions = self.question_sets[0]['questions'].copy()

    def get_current_set_name(self):
        """Возвращает название текущего набора"""
        if self.current_set_index < len(self.question_sets):
            return self.question_sets[self.current_set_index]['name']
        return None

    def get_question(self):
        """Возвращает следующий вопрос из текущего набора"""
        if not self.current_questions:
            return None    # Если вопросы закончились, возвращаем None
        return self.current_questions.pop(0)  # Берем первый вопрос

    def has_more_questions(self):
        """Проверяет, есть ли еще вопросы в текущем наборе"""
        return len(self.current_questions) > 0

    def load_next_set(self):
        """Загружает следующий набор вопросов и возвращает True если успешно"""
        if self.current_set_index < len(self.question_sets) - 1:
            self.current_set_index += 1
            self.current_questions = self.question_sets[self.current_set_index]['questions'].copy()
            print(f"Переход к набору {self.current_set_index + 1}: {self.get_current_set_name()}")
            return True
        return False

    def reset_to_first_set(self):
        """Сбрасывает к первому набору (полный сброс)"""
        self.current_set_index = 0
        if self.question_sets:
            self.current_questions = self.question_sets[0]['questions'].copy()
        print("Сброс к первому набору вопросов")

    def reset_current_set(self):
        """Сбрасывает текущий набор вопросов (для переигрывания)"""
        if self.question_sets and self.current_set_index < len(self.question_sets):
            self.current_questions = self.question_sets[self.current_set_index]['questions'].copy()
            print(f"Сброс текущего набора: {self.get_current_set_name()}")

    def get_total_sets(self):
        """Возвращает общее количество наборов вопросов"""
        return len(self.question_sets)

    def is_last_set(self):
        """Проверяет, является ли текущий набор последним"""
        return self.current_set_index >= len(self.question_sets) - 1

    def get_current_set_number(self):
        """Возвращает номер текущего набора (начиная с 1)"""
        return self.current_set_index + 1
