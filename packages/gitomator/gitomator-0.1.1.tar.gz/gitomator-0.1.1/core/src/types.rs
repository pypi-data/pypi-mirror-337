//! # Core types for Git operations
//! 
//! This module provides type-safe wrappers for Git concepts such as URLs, branch names,
//! and common result types. Using these types instead of raw strings helps prevent errors
//! and provides better compile-time validation.

use crate::error::GitError;
use regex::Regex;
use std::str::FromStr;
use std::{fmt, fmt::{Display, Formatter}, result::Result as stdResult};
#[cfg(feature = "serde")]
use serde::{Deserialize, Deserializer, de};

/// Result type used throughout the library
/// 
/// This is a convenience alias for `Result<T, GitError>`.
pub type Result<T> = stdResult<T, GitError>;

/// A type-safe wrapper around Git URLs
/// 
/// This type ensures that a URL is valid for use with Git operations.
/// It validates the URL format during construction.
/// 
/// # Examples
/// 
/// ```
/// use gitomator_core::GitUrl;
/// use std::str::FromStr;
/// 
/// // Create from a valid URL
/// let url = GitUrl::from_str("https://github.com/user/repo.git").unwrap();
/// assert_eq!(url.to_string(), "https://github.com/user/repo.git");
/// 
/// // Invalid URLs will return an error
/// let invalid = GitUrl::from_str("not a git url");
/// assert!(invalid.is_err());
/// ```
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GitUrl {
    pub(crate) value: String,
}

impl GitUrl {
    /// Returns the underlying URL as a string slice
    pub fn as_str(&self) -> &str {
        &self.value
    }
    
    /// Returns true if this URL uses the HTTPS protocol
    pub fn is_https(&self) -> bool {
        self.value.starts_with("https://")
    }
    
    /// Returns true if this URL uses the SSH protocol
    pub fn is_ssh(&self) -> bool {
        self.value.starts_with("git@")
    }
    
    /// Attempts to extract the repository name from the URL
    pub fn repository_name(&self) -> Option<String> {
        let parts: Vec<&str> = self.value.split('/').collect();
        
        if parts.is_empty() {
            return None;
        }
        
        let last = parts.last().unwrap();
        
        if last.ends_with(".git") {
            // Remove .git suffix
            Some(last[..last.len() - 4].to_string())
        } else {
            Some(last.to_string())
        }
    }
}

impl FromStr for GitUrl {
    type Err = GitError;

    fn from_str(value: &str) -> Result<Self> {
        // Regex from https://github.com/jonschlinkert/is-git-url
        let re =
            Regex::new("(?:git|ssh|https?|git@[-\\w.]+):(//)?(.*?)(\\.git)(/?|\\#[-\\d\\w._]+?)$")
                .unwrap();
        if re.is_match(value) {
            Ok(GitUrl {
                value: String::from(value),
            })
        } else {
            Err(GitError::invalid_url(value))
        }
    }
}

impl Display for GitUrl {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[cfg(feature = "serde")]
impl<'de> Deserialize<'de> for GitUrl {
    fn deserialize<D>(deserializer: D) -> stdResult<GitUrl, D::Error>
    where
        D: Deserializer<'de>,
    {
        let s = String::deserialize(deserializer)?;
        GitUrl::from_str(&s).map_err(de::Error::custom)
    }
}

/// A type-safe wrapper around Git branch names
/// 
/// This type ensures that a branch name is valid according to Git's rules.
/// It validates the name format during construction.
/// 
/// # Examples
/// 
/// ```
/// use gitomator_core::BranchName;
/// use std::str::FromStr;
/// 
/// // Create from a valid branch name
/// let branch = BranchName::from_str("feature/new-login").unwrap();
/// assert_eq!(branch.to_string(), "feature/new-login");
/// 
/// // Invalid branch names will return an error
/// let invalid = BranchName::from_str("feature/invalid/");
/// assert!(invalid.is_err());
/// ```
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BranchName {
    pub(crate) value: String,
}

impl BranchName {
    /// Returns the underlying branch name as a string slice
    pub fn as_str(&self) -> &str {
        &self.value
    }
    
    /// Returns true if this is a feature branch (starts with 'feature/')
    pub fn is_feature_branch(&self) -> bool {
        self.value.starts_with("feature/")
    }
    
    /// Returns true if this is the main branch ('main' or 'master')
    pub fn is_main_branch(&self) -> bool {
        self.value == "main" || self.value == "master"
    }
}

impl FromStr for BranchName {
    type Err = GitError;

    fn from_str(s: &str) -> Result<Self> {
        if is_valid_reference_name(s) {
            Ok(BranchName {
                value: String::from(s)
            })
        } else {
            Err(GitError::invalid_ref_name(s))
        }
    }
}

impl Display for BranchName {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[cfg(feature = "serde")]
impl<'de> Deserialize<'de> for BranchName {
    fn deserialize<D>(deserializer: D) -> stdResult<BranchName, D::Error>
    where
        D: Deserializer<'de>,
    {
        let s = String::deserialize(deserializer)?;
        BranchName::from_str(&s).map_err(de::Error::custom)
    }
}

/// A type-safe wrapper around Git commit hashes
/// 
/// This type ensures that a commit hash is in the correct format.
/// It validates the hash format during construction.
/// 
/// # Examples
/// 
/// ```
/// use gitomator_core::types::CommitHash;
/// use std::str::FromStr;
/// 
/// // Create from a valid full commit hash
/// let full = CommitHash::from_str("abcdef1234567890abcdef1234567890abcdef12").unwrap();
/// 
/// // Create from a valid short commit hash
/// let short = CommitHash::from_str("abcdef1").unwrap();
/// 
/// // Invalid hashes will return an error
/// let invalid = CommitHash::from_str("zzz");
/// assert!(invalid.is_err());
/// ```
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CommitHash {
    pub(crate) value: String,
    pub(crate) short: bool,
}

impl CommitHash {
    /// Create a new commit hash
    pub fn new(value: String, short: bool) -> Self {
        Self { value, short }
    }
    
    /// Get the hash value
    pub fn value(&self) -> &str {
        &self.value
    }
    
    /// Check if this is a short hash
    pub fn is_short(&self) -> bool {
        self.short
    }
}

impl Display for CommitHash {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

impl FromStr for CommitHash {
    type Err = GitError;
    
    fn from_str(s: &str) -> Result<Self> {
        // Simple validation: Git hashes are hexadecimal and at least 7 chars
        if s.len() >= 7 && s.chars().all(|c| c.is_ascii_hexdigit()) {
            Ok(CommitHash {
                value: s.to_string(),
                short: s.len() < 40,
            })
        } else {
            Err(GitError::invalid_commit_hash(s))
        }
    }
}

const INVALID_REFERENCE_CHARS: [char; 5] = [' ', '~', '^', ':', '\\'];
const INVALID_REFERENCE_START: &str = "-";
const INVALID_REFERENCE_END: &str = ".";

/// Validates if a string is a valid Git reference name
pub fn is_valid_reference_name(name: &str) -> bool {
    !name.starts_with(INVALID_REFERENCE_START)
        && !name.ends_with(INVALID_REFERENCE_END)
        && name.chars().all(|c| {
            !c.is_ascii_control() && INVALID_REFERENCE_CHARS.iter().all(|invalid| &c != invalid)
        })
        && !name.contains("/.")
        && !name.contains("@{")
        && !name.contains("..")
        && name != "@"
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_git_urls() {
        let valid_urls = vec!(
            "git://github.com/ember-cli/ember-cli.git#ff786f9f",
            "git://github.com/ember-cli/ember-cli.git#gh-pages",
            "git://github.com/ember-cli/ember-cli.git#master",
            "git://github.com/ember-cli/ember-cli.git#Quick-Fix",
            "git://github.com/ember-cli/ember-cli.git#quick_fix",
            "git://github.com/ember-cli/ember-cli.git#v0.1.0",
            "git://host.xz/path/to/repo.git/",
            "git://host.xz/~user/path/to/repo.git/",
            "git@192.168.101.127:user/project.git",
            "git@github.com:user/project.git",
            "git@github.com:user/some-project.git",
            "git@github.com:user/some-project.git",
            "git@github.com:user/some_project.git",
            "git@github.com:user/some_project.git",
            "http://192.168.101.127/user/project.git",
            "http://github.com/user/project.git",
            "http://host.xz/path/to/repo.git/",
            "https://192.168.101.127/user/project.git",
            "https://github.com/user/project.git",
            "https://host.xz/path/to/repo.git/",
            "https://username::;*%$:@github.com/username/repository.git",
            "https://username:$fooABC@:@github.com/username/repository.git",
            "https://username:password@github.com/username/repository.git",
            "ssh://host.xz/path/to/repo.git/",
            "ssh://host.xz/path/to/repo.git/",
            "ssh://host.xz/~/path/to/repo.git",
            "ssh://host.xz/~user/path/to/repo.git/",
            "ssh://host.xz:port/path/to/repo.git/",
            "ssh://user@host.xz/path/to/repo.git/",
            "ssh://user@host.xz/path/to/repo.git/",
            "ssh://user@host.xz/~/path/to/repo.git",
            "ssh://user@host.xz/~user/path/to/repo.git/",
            "ssh://user@host.xz:port/path/to/repo.git/",
        );

        for url in valid_urls.iter() {  
            assert!(GitUrl::from_str(url).is_ok(), "URL should be valid: {}", url)
        }
    }

    #[test]
    fn test_invalid_git_urls() {
        let invalid_urls = vec!(
            "/path/to/repo.git/",
            "file:///path/to/repo.git/",
            "file://~/path/to/repo.git/",
            "git@github.com:user/some_project.git/foo",
            "git@github.com:user/some_project.gitfoo",
            "host.xz:/path/to/repo.git/",
            "host.xz:path/to/repo.git",
            "host.xz:~user/path/to/repo.git/",
            "path/to/repo.git/",
            "rsync://host.xz/path/to/repo.git/",
            "user@host.xz:/path/to/repo.git/",
            "user@host.xz:path/to/repo.git",
            "user@host.xz:~user/path/to/repo.git/",
            "~/path/to/repo.git"
        );

        for url in invalid_urls.iter() {  
            assert!(GitUrl::from_str(url).is_err(), "URL should be invalid: {}", url)
        }
    }

    #[test]
    fn test_valid_reference_names() {
        let valid_reference = "avalidreference";

        assert!(is_valid_reference_name(valid_reference))
    }

    #[test]
    fn test_invalid_reference_names() {
        let invalid_references = vec!(
            "double..dot",
            "inavlid^character",
            "invalid~character",
            "invalid:character",
            "invalid\\character",
            "@",
            "inavlid@{sequence"
        );

        for reference_name in invalid_references.iter() {
            assert!(!is_valid_reference_name(reference_name))
        }
    }
    
    #[test]
    fn test_commit_hash() {
        // Valid commit hashes
        assert!(CommitHash::from_str("1234567").is_ok());
        assert!(CommitHash::from_str("abcdef0123456789").is_ok());
        assert!(CommitHash::from_str("1234567890abcdef1234567890abcdef12345678").is_ok());
        
        // Invalid commit hashes
        assert!(CommitHash::from_str("123456").is_err()); // Too short
        assert!(CommitHash::from_str("abcdefg").is_err()); // Contains non-hex character
        assert!(CommitHash::from_str("").is_err()); // Empty
    }
}