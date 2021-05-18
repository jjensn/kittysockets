import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES 


class AESCipher(object):

    def __init__(self, key, iv):
        self.bs = AES.block_size
        self.key = key.encode() + b'\x00'
        self.iv = iv.encode()

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(bytes(raw)))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

# a = AESCipher("4rf5KyEjw8cjdisnGieJIUhjjhj5f6z", "gd74jRE90vVD351R")

# print(a.encrypt("kung fu u"))
# a = AESCipher("4rf5KyEjw8cjdisnGieJIUhjjhj5f6z", "gd74jRE90vVD351R")

#             encoded = a.encrypt(to_encrypt)
#             msg = msg.replace(to_encrypt, encoded)
