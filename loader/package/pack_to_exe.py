# package/pack_to_exe.py
import subprocess
import sys
import os

def pack_to_exe(py_file: str, exe_name: str, onefile: bool = True, noconsole: bool = False) -> bool:
    cmd = [sys.executable, "-m", "PyInstaller"]

    if onefile:
        cmd.append("--onefile")
    if noconsole:
        cmd.append("--noconsole")

    # 通用依赖
    hidden_imports = [
        "Cryptodome.Util.Padding",
        "templates.exec_template"
    ]

    # 动态根据 encrypt_loader 中记录的插件决定
    plugin_module_map = {
        "AESPlugin": ["Cryptodome.Cipher.AES"],
        "XORPlugin": [],
        "Base64Plugin": [],
        "CustomBase64Plugin": [],
        "DESPlugin": ["Cryptodome.Cipher.DES"],
        "RSAPlugin": ["Cryptodome.PublicKey.RSA", "Cryptodome.Cipher.PKCS1_OAEP", "Cryptodome.Random"]
    }

    # 加载 used_plugins.txt
    if os.path.exists("used_plugins.txt"):
        with open("used_plugins.txt", "r") as f:
            used = list(set(line.strip() for line in f if line.strip()))
        for plugin in used:
            hidden_imports.extend(plugin_module_map.get(plugin, []))
            hidden_imports.append(f"encrypt_plugins.{plugin.lower()}")
        os.remove("used_plugins.txt")
    else:
        print("[!] 未找到 used_plugins.txt，将无法推导所需模块")

    for module in hidden_imports:
        cmd.append(f"--hidden-import={module}")

    cmd.extend(["--name", exe_name, py_file])

    print(f"[*] 运行命令：{' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] PyInstaller 打包成功，生成的 exe 在 dist/{exe_name}.exe")
        return True
    else:
        print("[!] PyInstaller 打包失败:")
        print(result.stdout)
        print(result.stderr)
        return False
