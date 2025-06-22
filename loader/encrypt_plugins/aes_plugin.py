from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
from encrypt_plugins.plugin_base import EncryptPlugin

class AESPlugin(EncryptPlugin):
    def encrypt(self, data: bytes) -> bytes:
        key_bytes = hashlib.md5(self.key.encode()).digest()
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        return cipher.encrypt(pad(data, AES.block_size))

    def decrypt_code(self, input_var: str, output_var: str) -> str:
        return f'''
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import hashlib
key_bytes = hashlib.md5("{self.key}".encode()).digest()
cipher = AES.new(key_bytes, AES.MODE_ECB)
{output_var} = unpad(cipher.decrypt({input_var}), AES.block_size)
'''