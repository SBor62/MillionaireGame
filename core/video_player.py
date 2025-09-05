import cv2
import pygame
import os
import sys


class VideoPlayer:
    def __init__(self):
        # Инициализация mixer с параметрами, подходящими для аудио
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        self.screen = None

    def get_resource_path(self, relative_path):
        """Получает правильный путь к ресурсам для PyInstaller"""
        try:
            # PyInstaller создает временную папку в _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def play(self, video_path, audio_path="assets/audio/ascreen.mp3", exit_on_click=False):
        """
        Воспроизводит видео и аудио одновременно.
        """
        # Используем правильные пути для PyInstaller
        video_path = self.get_resource_path(video_path)
        audio_path = self.get_resource_path(audio_path)

        # Проверяем существование файлов
        if not os.path.exists(video_path):
            print(f"❌ Видео не найдено: {video_path}")
            return False

        if not os.path.exists(audio_path):
            print(f"❌ Аудио не найдено: {audio_path}")
            # Попробуем альтернативный путь
            audio_path = self.get_resource_path("assets/sounds/menu.mp3")
            print(f"Пробую альтернативное аудио: {audio_path}")
            if not os.path.exists(audio_path):
                print(f"❌ Альтернативное аудио тоже не найдено!")
                return False

        # Открываем видео
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Не удалось открыть видео: {video_path}")
            return False

        # Получаем FPS
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 24

        # Настройка pygame
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Видеозаставка")
        clock = pygame.time.Clock()

        # Загружаем и запускаем аудио
        if os.path.exists(audio_path):
            try:
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Не удалось воспроизвести аудио: {e}")
        else:
            print(f"Аудиофайл не найден: {audio_path}")

        # Главный цикл воспроизведения
        running = True
        while running:
            ret, frame = cap.read()
            if not ret:
                break

            # Конвертируем BGR → RGB, транспонируем под pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.transpose(frame)
            surface = pygame.surfarray.make_surface(frame)

            # Масштабируем на весь экран
            screen_size = self.screen.get_size()
            surface = pygame.transform.scale(surface, screen_size)

            # Отрисовка
            self.screen.blit(surface, (0, 0))
            pygame.display.update()

            # Обработка событий
            for event in pygame.event.get():
                if event.type in [pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    running = False

            clock.tick(fps)

        # Очистка
        cap.release()
        pygame.mixer.music.stop()
        pygame.display.quit()
        return True
