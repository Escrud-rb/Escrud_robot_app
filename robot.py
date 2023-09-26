import websocket
import _thread
import time
import rel
import json

#import model


def on_message(ws, message):
    # ws.send()
    print(message)
    data = json.loads(message)
    if data['type'] == 'test_robot':
        if True:
            ws.send(json.dumps({
                'type': 'create_test_response',
                'content': {},
                'status': 200
            }))
    else:
        ws.send(json.dumps({
            'type': data.get('type'),
            'status': 400
        }))


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


def main():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.1.105:8000/ws/robot/main/",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()


if __name__ == '__main__':
    main()
