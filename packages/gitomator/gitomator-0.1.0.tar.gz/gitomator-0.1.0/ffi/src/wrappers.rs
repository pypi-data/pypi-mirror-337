use gitomator_core::{Repository, GitUrl, BranchName, Result as CoreResult, GitError as CoreError};
use std::ffi::{c_char, CStr, CString};
use std::path::Path;
use std::ptr;
use std::str::FromStr;
use std::time::Duration;

/// FFI-compatible Repository wrapper
pub struct GitRepository {
    pub inner: Repository,
}

/// Error handling for FFI
#[repr(C)]
pub struct GitResultCode {
    pub success: bool,
    pub error_message: *mut c_char,
}

impl GitResultCode {
    pub fn success() -> Self {
        Self {
            success: true,
            error_message: ptr::null_mut(),
        }
    }

    pub fn error(message: &str) -> Self {
        let error_message = match CString::new(message) {
            Ok(s) => s.into_raw(),
            Err(_) => CString::new("Failed to create error message").unwrap().into_raw(),
        };

        Self {
            success: false,
            error_message,
        }
    }

    pub fn from_git_error(error: CoreError) -> Self {
        match error {
            CoreError::Execution { operation, reason } => {
                let op = operation.unwrap_or_else(|| "git command".to_string());
                Self::error(&format!("{}: {}", op, reason))
            }
            CoreError::Timeout { operation, timeout_secs } => {
                let op = operation.unwrap_or_else(|| "git command".to_string());
                Self::error(&format!("{} timed out after {} seconds", op, timeout_secs))
            }
            CoreError::InvalidUrl { url } => {
                Self::error(&format!("Invalid Git URL: {}", url))
            }
            CoreError::InvalidRefName { name } => {
                Self::error(&format!("Invalid Git reference name: {}", name))
            }
            CoreError::InvalidCommitHash { hash } => {
                Self::error(&format!("Invalid Git commit hash: {}", hash))
            }
            CoreError::GitError { operation, stdout, stderr } => {
                let op = operation.unwrap_or_else(|| "git command".to_string());
                let mut msg = format!("Git error during {}: ", op);
                if !stdout.is_empty() {
                    msg.push_str(&format!("\nstdout: {}", stdout));
                }
                if !stderr.is_empty() {
                    msg.push_str(&format!("\nstderr: {}", stderr));
                }
                Self::error(&msg)
            }
            CoreError::NoRemoteRepositorySet { repository } => {
                Self::error(&format!("No remote repository set for {}", repository.display()))
            }
            CoreError::ProviderError { provider, message } => {
                Self::error(&format!("Provider '{}' error: {}", provider, message))
            }
            CoreError::IoError(e) => {
                Self::error(&format!("I/O error: {}", e))
            }
            CoreError::PathError { path, message } => {
                Self::error(&format!("Path error for {}: {}", path.display(), message))
            }
            CoreError::Undecodable { operation } => {
                let op = operation.unwrap_or_else(|| "git command".to_string());
                Self::error(&format!("Failed to decode output during {}", op))
            }
            CoreError::WorkingDirectoryInaccessible => {
                Self::error("Unable to access current working directory")
            }
        }
    }
}

/// Convert core Result to GitResultCode
pub fn result_to_code<T>(result: CoreResult<T>) -> (Option<T>, GitResultCode) {
    match result {
        Ok(value) => (Some(value), GitResultCode::success()),
        Err(err) => (None, GitResultCode::error(&err.to_string())),
    }
}

/// Safe wrapper for freeing error message
pub fn free_error(result: *mut GitResultCode) {
    if result.is_null() {
        return;
    }

    unsafe {
        let result = &mut *result;
        if !result.error_message.is_null() {
            let _ = CString::from_raw(result.error_message);
            result.error_message = ptr::null_mut();
        }
    }
}

/// Safe wrapper for freeing a repository
pub fn free_repository(repo: *mut GitRepository) {
    if !repo.is_null() {
        unsafe {
            drop(Box::from_raw(repo));
        }
    }
}

/// Convert C string to Rust string safely
pub fn c_char_to_string(ptr: *const c_char) -> Result<String, GitResultCode> {
    if ptr.is_null() {
        return Err(GitResultCode::error("Null pointer provided"));
    }

    let c_str = unsafe { CStr::from_ptr(ptr) };
    match c_str.to_str() {
        Ok(s) => Ok(s.to_owned()),
        Err(_) => Err(GitResultCode::error("Invalid string encoding")),
    }
}

/// Convert path pointer to Path string safely
pub fn c_char_to_path_str(path: *const c_char) -> Result<String, GitResultCode> {
    c_char_to_string(path)
}

/// Initialize a new repository wrapper
pub fn init_repository(path: *const c_char) -> Result<*mut GitRepository, GitResultCode> {
    let path_str = c_char_to_string(path)?;
    
    match gitomator_core::init(Path::new(&path_str)) {
        Ok(repo) => {
            let boxed = Box::new(GitRepository { inner: repo });
            Ok(Box::into_raw(boxed))
        }
        Err(e) => Err(GitResultCode::error(&e.to_string())),
    }
}

/// Open an existing repository wrapper
pub fn open_repository(path: *const c_char) -> Result<*mut GitRepository, GitResultCode> {
    let path_str = c_char_to_string(path)?;
    
    let repo = gitomator_core::open(Path::new(&path_str));
    let boxed = Box::new(GitRepository { inner: repo });
    Ok(Box::into_raw(boxed))
}

/// Clone a repository wrapper
pub fn clone_repository(url: *const c_char, path: *const c_char) -> Result<*mut GitRepository, GitResultCode> {
    let url_str = c_char_to_string(url)?;
    let path_str = c_char_to_string(path)?;
    
    let git_url = match GitUrl::from_str(&url_str) {
        Ok(url) => url,
        Err(_) => return Err(GitResultCode::error(&format!("Invalid Git URL: {}", url_str))),
    };

    match gitomator_core::clone(git_url, Path::new(&path_str)) {
        Ok(repo) => {
            let boxed = Box::new(GitRepository { inner: repo });
            Ok(Box::into_raw(boxed))
        }
        Err(e) => Err(GitResultCode::from_git_error(e)),
    }
}

/// Add files to a repository wrapper
pub fn add_files(repo: *mut GitRepository, paths: *const *const c_char, count: usize) -> GitResultCode {
    if repo.is_null() || paths.is_null() {
        return GitResultCode::error("Null pointer provided");
    }

    let repository = unsafe { &mut (*repo).inner };
    let mut path_strs = Vec::with_capacity(count);

    for i in 0..count {
        let path_ptr = unsafe { *paths.add(i) };
        match c_char_to_string(path_ptr) {
            Ok(s) => path_strs.push(s),
            Err(result) => return result,
        }
    }

    // Convert Vec<String> to Vec<&str>
    let path_refs: Vec<&str> = path_strs.iter().map(|s| s.as_str()).collect();
    
    match repository.add(path_refs) {
        Ok(_) => GitResultCode::success(),
        Err(e) => GitResultCode::error(&e.to_string()),
    }
}

/// Commit all changes wrapper
pub fn commit_all(repo: *mut GitRepository, message: *const c_char) -> GitResultCode {
    if repo.is_null() || message.is_null() {
        return GitResultCode::error("Null pointer provided");
    }

    let repository = unsafe { &mut (*repo).inner };
    let message_str = match c_char_to_string(message) {
        Ok(s) => s,
        Err(result) => return result,
    };

    match repository.commit_all(&message_str) {
        Ok(_) => GitResultCode::success(),
        Err(e) => GitResultCode::error(&e.to_string()),
    }
}

/// Create a branch wrapper
pub fn create_branch(repo: *mut GitRepository, branch_name: *const c_char) -> GitResultCode {
    if repo.is_null() || branch_name.is_null() {
        return GitResultCode::error("Null pointer provided");
    }

    let repository = unsafe { &mut (*repo).inner };
    let branch_str = match c_char_to_string(branch_name) {
        Ok(s) => s,
        Err(result) => return result,
    };

    let branch = match BranchName::from_str(&branch_str) {
        Ok(b) => b,
        Err(e) => return GitResultCode::error(&e.to_string()),
    };

    match repository.create_local_branch(&branch) {
        Ok(_) => GitResultCode::success(),
        Err(e) => GitResultCode::error(&e.to_string()),
    }
}

/// List branches wrapper, allocates necessary memory
pub fn list_branches(
    repo: *mut GitRepository
) -> Result<(Vec<String>, usize), GitResultCode> {
    if repo.is_null() {
        return Err(GitResultCode::error("Null pointer provided"));
    }

    let repository = unsafe { &(*repo).inner };
    
    match repository.list_branches() {
        Ok(branches) => {
            let len = branches.len();
            Ok((branches, len))
        },
        Err(e) => Err(GitResultCode::error(&e.to_string())),
    }
}

/// Convert branches to C array and string pointers
pub fn branches_to_c_array(branches: Vec<String>) -> (*mut *mut c_char, usize) {
    let count = branches.len();
    
    // Handle empty branch list case
    if count == 0 {
        return (ptr::null_mut(), 0);
    }
    
    // Allocate memory for branch name pointers
    let layout = std::alloc::Layout::array::<*mut c_char>(count).unwrap();
    let c_array = unsafe { std::alloc::alloc(layout) as *mut *mut c_char };
    
    if c_array.is_null() {
        return (ptr::null_mut(), 0);
    }
    
    // Convert each branch name to a C string
    for (i, branch) in branches.iter().enumerate() {
        match CString::new(branch.clone()) {
            Ok(c_str) => unsafe { *c_array.add(i) = c_str.into_raw() },
            Err(_) => {
                // Clean up on error
                for j in 0..i {
                    let ptr = unsafe { *c_array.add(j) };
                    if !ptr.is_null() {
                        unsafe { let _ = CString::from_raw(ptr); }
                    }
                }
                unsafe { std::alloc::dealloc(c_array as *mut u8, layout); }
                return (ptr::null_mut(), 0);
            }
        }
    }
    
    (c_array, count)
}

/// Free a list of branches
pub fn free_branch_list(branches: *mut *mut c_char, count: usize) {
    if branches.is_null() || count == 0 {
        return;
    }

    // Free each branch name
    for i in 0..count {
        let branch_ptr = unsafe { *branches.add(i) };
        if !branch_ptr.is_null() {
            unsafe { let _ = CString::from_raw(branch_ptr); }
        }
    }

    // Free the array itself
    let layout = std::alloc::Layout::array::<*mut c_char>(count).unwrap();
    unsafe { std::alloc::dealloc(branches as *mut u8, layout); }
}

/// Get current commit hash wrapper
pub fn get_hash(
    repo: *mut GitRepository,
    short: bool
) -> Result<String, GitResultCode> {
    if repo.is_null() {
        return Err(GitResultCode::error("Null pointer provided"));
    }

    let repository = unsafe { &(*repo).inner };
    
    match repository.get_hash(short) {
        Ok(hash) => Ok(hash),
        Err(e) => Err(GitResultCode::error(&e.to_string())),
    }
}

/// Convert string to C string pointer
pub fn string_to_c_ptr(s: String) -> *mut c_char {
    match CString::new(s) {
        Ok(c_str) => c_str.into_raw(),
        Err(_) => ptr::null_mut(),
    }
}

/// Free a string
pub fn free_string(string: *mut c_char) {
    if !string.is_null() {
        unsafe { let _ = CString::from_raw(string); }
    }
}
