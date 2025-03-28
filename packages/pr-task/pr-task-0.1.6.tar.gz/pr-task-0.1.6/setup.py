from setuptools import setup, find_packages

__version__ = "0.1.6"

setup(
    name="pr-task",  # 包名（PyPI 显示的名称，需唯一）
    version=__version__,  # 版本号
    author="penr",
    author_email="1944542244@qq.com",
    description="prtask",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # 自动发现包
    install_requires=["aioredis", 'loguru'],  # 依赖列表（如 ["requests>=2.25.1"]）
    python_requires=">=3.7",  # Python 版本要求
    url="https://github.com/yourusername/my-package",  # 项目地址
    license="MIT",
)
