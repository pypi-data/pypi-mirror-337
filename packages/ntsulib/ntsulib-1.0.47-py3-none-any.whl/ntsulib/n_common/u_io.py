import sys
import os

def getProjectPath() -> str:
    """
    获取调用此库的主工程路径（即最顶层调用者的路径）

    返回:
        str: 主工程路径

    异常:
        RuntimeError: 如果无法确定主工程路径
    """
    # 处理打包成exe的情况
    if getattr(sys, 'frozen', False):
        # PyInstaller打包后，返回exe所在目录作为工程路径
        return os.path.dirname(sys.executable)

    # 普通Python运行情况
    # 获取调用栈中最顶层的主模块路径
    main_module = sys.modules.get('__main__')

    if main_module is not None and hasattr(main_module, '__file__'):
        main_file = main_module.__file__

        # 如果是直接运行的脚本（不是模块）
        if not main_file.endswith('__main__.py'):
            return os.path.dirname(os.path.abspath(main_file))

        # 如果是作为模块运行（python -m package.module）
        # 则向上查找直到找到非__main__.py的目录
        path = os.path.dirname(os.path.abspath(main_file))
        while os.path.basename(path) != '':
            if not os.path.exists(os.path.join(path, '__main__.py')):
                return path
            path = os.path.dirname(path)

    # 如果以上方法都失败，尝试使用sys.path[0]
    if len(sys.path) > 0:
        return os.path.abspath(sys.path[0])

    raise RuntimeError("无法确定主工程路径")

def is_executable() -> bool:
    return not sys.executable.endswith('python.exe')

def is_dir_exists(path: str) -> bool:
    return os.path.isdir(path)

def is_file_exists(path: str) -> bool:
    return os.path.isfile(path)
