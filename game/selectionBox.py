import pygame
from .settings import *


class SelectionBox:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 0, 0)
        self.start_x = x
        self.start_y = y
        self.color = SELECTION_BOX_COLOR
        self.visible = False

    def update(self, current_x, current_y):
        # Update the rect to always have positive width and height
        new_width = current_x - self.start_x
        new_height = current_y - self.start_y
        if new_width < 0:
            self.rect.x = current_x
            self.rect.width = -new_width
        else:
            self.rect.x = self.start_x
            self.rect.width = new_width
        if new_height < 0:
            self.rect.y = current_y
            self.rect.height = -new_height
        else:
            self.rect.y = self.start_y
            self.rect.height = new_height

    def draw(self, surface):
        if self.visible:
            temp_surface = pygame.Surface(
                (self.rect.width, self.rect.height), pygame.SRCALPHA)
            temp_surface.fill(self.color)

            surface.blit(temp_surface, (self.rect.x, self.rect.y))

            pygame.draw.rect(
                surface, SELECTION_BOX_OUTLINE_COLOR, self.rect, 1)
