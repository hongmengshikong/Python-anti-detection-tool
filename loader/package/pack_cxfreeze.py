import subprocess
import sys
import os


def pack_cxfreeze(script_file):
    setup_script = "setup_cxfreeze.py"
    setup_code = f"""
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    pass

setup(
    name="loader_enc",
    version="1.0",
    description="Encrypted loader executable",
    options={{"build_exe": {{
        "packages": ["Cryptodome", "encrypt_plugins", "templates"],
        "includes": ["encrypt_plugins.aes_plugin", "encrypt_plugins.xor_plugin", "encrypt_plugins.base64_plugin", "encrypt_plugins.custom_base64_plugin", "templates.exec_template"]
    }}}},
    executables=[Executable("{script_file}", base=base)]
)
"""
    with open(setup_script, "w", encoding="utf-8") as f:
        f.write(setup_code)

    print("[*] 使用 cx_Freeze 打包...")
    result = subprocess.run([sys.executable, setup_script, "build"], capture_output=True, text=True)
    if result.returncode == 0:
        print("[+] cx_Freeze 打包成功，生成的 exe 在 build 目录下")
    else:
        print("[!] cx_Freeze 打包失败:")
        print(result.stdout)
        print(result.stderr)

    if os.path.exists(setup_script):
        os.remove(setup_script)
