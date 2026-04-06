"""
Model Uploader - A tool for uploading models to HuggingFace and ModelScope
"""

__version__ = "0.1.0"
__author__ = "Maicarons"
__description__ = "A tool for uploading models to HuggingFace and ModelScope"

from .config import HF_REPO_ID, MS_REPO_ID, REPO_TYPE, COMMIT_MESSAGE
from .gitignore_parser import load_gitignore_patterns
from .huggingface_uploader import upload_to_huggingface
from .i18n import get_text, set_language, detect_language, CURRENT_LANGUAGE
from .modelscope_uploader import upload_to_modelscope

__all__ = [
    "HF_REPO_ID",
    "MS_REPO_ID",
    "REPO_TYPE",
    "COMMIT_MESSAGE",
    "load_gitignore_patterns",
    "upload_to_huggingface",
    "upload_to_modelscope",
    "get_text",
    "set_language",
    "detect_language",
    "CURRENT_LANGUAGE",
]
