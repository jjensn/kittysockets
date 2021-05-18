from abnf import *
from kitty.model.low_level.encoder import *
from kitty.model.low_level.aliases import *
from kitty.model.low_level.field import *
import sys


class WebsocketTextEncoder(StrEncoder):

    def encode(self, value):
        # print("ENCODING2 " + str(type(value)))
        # value = str(value)
        # print("ENCODING1 " + str(type(value)))
        frame = ABNF.create_frame(value, ABNF.OPCODE_TEXT)

        frame = frame.format()
        # print("ENCODING " + str(type(frame)))
        return Bits(bytes=frame)


class WebsocketBitsEncoder(BitsEncoder):

    def encode(self, value):
        # print("ENCODING2 " + str(type(value)))
        # value = str(value)
        # print(value.tobytes())
        # print(str(value))
        # sys.exit("DONE")
        frame = ABNF.create_frame(value.tobytes(), ABNF.OPCODE_TEXT)

        frame = frame.format()
        # print("ENCODING " + str(type(frame)))
        return Bits(bytes=frame)


WEBSOCKET_TEXT = WebsocketTextEncoder()
WEBSOCKET_BITS = WebsocketBitsEncoder()
