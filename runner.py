from binascii import hexlify
from katnip.targets.tcp import TcpTarget
from kitty.model import GraphModel, Template
from kitty.interfaces import WebInterface
from kitty.fuzzers import ServerFuzzer
from kitty.model.low_level.aliases import *
from kitty.model.low_level.field import *
from kitty.model.low_level.container import *

from encoders import *
from server_controller import SessionServerController


import sys
import json

target_ip = "127.0.0.1"
target_port = 9700
web_port = 26001


init_websocket = Template(
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

init_handshake = Template(
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

user_id_fuzz = Template(
    name="set_user_id",
    fields=[
        String(value='{"execute_command":{"session":"', fuzzable=False),
        Dynamic(key="session_id", default_value=""),
        String(
            value='","command":"SET_USER_ID", "params":["user_id"],"values":[',
            fuzzable=False,
        ),
        String(value='9687498355'),
        String(value=']}}', fuzzable=False),
    ],
    encoder=WEBSOCKET_BITS,
)

# send_data = Template(name='send_data', fields=[
#     UInt8(value=2, name='op_code', fuzzable=False),
#     Dynamic(key='session_id', default_value='\x00\x00'),
#     String(name='data', value='some data')
# ])


def new_session_callback(fuzzer, edge, resp):
    """
    :param fuzzer: the fuzzer object
    :param edge: the edge in the graph we currently at.
                 edge.src is the get_session template
                 edge.dst is the send_data template
    :param resp: the response from the target
    """
    msg = resp[resp.find(b"{") :]
    resp = json.loads(msg.decode())
    if "handshake_resp" in resp:
        handshake_resp = resp["handshake_resp"]
        if "session" in handshake_resp:
            fuzzer.logger.info("session is: %s" % handshake_resp["session"])
            fuzzer.target.session_data["session_id"] = handshake_resp["session"]


# Define session target
target = TcpTarget(
    name="session_test_target", host=target_ip, port=target_port, timeout=2
)
# Make target expect response
target.set_expect_response(True)


# Define controller
controller = SessionServerController(
    name="ServerController", host=target_ip, port=target_port
)
target.set_controller(controller)

# Define model
model = GraphModel()
model.connect(init_websocket)
model.connect(init_websocket, init_handshake)
model.connect(init_handshake, user_id_fuzz, new_session_callback)

# Define fuzzer
fuzzer = ServerFuzzer()
fuzzer.set_interface(WebInterface(port=web_port))
fuzzer.set_model(model)
fuzzer.set_target(target)
fuzzer.set_delay_between_tests(0.2)

try:
    fuzzer.start()
except Exception as e:
    sys.exit(e)

sys.exit("Done!")
