"""
Gitomator - Python bindings for Git operations
"""

__version__ = "0.1.0"

from ._gitomator import (GitError, GitExecutionError,
                         GitInvalidCommitHashError, GitInvalidRefNameError,
                         GitInvalidUrlError, GitIOError, GitProviderError,
                         GitTimeoutError, Repository)

__all__ = [
    'Repository',
    'GitError',
    'GitExecutionError',
    'GitTimeoutError',
    'GitInvalidUrlError',
    'GitInvalidRefNameError',
    'GitInvalidCommitHashError',
    'GitProviderError',
    'GitIOError',
]
