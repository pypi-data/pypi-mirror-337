"""
Type stubs for the internal _gitomator module implemented in Rust
"""
from typing import Dict, List, Optional, Union, Any
import os

class GitError(Exception):
    """Base exception for all Git operation errors."""
    def __new__(cls, message: str) -> 'GitError': ...

class GitExecutionError(GitError):
    """Exception raised when a Git command execution fails."""
    def __new__(cls, message: str) -> 'GitExecutionError': ...

class GitTimeoutError(GitError):
    """Exception raised when a Git command times out."""
    def __new__(cls, message: str) -> 'GitTimeoutError': ...

class GitInvalidUrlError(GitError):
    """Exception raised when an invalid Git URL is provided."""
    def __new__(cls, message: str) -> 'GitInvalidUrlError': ...

class GitInvalidRefNameError(GitError):
    """Exception raised when an invalid reference name is provided."""
    def __new__(cls, message: str) -> 'GitInvalidRefNameError': ...

class GitInvalidCommitHashError(GitError):
    """Exception raised when an invalid commit hash is provided."""
    def __new__(cls, message: str) -> 'GitInvalidCommitHashError': ...

class GitProviderError(GitError):
    """Exception raised when an operation with a Git provider fails."""
    def __new__(cls, message: str) -> 'GitProviderError': ...

class GitIOError(GitError):
    """Exception raised when an I/O error occurs during a Git operation."""
    def __new__(cls, message: str) -> 'GitIOError': ...

class Repository:
    """A Git repository implementation."""
    
    @classmethod
    def init(cls, path: str) -> 'Repository': ...
    
    @classmethod
    def open(cls, path: str) -> 'Repository': ...
    
    @classmethod
    def clone(cls, url: str, path: str) -> 'Repository': ...
    
    def add(self, paths: list[str]) -> None: ...
    
    def commit_all(self, message: str) -> None: ...
    
    def create_branch(self, name: str) -> None: ...
    
    def list_branches(self) -> list[str]: ...
    
    def get_hash(self, short: bool) -> str: ...
    
    def run_command(
        self, 
        command: str, 
        args: list[str],
        timeout: Optional[float] = None,
        operation: Optional[str] = None
    ) -> str: ...
    
    def run_command_with_details(
        self, 
        command: str, 
        args: list[str],
        timeout: Optional[float] = None,
        operation: Optional[str] = None
    ) -> Dict[str, Any]: ... 