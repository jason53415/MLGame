import pygame

from mlgame.gamedev.generic import quit_or_esc, KeyCommandMap

from .gamecore import GameStatus, PlatformAction, Scene
from .record import get_record_handler

class Arkanoid:
    def __init__(self, fps: int, difficulty, level: int, record_progress, one_shot_mode):
        self._init_pygame()

        self._fps = fps
        self._scene = Scene(difficulty, level)
        self._keyboard = KeyCommandMap({
                pygame.K_a:     PlatformAction.SERVE_TO_LEFT,
                pygame.K_d:     PlatformAction.SERVE_TO_RIGHT,
                pygame.K_LEFT:  PlatformAction.MOVE_LEFT,
                pygame.K_RIGHT: PlatformAction.MOVE_RIGHT,
            }, PlatformAction.NONE)

        self._record_handler = get_record_handler(record_progress, \
            "manual_" + str(difficulty) + "_" + str(level))
        self._one_shot_mode = one_shot_mode

    def _init_pygame(self):
        pygame.display.init()
        pygame.display.set_caption("Arkanoid")
        self._screen = pygame.display.set_mode(Scene.area_rect.size)
        self._clock = pygame.time.Clock()

    def game_loop(self):
        while not quit_or_esc():
            command = self._keyboard.get_command()
            self._record_scene_info(command)
            game_status = self._scene.update(command)

            if game_status == GameStatus.GAME_OVER or \
               game_status == GameStatus.GAME_PASS:
                print(game_status.value)
                self._record_scene_info(None)

                if self._one_shot_mode:
                    return

                self._scene.reset()

            self._screen.fill((0, 0, 0))
            self._scene.draw_gameobjects(self._screen)
            pygame.display.flip()

            self._clock.tick(self._fps)

    def _record_scene_info(self, command):
        scene_info = self._scene.get_scene_info()
        if command:
            scene_info.command = command
        self._record_handler(scene_info)
