import base64
from encrypt_plugins.plugin_base import EncryptPlugin

class Base64Plugin(EncryptPlugin):
    def encrypt(self, data: bytes) -> bytes:
        return base64.b64encode(data)

    def decrypt_code(self, input_var: str, output_var: str) -> str:
        return f'''
import base64
{output_var} = base64.b64decode({input_var})
'''