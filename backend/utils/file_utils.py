import os

SUPPORTED_EXTENSIONS = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rb', '.cpp', '.c', '.h', '.md', '.json']
IGNORED_DIRS = ['.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build', '.next', 'vendor']

def walk_repo_files(repo_path: str, max_file_size_kb: int) -> list[dict]:
    """
    Walks repo_path recursively.
    Returns a list of dicts: [{ "path": relative_path, "full_path": absolute_path, "size_kb": float }]
    Skips: any directory in IGNORED_DIRS, files without a SUPPORTED_EXTENSIONS suffix,
    and files larger than max_file_size_kb (these are almost always generated/binary/lockfiles, not worth embedding).
    """
    valid_files = []
    
    for root, dirs, files in os.walk(repo_path):
        # Modifying dirs in-place filters out subfolders from being descended into by os.walk.
        # This is more efficient than walking files/folders first and filtering them after the fact.
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() not in SUPPORTED_EXTENSIONS:
                continue
                
            full_path = os.path.join(root, file)
            try:
                size_bytes = os.path.getsize(full_path)
            except OSError:
                # Skip files where file size cannot be resolved (e.g., broken symlinks or permission errors)
                continue
                
            size_kb = size_bytes / 1024.0
            if size_kb > max_file_size_kb:
                continue
                
            # Convert Windows backslashes to Unix-style forward slashes for database consistency
            relative_path = os.path.relpath(full_path, repo_path).replace('\\', '/')
            
            valid_files.append({
                "path": relative_path,
                "full_path": os.path.abspath(full_path),
                "size_kb": size_kb
            })
            
    return valid_files

def read_file_safe(full_path: str) -> str | None:
    """
    Reads a file as UTF-8 text. Returns None (instead of crashing) if the file
    can't be decoded as text (e.g. it's actually a binary file with a misleading extension).
    """
    try:
        with open(full_path, 'r', encoding='utf-8', errors='strict') as f:
            return f.read()
    except (UnicodeDecodeError, OSError):
        return None
