import threading
import websockets
import time
import asyncio

class SessionManager:

    def __init__(self, ip, port):
        self._session_id = None
        self._ip = ip
        self._port = port

    async def create_session(self, recreate=False):
        if recreate or not self._session_id:
            # socket = websockets.connect("ws://%s:%i" % (self._ip, self._port))
            async with websockets.connect("ws://%s:%i" % (self._ip, self._port)) as websocket:
                websocket.send('{"handshake_req":{"version":"3.1.1.3","browser":"Firefox 88.0","js_lib_version":"3.1.1.3","installer_key":"qSytHg7BcJ","env":"production"}}')
                session = websocket.recv()
                print(session)

            