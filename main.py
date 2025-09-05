import tkinter as tk
from core.theme_manager import ThemeManager
from core.game import Game
from core.settings import Settings
from core.resources import SoundManager
from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_MAP
from ui.main_menu import MainMenu
from ui.game_screen import GameScreen


class MillionaireApp:
    """Главный класс приложения, управляющий окнами."""

    def __init__(self, root):
        self.sound_manager = SoundManager()
        self.theme_manager = ThemeManager()

        # Инициализация компонентов
        self.settings = Settings()
        self.game = Game()
        self.sound_manager = SoundManager()
        self.current_frame = None
        self.current_theme = 'dark'
        self.bg_manager = None
        self.theme_manager = ThemeManager()

        self.root = root
        self.root.millionaire_app = self
        self.show_video_intro()

        self.width = None
        self.height = None

        # Центрируем окно
        self.show_center_window()

        # Устанавливаем громкость из настроек при запуске
        self.sound_manager.set_music_volume(self.settings.music_volume)

        self.root.overrideredirect(True)
        self.show_main_menu()

    def show_video_intro(self):
        """Показ видео заставки"""
        try:
            from core.video_player import VideoPlayer
            video_player = VideoPlayer()
            video_player.play("assets/videos/vscreen.mp4", exit_on_click=True)

        except Exception as e:
            print(f"Ошибка воспроизведения видео: {e}")
            raise
        finally:
            # ПОСЛЕ видео (успешного или с ошибкой) показываем меню
            self.show_main_menu()

    def show_center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.root.geometry(f"{self.width}x{self.height}")

        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 3
        self.root.geometry(f"+{x}+{y}")

    def show_main_menu(self):
        """Показывает главное меню"""
        self.clear_frame()
        self.sound_manager.stop_all_sounds()

        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.update_idletasks()

        theme_bg = "menu_dark" if self.theme_manager.current_theme == "dark" else "menu_light"
        self.show_screen_with_background(MainMenu, BACKGROUND_MAP[theme_bg])

        # Устанавливаем callback-функции
        self.current_frame.start_game_callback = self.start_game
        self.current_frame.show_records_callback = self.show_records
        self.current_frame.switch_theme_callback = self.switch_theme
        self.current_frame.show_settings_callback = self.show_settings
        self.current_frame.exit_game_callback = self.show_end_screen

        # Устанавливаем громкость из настроек
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.play_sound("menu", loop=True)

    def start_game(self, is_new_session=True):
        """Запускает игровой экран"""
        self.clear_frame()
        self.sound_manager.stop_all_sounds()
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.update_idletasks()

        # Важно: передаем параметр is_new_session в game
        self.game.start_new_game(reset_questions=True, is_new_session=is_new_session)

        theme_bg = "game_dark" if self.theme_manager.current_theme == "dark" else "game_light"
        self.show_screen_with_background(GameScreen, BACKGROUND_MAP[theme_bg], self.game, self)

        # Устанавливаем громкость из настроек
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.play_sound("game", loop=True)

    def set_background(self, image_path):
        """Универсальный метод установки фона"""
        from core.background import BackgroundManager

        if hasattr(self, 'bg_manager') and self.bg_manager is not None:
            self.bg_manager.clear_background()
            self.bg_manager = None

        self.bg_manager = BackgroundManager(self.root)
        self.bg_manager.set_background(image_path)

    def show_screen_with_background(self, screen_class, background_path, *args, **kwargs):
        """Показывает экран с фоном"""
        self.clear_frame()
        self.sound_manager.stop_all_sounds()
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.show_center_window()
        self.root.update_idletasks()

        self.set_background(background_path)
        self.current_frame = screen_class(self.root, *args, **kwargs)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # Устанавливаем громкость из настроек для нового экрана
        self.sound_manager.set_music_volume(self.settings.music_volume)

    def show_records(self):
        """Показывает таблицу рекордов"""
        self.clear_frame()
        self.sound_manager.stop_all_sounds()
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.update_idletasks()

        from ui.leaderboard import LeaderboardScreen
        self.current_frame = LeaderboardScreen(self.root, self.settings)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # Устанавливаем громкость из настроек
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.play_sound("menu", loop=True)

    def show_settings(self):
        """Показывает экран настроек"""
        try:
            self.clear_frame()
            self.sound_manager.stop_all_sounds()
            self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
            self.root.update_idletasks()

            from ui.settings_screen import SettingsScreen
            self.current_frame = SettingsScreen(self.root, self)
            self.current_frame.pack(fill=tk.BOTH, expand=True)

            # Устанавливаем громкость из настроек
            self.sound_manager.set_music_volume(self.settings.music_volume)
            self.sound_manager.play_sound("menu", loop=True)

        except ImportError as e:
            print(f"Ошибка загрузки настроек: {e}")
            from ui.dialog import show_info
            show_info(self.root, "Функция настроек временно недоступна", "Внимание")
            self.show_main_menu()

    def switch_theme(self):
        """Применяет новую тему ТОЛЬКО к меню и игре"""
        theme = self.theme_manager.switch_theme()
        print(f"Тема изменена на {self.theme_manager.current_theme}")

        if hasattr(self, 'current_frame'):
            from ui.main_menu import MainMenu
            from ui.game_screen import GameScreen

            if isinstance(self.current_frame, MainMenu):
                theme_bg = "menu_dark" if self.theme_manager.current_theme == "dark" else "menu_light"
                self.set_background(BACKGROUND_MAP[theme_bg])
                if hasattr(self.current_frame, 'apply_theme'):
                    self.current_frame.apply_theme(theme)

            elif isinstance(self.current_frame, GameScreen):
                theme_bg = "game_dark" if self.theme_manager.current_theme == "dark" else "game_light"
                self.set_background(BACKGROUND_MAP[theme_bg])
                if hasattr(self.current_frame, 'apply_theme'):
                    self.current_frame.apply_theme(theme)

        self.settings.current_theme = self.theme_manager.current_theme
        self.settings.save_settings()

    def show_win_screen(self):
        """Показывает экран победы"""
        self.sound_manager.stop_all_sounds()
        self.clear_frame()

        # используем ОБЩУЮ накопленную сумму
        total_prize = self.game.get_total_prize()

        # Проверяем все ли 7 игр пройдены
        if self.game.is_final_win():
            try:
                from ui.final_win_screen import FinalWinScreen
                self.current_frame = FinalWinScreen(self.root, self, total_prize)
            except ImportError:
                # Fallback на обычный экран победы
                from ui.win_lose_screens import WinScreen
                self.current_frame = WinScreen(self.root, self, total_prize)
        else:
            from ui.win_lose_screens import WinScreen
            self.current_frame = WinScreen(self.root, self, total_prize)

        self.current_frame.pack(fill=tk.BOTH, expand=True)
        self.sound_manager.set_music_volume(self.settings.music_volume)

    def show_lose_screen(self):
        """Показывает экран проигрыша"""
        self.clear_frame()
        from ui.win_lose_screens import LoseScreen

        # ИСПРАВЛЕНО: При проигрыше игрок получает несгораемую сумму + накопленные выигрыши
        safe_sum = self.game.get_last_safe_sum()
        total_prize = self.game.total_accumulated_winnings + safe_sum

        self.current_frame = LoseScreen(self.root, self, total_prize)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # Устанавливаем громкость из настроек
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.play_sound("lose", loop=True)

    def clear_frame(self):
        """Очищает текущий экран и фон"""
        self.sound_manager.stop_all_sounds()

        if hasattr(self, 'current_frame') and self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

        if hasattr(self, 'bg_manager') and self.bg_manager is not None:
            self.bg_manager.clear_background()
            self.bg_manager = None

    def show_final_win_screen(self, total_prize):
        """Показывает финальный экран победы"""
        self.sound_manager.stop_all_sounds()
        self.clear_frame()

        try:
            from ui.final_win_screen import FinalWinScreen
            self.current_frame = FinalWinScreen(self.root, self, total_prize)
        except ImportError:
            # Fallback на обычный экран победы
            from ui.win_lose_screens import WinScreen
            self.current_frame = WinScreen(self.root, self, total_prize)

        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_end_screen(self):
        """Показывает экран конца игры"""
        self.clear_frame()
        self.sound_manager.stop_all_sounds()

        from ui.end_screen import EndScreen  # ← ПРАВИЛЬНЫЙ ИМПОРТ
        self.current_frame = EndScreen(self.root, self)
        self.current_frame.pack(fill=tk.BOTH, expand=True)


def main():
    """Точка входа в приложение."""
    root = tk.Tk()
    app = MillionaireApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
