import time
from microWebSrv import MicroWebSrv
from machine import Pin
d12 = Pin(12, Pin.OUT)
# ----------------------------------------------------------------------------


def _acceptWebSocketCallback(webSocket, httpClient):
    print("WS ACCEPT")
    webSocket.RecvTextCallback = _recvTextCallback
    ## webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback = _closedCallback


def _recvTextCallback(webSocket, msg):
    if msg == "LEDon":
    d12.on()
    elif msg == "LEDoff":
    d12.off()
    else:
    print('*')

    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)


def _closedCallback(webSocket):
    print("WS CLOSED")


# ----------------------------------------------------------------------------
if __name__ == "__main__":

    print("Preparing server")
    srv = MicroWebSrv(webPath='www/')
    srv.MaxWebSocketRecvLen = 256
    srv.WebSocketThreaded = True
    srv.AcceptWebSocketCallback = _acceptWebSocketCallback
    print("Starting server")
    srv.Start(threaded=True)

    while True:
    print("*", end='')
    time.sleep(2)
