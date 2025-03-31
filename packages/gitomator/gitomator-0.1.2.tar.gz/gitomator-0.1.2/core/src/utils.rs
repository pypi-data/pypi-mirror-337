use std::path::{Path, PathBuf};
use crate::Result;

/// Check if a path is a git repository
pub fn is_git_repository<P: AsRef<Path>>(path: P) -> bool {
    let git_dir = path.as_ref().join(".git");
    git_dir.exists() && git_dir.is_dir()
}

/// Find the git root directory starting from a given path
pub fn find_git_root<P: AsRef<Path>>(path: P) -> Option<PathBuf> {
    let path = path.as_ref();
    
    if is_git_repository(path) {
        return Some(path.to_path_buf());
    }
    
    let mut current = path;
    while let Some(parent) = current.parent() {
        if is_git_repository(parent) {
            return Some(parent.to_path_buf());
        }
        current = parent;
    }
    
    None
}

/// Get the relative path from the git root
pub fn path_relative_to_git_root<P: AsRef<Path>>(path: P) -> Result<PathBuf> {
    let path = path.as_ref();
    
    if let Some(root) = find_git_root(path) {
        if let Ok(relative) = path.strip_prefix(&root) {
            Ok(relative.to_path_buf())
        } else {
            Ok(path.to_path_buf())
        }
    } else {
        Ok(path.to_path_buf())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;
    use std::fs;
    use crate::Repository;
    
    #[test]
    fn test_is_git_repository() {
        let dir = tempdir().unwrap();
        assert!(!is_git_repository(dir.path()));
        
        // Initialize git repo
        let _ = Repository::init(dir.path()).unwrap();
        assert!(is_git_repository(dir.path()));
    }
    
    #[test]
    fn test_find_git_root() {
        let dir = tempdir().unwrap();
        let _ = Repository::init(dir.path()).unwrap();
        
        // Create subdirectory
        let subdir = dir.path().join("subdir");
        fs::create_dir(&subdir).unwrap();
        
        // Find git root from subdirectory
        let root = find_git_root(&subdir).unwrap();
        assert_eq!(root, dir.path());
    }
    
    #[test]
    fn test_path_relative_to_git_root() {
        let dir = tempdir().unwrap();
        let _ = Repository::init(dir.path()).unwrap();
        
        // Create subdirectory and file
        let subdir = dir.path().join("subdir");
        fs::create_dir(&subdir).unwrap();
        let file_path = subdir.join("test.txt");
        
        // Get relative path
        let relative = path_relative_to_git_root(&file_path).unwrap();
        assert_eq!(relative, PathBuf::from("subdir/test.txt"));
    }
}