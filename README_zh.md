# Model Uploader

[![PyPI version](https://badge.fury.io/py/modeluploadhelper.svg)](https://pypi.org/project/modeluploadhelper/)
[![Python Versions](https://img.shields.io/pypi/pyversions/modeluploadhelper.svg)](https://pypi.org/project/modeluploadhelper/)
[![License](https://img.shields.io/pypi/l/modeluploadhelper.svg)](https://github.com/Maicarons/modeluploader/blob/main/LICENSE)
[![Downloads](https://pepy.tech/badge/modeluploadhelper)](https://pepy.tech/project/modeluploadhelper)

一个支持 HuggingFace 和 ModelScope 双平台上传的 Python 工具。

## 功能特性

- 🚀 支持同时上传到 HuggingFace Hub 和 ModelScope
- 📦 自动读取 `.gitignore` 文件，智能忽略不需要的文件
- 🔧 灵活的命令行配置，支持选择性上传平台
- 📝 详细的日志输出，实时显示上传进度和状态
- 🌍 自动语言检测（英文/中文）
- 🎯 模块化设计，易于集成到其他项目

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install modeluploadhelper
```

### 从源码安装

```bash
git clone https://github.com/Maicarons/modeluploader.git
cd modeluploader
pip install .
```

### 开发模式安装

```bash
git clone https://github.com/Maicarons/modeluploader.git
cd modeluploader
pip install -e ".[dev]"
```

## 快速开始

### 1. 前置准备

在使用之前，请确保：

- 已安装 `huggingface_hub` 和 `modelscope` 库
- 已登录 HuggingFace: `huggingface-cli login`
- 已登录 ModelScope: `modelscope login` 或准备好 access token

### 2. 配置仓库 ID（三种方式）

#### 方式一：命令行参数（推荐）

```bash
modeluploader --hf-repo your_username/hf_repo --ms-repo your_username/ms_repo
```

#### 方式二：环境变量

```bash
# Windows
set MODELUPLOADER_HF_REPO=your_username/hf_repo
set MODELUPLOADER_MS_REPO=your_username/ms_repo
set MODELUPLOADER_REPO_TYPE=model
set MODELUPLOADER_COMMIT_MESSAGE="Upload model files"

# Linux/macOS
export MODELUPLOADER_HF_REPO=your_username/hf_repo
export MODELUPLOADER_MS_REPO=your_username/ms_repo
export MODELUPLOADER_REPO_TYPE=model
export MODELUPLOADER_COMMIT_MESSAGE="Upload model files"

modeluploader
```

#### 方式三：Python API

```python
from modeluploader import upload_to_huggingface, upload_to_modelscope

# 直接传入 repo_id
upload_to_huggingface("./model", repo_id="your_username/hf_repo")
upload_to_modelscope("./model", repo_id="your_username/ms_repo")
```

### 3. 基本用法

```bash
# 上传到两个平台（默认）
modeluploader --hf-repo user/repo1 --ms-repo user/repo2

# 上传数据集并自定义提交信息
modeluploader \
  --hf-repo user/dataset_repo \
  --ms-repo user/dataset_repo \
  --repo-type dataset \
  --commit-message "Upload training dataset v1.0"

# 仅上传到 HuggingFace
modeluploader --platform hf --hf-repo user/repo1

# 仅上传到 ModelScope
modeluploader --platform ms --ms-repo user/repo2

# 指定上传目录
modeluploader --hf-repo user/repo1 --path /path/to/your/model

# 使用 ModelScope token
modeluploader --ms-repo user/repo2 --ms-token YOUR_TOKEN
```

### 4. 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--platform` | 选择上传平台: `hf`, `ms`, `both` | `both` |
| `--path` | 要上传的文件夹路径 | `.` (当前目录) |
| `--hf-repo` | HuggingFace 仓库 ID (格式: username/repo_name) | 无（必需） |
| `--ms-repo` | ModelScope 仓库 ID (格式: username/repo_name) | 无（必需） |
| `--repo-type` | 仓库类型: `model`, `dataset`, 或 `space` | `model` |
| `--commit-message` | 上传提交信息 | `Upload model files` |
| `--gitignore` | `.gitignore` 文件路径 | `.gitignore` |
| `--ms-token` | ModelScope 访问令牌（可选） | `None` |

### 5. 作为 Python 模块使用

```python
from modeluploader import (
    upload_to_huggingface,
    upload_to_modelscope,
    load_gitignore_patterns
)

# 加载忽略模式
ignore_patterns = load_gitignore_patterns(".gitignore")

# 上传到 HuggingFace
success_hf = upload_to_huggingface(
    folder_path="./my_model",
    repo_id="your_username/hf_repo",
    ignore_patterns=ignore_patterns
)

# 上传到 ModelScope
success_ms = upload_to_modelscope(
    folder_path="./my_model",
    repo_id="your_username/ms_repo",
    token="your_token",  # 可选
    ignore_patterns=ignore_patterns
)

if success_hf and success_ms:
    print("所有上传成功！")
```

## 配置说明

### 环境变量

可以通过环境变量设置默认配置：

- `MODELUPLOADER_HF_REPO`: HuggingFace 仓库 ID
- `MODELUPLOADER_MS_REPO`: ModelScope 仓库 ID
- `MODELUPLOADER_REPO_TYPE`: 仓库类型（`model`, `dataset`, 或 `space`）
- `MODELUPLOADER_COMMIT_MESSAGE`: 上传提交信息

命令行参数会覆盖环境变量。

### 配置优先级

配置优先级从高到低：
1. 命令行参数 (`--hf-repo`, `--ms-repo`, `--repo-type`, `--commit-message`)
2. 环境变量 (`MODELUPLOADER_*`)
3. 代码 API 调用时直接传入的参数

### .gitignore 支持

工具会自动读取 `.gitignore` 文件中的规则，忽略以下类型的文件：

- Python 缓存文件 (`__pycache__/`, `*.pyc`)
- 虚拟环境 (`venv/`, `.env`)
- IDE 配置文件 (`.idea/`, `.vscode/`)
- 构建产物 (`build/`, `dist/`)
- 其他你在 `.gitignore` 中定义的模式

### 语言检测

工具会自动检测系统语言并显示相应语言的消息：
- **英文**（默认）
- **中文**（如果系统语言为中文）

也可以手动设置语言：

```python
from modeluploader import set_language

# 强制使用英文
set_language('en')

# 强制使用中文
set_language('zh')
```

## 项目结构

```
modeluploader/
├── modeluploader/
│   ├── __init__.py              # 包初始化
│   ├── __main__.py              # 支持 python -m 调用
│   ├── cli.py                   # 命令行接口
│   ├── config.py                # 配置模块
│   ├── i18n.py                  # 国际化模块
│   ├── gitignore_parser.py      # .gitignore 解析器
│   ├── huggingface_uploader.py  # HuggingFace 上传模块
│   └── modelscope_uploader.py   # ModelScope 上传模块
├── tests/
│   └── test_modeluploader.py    # 单元测试
├── main.py                      # 向后兼容入口
├── pyproject.toml               # 项目配置
├── README.md                    # 英文文档
├── README_zh.md                 # 中文文档
└── LICENSE                      # Apache 2.0 许可证
```

## 开发指南

### 运行测试

```bash
pytest tests/
```

### 代码格式化

```bash
black modeluploader/
flake8 modeluploader/
```

### 构建分发包

```bash
pip install build
python -m build
```

这将在 `dist/` 目录中生成 `.tar.gz` 和 `.whl` 文件。

### 发布到 PyPI

```bash
# 安装 twine
pip install twine

# 上传到 TestPyPI（测试）
twine upload --repository testpypi dist/*

# 上传到 PyPI（正式）
twine upload dist/*
```

## 常见问题

### Q: 如何只上传到一个平台？

A: 使用 `--platform` 参数：
```bash
modeluploader --platform hf --hf-repo user/repo  # 仅 HuggingFace
modeluploader --platform ms --ms-repo user/repo  # 仅 ModelScope
```

### Q: 上传失败怎么办？

A: 检查以下几点：
1. 是否已正确登录对应的平台
2. 网络连接是否正常
3. 仓库 ID 是否正确
4. 查看详细错误日志进行排查

### Q: 如何自定义忽略的文件？

A: 在项目根目录创建或编辑 `.gitignore` 文件，添加需要忽略的文件或目录模式。

### Q: 可以在代码中动态配置仓库吗？

A: 可以，通过以下方式：

```python
# 方式 1: 直接传入参数
from modeluploader import upload_to_huggingface

upload_to_huggingface(
    "./model",
    repo_id="user/repo",
    repo_type="dataset",
    commit_message="Custom message"
)

# 方式 2: 设置环境变量
import os
os.environ['MODELUPLOADER_HF_REPO'] = 'user/repo'
os.environ['MODELUPLOADER_REPO_TYPE'] = 'dataset'
os.environ['MODELUPLOADER_COMMIT_MESSAGE'] = 'Custom message'

from modeluploader import upload_to_huggingface
upload_to_huggingface("./model")
```

### Q: 优先级是怎样的？

A: 配置优先级从高到低：
1. 命令行参数 (`--hf-repo`, `--ms-repo`, `--repo-type`, `--commit-message`)
2. 环境变量 (`MODELUPLOADER_HF_REPO`, `MODELUPLOADER_MS_REPO`, `MODELUPLOADER_REPO_TYPE`, `MODELUPLOADER_COMMIT_MESSAGE`)
3. 代码中直接传入的参数 (`repo_id`, `repo_type`, `commit_message`)

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 Apache 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 致谢

- [HuggingFace Hub](https://huggingface.co/)
- [ModelScope](https://modelscope.cn/)
- 所有贡献者

## 联系方式

- 项目主页: https://github.com/Maicarons/modeluploader
- 问题反馈: https://github.com/Maicarons/modeluploader/issues
