"""
Command-line interface module
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List

from .config import HF_REPO_ID, MS_REPO_ID
from .gitignore_parser import load_gitignore_patterns
from .huggingface_uploader import upload_to_huggingface
from .i18n import get_text
from .modelscope_uploader import upload_to_modelscope

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def parse_args(args=None):
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description=get_text('description')
    )
    parser.add_argument(
        "--platform",
        type=str,
        choices=["hf", "ms", "both"],
        default="both",
        help=get_text('platform_help')
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help=get_text('path_help')
    )
    parser.add_argument(
        "--hf-repo",
        type=str,
        default=None,
        help="HuggingFace repository ID (format: username/repo_name). Overrides MODELUPLOADER_HF_REPO env var"
    )
    parser.add_argument(
        "--ms-repo",
        type=str,
        default=None,
        help="ModelScope repository ID (format: username/repo_name). Overrides MODELUPLOADER_MS_REPO env var"
    )
    parser.add_argument(
        "--repo-type",
        type=str,
        default=None,
        help="Repository type: model, dataset, or space. Overrides MODELUPLOADER_REPO_TYPE env var (default: model)"
    )
    parser.add_argument(
        "--commit-message",
        type=str,
        default=None,
        help="Commit message for upload. Overrides MODELUPLOADER_COMMIT_MESSAGE env var (default: Upload model files)"
    )
    parser.add_argument(
        "--gitignore",
        type=str,
        default=".gitignore",
        help=get_text('gitignore_help')
    )
    parser.add_argument(
        "--ms-token",
        type=str,
        default=None,
        help=get_text('ms_token_help')
    )
    
    return parser.parse_args(args)


def run(args=None):
    """
    Run the model uploader tool
    
    Args:
        args: Command-line arguments (optional, for testing)
        
    Returns:
        Exit code
    """
    parsed_args = parse_args(args)
    
    # Validate path
    if not Path(parsed_args.path).exists():
        logger.error(get_text('path_not_exist', path=parsed_args.path))
        return 1
    
    logger.info("=" * 60)
    logger.info(get_text('tool_start'))
    logger.info("=" * 60)
    hf_repo = parsed_args.hf_repo or HF_REPO_ID or "(not set)"
    ms_repo = parsed_args.ms_repo or MS_REPO_ID or "(not set)"
    repo_type = parsed_args.repo_type or REPO_TYPE
    commit_msg = parsed_args.commit_message or COMMIT_MESSAGE
    logger.info(f"{get_text('hf_repo')}: {hf_repo}")
    logger.info(f"{get_text('ms_repo')}: {ms_repo}")
    logger.info(f"Repository Type: {repo_type}")
    logger.info(f"Commit Message: {commit_msg}")
    logger.info(f"{get_text('upload_platform')}: {parsed_args.platform}")
    logger.info(f"{get_text('upload_path')}: {parsed_args.path}")
    
    # Load ignore patterns
    ignore_patterns = load_gitignore_patterns(parsed_args.gitignore)
    
    success_count = 0
    total_count = 0
    
    # Execute uploads based on selection
    if parsed_args.platform in ["hf", "both"]:
        total_count += 1
        logger.info("-" * 60)
        logger.info(get_text('start_hf'))
        hf_repo_id = parsed_args.hf_repo or HF_REPO_ID
        repo_type = parsed_args.repo_type or REPO_TYPE
        commit_msg = parsed_args.commit_message or COMMIT_MESSAGE
        if upload_to_huggingface(parsed_args.path, repo_id=hf_repo_id, repo_type=repo_type, 
                                commit_message=commit_msg, ignore_patterns=ignore_patterns):
            success_count += 1
            logger.info(get_text('hf_success'))
        else:
            logger.error(get_text('hf_failed'))
    
    if parsed_args.platform in ["ms", "both"]:
        total_count += 1
        logger.info("-" * 60)
        logger.info(get_text('start_ms'))
        ms_repo_id = parsed_args.ms_repo or MS_REPO_ID
        commit_msg = parsed_args.commit_message or COMMIT_MESSAGE
        if upload_to_modelscope(parsed_args.path, repo_id=ms_repo_id, commit_message=commit_msg,
                               token=parsed_args.ms_token, ignore_patterns=ignore_patterns):
            success_count += 1
            logger.info(get_text('ms_success'))
        else:
            logger.error(get_text('ms_failed'))
    
    # Output summary
    logger.info("=" * 60)
    if success_count == total_count:
        logger.info(get_text('all_complete', success=success_count, total=total_count))
        return 0
    elif success_count > 0:
        logger.warning(get_text('partial_success', success=success_count, total=total_count))
        return 1
    else:
        logger.error(get_text('all_failed', success=success_count, total=total_count))
        return 1


def main():
    """Main entry point"""
    sys.exit(run())


if __name__ == "__main__":
    main()
