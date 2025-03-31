#![cfg(feature = "async")]

use std::ffi::{OsStr, OsString};
use std::path::{Path, PathBuf};
use std::process::Stdio;
use tokio::process::Command;
use std::str::{self, FromStr};

use crate::error::GitError;
use crate::repository::Repository;
use crate::types::{BranchName, GitUrl, Result};

/// Async wrapper for Repository operations
pub struct AsyncRepository {
    /// The underlying repository
    repo: Repository,
}

impl AsyncRepository {
    /// Create a new AsyncRepository from a Repository
    pub fn new(repo: Repository) -> Self {
        Self { repo }
    }
    
    /// Create a new AsyncRepository from a path
    pub fn from_path<P: AsRef<Path>>(path: P) -> Self {
        Self {
            repo: Repository::new(path),
        }
    }
    
    /// Clone a repository asynchronously
    pub async fn clone<P: AsRef<Path>>(url: GitUrl, path: P) -> Result<Self> {
        let path = path.as_ref();
        
        let output = Command::new("git")
            .current_dir(path)
            .arg("clone")
            .arg(url.as_str())
            .arg(".")
            .output()
            .await
            .map_err(|e| GitError::execution("clone", &e.to_string()))?;
            
        if output.status.success() {
            Ok(Self::from_path(path))
        } else {
            let stderr = String::from_utf8_lossy(&output.stderr);
            Err(GitError::git_error("clone", "", stderr.as_ref()))
        }
    }
    
    /// Initialize a repository asynchronously
    pub async fn init<P: AsRef<Path>>(path: P) -> Result<Self> {
        let path = path.as_ref();
        
        let output = Command::new("git")
            .current_dir(path)
            .arg("init")
            .output()
            .await
            .map_err(|e| GitError::execution("init", &e.to_string()))?;
            
        if output.status.success() {
            Ok(Self::from_path(path))
        } else {
            let stderr = String::from_utf8_lossy(&output.stderr);
            Err(GitError::git_error("init", "", stderr.as_ref()))
        }
    }
    
    /// Get the underlying repository
    pub fn as_repo(&self) -> &Repository {
        &self.repo
    }
    
    /// Get the repository location
    pub fn location(&self) -> &Path {
        self.repo.location()
    }
    
    /// Execute a git command asynchronously
    async fn execute_git<I, S>(&self, operation: &str, args: I) -> Result<String>
    where
        I: IntoIterator<Item = S>,
        S: AsRef<OsStr>,
    {
        let output = Command::new("git")
            .current_dir(self.location())
            .args(args)
            .output()
            .await
            .map_err(|e| GitError::execution(operation, &e.to_string()))?;
            
        if output.status.success() {
            let stdout = str::from_utf8(&output.stdout)
                .map_err(|_| GitError::undecodable(operation))?
                .to_owned();
            Ok(stdout)
        } else {
            let stdout = String::from_utf8_lossy(&output.stdout);
            let stderr = String::from_utf8_lossy(&output.stderr);
            
            Err(GitError::git_error(operation, stdout.as_ref(), stderr.as_ref()))
        }
    }
    
    /// Create and checkout a new local branch asynchronously
    pub async fn create_local_branch(&self, branch_name: &BranchName) -> Result<()> {
        self.execute_git("create_local_branch", ["checkout", "-b", branch_name.value.as_str()])
            .await
            .map(|_| ())
    }
    
    /// Checkout the specified branch asynchronously
    pub async fn switch_branch(&self, branch_name: &BranchName) -> Result<()> {
        self.execute_git("switch_branch", ["checkout", branch_name.value.as_str()])
            .await
            .map(|_| ())
    }
    
    /// Add file contents to the index asynchronously
    pub async fn add(&self, pathspecs: Vec<&str>) -> Result<()> {
        let mut args = Vec::with_capacity(pathspecs.len() + 1);
        args.push("add");
        args.extend(pathspecs.iter());
        
        self.execute_git("add", args).await.map(|_| ())
    }
    
    /// Commit all staged files asynchronously
    pub async fn commit_all(&self, message: &str) -> Result<()> {
        self.execute_git("commit_all", ["commit", "-am", message])
            .await
            .map(|_| ())
    }
    
    /// Push the current branch to its associated remote asynchronously
    pub async fn push(&self) -> Result<()> {
        self.execute_git("push", ["push"]).await.map(|_| ())
    }
    
    /// List local branches asynchronously
    pub async fn list_branches(&self) -> Result<Vec<String>> {
        let output = self.execute_git("list_branches", ["branch", "--format=%(refname:short)"]).await?;
        Ok(output.lines().map(String::from).collect())
    }
}

#[cfg(all(test, feature = "async"))]
mod tests {
    use super::*;
    use tempfile::tempdir;

    #[tokio::test]
    async fn test_async_clone() {
        let dir = tempdir().unwrap();
        let url = GitUrl::from_str("https://github.com/user/repo.git").unwrap();
        let _repo = AsyncRepository::clone(url, dir.path()).await.unwrap();
        assert!(dir.path().join(".git").exists());
    }

    #[tokio::test]
    async fn test_async_init() {
        let dir = tempdir().unwrap();
        let _repo = AsyncRepository::init(dir.path()).await.unwrap();
        assert!(dir.path().join(".git").exists());
    }
} 