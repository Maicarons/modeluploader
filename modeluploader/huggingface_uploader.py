"""
HuggingFace Hub upload module
"""

import logging
from typing import List, Optional

from huggingface_hub import HfApi

from .config import HF_REPO_ID, REPO_TYPE, COMMIT_MESSAGE
from .i18n import get_text

logger = logging.getLogger(__name__)


def upload_to_huggingface(
    folder_path: str = ".",
    repo_id: str = None,
    repo_type: str = None,
    commit_message: str = None,
    ignore_patterns: Optional[List[str]] = None
) -> bool:
    """
    Upload to HuggingFace Hub
    
    Args:
        folder_path: Path to folder to upload
        repo_id: HuggingFace repository ID (format: username/repo_name). 
                 If not provided, uses HF_REPO_ID from config
        repo_type: Repository type (model, dataset, or space).
                   If not provided, uses REPO_TYPE from config
        commit_message: Commit message for the upload.
                       If not provided, uses COMMIT_MESSAGE from config
        ignore_patterns: List of file patterns to ignore
        
    Returns:
        True if upload successful, False otherwise
    """
    try:
        # Use provided values or fall back to config
        target_repo = repo_id or HF_REPO_ID
        target_repo_type = repo_type or REPO_TYPE
        target_commit_msg = commit_message or COMMIT_MESSAGE
        
        if not target_repo:
            logger.error("HuggingFace repository ID not provided. Set MODELUPLOADER_HF_REPO environment variable or pass repo_id parameter.")
            return False
        
        logger.info(get_text('hf_upload_start', repo_id=target_repo))
        hfapi = HfApi()
        
        result = hfapi.upload_folder(
            folder_path=folder_path,
            repo_id=target_repo,
            repo_type=target_repo_type,
            ignore_patterns=ignore_patterns,
            commit_message=target_commit_msg,
        )
        
        logger.info(get_text('hf_upload_success', url=result))
        return True
        
    except Exception as e:
        logger.error(get_text('hf_upload_failed', error=str(e)))
        return False
