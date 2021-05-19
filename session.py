import threading
import websockets
import time
import asyncio
import json
import uuid

class SessionManager:

    def __init__(self, ip, port):
        self._session_id = None
        self._ip = ip
        self._port = port

    async def create_session(self, recreate=False):
      while True:
        if recreate or not self._session_id:
            # socket = websockets.connect("ws://%s:%i" % (self._ip, self._port))
            async with websockets.connect("ws://%s:%i" % (self._ip, self._port)) as websocket:
                await websocket.send('{"handshake_req":{"version":"3.1.1.3","browser":"Firefox 88.0","js_lib_version":"3.1.1.3","installer_key":"qSytHg7BcJ","env":"production"}}')
                resp = await websocket.recv()
                session = json.load(resp)
                self._session_id = session['handshake_resp']['session']
                print(self._session_id)
                while self._session_id:
                    print("pinging")
                    await asyncio.sleep(10)
                    websocket.ping(str(uuid.uuid4()))
                

    def shim(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_forever(self.create_session())
        # loop.run_until_complete(self.create_session())
        loop.close()

    def start(self):
        _thread = threading.Thread(target=self.shim)
        _thread.start()