import subprocess
import sys
import os

def pack_py2exe(py_file: str):
    setup_py = "setup_py2exe.py"
    # 生成简单的 setup 脚本
    with open(setup_py, "w", encoding="utf-8") as f:
        f.write(f"""
from distutils.core import setup
import py2exe
import sys
sys.argv.append('py2exe')

setup(
    options={{"py2exe": {{"bundle_files": 1, "compressed": True, "optimize": 2}}}},
    windows=[{{"script": "{py_file}"}}],
    zipfile=None,
)
""")

    print("[*] 使用 py2exe 打包...")
    result = subprocess.run([sys.executable, setup_py], capture_output=True, text=True)
    if result.returncode == 0:
        print("[+] py2exe 打包成功，生成的 exe 在 dist/ 目录下")
    else:
        print("[!] py2exe 打包失败:")
        print(result.stdout)
        print(result.stderr)

    # 删除临时 setup 文件（如果需要）
    if os.path.exists(setup_py):
        os.remove(setup_py)