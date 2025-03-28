import os
import re
import shutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install

def clean_dist_folder():
    """自动清理 dist 文件夹，避免旧文件干扰"""
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        print(f"🧹 清理旧 dist 文件夹: {dist_dir}")
        shutil.rmtree(dist_dir)


def update_version(version_file="ntsulib/__init__.py"):
    """自动将版本号 +0.0.1，并返回新版本号"""
    try:
        with open(version_file, "r+", encoding="utf-8") as f:
            content = f.read()
            # 使用正则匹配版本号（格式：x.y.z）
            version_match = re.search(r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']', content)
            if not version_match:
                raise ValueError("无法找到版本号！请确保 __init__.py 中有 __version__='x.y.z'")

            old_version = version_match.group(1)
            major, minor, patch = map(int, old_version.split('.'))
            new_version = f"{major}.{minor}.{patch + 1}"  # 自动 +0.0.1

            # 替换为新版本号
            new_content = re.sub(
                r'__version__\s*=\s*["\'][^"\']*["\']',
                f'__version__ = "{new_version}"',
                content
            )
            f.seek(0)
            f.write(new_content)
            f.truncate()

            print(f"🆕 版本号从 {old_version} 更新为 {new_version}")
            return new_version
    except Exception as e:
        print(f"⚠️ 版本号更新失败: {e}")
        return None


def generate_pyproject_toml(version):
    """根据 setup.py 配置自动生成 pyproject.toml"""
    pyproject_content = f"""[build-system]
requires = ["setuptools>=42"]
build-backend = "setuptools.build_meta"

[project]
name = "{setup_params['name']}"
version = "{version}"
authors = [
    {{ name = "{setup_params['author']}", email = "{setup_params['author_email']}" }}
]
description = "{setup_params['description']}"
dependencies = {setup_params['install_requires']}
"""
    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(pyproject_content)
    print("✅ 已生成 pyproject.toml")


def get_install_requires():
    """从 requirements.txt 读取依赖（如果文件存在）"""
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []


# 预执行清理
clean_dist_folder()

# 尝试自动更新版本号
current_version = update_version()
if current_version is None:
    current_version = "1.0.0"  # 默认版本（需手动修复）
    print(f"⚠️ 使用默认版本号: {current_version}")


def generate_requirements_file():
    """自动生成 requirements.txt 文件"""
    print("📦 正在生成 requirements.txt...")
    try:
        # 执行 pip freeze 命令获取当前环境所有依赖
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)

        # 过滤掉不需要的行（注释、可编辑安装等）
        dependencies = [
            line.strip() for line in result.stdout.split('\n')
            if line.strip() and not line.startswith(('#', '-e'))
        ]

        # 写入 requirements.txt
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(dependencies))

        print(f"✅ 已生成 requirements.txt，包含 {len(dependencies)} 个依赖")
        return dependencies
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 生成 requirements.txt 失败: {e.stderr}")
        return []

generate_requirements_file()

def get_pyinstaller_hook_dir():
    """动态获取 PyInstaller 的 hooks 目录路径（兼容 venv 和全局安装）"""
    import sys
    from pathlib import Path
    # 获取当前 Python 环境的 site-packages 路径
    site_packages = Path(sys.prefix) / "Lib" / "site-packages"  # Windows
    if not site_packages.exists():
        site_packages = Path(sys.prefix) / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"  # Linux/macOS
    # 检查 PyInstaller 是否存在
    pyinstaller_hooks = site_packages / "PyInstaller" / "hooks"
    if not pyinstaller_hooks.exists():
        raise FileNotFoundError("PyInstaller hooks 目录未找到，请确保已安装 PyInstaller")
    return str(pyinstaller_hooks)

def _clean_old_hooks():
    """清理旧版本的 Hook 文件"""
    try:
        import PyInstaller
        hook_path = os.path.join(os.path.dirname(PyInstaller.__file__), "hooks", "hook-ntsulib.py")
        if os.path.exists(hook_path):
            os.remove(hook_path)
    except:
        pass
# 在 setup() 前清理旧文件

_clean_old_hooks()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)  # 先执行标准安装
        # 检查 hook 文件是否已正确安装
        hook_src = "pyinstaller_hooks/hook-ntsulib.py"  # 你的 hook 文件路径
        hook_dest = os.path.join(get_pyinstaller_hook_dir(), "hook-ntsulib.py")
        if not os.path.exists(hook_dest):
            print(f"⚠️ Hook 文件未正确安装到: {hook_dest}")
            # 尝试手动复制（如果 data_files 未生效）
            try:
                shutil.copy(hook_src, hook_dest)
                print(f"✅ 手动复制 hook 文件到: {hook_dest}")
            except Exception as e:
                print(f"❌ 无法复制 hook 文件: {e}")
        else:
            print(f"✅ Hook 文件已正确安装到: {hook_dest}")


# 定义 setup() 的参数
setup_params = {
    "name": "ntsulib",
    "version": current_version,  # 使用自动更新的版本号
    "author": "NTsukine",
    "author_email": "398339897@qq.com",
    "description": "ntsulib",
    "long_description": open("README.md", encoding="utf-8").read(),
    "long_description_content_type": "text/markdown",
    "url": "",
    "packages": find_packages(exclude=["测试", "命令"]),
    "package_data": {
        "ntsulib": ["c_lib/*.dll"],  # 确保路径正确
    },
    "cmdclass": {
        'install': PostInstallCommand,  # 覆盖默认 install 命令
    },
    # 关键修改：添加 data_files 自动安装 Hook
    "data_files": [
        (get_pyinstaller_hook_dir(), ["pyinstaller_hooks/hook-ntsulib.py"]),
    ],
    "include_package_data": True,  # 确保 MANIFEST.in 生效
    "install_requires": get_install_requires(),
    "classifiers": [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    "python_requires": ">=3.8",
    "keywords": ['utility', 'library', 'python', 'tools', 'encryption', 'ntsulib'],
}

# 生成 pyproject.toml（使用更新后的版本号）
generate_pyproject_toml(current_version)

# 调用 setup()
setup(**setup_params)
