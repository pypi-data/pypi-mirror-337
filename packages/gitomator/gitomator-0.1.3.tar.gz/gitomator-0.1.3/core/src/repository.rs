use std::env;
use std::ffi::OsStr;
use std::path::{Path, PathBuf};
use crate::{GitCommand, GitError, GitUrl, BranchName, Result};

/// A local git repository
pub struct Repository {
    location: PathBuf,
}

impl Repository {
    /// Create a Repository struct from a pre-existing local git repository
    pub fn new<P: AsRef<Path>>(p: P) -> Repository {
        let p = p.as_ref();
        Repository {
            location: PathBuf::from(p),
        }
    }

    /// Clone a remote git repository locally
    pub fn clone<P: AsRef<Path>>(url: GitUrl, p: P) -> Result<Repository> {
        let p = p.as_ref();
        let cwd = env::current_dir().map_err(|_| GitError::WorkingDirectoryInaccessible)?;
        
        GitCommand::new(cwd)
            .operation("clone")
            .arg("clone")
            .arg(&url)
            .arg(p.to_str().unwrap())
            .run()?;
            
        Ok(Repository {
            location: PathBuf::from(p),
        })
    }

    /// Initialise a given folder as a git repository
    pub fn init<P: AsRef<Path>>(p: P) -> Result<Repository> {
        let p = p.as_ref();
        
        GitCommand::new(p)
            .operation("init")
            .arg("init")
            .run()?;
            
        Ok(Repository {
            location: PathBuf::from(p),
        })
    }

    /// Get the repository location
    pub fn location(&self) -> &Path {
        &self.location
    }

    /// Create and checkout a new local branch
    pub fn create_local_branch(&self, branch_name: &BranchName) -> Result<()> {
        GitCommand::new(&self.location)
            .operation("create_local_branch")
            .arg("checkout")
            .arg("-b")
            .arg(branch_name)
            .run()
            .map(|_| ())
    }

    /// Checkout the specified branch
    pub fn switch_branch(&self, branch_name: &BranchName) -> Result<()> {
        GitCommand::new(&self.location)
            .operation("switch_branch")
            .arg("checkout")
            .arg(branch_name)
            .run()
            .map(|_| ())
    }

    /// Add file contents to the index
    pub fn add(&self, pathspecs: Vec<&str>) -> Result<()> {
        GitCommand::new(&self.location)
            .operation("add")
            .arg("add")
            .args(pathspecs)
            .run()
            .map(|_| ())
    }

    /// Remove file contents from the index
    pub fn remove(&self, pathspecs: Vec<&str>, force: bool) -> Result<()> {
        let mut cmd = GitCommand::new(&self.location)
            .operation("remove")
            .arg("rm");
        
        if force {
            cmd = cmd.arg("-f");
        }
        
        cmd.args(pathspecs).run().map(|_| ())
    }
    
    /// Commit all staged files
    pub fn commit_all(&self, message: &str) -> Result<()> {
        GitCommand::new(&self.location)
            .operation("commit_all")
            .arg("commit")
            .arg("-am")
            .arg(message)
            .run()
            .map(|_| ())
    }

    /// Push the current branch to its associated remote
    pub fn push(&self) -> Result<()> {
        GitCommand::new(&self.location)
            .operation("push")
            .arg("push")
            .run()
            .map(|_| ())
    }

    /// Push the current branch to its associated remote, specifying the upstream branch
    pub fn push_to_upstream(&self, upstream: &str, upstream_branch: &BranchName) -> Result<()> {
        GitCommand::new(&self.location)
            .operation("push_to_upstream")
            .arg("push")
            .arg("-u")
            .arg(upstream)
            .arg(upstream_branch)
            .run()
            .map(|_| ())
    }

    /// Add a new remote
    pub fn add_remote(&self, name: &str, url: &GitUrl) -> Result<()> {
        GitCommand::new(&self.location)
            .operation("add_remote")
            .arg("remote")
            .arg("add")
            .arg(name)
            .arg(url)
            .run()
            .map(|_| ())
    }

    /// Fetch a remote
    pub fn fetch_remote(&self, remote: &str) -> Result<()> {
        GitCommand::new(&self.location)
            .operation("fetch_remote")
            .arg("fetch")
            .arg(remote)
            .run()
            .map(|_| ())
    }

    /// Create a new branch from a start point, such as another local or remote branch
    pub fn create_branch_from_startpoint(
        &self,
        branch_name: &BranchName,
        startpoint: &str,
    ) -> Result<()> {
        GitCommand::new(&self.location)
            .operation("create_branch_from_startpoint")
            .arg("checkout")
            .arg("-b")
            .arg(branch_name)
            .arg(startpoint)
            .run()
            .map(|_| ())
    }

    /// List local branches
    pub fn list_branches(&self) -> Result<Vec<String>> {
        GitCommand::new(&self.location)
            .operation("list_branches")
            .arg("branch")
            .arg("--format=%(refname:short)")
            .run()
            .map(|result| result.lines())
    }

    /// List files added to staging area
    pub fn list_added(&self) -> Result<Vec<String>> {
        self.git_status("A")
    }

    /// List all modified files
    pub fn list_modified(&self) -> Result<Vec<String>> {
        self.git_status(" M")
    }

    /// List all untracked files
    pub fn list_untracked(&self) -> Result<Vec<String>> {
        self.git_status("??")
    }

    // Helper for status commands
    fn git_status(&self, prefix: &str) -> Result<Vec<String>> {
        GitCommand::new(&self.location)
            .operation("git_status")
            .arg("status")
            .arg("-s")
            .run()
            .map(|result| {
                result
                    .filtered_lines(|line| line.starts_with(prefix))
                    .into_iter()
                    .map(|line| line[3..].to_owned())
                    .collect()
            })
    }

    /// List tracked files
    pub fn list_tracked(&self) -> Result<Vec<String>> {
        GitCommand::new(&self.location)
            .operation("list_tracked")
            .arg("ls-files")
            .run()
            .map(|result| result.lines())
    }

    /// List all the remote URI for name
    pub fn show_remote_uri(&self, remote_name: &str) -> Result<String> {
        GitCommand::new(&self.location)
            .operation("show_remote_uri")
            .arg("config")
            .arg("--get")
            .arg(format!("remote.{}.url", remote_name))
            .run()
            .map(|result| result.trim())
    }

    /// List all the remote URI for name
    pub fn list_remotes(&self) -> Result<Vec<String>> {
        let result = GitCommand::new(&self.location)
            .operation("list_remotes")
            .arg("remote")
            .arg("show")
            .run()?;
            
        if result.is_empty() {
            Err(GitError::no_remote_set(&self.location))
        } else {
            Ok(result.lines())
        }
    }

    /// Obtains commit hash of the current `HEAD`.
    pub fn get_hash(&self, short: bool) -> Result<String> {
        let mut cmd = GitCommand::new(&self.location)
            .operation("get_hash")
            .arg("rev-parse");
            
        if short {
            cmd = cmd.arg("--short");
        }
        
        cmd.arg("HEAD")
            .run()
            .map(|result| result.trim())
    }

    /// Execute user defined command
    pub fn cmd<I, S>(&self, args: I) -> Result<()>
    where
        I: IntoIterator<Item = S>,
        S: AsRef<OsStr>,
    {
        let mut command = GitCommand::new(&self.location)
            .operation("cmd");
        
        for arg in args {
            command = command.arg(arg.as_ref());
        }
        
        command.run().map(|_| ())
    }

    /// Execute user defined command and return its output
    pub fn cmd_out<I, S>(&self, args: I) -> Result<Vec<String>>
    where
        I: IntoIterator<Item = S>,
        S: AsRef<OsStr>,
    {
        let mut command = GitCommand::new(&self.location)
            .operation("cmd_out");
        
        for arg in args {
            command = command.arg(arg.as_ref());
        }
        
        command.run().map(|result| result.lines())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs::File;
    use std::io::Write;
    use std::str::FromStr;
    use tempfile::tempdir;

    #[test]
    fn test_repository_init() {
        let dir = tempdir().unwrap();
        let _repo = Repository::init(dir.path()).unwrap();
        
        // Check that .git directory was created
        assert!(dir.path().join(".git").exists());
    }

    #[test]
    fn test_add_and_commit() {
        let dir = tempdir().unwrap();
        let repo = Repository::init(dir.path()).unwrap();
        
        // Create a test file
        let file_path = dir.path().join("test.txt");
        let mut file = File::create(&file_path).unwrap();
        write!(file, "test content").unwrap();
        
        // Add and commit
        repo.add(vec!["test.txt"]).unwrap();
        repo.commit_all("Initial commit").unwrap();
        
        // Check that file is tracked
        let tracked_files = repo.list_tracked().unwrap();
        assert!(tracked_files.contains(&"test.txt".to_string()));
    }

    #[test]
    fn test_branch_operations() {
        let dir = tempdir().unwrap();
        let repo = Repository::init(dir.path()).unwrap();
        
        // Create a test file and commit
        let file_path = dir.path().join("test.txt");
        let mut file = File::create(&file_path).unwrap();
        write!(file, "test content").unwrap();
        repo.add(vec!["test.txt"]).unwrap();
        repo.commit_all("Initial commit").unwrap();
        
        // Create a new branch
        let branch = BranchName::from_str("test-branch").unwrap();
        repo.create_local_branch(&branch).unwrap();
        
        // Check that branch exists
        let branches = repo.list_branches().unwrap();
        assert!(branches.contains(&"test-branch".to_string()));
    }
}