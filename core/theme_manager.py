import json


class ThemeManager:
    def __init__(self):
        self.themes = {}
        self.current_theme = "dark"

        self.define_themes()     # ...и заменим на этот метод

    def define_themes(self):
        """Определяем темы напрямую из constants.py, без загрузки JSON"""
        from core.constants import THEMES    # Импортируем новые темы
        self.themes = THEMES
        print(f"[ThemeManager] Темы 'dark' и 'light' загружены из constants.py")

    def load_themes(self):
        """Загружает тему из JSON-файла и добавляет резервные темы"""

        # Путь к файлу темы
        path = "themes/default/config.json"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                colors = data.get("colors", {})

            # Тема "dark" из config.json
            self.themes["dark"] = {
                "bg": colors.get("question_bg", "#2c3e50"),
                "text": colors.get("text_color", "white"),
                "btn": colors.get("answer_bg", "#3498db")
            }
            print(f"[ThemeManager] Тема 'dark' загружена из {path}")

        except FileNotFoundError:
            print(f"[ThemeManager] Файл темы не найден: {path}. Используем стандартные цвета.")
            self.themes["dark"] = {
                "bg": "black",
                "text": "white",
                "btn": "#3498db"
            }
        except json.JSONDecodeError as e:
            print(f"[ThemeManager] Ошибка чтения JSON: {e}")
            self.themes["dark"] = {
                "bg": "black",
                "text": "white",
                "btn": "#3498db"
            }

        # Добавляем светлую тему
        self.themes["light"] = {
            "bg": "white",
            "text": "black",
            "btn": "#2980b9"
        }

        # ← ВАЖНО: убедимся, что current_theme существует
        if self.current_theme not in self.themes:
            self.current_theme = "dark"  # fallback

    def switch_theme(self):
        """Переключает тему и возвращает новые цвета"""
        themes = list(self.themes.keys())
        idx = themes.index(self.current_theme)
        self.current_theme = themes[(idx + 1) % len(themes)]
        return self.themes[self.current_theme]
