from time import sleep
import sys
import pygame
from pygame.constants import BUTTON_X2
from core.settings import Settings
from core.characters.goblin import Goblin
import core.game_functions as gf
from core.api_call import Query
from core.util import InputBox, Worker, DummyInputBox
from kombu import Exchange
from kombu.mixins import ConsumerMixin
from kombu import Connection, Queue
import redis

pygame.init()


def callback(body, message):
    print(body)
    message.ack()


def run_game():
    settings = Settings()
    r = redis.Redis(decode_responses=True)
    username = r.get('username')

    screen = pygame.display.set_mode(
        (settings.screen_width,  settings.screen_height)
    )
    pygame.display.set_caption('Goblins')

    # instancia um goblin
    goblin = Goblin('player', screen)

    # foo = Goblin('teste 1', screen)
    # baz = Goblin('teste 2', screen)

    # entrada de texto
    players = Query.get_logged_entities()
    ents = [Goblin(p['name'], screen) for p in players['entities']]

    for ent in ents:
        ent.update_location_from_api()
        if ent.reference == username:
            input_box = InputBox(0, settings.screen_height - 40, 140, 32, screen, ent)

    ents.extend([input_box])

    # rabbit
    queue = Queue('action_commands', routing_key='action_command')

    conn =  Connection(
        hostname='192.168.25.3',
        userid='guest',
        password='guest',
        virtual_host='beelze')

    worker = Worker(conn, ents)

    while True:
        # captura de eventos
        gf.check_events(input_box)
        input_box.update()
        input_box.draw(screen)

        gf.update_screen(settings, screen, ents)

        try:
            next(worker.consume(timeout=1))
        except:
            pass


def login_screen():
    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width,  settings.screen_height)
    )
    pygame.display.set_caption('Goblins')

    logged = False

    r = redis.Redis(decode_responses=True)
    username = r.get('username')
    password = r.get('password')

    import requests
    box = DummyInputBox(200, 180, 140, 32, screen, 'username')
    box2 = DummyInputBox(200, 180, 140, 32, screen, 'password', is_pwd=True)
    while True:
        if not username:
            
            gf.check_events(box)

            box.update()
            box.draw(screen)

            gf.update_screen(settings, screen, [box])


        elif not password:
            gf.check_events(box2)

            box2.update()
            box2.draw(screen)

            gf.update_screen(settings, screen, [box2])

        username = r.get('username')
        password = r.get('password')

        if username and password:
            url = 'http://localhost:11000/graphql/'
            data = f'''
            mutation {{
                logIn(username: "{username}" password: "{username}"){{
                    token
                }}
            }}
            '''
            rq = requests.post(url, json={'query': data}).json()
            if not rq['data']['logIn']:
                r.delete('username')
                r.delete('password')
                print('Login failed')
            else:
                r.set('login', rq['data']['logIn']['token'])
                r.delete('password')
                print('Login succesfull')
                return 'logged'


login = login_screen()
if login == 'logged':
    run_game()

