import requests
import pygame
from core.settings import Settings
from core.api_call import Query


class Goblin:
    def __init__(self, reference, screen):
        self.reference = reference
        self.screen = screen
        self.settings = Settings()

        self.image = pygame.image.load('static/img/goblins/goblin.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Inicializa os goblins na parte inferior central da tela
        self.rect.centerx = self.screen_rect.centerx
        self.rect_bottom = self.screen_rect.bottom


    def update(self):
        """
        Atualiza posição no cenário de acordo com a flag de movimento.
        """
        pass

    def update_location_from_api(self):
        response = Query.get_position(self.reference)
        position = response['position']['location']
        self.rect.centerx = position['x']
        self.rect.centery = position['y']
        self.blitme()


    def blitme(self):
        self.screen.blit(self.image, self.rect)
