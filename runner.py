
from command_fuzzers.user_id import SetUserID
import sys


# from binascii import hexlify
# from katnip.targets.tcp import TcpTarget
from targets.websocket import WebsocketTarget
from kitty.model import GraphModel, Template
from kitty.interfaces import WebInterface
from kitty.fuzzers import ServerFuzzer

from server_controller import SessionServerController
# from katnip.model.low_level.radamsa import RadamsaField

from command_fuzzers import *

target_ip = "127.0.0.1"
target_port = 9700
web_port = 26001

# Define session target
target = WebsocketTarget(
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
cmdfuzz = SetUserID(model)
# model.connect(init_websocket)
# model.connect(init_websocket, init_handshake)
# model.connect(init_handshake, user_id_fuzz, new_session_callback)

# Define fuzzer
fuzzer = ServerFuzzer()
fuzzer.set_interface(WebInterface(port=web_port))
fuzzer.set_model(model)
fuzzer.set_target(target)
fuzzer.set_delay_between_tests(0.2)

#try:
fuzzer.start()
# except Exception as e:
#     sys.exit(e)

sys.exit("Done!")
