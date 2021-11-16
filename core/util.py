
from kombu import Producer, Queue
from kombu.mixins import ConsumerMixin
import pygame
import msgpack
from core.handlers import handle_command_input
import redis

pygame.init()
# screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, screen, player, text=''):
        self.reference = 'InputBox'
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.screen = screen
        self.player = player

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    handle_command_input(self.player, self.text.lower())
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def blitme(self):
        self.draw(self.screen)


class DummyInputBox:

    def __init__(self, x, y, w, h, screen, text='', is_pwd=False):
        self.reference = 'DummyBox'
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.active = False
        self.screen = screen
        self.is_pwd = is_pwd
        # self.txt_surface = self.get_text_surface()

    def get_text_surface(self):
        if not self.is_pwd:
            return FONT.render(self.text, True, self.color)

        secret = '*' * len(self.text)
        return FONT.render(secret, True, self.color)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    r = redis.Redis()
                    if self.is_pwd:
                        r.set('password', self.text)
                    else:
                        r.set('username', self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.get_text_surface()

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.get_text_surface().get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.get_text_surface(), (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def blitme(self):
        self.draw(self.screen)


rpc_queue = Queue('action_commands', routing_key='action_command')

class Worker(ConsumerMixin):

    def __init__(self, connection, ents):
        self.connection = connection
        self.ents = ents

    def get_consumers(self, Consumer, channel):
        return [Consumer(
            queues=[rpc_queue],
            on_message=self.on_request,
            accept=['msgpack'],
            prefetch_count=1,
        )]

    def on_request(self, message):
        content = msgpack.unpackb(message.body)
        for ent in self.ents:
            if ent.reference == content.get('reference'):
                ent.rect.centerx = content.get('x')
                ent.rect.centery = content.get('y')
                ent.blitme()
                message.ack()

broker_address='192.168.2.169'

def on_message(client, userdata, message):
    print("message received " , msgpack.unpackb(message.payload))

class W:
    def __init__(self, client, ents):
        self.client = client
        self.client.on_message = self.on_message
        self.client.connect(broker_address, port=18883) #connect to broker
        self.client.subscribe("foo/baz")
        self.ents = ents

    def on_message(self, client, userdata, message):
        print("message received " , msgpack.unpackb(message.payload))
        content = msgpack.unpackb(message.payload)
        for ent in self.ents:
            if ent.reference == content.get('reference'):
                ent.rect.centerx = content.get('x')
                ent.rect.centery = content.get('y')
                ent.blitme()


    def consume(self):
        self.client.loop()
