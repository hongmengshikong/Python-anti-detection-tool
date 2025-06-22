import subprocess
import sys
import os

def pack_nuitka(py_file: str, exe_name: str) -> bool:
    """
    使用 Nuitka + MSVC 打包 Python 脚本为独立的可执行文件。
    根据 used_plugins.txt 自动推导依赖。
    """
    cmd = [
        sys.executable, "-m", "nuitka",
        "--msvc=latest",
        "--standalone",
        "--onefile",
        f"--output-filename={exe_name}"
    ]

    # 通用包
    included_packages = ["Cryptodome", "encrypt_plugins", "templates"]

    # 插件映射
    plugin_module_map = {
        "AESPlugin": ["Cryptodome.Cipher.AES"],
        "XORPlugin": [],
        "Base64Plugin": [],
        "CustomBase64Plugin": [],
        "DESPlugin": ["Cryptodome.Cipher.DES"],
        "RSAPlugin": ["Cryptodome.PublicKey.RSA", "Cryptodome.Cipher.PKCS1_OAEP", "Cryptodome.Random"]
    }

    if os.path.exists("used_plugins.txt"):
        with open("used_plugins.txt", "r") as f:
            used = sorted(set(line.strip() for line in f if line.strip()))
        for plugin in used:
            included_packages.extend(plugin_module_map.get(plugin, []))

        #打包完成删除文件
        # os.remove("used_plugins.txt")
    else:
        print("[!] 未找到 used_plugins.txt，将使用默认包")

    for pkg in included_packages:
        cmd.append(f"--include-package={pkg}")

    cmd.append(py_file)

    print(f"[*] 正在执行 Nuitka 打包命令：\n{' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Nuitka 打包成功，生成的可执行文件为：{exe_name}")
        return True
    else:
        print("[!] Nuitka 打包失败：")
        print(result.stdout)
        print(result.stderr)
        return False
