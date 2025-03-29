import os
import re
import shutil
import site
import subprocess
import sysconfig

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
                raise ValueError("无法找到版本号！请确保 __init__.py.py 中有 __version__='x.y.z'")

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


def get_site_packages_path():
    """获取当前 Python 环境的 site-packages 路径"""
    try:
        # 优先使用 sysconfig（更可靠）
        paths = sysconfig.get_paths()
        if "purelib" in paths:
            return paths["purelib"]

        # 回退到 site 模块
        return site.getsitepackages()[0]
    except Exception as e:
        print(f"⚠️ 无法获取 site-packages 路径: {e}")
        return None


class PostInstallCommand(install):
    def run(self):
        install.run(self)  # 标准安装
        # 1. 处理 Hook 文件（原有逻辑）
        hook_src = "pyinstaller_hooks/hook-ntsulib.py"
        hook_dest = os.path.join(get_pyinstaller_hook_dir(), "hook-ntsulib.py")
        if not os.path.exists(hook_dest):
            try:
                shutil.copy(hook_src, hook_dest)
                print(f"✅ Hook 文件已复制到: {hook_dest}")
            except Exception as e:
                print(f"❌ 无法复制 Hook 文件: {e}")
        # 2. 检查是否是用户安装（StubsFlag 不存在）
        if not os.path.exists("StubsFlag"):
            print("🔄 检测到用户安装，开始复制存根文件...")
            stubs_src = os.path.abspath("stubs/ntsulib")
            site_packages_path = get_site_packages_path()

            if not site_packages_path:
                print("❌ 无法确定 site-packages 路径，跳过存根文件复制")
                return
            stubs_dest = os.path.join(site_packages_path, "ntsulib")
            if not os.path.exists(stubs_src):
                print(f"⚠️ 未找到存根文件目录: {stubs_src}")
                return
            # 递归复制所有 .pyi 文件
            for root, dirs, files in os.walk(stubs_src):
                for file in files:
                    if file.endswith(".pyi"):
                        src_path = os.path.join(root, file)
                        rel_path = os.path.relpath(src_path, stubs_src)
                        dest_path = os.path.join(stubs_dest, rel_path)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.copy2(src_path, dest_path)
                        print(f"✅ 已复制存根文件到: {dest_path}")
            print("🎉 存根文件复制完成")
        else:
            print("🛠️ 开发者模式：跳过存根文件复制（检测到 StubsFlag）")


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
    "packages": find_packages(exclude=["测试", "命令","注意","StubsFlag"]),
    "package_data": {
        "ntsulib": ["c_libs/*.dll"],  # 确保路径正确
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
