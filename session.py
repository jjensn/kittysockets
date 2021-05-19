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
            # socket = websockets.connect("ws://%s:%i" % (self._ip, self._port))
      async with websockets.connect("ws://%s:%i" % (self._ip, self._port)) as websocket:
          await websocket.send('{"handshake_req":{"version":"3.1.1.3","browser":"Firefox 88.0","js_lib_version":"3.1.1.3","installer_key":"qSytHg7BcJ","env":"production"}}')
          resp = await websocket.recv()
          session = json.loads(resp)
          self._session_id = session['handshake_resp']['session']
          print(self._session_id)
          websocket.run_forever(ping_interval=10, ping_timeout=10)
                

    def shim(self):
        while True:
            if not self._session_id:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                loop.create_task(self.create_session())
                loop.run_forever()
        # loop.close()

    def start(self):
        _thread = threading.Thread(target=self.shim)
        _thread.start()