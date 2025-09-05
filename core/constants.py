import os
import tkinter as tk

# Автоматическое определение размеров экрана
root = tk.Tk()
root.withdraw()  # Скрываем временное окно

SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

# Базовые размеры для 16:9
BASE_WIDTH = 1536
BASE_HEIGHT = 864

# Масштабируем под текущий экран
if SCREEN_WIDTH / SCREEN_HEIGHT > 1.7:  # 16:9
    WINDOW_WIDTH = min(SCREEN_WIDTH - 100, BASE_WIDTH)
    WINDOW_HEIGHT = min(SCREEN_HEIGHT - 100, BASE_HEIGHT)
else:  # 4:3 или другие
    WINDOW_WIDTH = min(SCREEN_WIDTH - 100, 1024)
    WINDOW_HEIGHT = min(SCREEN_HEIGHT - 100, 768)

root.destroy()

# Правильный способ получить папку проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Папка проекта
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')  # Папка assets/

BACKGROUND_MAP = {
    "menu_light": os.path.join(ASSETS_DIR, "backgrounds", "menu_light.png"),
    "menu_dark": os.path.join(ASSETS_DIR, "backgrounds", "menu_dark.png"),
    "game_light": os.path.join(ASSETS_DIR, "backgrounds", "game_light.png"),
    "game_dark": os.path.join(ASSETS_DIR, "backgrounds", "game_dark.png"),
    "record": os.path.join(ASSETS_DIR, "backgrounds", "record.png"),
    "win": os.path.join(ASSETS_DIR, "backgrounds", "win.png"),
    "win_out": os.path.join(ASSETS_DIR, "backgrounds", "win_out.png"),
    "setting": os.path.join(ASSETS_DIR, "backgrounds", "setting.png"),
    "lose": os.path.join(ASSETS_DIR, "backgrounds", "lose.png"),
    "end": os.path.join(ASSETS_DIR, "backgrounds", "end.png")
}

# Пути к темам
THEMES_DIR = os.path.join("assets", "themes")
CURRENT_THEME = "default"

# Прозрачность
WINDOW_ALPHA = 0.93  # 93% непрозрачности

# Вертикальные смещения (в процентах от высоты окна)
MENU_VERTICAL_OFFSET = 0.10  # 12% сверху для меню
LEADERBOARD_VERTICAL_OFFSET = 0.10  # 15% сверху для таблицы рекордов

PRIZE_SCALE_BG = "#120A2F"  # Темно-фиолетовый
PRIZE_SCALE_FG = "#FFD700"  # Золотистый

# Цвета для игрового экрана
QUESTION_COLOR = "black"
ANSWER_BG_COLOR = "#3498db"
ANSWER_FG_COLOR = "white"

THEMES = {
    'dark': {
        'bg': '#120A2F',          # Темно-синий фон
        'text': '#E8E0C1',        # Светлый бежевый текст
        'btn': '#3498db',         # Голубые кнопки
        'btn_text': 'white'       # БЕЛЫЙ текст на кнопках ← ДОБАВИТЬ
    },
    'light': {
        'bg': '#AFEEEE',           # '#52ceff',          # Светло-голубой  фон
        'bg1': '#dbcf9e',           # '#e1d6ad',         # Светлый бежевый фон
        'text': '#120A2F',        # Темно-синий текст
        'btn': '#2980b9',         # Темно-голубые кнопки
        'btn_text': 'white'       # БЕЛЫЙ текст на кнопках ← ДОБАВИТЬ
    }
}
