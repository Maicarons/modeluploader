"""
Configuration module for model uploader
Supports environment variables and runtime configuration
"""

import os

# HuggingFace Configuration
# Can be set via environment variable: MODELUPLOADER_HF_REPO
HF_REPO_ID = os.environ.get('MODELUPLOADER_HF_REPO', '')

# ModelScope Configuration
# Can be set via environment variable: MODELUPLOADER_MS_REPO
MS_REPO_ID = os.environ.get('MODELUPLOADER_MS_REPO', '')

# Repository type (model, dataset, or space)
# Can be set via environment variable: MODELUPLOADER_REPO_TYPE
REPO_TYPE = os.environ.get('MODELUPLOADER_REPO_TYPE', 'model')

# Default commit message
# Can be set via environment variable: MODELUPLOADER_COMMIT_MESSAGE
COMMIT_MESSAGE = os.environ.get('MODELUPLOADER_COMMIT_MESSAGE', 'Upload model files')
