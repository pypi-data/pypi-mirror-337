#![allow(dead_code)]
//! # Gitomator Core
//! 
//! A Rust library for Git operations with a clean, intuitive API.
//! 
//! Gitomator provides a high-level interface for common Git operations without requiring
//! external Git binaries (implemented using libgit2).
//! 
//! ## Quick Start
//! 
//! ```rust
//! use gitomator_core::{init, GitUrl, BranchName};
//! use std::str::FromStr;
//! 
//! // Initialize a new Git repository
//! let repo = init("/path/to/repo").expect("Failed to initialize repository");
//! 
//! // Create a file and make your first commit
//! std::fs::write("/path/to/repo/README.md", "# My Project").expect("Failed to write file");
//! repo.add(vec!["README.md"]).expect("Failed to add file");
//! repo.commit_all("Initial commit").expect("Failed to commit");
//! 
//! // Create and switch to a feature branch
//! let branch = BranchName::from_str("feature-branch").expect("Invalid branch name");
//! repo.create_local_branch(&branch).expect("Failed to create branch");
//! 
//! // List branches
//! let branches = repo.list_branches().expect("Failed to list branches");
//! println!("Branches: {:?}", branches);
//! ```
//! 
//! ## Modules
//! 
//! - [`Repository`]: Primary interface for repository operations
//! - [`Provider`]: Git hosting providers (GitHub, GitLab)
//! - [`GitUrl`], [`BranchName`]: Type-safe wrappers for Git concepts

// Internal modules
mod async_impl;
mod utils;

// Public modules with implementation details
pub mod error;
pub mod providers;
pub mod repository;
pub mod types;

// Internal imports
use std::ffi::{OsStr, OsString};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::str;
use std::time::{Duration, Instant};
use std::thread;
use std::io::Write;

// ===== PUBLIC API =====
// Re-exports of primary types that users should depend on
pub use error::GitError;
pub use repository::Repository;
pub use types::{BranchName, GitUrl, Result};

// Re-export provider interfaces
pub use providers::Provider;
pub use providers::github::GithubProvider;
pub use providers::gitlab::GitlabProvider;

// ===== PRIMARY FACTORY FUNCTIONS =====

/// Opens an existing Git repository at the specified path
///
/// # Arguments
///
/// * `path` - Path to the existing repository
///
/// # Returns
///
/// A `Repository` instance for the specified path
///
/// # Examples
///
/// ```
/// use gitomator_core::open;
/// 
/// let repo = open("/path/to/existing/repo");
/// println!("Opened repository");
/// ```
pub fn open<P: AsRef<Path>>(path: P) -> Repository {
    Repository::new(path)
}

/// Clones a Git repository from a URL to a local path
///
/// # Arguments
///
/// * `url` - The URL of the repository to clone
/// * `path` - The local path where the repository will be cloned
///
/// # Returns
///
/// A `Result<Repository, GitError>` containing the repository or an error
///
/// # Examples
///
/// ```
/// use gitomator_core::{clone, GitUrl};
/// use std::str::FromStr;
/// 
/// let url = GitUrl::from_str("https://github.com/user/repo.git").unwrap();
/// let repo = clone(url, "/path/to/clone").expect("Failed to clone repository");
/// ```
pub fn clone<P: AsRef<Path>>(url: GitUrl, path: P) -> Result<Repository> {
    Repository::clone(url, path)
}

/// Initializes a new Git repository at the specified path
///
/// # Arguments
///
/// * `path` - Path where the new repository will be created
///
/// # Returns
///
/// A `Result<Repository, GitError>` containing the repository or an error
///
/// # Examples
///
/// ```
/// use gitomator_core::init;
/// 
/// let repo = init("/path/to/new/repo").expect("Failed to initialize repository");
/// println!("Initialized new repository");
/// ```
pub fn init<P: AsRef<Path>>(path: P) -> Result<Repository> {
    Repository::init(path)
}

// ===== COMMAND INTERFACE =====
// This section contains the command building interface which allows for
// fine-grained control over Git operations

/// Trait for converting values into Git command arguments
pub trait IntoGitArg {
    /// Converts the value into a string representation suitable for Git commands
    fn into_git_arg(self) -> OsString;
}

// Implement for common types
impl<T: AsRef<OsStr>> IntoGitArg for T {
    fn into_git_arg(self) -> OsString {
        self.as_ref().to_owned()
    }
}

impl IntoGitArg for &BranchName {
    fn into_git_arg(self) -> OsString {
        self.value.as_str().into()
    }
}

impl IntoGitArg for &GitUrl {
    fn into_git_arg(self) -> OsString {
        self.value.as_str().into()
    }
}

/// Result type for Git command execution
pub struct GitCommandResult {
    stdout: String,
    stderr: Vec<u8>,
    args: Vec<OsString>,
    operation_name: Option<String>,
}

impl GitCommandResult {
    fn new(stdout: String, stderr: Vec<u8>, args: Vec<OsString>, operation_name: Option<String>) -> Self {
        Self { stdout, stderr, args, operation_name }
    }

    /// Returns the raw command output
    pub fn raw_output(&self) -> &str {
        &self.stdout
    }
    
    /// Returns the raw stderr output as a string if decodable
    pub fn stderr(&self) -> Option<String> {
        String::from_utf8(self.stderr.clone()).ok()
    }
    
    /// Returns the operation name if available
    pub fn operation_name(&self) -> Option<&str> {
        self.operation_name.as_deref()
    }

    /// Returns the command arguments used
    pub fn args(&self) -> &[OsString] {
        &self.args
    }

    /// Returns the command output as a vector of lines
    pub fn lines(&self) -> Vec<String> {
        self.stdout.lines().map(|s| s.to_owned()).collect()
    }

    /// Returns the command output with whitespace trimmed
    pub fn trim(&self) -> String {
        self.stdout.trim().to_owned()
    }

    /// Returns whether the command output is empty (after trimming)
    pub fn is_empty(&self) -> bool {
        self.stdout.trim().is_empty()
    }

    /// Returns lines from the command output filtered by the provided function
    pub fn filtered_lines<F>(&self, filter: F) -> Vec<String>
    where
        F: Fn(&str) -> bool,
    {
        self.stdout
            .lines()
            .filter(|line| filter(line))
            .map(|line| line.to_owned())
            .collect()
    }
}

/// Builder for Git command execution
///
/// This provides a fluent interface for constructing and running Git commands.
///
/// # Examples
///
/// ```
/// use gitomator_core::{GitCommand, init};
///
/// let repo = init("/path/to/repo").unwrap();
/// let result = GitCommand::new("/path/to/repo")
///     .arg("log")
///     .arg("--oneline")
///     .arg("--max-count=5")
///     .run()
///     .expect("Failed to run git log");
///
/// for line in result.lines() {
///     println!("Commit: {}", line);
/// }
/// ```
pub struct GitCommand {
    dir: PathBuf,
    args: Vec<OsString>,
    operation_name: Option<String>,
    timeout: Option<Duration>,
    stdin: Option<Vec<u8>>,
}

impl GitCommand {
    /// Creates a new Git command builder for the specified directory
    pub fn new<P: AsRef<Path>>(dir: P) -> Self {
        Self {
            dir: dir.as_ref().to_path_buf(),
            args: Vec::new(),
            operation_name: None,
            timeout: None,
            stdin: None,
        }
    }

    /// Sets a name for this operation, used in error reporting
    pub fn operation<S: Into<String>>(mut self, name: S) -> Self {
        self.operation_name = Some(name.into());
        self
    }

    /// Sets a timeout for this command
    pub fn timeout(mut self, duration: Duration) -> Self {
        self.timeout = Some(duration);
        self
    }

    /// Sets a timeout for this command in seconds
    pub fn timeout_secs(mut self, seconds: u64) -> Self {
        self.timeout = Some(Duration::from_secs(seconds));
        self
    }

    /// Provides input data to be passed to the command's stdin
    pub fn stdin(mut self, data: Vec<u8>) -> Self {
        self.stdin = Some(data);
        self
    }

    /// Provides string input data to be passed to the command's stdin
    pub fn stdin_str<S: AsRef<str>>(mut self, data: S) -> Self {
        self.stdin = Some(data.as_ref().as_bytes().to_vec());
        self
    }

    /// Adds a single argument to the Git command
    pub fn arg<A: IntoGitArg>(mut self, arg: A) -> Self {
        self.args.push(arg.into_git_arg());
        self
    }

    /// Adds multiple arguments to the Git command
    pub fn args<I, A>(mut self, args: I) -> Self
    where
        I: IntoIterator<Item = A>,
        A: IntoGitArg,
    {
        for arg in args {
            self.args.push(arg.into_git_arg());
        }
        self
    }

    /// Executes the Git command and returns the result
    pub fn run(self) -> Result<GitCommandResult> {
        // Create the command
        let mut cmd = Command::new("git");
        cmd.current_dir(&self.dir)
            .args(&self.args)
            .stdout(Stdio::piped())
            .stderr(Stdio::piped());

        // Configure stdin if provided
        if let Some(input) = &self.stdin {
            cmd.stdin(Stdio::piped());
        }

        // If no timeout is set, run the command directly
        if self.timeout.is_none() {
            return self.execute_command(cmd);
        }

        // With timeout, spawn in a separate thread and monitor
        let timeout = self.timeout.unwrap();
        let operation = self.operation_name.clone();
        
        // Use a separate thread to handle the timeout
        let handle = thread::spawn(move || {
            self.execute_command(cmd)
        });

        // Wait for completion with timeout
        let start = Instant::now();
        while start.elapsed() < timeout {
            if handle.is_finished() {
                return match handle.join() {
                    Ok(result) => result,
                    Err(_) => Err(GitError::execution_simple("Command thread panicked")),
                };
            }
            thread::sleep(Duration::from_millis(10));
        }

        // Timeout occurred
        Err(GitError::timeout(
            operation.unwrap_or_else(|| "git command".to_string()), 
            timeout.as_secs()
        ))
    }

    // Helper method to actually execute the command
    fn execute_command(self, mut cmd: Command) -> Result<GitCommandResult> {
        // Handle stdin if provided
        let mut child = match cmd.spawn() {
            Ok(child) => child,
            Err(e) => {
                return Err(GitError::execution(
                    self.operation_name.unwrap_or_else(|| "git command".to_string()),
                    format!("Failed to spawn process: {}", e)
                ));
            }
        };

        // Write to stdin if provided
        if let Some(input) = self.stdin {
            if let Some(stdin) = &mut child.stdin {
                if let Err(e) = stdin.write_all(&input) {
                    return Err(GitError::execution(
                        self.operation_name.unwrap_or_else(|| "git command".to_string()),
                        format!("Failed to write to stdin: {}", e)
                    ));
                }
            }
        }

        // Wait for the command to complete
        let output = match child.wait_with_output() {
            Ok(output) => output,
            Err(e) => {
                return Err(GitError::execution(
                    self.operation_name.unwrap_or_else(|| "git command".to_string()),
                    format!("Failed to wait for process: {}", e)
                ));
            }
        };

        if output.status.success() {
            let stdout = match str::from_utf8(&output.stdout) {
                Ok(s) => s.to_owned(),
                Err(_) => {
                    return Err(GitError::undecodable(
                        self.operation_name.unwrap_or_else(|| "git command".to_string())
                    ));
                }
            };
            
            Ok(GitCommandResult::new(
                stdout,
                output.stderr,
                self.args,
                self.operation_name
            ))
        } else {
            let stdout = match str::from_utf8(&output.stdout) {
                Ok(s) => s.to_owned(),
                Err(_) => String::from("[undecodable stdout]"),
            };
            
            let stderr = match str::from_utf8(&output.stderr) {
                Ok(s) => s.to_owned(),
                Err(_) => String::from("[undecodable stderr]"),
            };
            
            Err(GitError::git_error(
                self.operation_name.unwrap_or_else(|| "git command".to_string()),
                stdout,
                stderr
            ))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    #[test]
    fn test_init_repository() {
        let dir = tempdir().unwrap();
        let _repo = init(dir.path()).unwrap();
        assert!(dir.path().join(".git").exists());
    }

    #[test]
    fn test_open_repository() {
        let dir = tempdir().unwrap();
        let _ = init(dir.path()).unwrap();
        let _repo = open(dir.path());
        // Repository exists and can be opened
        assert!(dir.path().join(".git").exists());
    }

    #[test]
    fn test_git_command() {
        let dir = tempdir().unwrap();
        let _ = init(dir.path()).unwrap();
        
        // Test GitCommand builder
        let result = GitCommand::new(dir.path())
            .arg("status")
            .run()
            .unwrap();
            
        assert!(!result.is_empty());
    }
}