from core.api_call import Mutation


def move(player, params):
    if not params:
        return

    direction = params[0]

    move = {
        'up': lambda x, y: (x, y - 48),
        'down': lambda x, y: (x, y + 48),
        'left': lambda x, y: (x - 48, y),
        'right': lambda x, y: (x + 48, y),\
    }
    move.update({
        'u': move['up'],
        'd': move['down'],
        'l': move['left'],
        'r': move['right']
    })
    if direction in move:
        x, y = player.rect.centerx, player.rect.centery
        new_x, new_y = move[direction](x, y)

    response = Mutation.update_position(new_x, new_y, player.reference)