from typing import Any

import unibox as ub
from smolagents import tool

@tool
def ub_ls(path: str = ".") -> str:
    """List the contents of a directory from local storage, S3, or Hugging Face repos.

    Args:
        path: Path to the directory to list. Default is the current directory ".".
              Accepted formats:
                - Local path: "/home/user/documents"
                - S3 path: "s3://mybucket/myfolder"
                - Hugging Face repo: "hf://username/repo_name"

    Returns:
        A string listing the contents of the specified path,
        or an error message if the directory cannot be accessed.
    """
    try:
        res = ub.ls(path)
        if not res:
            return f"Contents of '{path}':\n- (empty directory)"
        return "Contents of '{}':\n{}".format(path, "\n".join(f"- {item}" for item in res))
    except Exception as e:
        return f"Error listing directory '{path}': {str(e)}"


@tool
def ub_loads(path: str, file: bool = False) -> Any:
    """Loads a file into corresponding format from local storage, S3, or Hugging Face repos.

    Args:
        path: Path to the file to load.
        file: If True, returns the raw file path instead of parsing it.

    Returns:
        The loaded content, unwrapped and unannotated.
    """
    try:
        return ub.loads(path, file=file)
    except Exception as e:
        return f"Error loading file '{path}': {str(e)}"
