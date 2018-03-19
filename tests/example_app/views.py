from manifold.handler import create_handler


handler = create_handler()


@handler.map_function('pingPong')
def handle_ping_pong(value):

    if value == 5:
        return True

    return False
