from core.action_commands import move



def handle_action(player, command_input):
    commands = {
        'move': move
    }
    command, *params = command_input.split()
    if command in commands:
        commands[command](player, params)



def handle_combat(command_input):
    print('combat handler not implemented')
    print(command_input)


def handle_say(command_input):
    print('say handler not implemented')
    print(command_input)


def handle_command_input(player, text_input):
    """
    Handling de comandos.
    """
    handlers = {
        '/': handle_action,
        '>': handle_combat,
        '+': handle_say
    }
    prefix = text_input[0]

    if prefix in handlers:
        handlers[prefix](player, text_input[1:])
