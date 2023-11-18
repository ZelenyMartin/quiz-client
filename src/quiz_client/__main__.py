import asyncio
from websockets import connect, WebSocketClientProtocol
import aioconsole
import sys

async def send_receive_messages(uri: str, client_id: str):
    async with connect(uri) as ws:
        send_task = asyncio.create_task(send_messages(ws, client_id))
        receive_task = asyncio.create_task(receive_messages(ws))
        await asyncio.gather(send_task, receive_task)


async def send_messages(ws: WebSocketClientProtocol, client_id: str):
    while True:
        user_input = await aioconsole.ainput(f"Client {client_id}: ")
        if not user_input:
            continue
        await ws.send(f"{client_id}: {user_input}")


async def receive_messages(ws: WebSocketClientProtocol):
    while True:
        response = await ws.recv()
        print(f"\nReceived from server: {response}")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <client_id>")
        sys.exit(1)

    client_id = sys.argv[1]
    server_uri = f"ws://127.0.0.1:8000/ws/{client_id}"

    asyncio.get_event_loop().run_until_complete(send_receive_messages(server_uri, client_id))


if __name__ == "__main__":
    main()
