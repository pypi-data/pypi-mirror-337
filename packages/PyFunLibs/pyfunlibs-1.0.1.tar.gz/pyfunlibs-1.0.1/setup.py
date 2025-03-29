from setuptools import setup, find_packages
import os

# 获取当前脚本所在的目录
current_directory = os.path.abspath(os.path.dirname(__file__))

# 构建 README.md 的完整路径
readme_path = os.path.join(current_directory, "README.md")

# 读取 README.md 内容
with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PyFunLibs",
    version="1.0.1",
    author="Your Name",
    author_email="3358048037@qq.com",
    description="Yeah! This is a Funn Libs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Conla-AC/PyFunLibs",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
