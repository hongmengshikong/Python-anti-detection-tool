from encrypt_plugins.plugin_base import EncryptPlugin

class XORPlugin(EncryptPlugin):
    def encrypt(self, data: bytes) -> bytes:
        key_bytes = self.key.encode()
        key_len = len(key_bytes)
        return bytes([b ^ key_bytes[i % key_len] for i, b in enumerate(data)])

    def decrypt_code(self, input_var: str, output_var: str) -> str:
        return f'''
key = "{self.key}"
key_bytes = key.encode()
{output_var} = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate({input_var})])
'''