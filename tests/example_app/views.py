from manifold.handler import handler


@handler.map_function('pingPong')
def handle_ping_pong(value):

    if value == 5:
        return True

    return False
