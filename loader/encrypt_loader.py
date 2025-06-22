from encrypt_plugins.aes_plugin import AESPlugin
from encrypt_plugins.xor_plugin import XORPlugin
from encrypt_plugins.base64_plugin import Base64Plugin
from encrypt_plugins.custom_base64_plugin import CustomBase64Plugin
from encrypt_plugins.des_plugin import DESPlugin
from encrypt_plugins.rsa_plugin import RSAPlugin
import importlib.util

def encrypt_loader():

    # --- 第一步：生成普通 loader.py（参考已有流程） ---
    # 这里可以把生成 loader.py 的代码放这里，或者之前已经生成好了 loader.py

    # --- 第二步：读取 loader.py 文件内容 ---
    with open("loader.py", "r", encoding="utf-8") as f:
        loader_code = f.read().encode("utf-8")  # 以 bytes 形式读取方便加密

    # --- 第三步：选择加密插件对 loader_code 做多层加密 ---
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

    # --- 第四步：多层加密 loader_code ---
    data = loader_code
    for plugin in plugins:
        data = plugin.encrypt(data)

    # --- 第五步：生成解密代码变量链 ---
    var_chain = ["ciphertext"] + [f"layer_{i}" for i in range(len(plugins) - 1)] + ["loader_code"]
    decrypt_code = ""
    for i, plugin in enumerate(reversed(plugins)):
        decrypt_code += plugin.decrypt_code(var_chain[i], var_chain[i + 1]) + "\n"

    # 如果没加密，直接转换
    if not plugins:
        decrypt_code += "loader_code = ciphertext.decode('utf-8')\n"

    # --- 第六步：生成最终解密+exec代码 ---
    final_exec_code = (
        'print("[*] 解密并执行 loader.py 代码...")\n'
        'exec(loader_code)\n'
    )

    # --- 第七步：写入加密版 loader_enc.py ---
    with open("loader_enc.py", "w", encoding="utf-8") as f:
        f.write(f"ciphertext = {repr(data)}\n\n")
        f.write(decrypt_code)
        f.write(final_exec_code)

    print("[+] loader_enc.py 已生成，运行它即可自动解密并执行原始 loader.py")
    # 最后记录下来
    with open("used_plugins.txt", "a", encoding="utf-8") as f:
        f.write("\n".join(used_plugins) + "\n")

if __name__ == '__main__':
    encrypt_loader()

    # key = "nR6X70Ws"
    # key = "msyt_kry_ecee"