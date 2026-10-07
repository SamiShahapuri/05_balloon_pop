"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.

Starter version: one balloon type (random size, fixed points), no
lives system yet, no timer yet. Click detection also has a known bug
(see game/click_detection.py) that Task 1 asks you to fix.
"""

import random

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)

        balloon_type = random.choices(
            ["normal", "bonus", "penalty"],
            weights=[70, 15, 15],
            k=1,
        )[0]

        self.balloons.append(
            Balloon(
                x=x,
                y=-radius,
                radius=radius,
                speed=speed,
                balloon_type=balloon_type,
            )
        )

    def handle_click(self, pos):
        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0 and not self.game_over:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        remaining_balloons = []

        for b in self.balloons:
            if b.is_past_bottom(HEIGHT):
                self.lives -= 1
            else:
                remaining_balloons.append(b)

        self.balloons = remaining_balloons

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 40))

        if self.game_over:
            renderer.draw_text(
                surface,
                font,
                "GAME OVER",
                (WIDTH // 2 - 70, HEIGHT // 2),
            )
            renderer.draw_text(
                surface,
                font,
                f"Final Score: {self.score}",
                (WIDTH // 2 - 90, HEIGHT // 2 + 40),
            )
