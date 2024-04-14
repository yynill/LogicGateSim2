import pygame
from .settings import *


class AlertHandler():
    def __init__(self, message, alert_type, position):
        super().__init__()
        self.message = message
        self.position = position
        self.duration = 3
        self.background_color = WHITE
        self.alert_type = alert_type

        if self.alert_type == "error":
            self.text_color = ALERT_ERROR_COLOR
        elif self.alert_type == "success":
            self.text_color = ALERT_SUCCESS_COLOR
        else:
            self.text_color = BLACK

        self.font = pygame.font.Font(None, 20)
        self.start_ticks = pygame.time.get_ticks()  # Start time
        self.visible = True

        # Render the alert box
        self.image = self.font.render(self.message, True, self.text_color)
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        current_ticks = pygame.time.get_ticks()
        if current_ticks - self.start_ticks >= self.duration * 1000:
            self.visible = False

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.background_color,
                             self.rect.inflate(20, 10))
            surface.blit(self.image, self.rect)
