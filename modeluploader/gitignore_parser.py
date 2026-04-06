"""
.gitignore file parser module
"""

import logging
from pathlib import Path
from typing import List

from .i18n import get_text

logger = logging.getLogger(__name__)


def load_gitignore_patterns(gitignore_path: str = ".gitignore") -> List[str]:
    """
    Load ignore patterns from .gitignore file
    
    Args:
        gitignore_path: Path to .gitignore file
        
    Returns:
        List of ignore patterns
    """
    patterns = []
    
    try:
        gitignore_file = Path(gitignore_path)
        if not gitignore_file.exists():
            logger.warning(get_text('gitignore_not_found', path=gitignore_path))
            return ["__pycache__", "*.pyc", ".DS_Store"]
        
        with open(gitignore_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    patterns.append(line)
        
        logger.info(get_text('gitignore_loaded', count=len(patterns)))
        
    except Exception as e:
        logger.error(get_text('gitignore_error', error=str(e)))
        patterns = ["__pycache__", "*.pyc", ".DS_Store"]
    
    return patterns
