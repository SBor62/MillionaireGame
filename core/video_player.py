import cv2
import pygame
import os


class VideoPlayer:
    def __init__(self):
        # Инициализация mixer с параметрами, подходящими для аудио
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        self.screen = None

    def play(self, video_path, audio_path="assets/audio/ascreen.mp3", exit_on_click=False):
        """
        Воспроизводит видео и аудио одновременно.
        :param video_path: путь к видео (.mp4)
        :param audio_path: путь к аудио (.mp3, .wav)
        :param exit_on_click: выход по клику
        """
        # Проверяем видео
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Видео не найдено: {video_path}")

        # Открываем видео
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Не удалось открыть видео: {video_path}")

        # Получаем FPS и размеры
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 24  # Подстраховка
        # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Настройка pygame
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Видеозаставка")
        clock = pygame.time.Clock()

        # Загружаем и запускаем аудио
        if os.path.exists(audio_path):
            try:
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()  # Запускаем аудио
            except Exception as e:
                print(f"[Предупреждение] Не удалось воспроизвести аудио: {e}")
        else:
            print(f"[Предупреждение] Аудиофайл не найден: {audio_path}")

        # Главный цикл воспроизведения
        running = True
        while running:
            # Читаем кадр
            ret, frame = cap.read()
            if not ret:
                break  # Конец видео

            # Конвертируем BGR → RGB, транспонируем под pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    # BGR → RGB
            frame = cv2.transpose(frame)
            # frame = cv2.flip(frame, 0)  # Поворот на 90° и отражение
            surface = pygame.surfarray.make_surface(frame)

            # Масштабируем на весь экран
            screen_size = self.screen.get_size()
            surface = pygame.transform.scale(surface, screen_size)

            # Отрисовка
            self.screen.blit(surface, (0, 0))
            pygame.display.update()

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if exit_on_click and event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            clock.tick(fps)

        # Очистка
        cap.release()
        pygame.mixer.music.stop()
        pygame.display.quit()  # Закрываем окно pygame
