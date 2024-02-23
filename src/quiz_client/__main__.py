import asyncio
from websockets import connect, WebSocketClientProtocol
from websockets.exceptions import ConnectionClosedError
import aioconsole
import sys
import json
import string


async def send_receive_messages(uri: str, client_id: str):
    async with connect(uri) as ws:
        await asyncio.gather(
            asyncio.create_task(send_messages(ws, client_id)),
            asyncio.create_task(receive_messages(ws))
        )


async def send_messages(ws: WebSocketClientProtocol, client_id: str):
    while True:
        user_input = await aioconsole.ainput()
        if not user_input:
            continue
        await ws.send(f"{client_id}: {user_input}")


async def receive_messages(ws: WebSocketClientProtocol):
    while True:
        response = await ws.recv()
        message = json.loads(response)
        if isinstance(message, dict):
            print_question(message)
        else:
            print(message)
        print(f"Answer:")


def print_question(question: dict[str, list]):
    '''Nicely print text of the question with possible answeres'''

    print(question['text'])
    for letter, opt in zip(string.ascii_letters, question['options']):
        print(f'\t{letter}) {opt}')


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <client_id>")
        sys.exit(1)

    client_id = sys.argv[1]
    server_uri = f"ws://127.0.0.1:8000/register/{client_id}"

    print("Press Ctrl+C to exit")
    try:
        asyncio.get_event_loop().run_until_complete(
            send_receive_messages(server_uri, client_id))
    except ConnectionClosedError:
        print("\nConnection closed")
        sys.exit()
    except KeyboardInterrupt:
        print("\nExit client")
        sys.exit()
