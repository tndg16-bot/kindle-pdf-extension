"""App package initialization - Local Distribution Version."""

import os
from pathlib import Path
import uuid


def get_temp_dir(prefix: str = "moji_") -> Path:
    """Get temporary directory path.
    
    ローカル配布版では /tmp を使用
    
    Args:
        prefix: ディレクトリ名のプレフィックス
        
    Returns:
        作成された一時ディレクトリのPath
    """
    # ローカル環境では /tmp を使用
    import tempfile
    return Path(tempfile.mkdtemp(prefix=prefix))