import tkinter as tk
from tkinter import font as tkfont
from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class SettingsScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.master = master
        self.app = app
        self.pack(expand=True, fill=tk.BOTH)
        self.volume_scale = None

        # Используем стандартные размеры окна
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.master.update_idletasks()

        # Создаем Canvas без прокрутки
        self.canvas = tk.Canvas(self, highlightthickness=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_background()
        self.create_widgets()

    def load_background(self):
        """Загружает фоновую картинку без белой полосы"""
        from PIL import Image, ImageTk
        import os

        # Пробуем разные пути к фону
        possible_paths = [
            "assets/backgrounds/menu_dark.png",
            "assets/backgrounds/menu_light.png",
            "assets/backgrounds/record.png"
        ]

        for image_path in possible_paths:
            if os.path.exists(image_path):
                try:
                    # Получаем реальные размеры окна
                    self.master.update_idletasks()
                    width = self.master.winfo_width() or WINDOW_WIDTH
                    height = self.master.winfo_height() or WINDOW_HEIGHT

                    img = Image.open(image_path)
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    self.bg_image = ImageTk.PhotoImage(img)
                    self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
                    print(f"Фон настроек загружен: {image_path}")

                    # Устанавливаем размер Canvas под фон
                    self.canvas.config(width=width, height=height)
                    return

                except Exception as e:
                    print(f"Ошибка загрузки фона {image_path}: {e}")

        # Fallback - цветной фон
        self.canvas.configure(bg="#2c3e50")
        print("Используется fallback фон")

    def create_widgets(self):
        """Создаёт элементы интерфейса с правильными отступами"""
        # Основной контейнер с отступами
        main_container = tk.Frame(self.canvas, bg="#2c3e50", padx=50, pady=40)
        self.canvas.create_window(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                 window=main_container, anchor="center")

        # Заголовок с отступом
        title_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        title_label = tk.Label(
            main_container,
            text="НАСТРОЙКИ",
            font=title_font,
            fg="#3498db",
            bg="#2c3e50"
        )
        title_label.pack(pady=(0, 30))

        # Контейнер для кнопки темы
        theme_frame = tk.Frame(main_container, bg="#2c3e50")
        theme_frame.pack(pady=20, fill="x")

        # Кнопка смены темы
        theme_btn = tk.Button(
            theme_frame,
            text="СМЕНИТЬ ТЕМУ",
            font=tkfont.Font(size=18, weight="bold"),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            command=self.switch_theme,
            cursor="hand2"
        )
        theme_btn.pack()

        # Контейнер для громкости
        volume_frame = tk.Frame(main_container, bg="#2c3e50", pady=30)
        volume_frame.pack(fill="x")

        # Надпись громкости
        volume_label = tk.Label(
            volume_frame,
            text="ГРОМКОСТЬ МУЗЫКИ",
            font=tkfont.Font(size=16, weight="bold"),
            fg="white",
            bg="#2c3e50"
        )
        volume_label.pack(pady=(0, 15))

        # Контейнер для слайдера и значения
        slider_frame = tk.Frame(volume_frame, bg="#2c3e50")
        slider_frame.pack()

        # Ползунок громкости
        current_volume = int(self.app.settings.music_volume * 100)
        self.volume_scale = tk.Scale(
            slider_frame,
            from_=0,
            to=100,
            orient="horizontal",
            bg="#34495e",
            fg="white",
            troughcolor="#3498db",
            sliderrelief="raised",
            length=300,
            width=20,
            command=self.on_volume_change
        )
        self.volume_scale.set(current_volume)
        self.volume_scale.pack(side=tk.LEFT, padx=(0, 15))

        # Текущее значение громкости
        self.volume_value = tk.Label(
            slider_frame,
            text=f"{current_volume}%",
            font=tkfont.Font(size=14),
            fg="white",
            bg="#2c3e50",
            width=5
        )
        self.volume_value.pack(side=tk.LEFT)

        # Контейнер для кнопки назад
        back_frame = tk.Frame(main_container, bg="#2c3e50", pady=40)
        back_frame.pack()

        # Кнопка "Назад"
        back_btn = tk.Button(
            back_frame,
            text="НАЗАД",
            font=tkfont.Font(size=18, weight="bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            height=2,
            command=self.back_to_menu,
            cursor="hand2"
        )
        back_btn.pack()

    def on_volume_change(self, val):
        """Изменение громкости в реальном времени"""
        volume = int(val) / 100.0
        # Обновляем громкость в ОБОИХ местах:
        self.app.sound_manager.set_music_volume(volume)  # текущий звук
        self.app.settings.music_volume = volume  # настройки приложения
        self.volume_value.config(text=f"{int(val)}%")
        # Немедленно сохраняем
        self.app.settings.save_settings()
        print(f"Громкость обновлена: {volume}")

    def switch_theme(self):
        """Смена темы"""
        self.app.switch_theme()

    def back_to_menu(self):
        """Возврат в главное меню"""
        # СОХРАНЯЕМ настройки перед выходом!
        self.app.settings.save_settings()
        print("Настройки сохранены при выходе из настроек")
        self.destroy()
        self.app.show_main_menu()
