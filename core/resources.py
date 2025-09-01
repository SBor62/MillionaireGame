import pygame
from pathlib import Path


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.loaded = False
        self.current_music = None
        self.initialize_audio()

    def set_music_volume(self, volume):
        """Устанавливает громкость ТОЛЬКО для фоновой музыки"""
        pygame.mixer.music.set_volume(volume)
        print(f"Громкость музыки установлена: {volume}")

    def get_music_volume(self):
        """Возвращает текущую громкость музыки"""
        return pygame.mixer.music.get_volume()

    def initialize_audio(self):
        """Инициализирует аудиосистему"""
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.load_sounds()
            self.loaded = True
            print("Аудиосистема инициализирована успешно")
        except Exception as e:
            print(f"Ошибка инициализации аудио: {e}")

    def load_sounds(self):
        """Загружает звуки из указанной директории"""
        sound_files = {
            "correct": "correct.mp3",
            "wrong": "wrong.mp3",
            "menu": "menu.mp3",
            "game": "game.mp3",
            "win": "win.mp3",
            "lose": "lose.mp3",
            "end": "end.mp3",
            "victory": "victory.mp3",
            "win_end": "win_end.mp3"
        }

        for name, filename in sound_files.items():
            try:
                path = Path("assets/sounds") / filename
                if path.exists():
                    self.sounds[name] = pygame.mixer.Sound(path)
                    print(f"Звук {filename} загружен успешно")
                else:
                    print(f"Файл не найден: {path}")
            except Exception as e:
                print(f"Ошибка загрузки звука {filename}: {e}")

    def play_sound(self, sound_name, volume=1.0, loop=False):

        """Воспроизводит указанный звук"""
        if not self.loaded:
            return False

        # Звуки с голосом всегда на 100% громкости
        voice_sounds = ["correct", "wrong", "victory", "end"]
        if sound_name in voice_sounds:
            volume = 1.0  # Всегда 100% для голосовых звуков
        else:
            # Для фоновой музыки используем ТЕКУЩУЮ громкость из настроек
            volume = self.get_music_volume()  # ← ВОТ ИСПРАВЛЕНИЕ!

        # Для фоновой музыки используем pygame.mixer.music
        if sound_name in ["menu", "game", "win", "lose"]:
            return self._play_background_music(sound_name, volume, loop)

        if sound_name not in self.sounds:
            return False

        try:
            channel = pygame.mixer.find_channel()
            if channel:
                sound = self.sounds[sound_name]
                sound.set_volume(volume)
                if loop:
                    channel.play(sound, loops=-1)
                else:
                    channel.play(sound)
                return True
        except Exception as e:
            print(f"Ошибка воспроизведения {sound_name}: {e}")
        return False

    def _play_background_music(self, music_name, volume=0.7, loop=True):
        """Воспроизводит фоновую музыку (внутренний метод)"""
        if not self.loaded:
            return False

        try:
            # Останавливаем текущую музыку
            pygame.mixer.music.stop()

            # Загружаем и воспроизводим новую музыку
            music_path = Path("assets/sounds") / f"{music_name}.mp3"
            if music_path.exists():
                pygame.mixer.music.load(music_path)
                # ВОТ ИСПРАВЛЕНИЕ: Устанавливаем громкость ПЕРЕД воспроизведением
                pygame.mixer.music.set_volume(volume)
                if loop:
                    pygame.mixer.music.play(loops=-1)
                else:
                    pygame.mixer.music.play()
                self.current_music = music_name
                return True
            else:
                print(f"Музыкальный файл не найден: {music_path}")
        except Exception as e:
            print(f"Ошибка воспроизведения музыки {music_name}: {e}")
        return False

    def stop_all_sounds(self):
        """Останавливает все звуки и музыку"""
        if self.loaded:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            self.current_music = None

    def stop_music(self):
        """Останавливает только фоновую музыку"""
        if self.loaded:
            pygame.mixer.music.stop()
            self.current_music = None

    def pause_music(self):
        """Приостанавливает музыку"""
        if self.loaded and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def unpause_music(self):
        """Возобновляет музыку"""
        if self.loaded:
            pygame.mixer.music.unpause()
