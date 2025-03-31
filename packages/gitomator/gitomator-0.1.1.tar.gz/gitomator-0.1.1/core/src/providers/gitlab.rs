use std::str::FromStr;
use crate::{GitUrl, Result};
use crate::providers::Provider;

/// GitLab provider for Git operations
pub struct GitlabProvider {
    token: String,
    username: String,
    server: String,
}

impl GitlabProvider {
    /// Create a new GitLab provider
    pub fn new(token: String, username: String, server: String) -> Self {
        Self { token, username, server }
    }
    
    /// Create a new GitLab provider with the default server (gitlab.com)
    pub fn new_with_default_server(token: String, username: String) -> Self {
        Self {
            token,
            username,
            server: "gitlab.com".to_string(),
        }
    }
    
    /// Get the token
    pub fn token(&self) -> &str {
        &self.token
    }
    
    /// Get the username
    pub fn username(&self) -> &str {
        &self.username
    }
    
    /// Get the server
    pub fn server(&self) -> &str {
        &self.server
    }
}

impl Provider for GitlabProvider {
    fn create_repository(&self, name: &str, _description: &str, _private: bool) -> Result<GitUrl> {
        // In a real implementation, this would make an API call to GitLab
        // For now, we'll just construct the URL
        let url = format!("https://{}/{}/{}.git", self.server, self.username, name);
        GitUrl::from_str(&url)
    }
    
    fn delete_repository(&self, _name: &str) -> Result<()> {
        // In a real implementation, this would make an API call to GitLab
        Ok(())
    }
    
    fn list_repositories(&self) -> Result<Vec<String>> {
        // In a real implementation, this would make an API call to GitLab
        Ok(vec![])
    }
    
    fn get_repository_url(&self, name: &str) -> Result<GitUrl> {
        let url = format!("https://{}/{}/{}.git", self.server, self.username, name);
        GitUrl::from_str(&url)
    }
    
    fn repository_exists(&self, _name: &str) -> Result<bool> {
        // In a real implementation, this would make an API call to GitLab
        Ok(false)
    }
    
    fn provider_name(&self) -> &'static str {
        "gitlab"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_gitlab_provider() {
        let provider = GitlabProvider::new(
            "token".to_string(), 
            "username".to_string(),
            "gitlab.com".to_string()
        );
        
        assert_eq!(provider.provider_name(), "gitlab");
        assert_eq!(provider.username(), "username");
        assert_eq!(provider.token(), "token");
        assert_eq!(provider.server(), "gitlab.com");
    }
    
    #[test]
    fn test_get_repository_url() {
        let provider = GitlabProvider::new(
            "token".to_string(), 
            "username".to_string(),
            "gitlab.com".to_string()
        );
        
        let url = provider.get_repository_url("repo-name").unwrap();
        assert_eq!(url.to_string(), "https://gitlab.com/username/repo-name.git");
    }
    
    #[test]
    fn test_default_server() {
        let provider = GitlabProvider::new_with_default_server(
            "token".to_string(), 
            "username".to_string()
        );
        
        assert_eq!(provider.server(), "gitlab.com");
    }
}