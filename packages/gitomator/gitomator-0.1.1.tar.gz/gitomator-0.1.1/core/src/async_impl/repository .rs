#![cfg(feature = "async")]

use std::ffi::OsString;
use std::path::{Path, PathBuf};
use std::process::Stdio;
use tokio::process::Command;
use std::str;

use crate::{BranchName, GitError, GitUrl, Result};
use crate::Repository;

/// Asynchronous wrapper for a git repository
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
        Self::new(Repository::new(path))
    }
    
    /// Clone a repository asynchronously
    pub async fn clone<P: AsRef<Path>>(url: GitUrl, path: P) -> Result<Self> {
        let path = path.as_ref();
        
        let status = Command::new("git")
            .arg("clone")
            .arg(url.to_string())
            .arg(path.to_str().unwrap())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .status()
            .await
            .map_err(|_| GitError::Execution)?;
            
        if status.success() {
            Ok(Self::from_path(path))
        } else {
            Err(GitError::GitError {
                stdout: String::new(),
                stderr: String::from("Git clone failed"),
            })
        }
    }
    
    /// Initialize a repository asynchronously
    pub async fn init<P: AsRef<Path>>(path: P) -> Result<Self> {
        let path = path.as_ref();
        
        let status = Command::new("git")
            .current_dir(path)
            .arg("init")
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .status()
            .await
            .map_err(|_| GitError::Execution)?;
            
        if status.success() {
            Ok(Self::from_path(path))
        } else {
            Err(GitError::GitError {
                stdout: String::new(),
                stderr: String::from("Git init failed"),
            })
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
    async fn execute_git<I, S>(&self, args: I) -> Result<String>
    where
        I: IntoIterator<Item = S>,
        S: Into<OsString>,
    {
        let output = Command::new("git")
            .current_dir(self.location())
            .args(args)
            .output()
            .await
            .map_err(|_| GitError::Execution)?;
            
        if output.status.success() {
            let stdout = str::from_utf8(&output.stdout)
                .map_err(|_| GitError::Undecodable)?
                .to_owned();
            Ok(stdout)
        } else {
            let stdout = str::from_utf8(&output.stdout)
                .map_err(|_| GitError::Undecodable)?
                .to_owned();
            let stderr = str::from_utf8(&output.stderr)
                .map_err(|_| GitError::Undecodable)?
                .to_owned();
                
            Err(GitError::GitError { stdout, stderr })
        }
    }
    
    /// Create and checkout a new local branch asynchronously
    pub async fn create_local_branch(&self, branch_name: &BranchName) -> Result<()> {
        self.execute_git(["checkout", "-b", branch_name.value.as_str()])
            .await
            .map(|_| ())
    }
    
    /// Checkout the specified branch asynchronously
    pub async fn switch_branch(&self, branch_name: &BranchName) -> Result<()> {
        self.execute_git(["checkout", branch_name.value.as_str()])
            .await
            .map(|_| ())
    }
    
    /// Add file contents to the index asynchronously
    pub async fn add(&self, pathspecs: Vec<&str>) -> Result<()> {
        let mut args = Vec::with_capacity(pathspecs.len() + 1);
        args.push("add");
        args.extend(pathspecs.iter());
        
        self.execute_git(args).await.map(|_| ())
    }
    
    /// Commit all staged files asynchronously
    pub async fn commit_all(&self, message: &str) -> Result<()> {
        self.execute_git(["commit", "-am", message])
            .await
            .map(|_| ())
    }
    
    /// Push the current branch to its associated remote asynchronously
    pub async fn push(&self) -> Result<()> {
        self.execute_git(["push"]).await.map(|_| ())
    }
    
    /// List local branches asynchronously
    pub async fn list_branches(&self) -> Result<Vec<String>> {
        let output = self.execute_git(["branch", "--format=%(refname:short)"]).await?;
        Ok(output.lines().map(String::from).collect())
    }
}

#[cfg(all(test, feature = "async"))]
mod tests {
    use super::*;
    use std::fs::File;
    use std::io::Write;
    use std::str::FromStr;
    use tempfile::tempdir;
    use tokio::runtime::Runtime;
    
    #[test]
    fn test_async_init() {
        let rt = Runtime::new().unwrap();
        
        rt.block_on(async {
            let dir = tempdir().unwrap();
            let repo = AsyncRepository::init(dir.path()).await.unwrap();
            
            assert!(dir.path().join(".git").exists());
        });
    }
    
    #[test]
    fn test_async_add_commit() {
        let rt = Runtime::new().unwrap();
        
        rt.block_on(async {
            let dir = tempdir().unwrap();
            let repo = AsyncRepository::init(dir.path()).await.unwrap();
            
            // Create a test file
            let file_path = dir.path().join("test.txt");
            let mut file = File::create(&file_path).unwrap();
            write!(file, "test content").unwrap();
            
            // Add and commit
            repo.add(vec!["test.txt"]).await.unwrap();
            repo.commit_all("Initial commit").await.unwrap();
            
            // Verify commit worked by getting branch info
            let branches = repo.list_branches().await.unwrap();
            assert!(branches.contains(&"main".to_string()) || branches.contains(&"master".to_string()));
        });
    }
}