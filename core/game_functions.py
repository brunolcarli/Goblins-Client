import sys
import pygame
import redis


def check_events(input_box):
    """
    Verifica e responde a eventos de teclas e mouse.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = redis.Redis()
            r.delete('login')
            sys.exit()
        else:
            input_box.handle_event(event)


def update_screen(settings, screen, entities):
    """
    Atualiza as imagens da tela.
    """
    # preenche a cor de fundo
    screen.fill(settings.bg_color)

    for entity in entities:
        entity.blitme()

    # Atualiza frame principal
    pygame.display.flip()
