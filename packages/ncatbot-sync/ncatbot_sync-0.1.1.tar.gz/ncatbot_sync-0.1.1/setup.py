from setuptools import setup, find_packages

with open("ncatbot_sync/__init__.py", "r") as f:
    version_line = [line for line in f if line.startswith("__version__")][0]
    version = eval(version_line.split("=")[-1])

setup(
    name="ncatbot_sync",
    version=version,
    packages=find_packages(),
    # 其他参数从 pyproject.toml 读取
)
