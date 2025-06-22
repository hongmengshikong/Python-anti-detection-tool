import base64
from encrypt_plugins.plugin_base import EncryptPlugin

class CustomBase64Plugin(EncryptPlugin):
    def __init__(self, key: str = ""):
        super().__init__(key)
        self.custom_table = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/"
        self.standard_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        self.encode_map = str.maketrans(self.standard_table, self.custom_table)
        self.decode_map = str.maketrans(self.custom_table, self.standard_table)

    def encrypt(self, data: bytes) -> bytes:
        std_encoded = base64.b64encode(data).decode("utf-8")
        custom_encoded = std_encoded.translate(self.encode_map)
        return custom_encoded.encode("utf-8")

    def decrypt_code(self, input_var: str, output_var: str) -> str:
        return f'''
import base64
custom_table = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/"
standard_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
decode_map = str.maketrans(custom_table, standard_table)
std_encoded = {input_var}.decode("utf-8").translate(decode_map)
{output_var} = base64.b64decode(std_encoded)
'''