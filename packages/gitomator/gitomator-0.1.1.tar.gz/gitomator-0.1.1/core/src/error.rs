use std::path::PathBuf;
use thiserror::Error;

/// Errors that can occur when interacting with Git
#[derive(Debug, Error)]
pub enum GitError {
    /// Unable to access current working directory
    #[error("Unable to access current working directory")]
    WorkingDirectoryInaccessible,
    
    /// Unable to execute git process
    #[error("Unable to execute git process{}: {reason}", format_operation(.operation))]
    Execution {
        operation: Option<String>,
        reason: String,
    },
    
    /// Operation timed out
    #[error("Git operation timed out after {timeout_secs} seconds{}", format_operation(.operation))]
    Timeout {
        operation: Option<String>,
        timeout_secs: u64,
    },
    
    /// Unable to decode output from git executable
    #[error("Unable to decode output from git executable{}", format_operation(.operation))]
    Undecodable {
        operation: Option<String>,
    },
    
    /// Git URL is invalid
    #[error("Git URL is invalid: {url}")]
    InvalidUrl {
        url: String,
    },
    
    /// Ref name is invalid
    #[error("Ref name is invalid: {name}")]
    InvalidRefName {
        name: String,
    },
    
    /// Commit hash is invalid
    #[error("Commit hash is invalid: {hash}")]
    InvalidCommitHash {
        hash: String,
    },
    
    /// Git failed with an error
    #[error("Git command{} failed with the following error:\nStdout: {stdout}\nStderr: {stderr}", format_operation(.operation))]
    GitError {
        operation: Option<String>,
        stdout: String,
        stderr: String,
    },
    
    /// No Git remote repository is available
    #[error("No Git remote repository is available for {}", .repository.display())]
    NoRemoteRepositorySet {
        repository: PathBuf,
    },
    
    /// Provider-specific error
    #[error("Provider '{provider}' error: {message}")]
    ProviderError {
        provider: String,
        message: String,
    },

    /// Input/output error
    #[error("I/O error: {0}")]
    IoError(#[from] std::io::Error),

    /// Path error (invalid or non-existent path)
    #[error("Path error for {}: {message}", .path.display())]
    PathError {
        path: PathBuf,
        message: String,
    },
}

// Helper function to format operation context if present
fn format_operation(operation: &Option<String>) -> String {
    if let Some(op) = operation {
        format!(" during '{}'", op)
    } else {
        String::new()
    }
}

// Factory methods for GitError to improve error creation
impl GitError {
    /// Create an Execution error with operation context
    pub fn execution<S: Into<String>>(operation: S, reason: S) -> Self {
        GitError::Execution {
            operation: Some(operation.into()),
            reason: reason.into(),
        }
    }
    
    /// Create an execution error without operation context
    pub fn execution_simple<S: Into<String>>(reason: S) -> Self {
        GitError::Execution {
            operation: None,
            reason: reason.into(),
        }
    }

    /// Create a timeout error with operation context
    pub fn timeout<S: Into<String>>(operation: S, timeout_secs: u64) -> Self {
        GitError::Timeout {
            operation: Some(operation.into()),
            timeout_secs,
        }
    }

    /// Create a timeout error without operation context
    pub fn timeout_simple(timeout_secs: u64) -> Self {
        GitError::Timeout {
            operation: None,
            timeout_secs,
        }
    }

    /// Create an Undecodable error with operation context
    pub fn undecodable<S: Into<String>>(operation: S) -> Self {
        GitError::Undecodable {
            operation: Some(operation.into()),
        }
    }
    
    /// Create an Undecodable error without operation context
    pub fn undecodable_simple() -> Self {
        GitError::Undecodable {
            operation: None,
        }
    }

    /// Create an InvalidUrl error
    pub fn invalid_url<S: Into<String>>(url: S) -> Self {
        GitError::InvalidUrl {
            url: url.into(),
        }
    }

    /// Create an InvalidRefName error
    pub fn invalid_ref_name<S: Into<String>>(name: S) -> Self {
        GitError::InvalidRefName {
            name: name.into(),
        }
    }

    /// Create an InvalidCommitHash error
    pub fn invalid_commit_hash<S: Into<String>>(hash: S) -> Self {
        GitError::InvalidCommitHash {
            hash: hash.into(),
        }
    }

    /// Create a GitError with operation context
    pub fn git_error<S: Into<String>>(operation: S, stdout: S, stderr: S) -> Self {
        GitError::GitError {
            operation: Some(operation.into()),
            stdout: stdout.into(),
            stderr: stderr.into(),
        }
    }
    
    /// Create a GitError without operation context
    pub fn git_error_simple<S: Into<String>>(stdout: S, stderr: S) -> Self {
        GitError::GitError {
            operation: None,
            stdout: stdout.into(),
            stderr: stderr.into(),
        }
    }

    /// Create a NoRemoteRepositorySet error
    pub fn no_remote_set<P: Into<PathBuf>>(repository: P) -> Self {
        GitError::NoRemoteRepositorySet {
            repository: repository.into(),
        }
    }

    /// Create a ProviderError
    pub fn provider_error<S: Into<String>>(provider: S, message: S) -> Self {
        GitError::ProviderError {
            provider: provider.into(),
            message: message.into(),
        }
    }

    /// Create a PathError
    pub fn path_error<P: Into<PathBuf>, S: Into<String>>(path: P, message: S) -> Self {
        GitError::PathError {
            path: path.into(),
            message: message.into(),
        }
    }
}