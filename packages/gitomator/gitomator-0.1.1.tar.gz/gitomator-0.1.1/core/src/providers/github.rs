use std::str::FromStr;
use crate::{GitUrl, Result};
use crate::providers::Provider;

/// GitHub provider for Git operations
pub struct GithubProvider {
    token: String,
    username: String,
}

impl GithubProvider {
    /// Create a new GitHub provider
    pub fn new(token: String, username: String) -> Self {
        Self { token, username }
    }
    
    /// Get the token
    pub fn token(&self) -> &str {
        &self.token
    }
    
    /// Get the username
    pub fn username(&self) -> &str {
        &self.username
    }
}

impl Provider for GithubProvider {
    fn create_repository(&self, name: &str, _description: &str, _private: bool) -> Result<GitUrl> {
        // In a real implementation, this would make an API call to GitHub
        // For now, we'll just construct the URL
        let url = format!("https://github.com/{}/{}.git", self.username, name);
        GitUrl::from_str(&url)
    }
    
    fn delete_repository(&self, _name: &str) -> Result<()> {
        // In a real implementation, this would make an API call to GitHub
        Ok(())
    }
    
    fn list_repositories(&self) -> Result<Vec<String>> {
        // In a real implementation, this would make an API call to GitHub
        Ok(vec![])
    }
    
    fn get_repository_url(&self, name: &str) -> Result<GitUrl> {
        let url = format!("https://github.com/{}/{}.git", self.username, name);
        GitUrl::from_str(&url)
    }
    
    fn repository_exists(&self, _name: &str) -> Result<bool> {
        // In a real implementation, this would make an API call to GitHub
        Ok(false)
    }
    
    fn provider_name(&self) -> &'static str {
        "github"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_github_provider() {
        let provider = GithubProvider::new(
            "token".to_string(), 
            "username".to_string()
        );
        
        assert_eq!(provider.provider_name(), "github");
        assert_eq!(provider.username(), "username");
        assert_eq!(provider.token(), "token");
    }
    
    #[test]
    fn test_get_repository_url() {
        let provider = GithubProvider::new(
            "token".to_string(), 
            "username".to_string()
        );
        
        let url = provider.get_repository_url("repo-name").unwrap();
        assert_eq!(url.to_string(), "https://github.com/username/repo-name.git");
    }
}