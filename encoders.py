from abnf import *
from aescipher import AESCipher
from kitty.model.low_level.encoder import *
from kitty.model.low_level.aliases import *
from kitty.model.low_level.field import *
import sys
import time

class WebsocketTextEncoder(StrEncoder):

    def encode(self, value):
        frame = ABNF.create_frame(value, ABNF.OPCODE_TEXT)
        frame = frame.format()
        return Bits(bytes=frame)


class WebsocketBitsEncoder(BitsEncoder):

    def encode(self, value):
        value = value.tobytes()
        # end_anchor = value.find(b"}}")
        # msg = value[value.find(b"}}") :]
        # if end_anchor < 0 and len(value) > 5:

        #     print(str(value))
            
        #     time.sleep(1000)

        frame = ABNF.create_frame(value, ABNF.OPCODE_TEXT)
        frame = frame.format()
        return Bits(bytes=frame)

class WebsocketBinaryBitsEncoder(BitsEncoder):

    def encode(self, value):
        value = value.tobytes()
        # end_anchor = value.find(b"}}")
        # msg = value[value.find(b"}}") :]
        # if end_anchor < 0 and len(value) > 5:

        #     print(str(value))
            
        #     time.sleep(1000)

        frame = ABNF.create_frame(value, ABNF.OPCODE_BINARY)
        frame = frame.format()
        return Bits(bytes=frame)

class WebsocketPingEncoder(BitsEncoder):

    def encode(self, value):
        value = value.tobytes()
        # end_anchor = value.find(b"}}")
        # msg = value[value.find(b"}}") :]
        # if end_anchor < 0 and len(value) > 5:

        #     print(str(value))
            
        #     time.sleep(1000)

        frame = ABNF.create_frame(value, ABNF.OPCODE_PING)
        frame = frame.format()
        return Bits(bytes=frame)

class AESEncrypt(StrEncoder):

    def __init__(self, key, iv):
        self._key = key
        self._iv = iv
        self._cipher = AESCipher(key, iv)

    def encode(self, value):
        return self._cipher.encrypt(value)

WEBSOCKET_TEXT = WebsocketTextEncoder()
WEBSOCKET_BITS = WebsocketBitsEncoder()
WEBSOCKET_PING = WebsocketPingEncoder()
WEBSOCKET_BINARY_BITS = WebsocketBinaryBitsEncoder()
AES_ENCRYPT = AESEncrypt("4rf5KyEjw8cjdisnGieJIUhjjhj5f6z", "gd74jRE90vVD351R")
