from __future__ import annotations

# NOTE: Remove this import for 0.4.0
import dsbase.mac as macos

from .compare import compare_files_by_mtime, find_duplicate_files_by_hash, sha256_checksum
from .file_manager import FileManager
