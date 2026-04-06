"""
Internationalization (i18n) module for automatic language detection
"""

import locale
import os
import sys


def detect_language() -> str:
    """
    Detect system language and return language code
    
    Returns:
        'zh' for Chinese, 'en' for English (default)
    """
    # Check environment variables first
    lang_env = os.environ.get('LANG', '').lower()
    lc_all = os.environ.get('LC_ALL', '').lower()
    
    # Check if any Chinese locale is set
    if any(zh in lang_env or zh in lc_all for zh in ['zh', 'chinese', 'cn']):
        return 'zh'
    
    # Try to get locale from system
    try:
        # Windows
        if sys.platform == 'win32':
            import ctypes
            windll = ctypes.windll.kernel32
            user_default_locale = windll.GetUserDefaultUILanguage()
            # Language codes: 0x0804 = Chinese (Simplified), 0x0404 = Chinese (Traditional)
            if user_default_locale in [0x0804, 0x0404, 0x7c04, 0x1404]:
                return 'zh'
        else:
            # Unix-like systems
            loc = locale.getdefaultlocale()
            if loc and loc[0] and loc[0].lower().startswith('zh'):
                return 'zh'
    except Exception:
        pass
    
    # Default to English
    return 'en'


# Language strings dictionary
STRINGS = {
    'en': {
        'description': 'Upload models to HuggingFace and/or ModelScope',
        'platform_help': 'Select upload platform: hf (HuggingFace), ms (ModelScope), both',
        'path_help': 'Path to folder to upload (default: current directory)',
        'gitignore_help': 'Path to .gitignore file (default: .gitignore)',
        'ms_token_help': 'ModelScope access token (optional, can also use modelscope login command)',
        'tool_start': 'Model Uploader Tool Started',
        'hf_repo': 'HuggingFace Repository',
        'ms_repo': 'ModelScope Repository',
        'upload_platform': 'Upload Platform',
        'upload_path': 'Upload Path',
        'start_hf': '[1/2] Starting HuggingFace upload process',
        'start_ms': '[2/2] Starting ModelScope upload process',
        'hf_success': '✓ HuggingFace upload successful',
        'hf_failed': '✗ HuggingFace upload failed',
        'ms_success': '✓ ModelScope upload successful',
        'ms_failed': '✗ ModelScope upload failed',
        'all_complete': '✓ All uploads complete! ({success}/{total})',
        'partial_success': '⚠ Partial upload success ({success}/{total})',
        'all_failed': '✗ All uploads failed ({success}/{total})',
        'path_not_exist': 'Path does not exist: {path}',
        'using_token': 'Logging in with provided token...',
        'using_saved': 'No token provided, attempting to use saved credentials...',
        'ignore_patterns': 'Will ignore the following patterns: {patterns}',
        'hf_upload_start': 'Starting upload to HuggingFace: {repo_id}',
        'hf_upload_success': 'HuggingFace upload successful! Repository URL: {url}',
        'hf_upload_failed': 'HuggingFace upload failed: {error}',
        'ms_upload_start': 'Starting upload to ModelScope: {repo_id}',
        'ms_upload_success': 'ModelScope upload successful!',
        'ms_upload_failed': 'ModelScope upload failed: {error}',
        'gitignore_loaded': 'Loaded {count} ignore patterns from .gitignore',
        'gitignore_not_found': '.gitignore file not found: {path}, using default ignore patterns',
        'gitignore_error': 'Failed to read .gitignore file: {error}, using default ignore patterns',
    },
    'zh': {
        'description': '上传模型到 HuggingFace 和/或 ModelScope',
        'platform_help': '选择上传平台: hf(HuggingFace), ms(ModelScope), both(两者)',
        'path_help': '要上传的文件夹路径 (默认: 当前目录)',
        'gitignore_help': '.gitignore 文件路径 (默认: .gitignore)',
        'ms_token_help': 'ModelScope 访问令牌 (可选，也可通过 modelscope login 命令登录)',
        'tool_start': '模型上传工具启动',
        'hf_repo': 'HuggingFace 仓库',
        'ms_repo': 'ModelScope 仓库',
        'upload_platform': '上传平台',
        'upload_path': '上传路径',
        'start_hf': '[1/2] 开始 HuggingFace 上传流程',
        'start_ms': '[2/2] 开始 ModelScope 上传流程',
        'hf_success': '✓ HuggingFace 上传成功',
        'hf_failed': '✗ HuggingFace 上传失败',
        'ms_success': '✓ ModelScope 上传成功',
        'ms_failed': '✗ ModelScope 上传失败',
        'all_complete': '✓ 所有上传完成! ({success}/{total})',
        'partial_success': '⚠ 部分上传成功 ({success}/{total})',
        'all_failed': '✗ 所有上传失败 ({success}/{total})',
        'path_not_exist': '路径不存在: {path}',
        'using_token': '使用提供的 token 进行登录...',
        'using_saved': '未提供 token，尝试使用已保存的凭证...',
        'ignore_patterns': '将忽略以下模式: {patterns}',
        'hf_upload_start': '开始上传到 HuggingFace: {repo_id}',
        'hf_upload_success': 'HuggingFace 上传成功! 仓库URL: {url}',
        'hf_upload_failed': 'HuggingFace 上传失败: {error}',
        'ms_upload_start': '开始上传到 ModelScope: {repo_id}',
        'ms_upload_success': 'ModelScope 上传成功!',
        'ms_upload_failed': 'ModelScope 上传失败: {error}',
        'gitignore_loaded': '从 .gitignore 加载了 {count} 个忽略模式',
        'gitignore_not_found': '.gitignore 文件不存在: {path}, 使用默认忽略模式',
        'gitignore_error': '读取 .gitignore 文件失败: {error}, 使用默认忽略模式',
    }
}

# Detect language on module load
CURRENT_LANGUAGE = detect_language()


def get_text(key: str, **kwargs) -> str:
    """
    Get localized text string
    
    Args:
        key: Text key
        **kwargs: Format arguments
        
    Returns:
        Localized and formatted string
    """
    text = STRINGS.get(CURRENT_LANGUAGE, STRINGS['en']).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text


def set_language(lang: str):
    """
    Manually set language
    
    Args:
        lang: 'en' or 'zh'
    """
    global CURRENT_LANGUAGE
    if lang in ['en', 'zh']:
        CURRENT_LANGUAGE = lang
