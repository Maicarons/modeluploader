"""
ModelScope upload module
"""

import logging
from typing import List, Optional

from modelscope.hub.api import HubApi

from .config import MS_REPO_ID, COMMIT_MESSAGE
from .i18n import get_text

logger = logging.getLogger(__name__)


def upload_to_modelscope(
    folder_path: str = ".",
    repo_id: str = None,
    commit_message: str = None,
    token: Optional[str] = None,
    ignore_patterns: Optional[List[str]] = None
) -> bool:
    """
    Upload to ModelScope
    
    Args:
        folder_path: Path to folder to upload
        repo_id: ModelScope repository ID (format: username/repo_name).
                 If not provided, uses MS_REPO_ID from config
        commit_message: Commit message for the upload.
                       If not provided, uses COMMIT_MESSAGE from config
        token: ModelScope access token (optional)
        ignore_patterns: List of file patterns to ignore
        
    Returns:
        True if upload successful, False otherwise
    """
    try:
        # Use provided values or fall back to config
        target_repo = repo_id or MS_REPO_ID
        target_commit_msg = commit_message or COMMIT_MESSAGE
        
        if not target_repo:
            logger.error("ModelScope repository ID not provided. Set MODELUPLOADER_MS_REPO environment variable or pass repo_id parameter.")
            return False
        
        logger.info(get_text('ms_upload_start', repo_id=target_repo))
        hubapi = HubApi()
        
        # Login if token provided
        if token:
            logger.info(get_text('using_token'))
            hubapi.login(access_token=token)
        else:
            logger.info(get_text('using_saved'))
        
        # Show ignore patterns
        if ignore_patterns:
            logger.info(get_text('ignore_patterns', patterns=ignore_patterns))
        
        hubapi.upload_folder(
            repo_id=target_repo,
            folder_path=folder_path,
            commit_message=target_commit_msg,
            ignore_patterns=ignore_patterns,
        )
        
        logger.info(get_text('ms_upload_success'))
        return True
        
    except Exception as e:
        logger.error(get_text('ms_upload_failed', error=str(e)))
        return False
