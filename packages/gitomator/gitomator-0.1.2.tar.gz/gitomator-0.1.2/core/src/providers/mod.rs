pub mod github;
pub mod gitlab;

use crate::{GitUrl, Result};

/// Trait for Git hosting providers (GitHub, GitLab, etc.)
pub trait Provider {
    /// Create a new repository on the provider
    fn create_repository(&self, name: &str, description: &str, private: bool) -> Result<GitUrl>;
    
    /// Delete a repository from the provider
    fn delete_repository(&self, name: &str) -> Result<()>;
    
    /// List all repositories for the authenticated user
    fn list_repositories(&self) -> Result<Vec<String>>;
    
    /// Get the URL for a repository
    fn get_repository_url(&self, name: &str) -> Result<GitUrl>;
    
    /// Check if a repository exists
    fn repository_exists(&self, name: &str) -> Result<bool>;
    
    /// Get the provider name
    fn provider_name(&self) -> &'static str;
}