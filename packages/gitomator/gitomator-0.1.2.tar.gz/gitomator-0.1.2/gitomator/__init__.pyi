"""
Type stubs for Gitomator - Python bindings for Git operations
"""
import os
from pathlib import Path
from typing import Optional, TypedDict, Union


class GitError(Exception):
    """Base exception for all Git operation errors."""
    pass


class GitExecutionError(GitError):
    """Exception raised when a Git command execution fails."""
    pass


class GitTimeoutError(GitError):
    """Exception raised when a Git command times out."""
    pass


class GitInvalidUrlError(GitError):
    """Exception raised when an invalid Git URL is provided."""
    pass


class GitInvalidRefNameError(GitError):
    """Exception raised when an invalid reference name is provided."""
    pass


class GitInvalidCommitHashError(GitError):
    """Exception raised when an invalid commit hash is provided."""
    pass


class GitProviderError(GitError):
    """Exception raised when an operation with a Git provider fails."""
    pass


class GitIOError(GitError):
    """Exception raised when an I/O error occurs during a Git operation."""
    pass


class CommandResult(TypedDict, total=False):
    """Type for command execution results with details."""
    stdout: str
    stderr: str
    operation: str
    args: list[str]


class Repository:
    """A Git repository."""

    @classmethod
    def init(cls, path: Union[str, os.PathLike]) -> 'Repository':
        """Initialize a new Git repository at the specified path."""
        ...

    @classmethod
    def open(cls, path: Union[str, os.PathLike]) -> 'Repository':
        """Open an existing Git repository at the specified path."""
        ...

    @classmethod
    def clone(cls, url: str, path: Union[str, os.PathLike]) -> 'Repository':
        """Clone a repository from the specified URL to the specified path."""
        ...

    def add(self, paths: list[str]) -> None:
        """Add files to the Git repository."""
        ...

    def commit_all(self, message: str) -> None:
        """Commit all changes with the provided message."""
        ...

    def create_branch(self, name: str) -> None:
        """Create a new branch with the specified name."""
        ...

    def list_branches(self) -> list[str]:
        """List all branches in the repository."""
        ...

    def get_hash(self, short: bool = True) -> str:
        """Get the current commit hash."""
        ...

    def run_command(
        self,
        command: str,
        args: list[str],
        timeout: Optional[float] = None,
        operation: Optional[str] = None
    ) -> str:
        """Run a Git command and return the output as a string."""
        ...

    def run_command_with_details(
        self,
        command: str,
        args: list[str],
        timeout: Optional[float] = None,
        operation: Optional[str] = None
    ) -> CommandResult:
        """Run a Git command and return detailed output information."""
        ...
