import logging
import os
import subprocess
from pathlib import Path
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

debug_env = os.getenv("DEBUG", "0")

if debug_env == "0":
    logging.getLogger("mcp.server.lowlevel.server").disabled = True
else:
    logging.getLogger("mcp.server.lowlevel.server").setLevel(logging.DEBUG)

OC_PATH = os.environ.get("OC_PATH", str(Path.cwd())).split(":")
ALLOWED_GIT_CMDS = {"status", "log", "branch", "commit", "diff", "pull", "rev-parse"}


mcp = FastMCP("FileEditor")


def validate_path(path: str) -> str:
    """Ensure the requested path is within allowed directories."""
    abs_path = os.path.abspath(path)
    if not any(abs_path.startswith(os.path.abspath(d)) for d in OC_PATH):
        raise ValueError("Access to this path is not allowed.")
    return abs_path


def safe_replace(file_path, old_text, new_text):
    with open(file_path, "r") as f:
        content = f.read()

    count = content.count(old_text)
    if count == 0:
        raise ValueError("Error: No match found")
    elif count > 1:
        raise ValueError(f"Error: Found {count} matches")

    new_content = content.replace(old_text, new_text)
    with open(file_path, "w") as f:
        f.write(new_content)

    return "Successfully replaced text"


@mcp.tool()
async def read_file(path: str) -> str:
    """Read file content with line numbers"""
    try:
        validated_path = validate_path(path)
        result = subprocess.run(
            ["cat", "-n", validated_path], capture_output=True, text=True
        )
        if result.returncode != 0:
            return f"Error:\n{result.stderr}"
        return result.stdout
    except Exception as e:
        return f"Error:\n{str(e)}"


@mcp.tool()
async def str_replace_editor(path: str, old_str: str, new_str: str) -> str:
    try:
        validated_path = validate_path(path)
        return safe_replace(validated_path, old_str, new_str)
    except Exception as e:
        return f"Error:\n{str(e)}"


@mcp.tool()
async def git(command: str, args: Optional[List[str]] = None) -> str:
    """Execute a whitelisted git command using subprocess."""
    try:
        if command.startswith("git "):
            command = command[4:]

        if command not in ALLOWED_GIT_CMDS:
            return f"Error: Command '{command}' is not whitelisted."

        git_command = ["git", command]
        if args:
            git_command.extend(args)

        result = subprocess.run(
            git_command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"

        return result.stdout
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
