import threading
import websocket
import time
try:
    import thread
except ImportError:
    import _thread as thread
import json
import uuid
import sys

class SessionManager:

    def __init__(self, ip, port):
        self._session_id = None
        self._ip = ip
        self._port = port

    def create_session(self, recreate=False):
          self._ws = websocket.WebSocketApp("ws://%s:%i" % (self._ip, self._port), on_open=self.on_open, on_message = self.on_message, on_error = self.on_error, on_close = self.on_close)
          self._ws.run_forever(ping_interval=15, ping_timeout=10)

    def on_message(self, ws, message):
        session = json.loads(message)
        self._session_id = session['handshake_resp']['session']
        print("[+] Session ID: %s" % self._session_id)

    def on_error(self, ws, error):
        self._session_id = None
        print(error)
        sys.exit("ON ERROR")

    def on_close(self, ws):
        self._session_id = None
        print("### closed ###")
        sys.exit("ON CLOSE")

    def on_open(self, ws):
        def run(*args):
            ws.send('{"handshake_req":{"version":"3.1.1.3","browser":"Firefox 88.0","js_lib_version":"3.1.1.3","installer_key":"qSytHg7BcJ","env":"production"}}')
        thread.start_new_thread(run, ())
        
    def shim(self):
        while True:
            if not self._session_id or not self._ws.sock.connected:
                self.create_session()

    def start(self):
        t=threading.Thread(target=self.shim)
        t.start()