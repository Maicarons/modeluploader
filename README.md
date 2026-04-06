# Model Uploader

[![PyPI version](https://badge.fury.io/py/modeluploadhelper.svg)](https://pypi.org/project/modeluploadhelper/)
[![Python Versions](https://img.shields.io/pypi/pyversions/modeluploadhelper.svg)](https://pypi.org/project/modeluploadhelper/)
[![License](https://img.shields.io/pypi/l/modeluploadhelper.svg)](https://github.com/Maicarons/modeluploader/blob/main/LICENSE)
[![Downloads](https://pepy.tech/badge/modeluploadhelper)](https://pepy.tech/project/modeluploadhelper)

A Python tool for uploading models to both HuggingFace Hub and ModelScope.

## Features

- 🚀 Upload to HuggingFace Hub and ModelScope simultaneously
- 📦 Automatically reads `.gitignore` to intelligently skip unwanted files
- 🔧 Flexible CLI configuration with selective platform upload
- 📝 Detailed logging with real-time progress and status updates
- 🌍 Automatic language detection (English/Chinese)
- 🎯 Modular design, easy to integrate into other projects

## Installation

### From PyPI (Recommended)

```bash
pip install modeluploadhelper
```

### From Source

```bash
git clone https://github.com/Maicarons/modeluploader.git
cd modeluploader
pip install .
```

### Development Mode

```bash
git clone https://github.com/Maicarons/modeluploader.git
cd modeluploader
pip install -e ".[dev]"
```

## Quick Start

### 1. Prerequisites

Before using, ensure:

- `huggingface_hub` and `modelscope` libraries are installed
- Logged in to HuggingFace: `huggingface-cli login`
- Logged in to ModelScope: `modelscope login` or have access token ready

### 2. Configure Repository IDs (Three Ways)

#### Method 1: Command-line Arguments (Recommended)

```bash
modeluploader --hf-repo your_username/hf_repo --ms-repo your_username/ms_repo
```

#### Method 2: Environment Variables

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

#### Method 3: Python API

```python
from modeluploader import upload_to_huggingface, upload_to_modelscope

# Pass repo_id directly
upload_to_huggingface("./model", repo_id="your_username/hf_repo")
upload_to_modelscope("./model", repo_id="your_username/ms_repo")
```

### 3. Basic Usage

```bash
# Upload to both platforms (default)
modeluploader --hf-repo user/repo1 --ms-repo user/repo2

# Upload dataset with custom commit message
modeluploader \
  --hf-repo user/dataset_repo \
  --ms-repo user/dataset_repo \
  --repo-type dataset \
  --commit-message "Upload training dataset v1.0"

# Upload to HuggingFace only
modeluploader --platform hf --hf-repo user/repo1

# Upload to ModelScope only
modeluploader --platform ms --ms-repo user/repo2

# Specify upload directory
modeluploader --hf-repo user/repo1 --path /path/to/your/model

# Use ModelScope token
modeluploader --ms-repo user/repo2 --ms-token YOUR_TOKEN
```

### 4. Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--platform` | Select platform: `hf`, `ms`, `both` | `both` |
| `--path` | Path to folder to upload | `.` (current directory) |
| `--hf-repo` | HuggingFace repository ID (format: username/repo_name) | Required |
| `--ms-repo` | ModelScope repository ID (format: username/repo_name) | Required |
| `--repo-type` | Repository type: `model`, `dataset`, or `space` | `model` |
| `--commit-message` | Commit message for the upload | `Upload model files` |
| `--gitignore` | Path to `.gitignore` file | `.gitignore` |
| `--ms-token` | ModelScope access token (optional) | `None` |

### 5. Using as Python Module

```python
from modeluploader import (
    upload_to_huggingface,
    upload_to_modelscope,
    load_gitignore_patterns
)

# Load ignore patterns
ignore_patterns = load_gitignore_patterns(".gitignore")

# Upload to HuggingFace
success_hf = upload_to_huggingface(
    folder_path="./my_model",
    ignore_patterns=ignore_patterns
)

# Upload to ModelScope
success_ms = upload_to_modelscope(
    folder_path="./my_model",
    token="your_token",  # Optional
    ignore_patterns=ignore_patterns
)

if success_hf and success_ms:
    print("All uploads successful!")
```

## Configuration

### Environment Variables

You can set default configuration via environment variables:

- `MODELUPLOADER_HF_REPO`: HuggingFace repository ID
- `MODELUPLOADER_MS_REPO`: ModelScope repository ID
- `MODELUPLOADER_REPO_TYPE`: Repository type (`model`, `dataset`, or `space`)
- `MODELUPLOADER_COMMIT_MESSAGE`: Commit message for uploads

Command-line arguments override environment variables.

### Priority Order

Configuration priority (highest to lowest):
1. Command-line arguments (`--hf-repo`, `--ms-repo`, `--repo-type`, `--commit-message`)
2. Environment variables (`MODELUPLOADER_*`)
3. Direct parameters in code API calls

### .gitignore Support

The tool automatically reads rules from `.gitignore` file and ignores:

- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `.env`)
- IDE configuration files (`.idea/`, `.vscode/`)
- Build artifacts (`build/`, `dist/`)
- Other patterns defined in your `.gitignore`

### Language Detection

The tool automatically detects your system language and displays messages in:
- **English** (default)
- **Chinese** (if system locale is Chinese)

You can also manually set the language:

```python
from modeluploader import set_language

# Force English
set_language('en')

# Force Chinese
set_language('zh')
```

## Project Structure

```
modeluploader/
├── modeluploader/
│   ├── __init__.py              # Package initialization
│   ├── __main__.py              # Support for python -m
│   ├── cli.py                   # Command-line interface
│   ├── config.py                # Configuration module
│   ├── i18n.py                  # Internationalization module
│   ├── gitignore_parser.py      # .gitignore parser
│   ├── huggingface_uploader.py  # HuggingFace upload module
│   └── modelscope_uploader.py   # ModelScope upload module
├── tests/
│   └── test_modeluploader.py    # Unit tests
├── main.py                      # Backward compatibility entry
├── pyproject.toml               # Project configuration
├── README.md                    # English documentation
├── README_zh.md                 # Chinese documentation
└── LICENSE                      # Apache 2.0 License
```

## Development Guide

### Run Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black modeluploader/
flake8 modeluploader/
```

### Build Distribution Package

```bash
pip install build
python -m build
```

This generates `.tar.gz` and `.whl` files in the `dist/` directory.

### Publish to PyPI

```bash
# Install twine
pip install twine

# Upload to TestPyPI (testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## FAQ

### Q: How to upload to only one platform?

A: Use the `--platform` argument:
```bash
modeluploader --platform hf  # HuggingFace only
modeluploader --platform ms  # ModelScope only
```

### Q: What if upload fails?

A: Check the following:
1. Are you properly logged in to the platform?
2. Is your network connection stable?
3. Is the repository ID correct?
4. Review the detailed error logs for troubleshooting

### Q: How to customize ignored files?

A: Create or edit the `.gitignore` file in your project root and add patterns for files or directories to ignore.

### Q: Can I configure repositories dynamically in code?

A: Yes, through these methods:

```python
# Method 1: Pass parameters directly
from modeluploader import upload_to_huggingface

upload_to_huggingface(
    "./model",
    repo_id="user/repo",
    repo_type="dataset",
    commit_message="Custom message"
)

# Method 2: Set environment variables
import os
os.environ['MODELUPLOADER_HF_REPO'] = 'user/repo'
os.environ['MODELUPLOADER_REPO_TYPE'] = 'dataset'
os.environ['MODELUPLOADER_COMMIT_MESSAGE'] = 'Custom message'

from modeluploader import upload_to_huggingface
upload_to_huggingface("./model")
```

## Contributing

Issues and Pull Requests are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [HuggingFace Hub](https://huggingface.co/)
- [ModelScope](https://modelscope.cn/)
- All contributors

## Contact

- Project Homepage: https://github.com/Maicarons/modeluploader
- Issue Tracker: https://github.com/Maicarons/modeluploader/issues
