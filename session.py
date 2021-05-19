import threading
import websocket
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
      # async with websockets.connect("ws://%s:%i" % (self._ip, self._port)) as websocket:
      #     await websocket.send('{"handshake_req":{"version":"3.1.1.3","browser":"Firefox 88.0","js_lib_version":"3.1.1.3","installer_key":"qSytHg7BcJ","env":"production"}}')
      #     resp = await websocket.recv()
      #     session = json.loads(resp)
      #     self._session_id = session['handshake_resp']['session']
      #     print(self._session_id)
      #     while self._session_id:
      #         # print("pinging")
      #         await asyncio.sleep(10)
      #         await websocket.send('2')
          self._ws = websocket.WebSocketApp("ws://%s:%i" % (self._ip, self._port), on_message = self.on_message, on_error = self.on_error, on_close = self.on_close)

          self._ws.on_open = self.on_open

          self._ws.run_forever(ping_interval=15, ping_timeout=10)

    def on_message(self, message):
        print(message)

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        ws = self._ws
        # p = 'ANY KIND OF OPENING YOU NEED'
        ws.send('{"handshake_req":{"version":"3.1.1.3","browser":"Firefox 88.0","js_lib_version":"3.1.1.3","installer_key":"qSytHg7BcJ","env":"production"}}')
                      

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