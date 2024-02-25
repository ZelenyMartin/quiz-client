import asyncio
from websockets import connect, WebSocketClientProtocol
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
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
        if user_input:
            await ws.send(json.dumps({client_id: user_input}))


async def receive_messages(ws: WebSocketClientProtocol):
    while True:
        response = await ws.recv()
        message = json.loads(response)

        if message.get('type') == 'question':
            print_question(message)
        else:
            print(message['text'])


def print_question(question: dict[str, list]):
    '''Nicely print text of the question with possible answeres'''

    print(f"Question: {question['text']}")
    for letter, opt in zip(string.ascii_letters, question['options']):
        print(f'\t{letter}) {opt}')
    print("Answer:")


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(f"Usage: {sys.argv[0]} <url> [<client_id>]")
    elif len(sys.argv) == 3:
        client_id = sys.argv[2]
    else:
        client_id = input("Pick you name: ")

    server_url = f"ws://{sys.argv[1]}/register/{client_id}"

    try:
        asyncio.get_event_loop().run_until_complete(
            send_receive_messages(server_url, client_id))
    except OSError:
        sys.exit("Client: cannot reach server")
    except ConnectionClosedOK as e:
        print(e.reason)
    except ConnectionClosedError:
        print("Client: server disconected")
    except KeyboardInterrupt:
        print("\nClient: exit")
        sys.exit()
