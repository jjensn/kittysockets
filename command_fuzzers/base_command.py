import json
import os
import sys

from kitty.model.low_level.aliases import *
from kitty.model.low_level.field import *
from kitty.model.low_level.container import *
from katnip.model.low_level.radamsa import RadamsaField
from encoders import *
import random

class BaseCommand:

    def __init__(self, model):
        if sys.platform == 'darwin':
            self._radamsa_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../utils/radamsa-osx')
        elif sys.platform == 'win32':
            self._radamsa_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\utils\\radamsa.exe')

        #print(self._radamsa_path)
        #sys.exit("hey")
        self._init_websocket = Template(
            name="init_websocket",
            fields=[
                Static(name="http_get", value="GET / HTTP/1.1\r\n"),
                Static(name="http_host", value="Host: wss.plc-gc.com:9700\r\n"),
                Static(
                    name="http_user",
                    value="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0\r\n",
                ),
                Static(name="http_sockversion", value="Sec-WebSocket-Version: 13\r\n"),
                Static(
                    name="http_socketkey",
                    value="Sec-WebSocket-Key: Pi2r1NMQ1ukNtA/TDvSVtQ==\r\n",
                ),
                Static(name="http_connect", value="Connection: keep-alive, Upgrade\r\n"),
                Static(name="http_ref", value="Origin: https://sportsbook.draftkings.com\r\n"),
                Static(name="http_upgrade", value="Upgrade: websocket\r\n\r\n"),
            ],
        )

        self._init_handshake = Template(
            name="init_handshake",
            fields=[
                String(
                    name="handshake",
                    fuzzable=False,
                    value='{"handshake_req":{"version":"3.1.1.3","browser":"Firefox 88.0","js_lib_version":"3.1.1.3","installer_key":"qSytHg7BcJ","env":"production"}}',
                    encoder=WEBSOCKET_TEXT,
                )
            ],
        )

        self._ping = Template(
            name="websocket_ping",
            fields=[
                Static(value='PING')
            ],encoder=WEBSOCKET_PING
        )

        self._static_user_id = Template(
            name="set_user_id",
            fields=[
                String(value='{"execute_command":{"session":"', fuzzable=False),
                Dynamic(key="session_id", default_value="AAAA"),
                String(
                    value='","command":"SET_USER_ID", "params":["user_id"],"values":[',
                    fuzzable=False,
                ),
                String(value='9687498355', fuzzable=False),
                String(value="]}}", fuzzable=False),
            ],
            encoder=WEBSOCKET_BITS,
        )

        self._model = model

        self._model.connect(self._init_websocket)
        self._model.connect(self._init_websocket, self._init_handshake)
        self._model.connect(self._init_handshake, self._ping, self.new_session_callback)

    def new_session_callback(self, fuzzer, edge, resp):
        """
        :param fuzzer: the fuzzer object
        :param edge: the edge in the graph we currently at.
                    edge.src is the get_session template
                    edge.dst is the send_data template
        :param resp: the response from the target
        """
        if resp and resp.find(b"{") > -1:
            msg = resp[resp.find(b"{") :]
            resp = json.loads(msg.decode())
            if "handshake_resp" in resp:
                handshake_resp = resp["handshake_resp"]
                if "session" in handshake_resp:
                    fuzzer.logger.info("session is: %s" % handshake_resp["session"])
                    fuzzer.target.session_data["session_id"] = handshake_resp["session"]
        else:
            fuzzer.target.session_data["session_id"] = "160c2e63-ad3c-444f-8da7-136698f25ff1"



