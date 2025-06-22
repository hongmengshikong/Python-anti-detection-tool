class EncryptPlugin:
    def __init__(self, key: str):
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        raise NotImplementedError

    def decrypt_code(self, input_var: str, output_var: str) -> str:
        raise NotImplementedError