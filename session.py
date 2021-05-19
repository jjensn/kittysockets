import threading
import websocket
import time
try:
    import thread
except ImportError:
    import _thread as thread
import json
import uuid

class SessionManager:

    def __init__(self, ip, port):
        self._session_id = None
        self._ip = ip
        self._port = port

    def create_session(self, recreate=False):
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
          self._ws = websocket.WebSocketApp("ws://%s:%i" % (self._ip, self._port), on_open=self.on_open, on_message = self.on_message, on_error = self.on_error, on_close = self.on_close)
          print("About to run forever")
          self._ws.run_forever(ping_interval=15, ping_timeout=10)

    def on_message(self, ws, message):
        print(message)
        session = json.loads(message)
        self._session_id = session['handshake_resp']['session']
        print(self._session_id)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        def run(*args):
            ws.send('{"handshake_req":{"version":"3.1.1.3","browser":"Firefox 88.0","js_lib_version":"3.1.1.3","installer_key":"qSytHg7BcJ","env":"production"}}')
            # ws.close()
            print("thread terminating...")
        thread.start_new_thread(run, ())
        
    def shim(self):
        print("in shim")
        while True:
            if not self._session_id or not self._ws.sock.connected:
                self.create_session()
                time.sleep(5)
                print("LOOPING")
                # loop = asyncio.new_event_loop()
                # asyncio.set_event_loop(loop)

                # loop.create_task(self.create_session())
                # loop.run_forever()
        # loop.close()

    def start(self):
        thread.start_new_thread(self.shim, ())
        #_thread = threading.Thread(target=self.shim)
        #_thread.start()