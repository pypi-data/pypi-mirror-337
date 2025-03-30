# Python自定义工具包发布流程

## 1. 准备工作

### 1.1 项目结构
一个标准的Python包结构如下：

### 1.2 必要文件说明

- **LICENSE**: 开源许可证文件
- **README.md**: 项目说明文档
- **setup.py**: 包含包的元数据和依赖信息
- **pyproject.toml**: 现代Python项目配置文件
- **my_package/\_\_init\_\_.py**: 包的初始化文件，定义`__version__`等信息

## 2. 配置文件编写

### 2.1 setup.py 示例
```python
from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18.0",
        "pandas>=1.0.0",
        "playwright>=1.16.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)