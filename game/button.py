import pygame
from .settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text='', image_path=None):
        super().__init__()
        self.image_path = image_path
        self.image = pygame.Surface([width, height])
        self.image.fill(BUTTON_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        if text != '':
            self.add_text(text)
        if image_path != None:
            self.add_image(image_path=image_path)

    def add_text(self, text):
        font = pygame.font.Font(None, 26)
        text_surf = font.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect()
        text_rect.center = (self.rect.width // 2, self.rect.height // 2)
        self.image.blit(text_surf, text_rect)

    def add_image(self, image_path):
        loaded_image = pygame.image.load(image_path)
        # Resize the image to fit the button if necessary
        loaded_image = pygame.transform.scale(
            loaded_image, (self.rect.width - 20, self.rect.height - 10))
        # center img
        img_rect = loaded_image.get_rect()
        img_rect.center = (self.rect.width // 2, self.rect.height // 2)
        self.image.blit(loaded_image, img_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos):
                    return True
        return False

    def getName(self):
        return self.text


class CableButton(Button):
    def __init__(self, x, y, width, height, image_path=None, text=''):
        super().__init__(x, y, width, height, text, image_path)
        self.mode = False

    def toggle(self, event):
        clicked = super().is_clicked(event)
        if clicked:
            self.mode = not self.mode
        return clicked
