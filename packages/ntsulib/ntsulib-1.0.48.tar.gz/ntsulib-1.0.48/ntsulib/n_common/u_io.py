import sys
import os


def getProjectPath(layer: int = 0, auto: bool = False) -> str:
    """
    获取调用此库的主工程路径，支持两种模式：
    1. 精确层级控制（auto=False）
    2. 自动查找项目根目录（auto=True）
    参数:
        layer: 向上查找的目录层数 (0=当前文件所在目录)
               当auto=True或打包为exe时，此参数将被忽略
        auto: 是否自动查找项目根目录（检测项目标记文件）
    返回:
        str: 指定层级的项目路径
    异常:
        ValueError: 如果layer是负数
        RuntimeError: 如果无法确定路径
    """
    if layer < 0:
        raise ValueError("layer参数不能为负数")
    # 处理打包成exe的情况（忽略所有参数）
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # 获取主模块路径
    main_module = sys.modules.get('__main__')
    if main_module is None or not hasattr(main_module, '__file__'):
        raise RuntimeError("无法确定主模块路径")
    # 获取主模块文件绝对路径
    main_file = os.path.abspath(main_module.__file__)
    current_path = os.path.dirname(main_file)
    # 非auto模式：按layer参数返回
    if not auto:
        if layer == 0:
            return current_path

        for _ in range(layer):
            parent = os.path.dirname(current_path)
            if parent == current_path:  # 已经到达根目录
                break
            current_path = parent
        return current_path

    # auto模式：自动查找项目根目录
    def is_project_dir(path: str) -> bool:
        """检查给定路径是否是项目根目录"""
        markers = [
            'pyproject.toml',
            'setup.py',
            'setup.cfg',
            'README.md',
            '.gitignore',
            'MANIFEST.in'
            '.git',
            '.hg',
            'LICENSE',
            'requirements.txt',
            'Pipfile',
            'poetry.lock',
            '.projectroot'  # 可以自定义的空标记文件
        ]
        return any(os.path.exists(os.path.join(path, marker)) for marker in markers)

    # 从当前路径向上查找项目根目录
    original_path = current_path
    while True:
        if is_project_dir(current_path):
            return current_path
        parent = os.path.dirname(current_path)
        if parent == current_path:  # 到达根目录
            break
        current_path = parent
    # 如果找不到项目标记，返回原始路径（相当于layer=0）
    return original_path

def is_executable() -> bool:
    return not sys.executable.endswith('python.exe')

def is_dir_exists(path: str) -> bool:
    return os.path.isdir(path)

def is_file_exists(path: str) -> bool:
    return os.path.isfile(path)
