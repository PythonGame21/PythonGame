import pygame
import random

from consts import *
from vector import Vector
from os import path

img_dir = path.join(path.dirname(__file__), 'img')


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, location, dir, size):
        pygame.sprite.Sprite.__init__(self)

        astr_image = pygame.image.load(path.join(img_dir, "asteroid.png"))
        self.size = size
        self.or_image = pygame.transform.scale(astr_image, (self.size, self.size))
        self.image = self.or_image

        self.location = location

        self.rect = self.image.get_rect(center=(self.location.x, self.location.y))
        self.radius = int(self.rect.width * 0.85 / 2)

        self.speed = random.randrange(20, 150) / FPS
        self.move_dir = dir.normalized() * self.speed

        self.rot_speed = random.randrange(-200, 200)
        self.rot_dir = Vector(1, 0)

    def move(self):
        self.location += self.move_dir

    def update(self):
        if self.rect.top > HEIGHT:
            x = self.rect.x + self.rect.width / 2
            y = -self.rect.height / 2
            self.relocate(x, y)
        if self.rect.bottom < 0:
            x = self.rect.x + self.rect.width / 2
            y = HEIGHT + self.rect.height / 2
            self.relocate(x, y)
        if self.rect.left > WIDTH:
            x = -self.rect.width / 2
            y = self.rect.y + self.rect.height / 2
            self.relocate(x, y)
        if self.rect.right < 0:
            x = WIDTH + self.rect.width / 2
            y = self.rect.y + self.rect.height / 2
            self.relocate(x, y)
        self.move()
        self.rotate(self.rot_speed)
        self.update_image()
        self.rect = self.image.get_rect(center=(self.location.x, self.location.y))

    def relocate(self, x, y):
        self.location = Vector(x, y)

    def rotate(self, rot_angle):
        self.rot_dir = self.rot_dir.rotate(rot_angle / FPS)

    def update_image(self):
        self.image = pygame.transform.rotozoom(self.or_image, self.rot_dir.angle(), 1)

    def __getstate__(self) -> dict:
        state = {}
        state["location"] = self.location
        state["speed"] = self.speed
        state["move_dir"] = self.move_dir
        state["rot_speed"] = self.rot_speed
        state["size"] = self.size
        return state

    def __setstate__(self, state: dict):
        self.__init__(state["location"], state["move_dir"], state["size"])
        self.speed = state["speed"]
        self.move_dir = state["move_dir"]
        self.rot_speed = state["rot_speed"]
