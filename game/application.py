import pygame
import sys
from .settings import *
from .loop import Loop


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.loop = Loop()
        pygame.display.set_caption('Digital Logic Simulator')

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.loop.run(dt, events)  # Pass events to Loop
            pygame.display.update()
