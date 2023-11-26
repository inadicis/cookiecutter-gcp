from typing import Callable

import socketio

from src.config.env_settings import get_env_settings


redis_manager = socketio.AsyncRedisManager(get_env_settings().redis_url)
sio = socketio.AsyncServer(
    async_mode="asgi",
    logger=True,
    client_manager=redis_manager,
)


def get_event_handlers(local: bool = False) -> list[tuple[Callable, str]]:
    # TODO-CONFIG: register new event handlers here
    from src.event_handlers import connect, disconnect, ping, pong
    event_handlers = [
        (connect, "connect"),
        (disconnect, "disconnect"),
        (ping, "ping"),
        (pong, "pong"),
    ]
    if local:
        from src.event_handlers import hello_local
        event_handlers.append((hello_local, "local"))
    return event_handlers
