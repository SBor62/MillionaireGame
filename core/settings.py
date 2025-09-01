import json
from pathlib import Path
from datetime import datetime


class Settings:
    def __init__(self, records_file="data/records.json"):
        self.records_file = Path(records_file)
        self.settings_file = Path("data/settings.json")
        self.current_theme = 'dark'
        self.music_volume = 0.7  # Значение по умолчанию
        self.records = []

        self._ensure_directories_exist()  # ← ДОБАВЬТЕ ЭТУ СТРОЧКУ В НАЧАЛО!
        self.load_settings()
        self.load_records()

    def _ensure_directories_exist(self):
        """Создает необходимые директории если они не существуют"""
        directories = [
            self.records_file.parent,
            self.settings_file.parent
        ]

        for directory in directories:
            if not directory.exists():
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                    print(f"Создана директория: {directory}")
                except Exception as e:
                    print(f"Ошибка создания директории {directory}: {e}")

    def load_settings(self):
        """Загружает настройки из файла"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.current_theme = data.get('theme', 'dark')
                    self.music_volume = data.get('music_volume', 0.7)
                print(f"Настройки загружены: тема={self.current_theme}, громкость={self.music_volume}")
        except (json.JSONDecodeError, Exception) as e:
            print(f"Ошибка загрузки настроек: {e}. Используем значения по умолчанию")

    def save_settings(self):
        """Сохраняет настройки в файл"""
        try:
            settings_data = {
                'theme': self.current_theme,
                'music_volume': self.music_volume
            }
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)
            print("Настройки сохранены")
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def load_records(self):
        """Загружает рекорды из файла"""
        if self.records_file.exists():
            try:
                with open(self.records_file, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
                print(f"Загружено рекордов: {len(self.records)}")
            except (json.JSONDecodeError, Exception) as e:
                print(f"Ошибка загрузки рекордов: {e}")
                self.records = []
        else:
            self.records = []
            print("Файл рекордов не найден, создан новый список")

    def add_record(self, name, score):
        """Добавляет новый рекорд"""
        if not name or not name.strip():
            name = "Аноним"

        self.records.append({
            "name": name.strip(),
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "theme": self.current_theme
        })

        # Сортируем по убыванию очков
        self.records.sort(key=lambda x: x["score"], reverse=True)

        # Оставляем только топ-10
        if len(self.records) > 10:
            self.records = self.records[:10]

        self.save_records()
        print(f"Добавлен новый рекорд: {name} - {score}")

    def save_records(self):
        """Сохраняет рекорды в файл"""
        try:
            with open(self.records_file, "w", encoding="utf-8") as f:
                json.dump(self.records, f, indent=2, ensure_ascii=False)
            print("Рекорды сохранены")
        except Exception as e:
            print(f"Ошибка сохранения рекордов: {e}")

    def get_records(self):
        """Возвращает список рекордов"""
        return self.records

    def get_music_volume(self):
        """Возвращает текущую громкость музыки"""
        return self.music_volume

    def set_music_volume(self, volume):
        """Устанавливает громкость музыки"""
        self.music_volume = max(0.0, min(1.0, volume))
        print(f"Громкость музыки установлена: {self.music_volume}")

    def set_theme(self, theme):
        """Устанавливает тему"""
        if theme in ['dark', 'light']:
            self.current_theme = theme
            print(f"Тема установлена: {theme}")
        else:
            print(f"Неизвестная тема: {theme}")

    def get_theme(self):
        """Возвращает текущую тему"""
        return self.current_theme
