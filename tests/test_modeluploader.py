"""
测试模型上传器模块
"""

import pytest
from pathlib import Path
from modeluploader import (
    HF_REPO_ID,
    MS_REPO_ID,
    REPO_TYPE,
    COMMIT_MESSAGE,
    load_gitignore_patterns,
)


def test_config_constants():
    """测试配置常量是否正确定义"""
    assert HF_REPO_ID == "Maicarons/UmaVoice_DDSP_6.3"
    assert MS_REPO_ID == "Mai2026/UmaVoice_DDSP_6.3"
    assert REPO_TYPE == "model"
    assert COMMIT_MESSAGE == "Upload model files"


def test_load_gitignore_patterns_default():
    """测试加载不存在的 .gitignore 文件时返回默认模式"""
    patterns = load_gitignore_patterns("nonexistent.gitignore")
    assert isinstance(patterns, list)
    assert "__pycache__" in patterns
    assert "*.pyc" in patterns


def test_load_gitignore_patterns_from_file(tmp_path):
    """测试从实际文件加载忽略模式"""
    # 创建临时 .gitignore 文件
    gitignore_file = tmp_path / ".gitignore"
    gitignore_file.write_text("# Comment\n*.pyc\n__pycache__/\nvenv/\n")
    
    patterns = load_gitignore_patterns(str(gitignore_file))
    assert isinstance(patterns, list)
    assert "*.pyc" in patterns
    assert "__pycache__/" in patterns
    assert "venv/" in patterns
    # 注释应该被忽略
    assert "# Comment" not in patterns


def test_cli_run_with_invalid_path():
    """测试使用无效路径时的行为"""
    from modeluploader.cli import run
    
    exit_code = run(["--path", "/nonexistent/path"])
    assert exit_code == 1


def test_cli_parse_args():
    """测试命令行参数解析"""
    from modeluploader.cli import parse_args
    
    args = parse_args(["--platform", "hf", "--path", "./test"])
    assert args.platform == "hf"
    assert args.path == "./test"
    assert args.gitignore == ".gitignore"
    assert args.ms_token is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
