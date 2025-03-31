from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 尝试读取 requirements.txt，如果不存在则使用默认依赖
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    requirements = [
        "pywin32>=309",
        "pillow>=11.1.0",
        "psutil>=7.0.0",
        "pyperclip>=1.9.0"
    ]

setup(
    name="weixin-auto",
    version="3.9.11.17",
    author="cluic",
    author_email="",  # 建议添加作者邮箱
    description="Windows版本微信客户端自动化，可实现简单的发送、接收微信消息、保存聊天图片",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cluic/wxauto",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    license="MIT",  # 使用 license 参数替代 classifier
    python_requires=">=3.6",
    install_requires=requirements,
) 