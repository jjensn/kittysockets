
from command_fuzzers.user_id import SetUserID
from session import SessionManager

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

session_mgr = SessionManager(target_ip, target_port)
# Make target expect response

# def set_var(fuzzer, edge, resp):
  # fuzzer.target.session_data["session_id"] = session_mgr._session_id
  #print("SET SESSION ID!! %s" % session_mgr._session_id)
  #sys.exit("DONE")

# Define model
model = GraphModel()
cmdfuzz = SetUserID(model)
# cmdfuzz = GenericCommand(model)
cmdfuzz.case_1()
cmdfuzz.finalize()

# Define session target
target = WebsocketTarget(
    name="session_test_target", host=target_ip, port=target_port, timeout=2
)
target.set_expect_response(True)
# Define controller
controller = SessionServerController(
    name="ServerController", host=target_ip, port=target_port, session_mgr=session_mgr
)
target.set_controller(controller)

# Define fuzzer
fuzzer = ServerFuzzer()
fuzzer.set_interface(WebInterface(port=web_port))
fuzzer.set_model(model)
fuzzer.set_target(target)
fuzzer.set_delay_between_tests(0.2)
# fuzzer.set_delay_between_tests(30)

fuzzer.start()

