import tkinter as tk
from tkinter import font as tkfont
from core.constants import WINDOW_HEIGHT, MENU_VERTICAL_OFFSET


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='')
        self.master = master
        self.root = self.master.winfo_toplevel()

        # Сохраняем ссылку на приложение
        self.app = self.root.millionaire_app

        self.create_widgets()

        # Callback-функции
        self.start_game_callback = None
        self.show_records_callback = None
        self.switch_theme_callback = None
        self.show_settings_callback = None

    def get_theme_color(self, key):
        """Получает цвет из текущей темы"""
        try:
            theme = self.app.theme_manager.themes.get(self.app.theme_manager.current_theme, {})
            return theme.get(key, {'bg': 'black', 'text': 'white', 'btn': '#3498db'}.get(key))
        except:
            return {'bg': 'black', 'text': 'white', 'btn': '#3498db'}.get(key)

    def create_widgets(self):
        """Создает элементы интерфейса"""
        # Рассчитываем смещение в пикселях
        vertical_offset = int(WINDOW_HEIGHT * MENU_VERTICAL_OFFSET)

        # Главный контейнер
        main_frame = tk.Frame(self, bg='')
        main_frame.pack(expand=True, fill=tk.BOTH, pady=(vertical_offset, 0))

        # Центрирующий фрейм
        center_frame = tk.Frame(main_frame, bg='')
        center_frame.pack(expand=True)

        # Заголовок
        title_font = tkfont.Font(family="Helvetica", size=42, weight="bold")
        title = tk.Label(
            center_frame,
            text="КТО ХОЧЕТ СТАТЬ МИЛЛИОНЕРОМ?",
            font=title_font,
            fg=self.get_theme_color('text'),
            bg=self.get_theme_color('bg'),
            pady=30
        )
        title.pack()

        # Стиль кнопок
        btn_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        btn_style = {
            "font": btn_font,
            "width": 18,
            "height": 2,
            "bd": 3,
            "relief": "raised",
            "cursor": "hand2"
        }

        # Список кнопок (УБИРАЕМ ТЕСТОВУЮ КНОПКУ)
        buttons = [
            ("ИГРАТЬ", self.start_game, False),
            ("РЕКОРДЫ", self.show_records, False),
            ("НАСТРОЙКИ", self.show_settings, False),
            ("ВЫХОД", self.exit_game, True)
        ]

        # Цвета кнопок
        normal_color = self.get_theme_color('btn')
        hover_color = self._darken_color(normal_color, 0.2)
        active_color = self._darken_color(normal_color, 0.3)
        fg_color = self.get_theme_color('btn_text')  # ← БЕЛЫЙ текст
        exit_color = "#e74c3c"
        exit_hover = "#c0392b"
        exit_active = "#a33226"

        # Создаем кнопки
        for text, command, is_exit in buttons:
            if is_exit:
                bg_color = exit_color
                hover_bg = exit_hover
                active_bg = exit_active
            else:
                bg_color = normal_color
                hover_bg = hover_color
                active_bg = active_color

            fg_color = "white"

            btn = tk.Button(
                center_frame,
                text=text,
                **btn_style,
                bg=bg_color,
                fg=fg_color,
                activebackground=active_bg,
                activeforeground=fg_color,
                command=command
            )

            # Анимация при наведении
            btn.bind("<Enter>", lambda e, b=btn, h=hover_bg: b.config(bg=h, relief="sunken"))
            btn.bind("<Leave>", lambda e, b=btn, bg=bg_color: b.config(bg=bg, relief="raised"))
            btn.bind("<ButtonPress-1>", lambda e, b=btn, a=active_bg: b.config(bg=a))
            btn.bind("<ButtonRelease-1>", lambda e, b=btn, h=hover_bg: b.config(bg=h))

            btn.pack(pady=12)

    def _darken_color(self, color, factor):
        """Затемняет цвет на указанный коэффициент"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            r = max(0, min(255, int(r * (1 - factor))))
            g = max(0, min(255, int(g * (1 - factor))))
            b = max(0, min(255, int(b * (1 - factor))))

            return f"#{r:02x}{g:02x}{b:02x}"
        return color

    def start_game(self):
        """Обработчик кнопки ИГРАТЬ"""
        if self.start_game_callback:
            self.start_game_callback()

    def show_records(self):
        """Обработчик кнопки РЕКОРДЫ"""
        if self.show_records_callback:
            self.show_records_callback()

    def show_settings(self):
        """Обработчик кнопки НАСТРОЙКИ"""
        if hasattr(self.app, 'show_settings'):
            self.app.show_settings()
        else:
            # Fallback: простой диалог громкости
            from tkinter import simpledialog
            volume = simpledialog.askinteger(
                "Громкость",
                "Введите громкость (0-100):",
                initialvalue=int(self.app.sound_manager.get_music_volume() * 100),
                minvalue=0,
                maxvalue=100
            )
            if volume is not None:
                self.app.sound_manager.set_music_volume(volume / 100.0)

    def switch_theme(self):
        """Обработчик смены темы"""
        if self.switch_theme_callback:
            self.switch_theme_callback()

    def exit_game(self):
        """Обработчик кнопки ВЫХОД"""
        if hasattr(self.app, 'show_end_screen'):
            self.app.show_end_screen()

    def apply_theme(self, theme):
        """Применяет новую тему (вызывается извне)"""
        # Обновляем только текст заголовка
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and "КТО ХОЧЕТ" in child.cget("text"):
                        child.configure(fg=theme['text'])
