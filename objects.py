import pygame
from typing import Literal
import random


class Snake:
    def __init__(
        self,
        name: str,
        surface: pygame.Surface,
        color: pygame.Color,
        position: list[int],
        start_direction: Literal["UP", "BOTTOM", "RIGHT", "LEFT"] | None = None,
    ):
        self.surface = surface
        self.x = self.surface.get_bounding_rect().x
        self.y = self.surface.get_bounding_rect().y
        self.name = name
        self._original_position = position
        self.position = position
        self._original_body = [[70, 50]]
        self.body = [[70, 50]]
        self.setup_keys()
        self.speed = 15
        self.score = 0
        self.direction = start_direction or "RIGHT"
        self.change_to = self.direction
        self.color = color

    def setup_movement(self, event: pygame.event.Event):
        if event.key == self.keys["UP"]:
            self.change_to = "UP"
        if event.key == self.keys["DOWN"]:
            self.change_to = "DOWN"
        if event.key == self.keys["LEFT"]:
            self.change_to = "LEFT"
        if event.key == self.keys["RIGHT"]:
            self.change_to = "RIGHT"

    def setup_keys(
        self,
        up: int | None = None,
        right: int | None = None,
        bottom: int | None = None,
        left: int | None = None,
    ):
        self.keys = {
            "UP": up or pygame.K_UP,
            "DOWN": bottom or pygame.K_DOWN,
            "LEFT": left or pygame.K_LEFT,
            "RIGHT": right or pygame.K_RIGHT,
        }

    def setup_collissions(self, fruit: "Fruit"):
        self.body.insert(0, list(self.position))

        if (
            self.position[0] == fruit.position[0]
            and self.position[1] == fruit.position[1]
        ):
            self.score += 10
            if self.score % 3 == 0:
                self.speed += 1
            fruit.should_spawn = False
        else:
            self.body.pop()

    def draw(self):
        for pos in self.body:
            pygame.draw.rect(
                self.surface, self.color, pygame.Rect(pos[0], pos[1], 10, 10)
            )

    def move(self):
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        if self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        if self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

        # Moving the snake
        if self.direction == "UP":
            self.position[1] -= 10
        if self.direction == "DOWN":
            self.position[1] += 10
        if self.direction == "LEFT":
            self.position[0] -= 10
        if self.direction == "RIGHT":
            self.position[0] += 10

    def reset(self):
        self.body = self._original_body
        self.position = self._original_position
        self.score = 0

    def did_collide_with_borders(self) -> bool:
        if (
            self.position[0] < 0
            or self.position[0] > self.surface.get_bounding_rect().width - 10
        ):
            return True
        if (
            self.position[1] < 0
            or self.position[1] > self.surface.get_bounding_rect().height - 10
        ):
            return True

        return False


class Fruit:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.should_spawn = True

        self.position = [
            random.randrange(1, (self.surface.get_bounding_rect().width // 10)) * 10,
            random.randrange(1, (self.surface.get_bounding_rect().height // 10)) * 10,
        ]

    def spawn(self):
        self.position = [
            random.randrange(1, (self.surface.get_bounding_rect().width // 10)) * 10,
            random.randrange(1, (self.surface.get_bounding_rect().height // 10)) * 10,
        ]
