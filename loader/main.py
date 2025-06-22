# main.py
from generate_loader import generate_loader
from encrypt_loader import encrypt_loader
from package.pack_py2exe import pack_py2exe
from package.pack_cxfreeze import pack_cxfreeze
from package.pack_to_exe_1 import pack_to_exe_1
from package.pack_to_exe import pack_to_exe
from package.pack_nuitka import pack_nuitka


def main():
    print("=== 生成 loader.py ===")
    generate_loader()

    print("\n=== 对 loader.py 进行加密生成 loader_enc.py ===")
    encrypt_loader()

    print("\n=== 选择打包方式 ===")
    print("1. py2exe")
    print("2. cx_Freeze")
    print("3. PyInstaller")
    print("4. Nuitka")
    choice = input("请输入序号 (1/2/3/4), 或其他退出: ").strip()

    if choice == "1":
        pack_py2exe("loader_enc.py")
    elif choice == "2":
        pack_cxfreeze("loader_enc.py")
    elif choice == "3":
        # success = pack_to_exe_1("loader_enc.py", "loader_enc", onefile=True, noconsole=False)
        success = pack_to_exe("loader_enc.py", "loader_enc", onefile=True, noconsole=False)
        if not success:
            print("[!] PyInstaller 打包失败，请检查错误信息。")
    elif choice == "4":
        pack_nuitka("loader_enc.py", "loader_enc")
    else:
        print("退出程序，不打包。")

    print("\n[+] 全部流程完成！")

if __name__ == "__main__":
    main()
