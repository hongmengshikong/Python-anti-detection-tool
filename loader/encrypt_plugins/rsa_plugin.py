# encrypt_plugins/rsa_plugin.py
from encrypt_plugins.plugin_base import EncryptPlugin
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import base64

class RSAPlugin(EncryptPlugin):
    def __init__(self, key: str = ""):
        super().__init__(key)
        self.key_pair = RSA.generate(2048)
        self.public_key = self.key_pair.publickey()
        self.private_key_pem = self.key_pair.export_key().decode()
        self.public_cipher = PKCS1_OAEP.new(self.public_key)

    def encrypt(self, data: bytes) -> bytes:
        # RSA 加密限制长度为 key_size - padding_overhead（如 2048bit = 256byte，最多加密 190~245 bytes）
        # 这里使用 base64 编码绕过非 ASCII shellcode 兼容性
        b64_encoded = base64.b64encode(data)
        chunks = [b64_encoded[i:i+190] for i in range(0, len(b64_encoded), 190)]
        encrypted_chunks = [self.public_cipher.encrypt(chunk) for chunk in chunks]
        return b"".join(encrypted_chunks)

    def decrypt_code(self, input_var: str, output_var: str) -> str:
        return f'''
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

private_key_pem = \"\"\"{self.private_key_pem}\"\"\"
private_key = RSA.import_key(private_key_pem)
cipher_rsa = PKCS1_OAEP.new(private_key)

chunk_size = 256  # 每段加密后的长度（2048位密钥 = 256字节）
chunks = [cipher_rsa.decrypt({input_var}[i:i+chunk_size]) for i in range(0, len({input_var}), chunk_size)]
{output_var} = base64.b64decode(b"".join(chunks))
'''
