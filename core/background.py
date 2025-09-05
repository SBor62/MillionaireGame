import tkinter as tk
from PIL import Image, ImageTk
import os
from pathlib import Path


class BackgroundManager:
    """
    Класс для управления фоном в Tkinter-приложении.
    Устанавливает фоновое изображение на весь экран, поддерживает смену фонов.
    Вызывается из любого модуля проекта.
    """

    def __init__(self, root):
        """
        :param root: главное окно Tkinter
        """
        self.root = root
        self.root.state('zoomed')
        self.bg_image = None
        self.bg_label = None
        self.current_image_path = None
        self.image_cache = {}  # Кэш загруженных изображений

        # Привязываем обработчик изменения размера окна
        self.root.bind('<Configure>', self._on_window_resize)

    def _on_window_resize(self, event):
        """Обработчик изменения размера окна"""
        if (event.widget == self.root and
                hasattr(self, 'current_image_path') and
                self.current_image_path):
            self._update_background_size()

    def _update_background_size(self):
        """Обновляет размер фона под текущий размер окна с сохранением пропорций"""
        if not self.current_image_path or not self.bg_label:
            return

        try:
            # Получаем текущие размеры окна
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()

            if width > 1 and height > 1:
                # Загружаем оригинальное изображение
                original_img = Image.open(self.current_image_path)

                # Сохраняем пропорции (растягиваем с заполнением)
                img = original_img.resize((width, height), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                self.bg_label.configure(image=self.bg_image)
        except Exception as e:
            print(f"Ошибка обновления размера фона: {e}")

    def _find_image_file(self, image_path):
        """Находит файл изображения по различным путям"""
        # Пробуем абсолютный путь
        if os.path.exists(image_path):
            return image_path

        # Пробуем относительный путь от корня проекта
        project_root = Path(__file__).parent.parent
        alternative_path = project_root / image_path
        if alternative_path.exists():
            return str(alternative_path)

        # Пробуем путь от assets
        assets_path = project_root / "assets" / image_path
        if assets_path.exists():
            return str(assets_path)

        # Пробуем найти в backgrounds
        backgrounds_path = project_root / "assets" / "backgrounds" / image_path
        if backgrounds_path.exists():
            return str(backgrounds_path)

        raise FileNotFoundError(f"Фоновое изображение не найдено: {image_path}")

    def set_background(self, image_path, resize=True):
        """Устанавливает фоновое изображение"""
        # Сначала очищаем предыдущий фон
        self.clear_background()

        try:
            # Находим файл изображения
            actual_path = self._find_image_file(image_path)
            self.current_image_path = actual_path

            # Проверяем кэш
            if actual_path in self.image_cache and resize:
                img = self.image_cache[actual_path]
            else:
                img = Image.open(actual_path)
                if resize:
                    self.root.update_idletasks()
                    width = self.root.winfo_width() or self.root.winfo_screenwidth()
                    height = self.root.winfo_height() or self.root.winfo_screenheight()

                    # Минимальные размеры для избежания ошибок
                    width = max(width, 100)
                    height = max(height, 100)

                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    self.image_cache[actual_path] = img  # Кэшируем

            self.bg_image = ImageTk.PhotoImage(img)
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()  # Отправляем на задний план

        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            # Устанавливаем черный фон как fallback
            self._set_fallback_background()
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            self._set_fallback_background()

    def _set_fallback_background(self):
        """Устанавливает fallback фон при ошибках"""
        self.clear_background()
        fallback_color = "#2c3e50"  # Темно-синий как fallback
        self.bg_label = tk.Label(self.root, bg=fallback_color)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()

    def clear_background(self):
        """Полностью очищает фон"""
        if self.bg_label is not None:
            self.bg_label.destroy()
            self.bg_label = None
        self.bg_image = None
        self.current_image_path = None

    def update_size(self):
        """Обновляет размер фона под текущий размер окна"""
        if self.current_image_path:
            self._update_background_size()

    def change_background(self, new_image_path, resize=True):
        """Смена фона с очисткой кэша для конкретного изображения"""
        if new_image_path in self.image_cache:
            del self.image_cache[new_image_path]
        self.set_background(new_image_path, resize)
