from encrypt_plugins.plugin_base import EncryptPlugin
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
import hashlib

class DESPlugin(EncryptPlugin):
    def __init__(self, key: str):
        # 只保留前 8 字节的 key
        super().__init__(key[:8])

    def encrypt(self, data: bytes) -> bytes:
        key_bytes = self.key.encode().ljust(8, b'\0')[:8]  # DES 固定 8 字节密钥
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        return cipher.encrypt(pad(data, DES.block_size))

    def decrypt_code(self, input_var: str, output_var: str) -> str:
        return f'''
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import unpad

key = "{self.key}".encode().ljust(8, b'\\0')[:8]
cipher = DES.new(key, DES.MODE_ECB)
{output_var} = unpad(cipher.decrypt({input_var}), DES.block_size)
'''
