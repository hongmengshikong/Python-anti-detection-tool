import subprocess
import sys
import os


def pack_to_exe_1(py_file: str, exe_name: str, onefile: bool = True, noconsole: bool = False) -> bool:
    cmd = [sys.executable, "-m", "PyInstaller"]

    if onefile:
        cmd.append("--onefile")
    if noconsole:
        cmd.append("--noconsole")

    # 显式指定必须导入的模块
    hidden_imports = [
        "Cryptodome.Cipher.AES",
        "Cryptodome.Cipher.DES",
        "Cryptodome.Cipher._mode_ecb",
        "Cryptodome.PublicKey.RSA",
        "Cryptodome.Random",
        "Cryptodome.Random.random",
        "Cryptodome.Util.Padding",
    ]

    plugin_imports = [
        "encrypt_plugins.aes_plugin",
        "encrypt_plugins.xor_plugin",
        "encrypt_plugins.base64_plugin",
        "encrypt_plugins.custom_base64_plugin",
        "encrypt_plugins.des_plugin",        # 如果你使用了 DES
        "encrypt_plugins.rsa_plugin",        # 如果你使用了 RSA
        "templates.exec_template"
    ]

    for module in hidden_imports + plugin_imports:
        cmd.append(f"--hidden-import={module}")

    # 也可以添加 hooks 路径
    if os.path.exists("hook-Cryptodome.PublicKey.RSA.py"):
        cmd.append("--additional-hooks-dir=.")

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
