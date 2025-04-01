from setuptools import setup, find_packages

setup(
    name="pymimi",  # 包名（上传到 PyPI 的名字）
    version="0.0.1003",
    author="ManiacsTraitor",
    author_email="2727671635@qq.com",
    description="这是一个适用于Midas Cvil NX二次开发库，旨在帮助摆脱繁琐的json编写",
    long_description=open("README.md", encoding="utf-8").read(),
    url="https://github.com/ManiacasTraitor/Midas-Civil--PyMiMi",
    packages=find_packages(where="src"),
    package_dir={"": "pymimi_v0.0.003"},
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',              # Python 版本要求
)