# 安装工具包
python3 -m pip install --upgrade build
pip3 install hatchling
python -m build
### 安装工具包
"""
    用于使用其中的工具如: playwright
"""
pip install -U "autogen-agentchat" "autogen-ext[openai]"

pip install -U "autogenstudio"


### 上传工具包


pip install twine
twine upload dist/*

### 上传后地址
https://pypi.org/project/moggy-mcp-server/0.1.0/

twine upload --repository-url https://test.pypi.org/legacy/ dist/*