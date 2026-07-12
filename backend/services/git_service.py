import os
import shutil
from urllib.parse import urlparse
import git
from config import settings

def get_repo_name(repo_url: str) -> str:
    """
    Returns just the folder name derived from the repo URL, without cloning.
    E.g. "https://github.com/user/repo.git" -> "user_repo"
    """
    parsed = urlparse(repo_url)
    path = parsed.path.strip('/')
    if path.endswith('.git'):
        path = path[:-4]
    return path.replace('/', '_')

def clone_repo(repo_url: str) -> str:
    """
    Clones a public GitHub repo into settings.CLONE_DIR.
    Returns the local path where it was cloned.
    """
    folder_name = get_repo_name(repo_url)
    target_path = os.path.join(settings.CLONE_DIR, folder_name)

    # Ensure CLONE_DIR exists before cloning
    os.makedirs(settings.CLONE_DIR, exist_ok=True)

    # Idempotency: If the path already exists, delete it first.
    # This ensures that calling clone_repo multiple times for the same repo
    # will overwrite the existing clone rather than failing with a destination-already-exists error.
    if os.path.exists(target_path):
        def remove_readonly(func, path, exc):
            import stat
            os.chmod(path, stat.S_IWRITE)
            func(path)
        shutil.rmtree(target_path, onexc=remove_readonly)

    try:
        # Perform a shallow clone (depth=1). We only need the current file contents
        # to build our index and answer questions, not the entire historical git logs.
        # This makes cloning significantly faster and saves disk space.
        git.Repo.clone_from(repo_url, target_path, depth=1)
    except git.exc.GitCommandError as e:
        raise ValueError("Could not clone repo. Check the URL is a valid public GitHub repository.") from e

    return target_path
