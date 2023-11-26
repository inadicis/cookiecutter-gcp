"""
Client useful for manual testing (meant as help tool next to the
automated test, should not replace them!), can be used to simulate
frontend logic.
Not part of the actual backend logic.
"""

import asyncio
import os

import socketio

sio = socketio.AsyncClient(logger=True, engineio_logger=True, ssl_verify=False)

jwtoken = ""
# update your token if auth is activated. If auth is not mocked, use the
# environment variable AUTH0_JWT instead


@sio.event
async def connect():
    print("Heyho - connection established")  # noqa: T201


@sio.event
async def my_message(data):
    print("message received with ", data)  # noqa: T201
    await sio.emit("my_response", {"response": "my response"})


@sio.event
async def disconnect():
    print("disconnected from server")  # noqa: T201


@sio.event
async def ping():
    print("ping received")  # noqa: T201
    await sio.emit("pong",
                   )


@sio.event
async def pong(data):
    print("pong received: ", data)  # noqa: T201
    await sio.emit("confirm_pong",
                   )
    # await sio.emit('pong')


async def main():
    signed_jwt = os.environ.get("AUTH0_JWT", jwtoken)
    ws_auth_active = False
    url = os.environ.get("ROBINQA_URL", "http://localhost:8000")
    try:
        if ws_auth_active:
            await sio.connect(url,
                              socketio_path="/ws",
                              auth=signed_jwt,
                              )
        else:
            await sio.connect(url,
                              socketio_path="/ws",
                              auth=None
                              )
        await sio.emit("ping", "Hello world",
                       )
        # await sio.wait()
        await sio.sleep(1)
        await sio.disconnect()
    except KeyboardInterrupt:
        await sio.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
