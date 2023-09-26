# chat/consumers.py
import json
from channels.db import database_sync_to_async
from .models import *


def robot_views():
    return {
        'main':         main,
        'DATA_TYPES':   [
            'test_robot',
        ],
    }


async def connect(socket):
    pass


async def disconnect(socket):
    pass


async def main(socket, data):
    if data['type'] == 'test_robot':
        await _handle_test_robot(socket, data)

    else:
        await _send(socket, {
            'type': 'ws_robot',
            'status': 'warning',
            'content': data['content']
        })


async def _send(socket, data, to=None):
    print('----------SEND DATA-----------')
    print(to)
    if to is not None:
        print('transfert send ')
        await socket.channel_layer.group_send(
            str(to),
            {
                'type': 'transfert',
                'data': data
            }
        )
    else:
        await socket.send(text_data=json.dumps(data))


async def _handle_test_robot(socket, data):
    print('_handle_get_fiche')
    data = await _test_robot(socket, data)

    print('send response fiche')
    await _send(socket, {
        'type': 'test_robot',
        'status': 'success',
        'content': data
    }, socket.client == 'app' and 'robot' or 'app')


@database_sync_to_async
def _test_robot(socket, data):
    return 'test success'
