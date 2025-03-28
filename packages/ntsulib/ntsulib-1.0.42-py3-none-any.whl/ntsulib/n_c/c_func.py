import os
import sys
from ctypes import *
from pathlib import Path

# class c_lib:
#     def __init__(self):
#         # 获取脚本所在目录的绝对路径
#         script_dir = Path(__file__).parent.absolute()
#         # 构造DLL的完整路径
#         dll_path = os.path.join(script_dir, "c_lib", "ntsulib.dll")
#         self._dll = cdll.LoadLibrary(dll_path)
#         # mydll = cdll.LoadLibrary("mylib.so")  # Linux
#         # mydll = cdll.LoadLibrary("mylib.dylib")  # Mac
#     def start_tmdprotect(self):
#         self._dll.start_tmdprotect()
#     def end_tmdprotect(self):
#         self._dll.end_tmdprotect()
#     def testfunc1(self):
#         self._dll.testfunc1.argtypes = []  # 指定参数类型
#         self._dll.testfunc1.restype = c_void_p
#         self._dll.testfunc1()
#     def mys_sum(self, a:int, b:int) -> int:
#         self._dll.mys_sum.argtypes = [c_int, c_int]  # 指定参数类型
#         self._dll.mys_sum.restype = c_int
#         return self._dll.mys_sum(a,b)

class c_lib:
    def __init__(self):
        # 动态获取 DLL 路径（兼容普通运行和 PyInstaller 打包）
        if getattr(sys, 'frozen', False):
            # PyInstaller 打包后，从临时目录 _MEIPASS 加载
            base_path = sys._MEIPASS
        else:
            # 普通运行时，从库的安装目录加载
            base_path = os.path.dirname(os.path.abspath(__file__))

        # 构造 DLL 的完整路径
        dll_path = os.path.join(base_path, "c_lib", "ntsulib.dll")

        try:
            self._dll = cdll.LoadLibrary(dll_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load DLL from {dll_path}: {e}")

    def start_tmdprotect(self):
        self._dll.start_tmdprotect()

    def end_tmdprotect(self):
        self._dll.end_tmdprotect()

    def testfunc1(self):
        self._dll.testfunc1.argtypes = []  # 指定参数类型
        self._dll.testfunc1.restype = c_void_p
        self._dll.testfunc1()

    def mys_sum(self, a: int, b: int) -> int:
        self._dll.mys_sum.argtypes = [c_int, c_int]  # 指定参数类型
        self._dll.mys_sum.restype = c_int
        return self._dll.mys_sum(a, b)