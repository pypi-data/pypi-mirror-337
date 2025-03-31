use pyo3::create_exception;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pyo3::types::{PyType, PyDict};
use std::ffi::CString;
use std::time::Duration;
use gitomator_core::{GitCommand, GitError as CoreError};
use crate::wrappers::{list_branches, get_hash};

// Define custom exception types for different Git errors
create_exception!(gitomator, GitError, PyException);
create_exception!(gitomator, GitExecutionError, GitError);
create_exception!(gitomator, GitTimeoutError, GitError);
create_exception!(gitomator, GitInvalidUrlError, GitError);
create_exception!(gitomator, GitInvalidRefNameError, GitError);
create_exception!(gitomator, GitInvalidCommitHashError, GitError);
create_exception!(gitomator, GitProviderError, GitError);
create_exception!(gitomator, GitIOError, GitError);

// Python wrapper for the Repository
#[pyclass(name = "Repository", unsendable)]
struct PyRepository {
    inner: *mut crate::GitRepository,
}

// Make sure repository is freed when the Python object is garbage collected
impl Drop for PyRepository {
    fn drop(&mut self) {
        if !self.inner.is_null() {
            crate::gitomator_free_repository(self.inner);
            self.inner = std::ptr::null_mut();
        }
    }
}

// Helper function to convert GitError to appropriate Python exception
fn git_error_to_py_err(error: CoreError) -> PyErr {
    match error {
        CoreError::Timeout { operation, timeout_secs } => {
            let op = operation.unwrap_or_else(|| "git command".to_string());
            GitTimeoutError::new_err(format!("Git operation timed out after {} seconds during '{}'", timeout_secs, op))
        }
        CoreError::InvalidUrl { url } => {
            GitInvalidUrlError::new_err(format!("Invalid Git URL: {}", url))
        }
        CoreError::InvalidRefName { name } => {
            GitInvalidRefNameError::new_err(format!("Invalid Git reference name: {}", name))
        }
        CoreError::InvalidCommitHash { hash } => {
            GitInvalidCommitHashError::new_err(format!("Invalid Git commit hash: {}", hash))
        }
        CoreError::NoRemoteRepositorySet { repository } => {
            GitExecutionError::new_err(format!("No remote repository set for {}", repository.display()))
        }
        CoreError::ProviderError { provider, message } => {
            GitProviderError::new_err(format!("Git provider '{}' error: {}", provider, message))
        }
        CoreError::IoError(e) => {
            GitIOError::new_err(format!("Git I/O error: {}", e))
        }
        CoreError::PathError { path, message } => {
            GitIOError::new_err(format!("Git path error for {}: {}", path.display(), message))
        }
        CoreError::Undecodable { operation } => {
            let op = operation.unwrap_or_else(|| "git command".to_string());
            GitExecutionError::new_err(format!("Failed to decode Git output during {}", op))
        }
        CoreError::WorkingDirectoryInaccessible => {
            GitIOError::new_err("Unable to access Git working directory")
        }
        CoreError::Execution { operation, reason } => {
            let op = operation.unwrap_or_else(|| "git command".to_string());
            GitExecutionError::new_err(format!("Git execution error during '{}': {}", op, reason))
        }
        CoreError::GitError { operation, stdout, stderr } => {
            let op = operation.unwrap_or_else(|| "git command".to_string());
            let mut msg = format!("Git error during '{}': ", op);
            if !stdout.is_empty() {
                msg.push_str(&format!("\nstdout: {}", stdout));
            }
            if !stderr.is_empty() {
                msg.push_str(&format!("\nstderr: {}", stderr));
            }
            GitExecutionError::new_err(msg)
        }
    }
}

// Generate Python API for our Repository class
#[pymethods]
impl PyRepository {
    #[classmethod]
    fn init(_cls: &Bound<'_, PyType>, path: &str) -> PyResult<Self> {
        let c_path = CString::new(path).map_err(|_| {
            GitError::new_err("Invalid path string")
        })?;
        
        let mut repo: *mut crate::GitRepository = std::ptr::null_mut();
        let mut result = crate::gitomator_init(c_path.as_ptr(), &mut repo);
        
        if !result.success {
            let error_msg = if result.error_message.is_null() {
                "Unknown error during repository initialization".to_string()
            } else {
                let c_str = unsafe { std::ffi::CStr::from_ptr(result.error_message) };
                let string = c_str.to_string_lossy().into_owned();
                crate::gitomator_free_error(&mut result as *mut _);
                string
            };
            
            return Err(GitError::new_err(error_msg));
        }
        
        Ok(PyRepository { inner: repo })
    }
    
    #[classmethod]
    fn open(_cls: &Bound<'_, PyType>, path: &str) -> PyResult<Self> {
        let c_path = CString::new(path).map_err(|_| {
            GitError::new_err("Invalid path string")
        })?;
        
        let mut repo: *mut crate::GitRepository = std::ptr::null_mut();
        
        let mut result = crate::gitomator_open(c_path.as_ptr(), &mut repo);
        
        if !result.success {
            let error_msg = if result.error_message.is_null() {
                "Unknown error opening repository".to_string()
            } else {
                let c_str = unsafe { std::ffi::CStr::from_ptr(result.error_message) };
                let string = c_str.to_string_lossy().into_owned();
                crate::gitomator_free_error(&mut result as *mut _);
                string
            };
            
            return Err(GitError::new_err(error_msg));
        }
        
        Ok(PyRepository { inner: repo })
    }
    
    #[classmethod]
    fn clone(_cls: &Bound<'_, PyType>, url: &str, path: &str) -> PyResult<Self> {
        let c_url = CString::new(url).map_err(|_| {
            GitError::new_err("Invalid URL string")
        })?;
        
        let c_path = CString::new(path).map_err(|_| {
            GitError::new_err("Invalid path string")
        })?;
        
        let mut repo: *mut crate::GitRepository = std::ptr::null_mut();
        
        let mut result = crate::gitomator_clone(c_url.as_ptr(), c_path.as_ptr(), &mut repo);
        
        if !result.success {
            let error_msg = if result.error_message.is_null() {
                "Unknown error cloning repository".to_string()
            } else {
                let c_str = unsafe { std::ffi::CStr::from_ptr(result.error_message) };
                let string = c_str.to_string_lossy().into_owned();
                crate::gitomator_free_error(&mut result as *mut _);
                string
            };
            
            return Err(GitError::new_err(error_msg));
        }
        
        Ok(PyRepository { inner: repo })
    }
    
    fn add(&self, paths: Vec<String>) -> PyResult<()> {
        // Convert paths to C strings
        let c_paths: Vec<CString> = paths.iter()
            .map(|p| CString::new(p.as_str()))
            .collect::<Result<Vec<CString>, _>>()
            .map_err(|_| GitError::new_err("Invalid path string"))?;
        
        // Create array of pointers
        let c_ptrs: Vec<*const i8> = c_paths.iter()
            .map(|p| p.as_ptr())
            .collect();
        
        let mut result = crate::gitomator_add(self.inner, c_ptrs.as_ptr(), c_ptrs.len());
        
        if !result.success {
            let error_msg = if result.error_message.is_null() {
                "Unknown error adding files".to_string()
            } else {
                let c_str = unsafe { std::ffi::CStr::from_ptr(result.error_message) };
                let string = c_str.to_string_lossy().into_owned();
                crate::gitomator_free_error(&mut result as *mut _);
                string
            };
            
            return Err(GitError::new_err(error_msg));
        }
        
        Ok(())
    }
    
    fn commit_all(&self, message: &str) -> PyResult<()> {
        let c_message = CString::new(message).map_err(|_| {
            GitError::new_err("Invalid message string")
        })?;
        
        let mut result = crate::gitomator_commit_all(self.inner, c_message.as_ptr());
        
        if !result.success {
            let error_msg = if result.error_message.is_null() {
                "Unknown error committing changes".to_string()
            } else {
                let c_str = unsafe { std::ffi::CStr::from_ptr(result.error_message) };
                let string = c_str.to_string_lossy().into_owned();
                crate::gitomator_free_error(&mut result as *mut _);
                string
            };
            
            return Err(GitError::new_err(error_msg));
        }
        
        Ok(())
    }
    
    fn create_branch(&self, name: &str) -> PyResult<()> {
        let c_name = CString::new(name).map_err(|_| {
            GitError::new_err("Invalid branch name")
        })?;
        
        let mut result = crate::gitomator_create_branch(self.inner, c_name.as_ptr());
        
        if !result.success {
            let error_msg = if result.error_message.is_null() {
                "Unknown error creating branch".to_string()
            } else {
                let c_str = unsafe { std::ffi::CStr::from_ptr(result.error_message) };
                let string = c_str.to_string_lossy().into_owned();
                crate::gitomator_free_error(&mut result as *mut _);
                string
            };
            
            return Err(GitError::new_err(error_msg));
        }
        
        Ok(())
    }
    
    fn list_branches(&self) -> PyResult<Vec<String>> {
        let result = match list_branches(self.inner) {
            Ok((branches, _)) => branches,
            Err(e) => return Err(GitError::new_err(unsafe {
                std::ffi::CStr::from_ptr(e.error_message)
                    .to_string_lossy()
                    .into_owned()
            })),
        };
        Ok(result)
    }
    
    fn get_hash(&self, short: bool) -> PyResult<String> {
        let result = match get_hash(self.inner, short) {
            Ok(hash) => hash,
            Err(e) => return Err(GitError::new_err(unsafe {
                std::ffi::CStr::from_ptr(e.error_message)
                    .to_string_lossy()
                    .into_owned()
            })),
        };
        Ok(result)
    }

    #[pyo3(signature = (command, args, timeout=None, operation=None))]
    fn run_command(&self, command: &str, args: Vec<String>, timeout: Option<f64>, operation: Option<String>) -> PyResult<String>
    {
        let repo = unsafe { &(*self.inner).inner };
        let mut cmd = GitCommand::new(repo.location())
            .arg(command);
            
        for arg in args {
            cmd = cmd.arg(arg);
        }
        
        if let Some(op) = operation {
            cmd = cmd.operation(op);
        }
        
        if let Some(t) = timeout {
            cmd = cmd.timeout(Duration::from_secs_f64(t));
        }
        
        match cmd.run() {
            Ok(result) => {
                // If there's stderr output, include it in the result
                if let Some(stderr) = result.stderr() {
                    if !stderr.trim().is_empty() {
                        return Ok(format!("{}\nstderr: {}", result.raw_output(), stderr));
                    }
                }
                Ok(result.raw_output().to_string())
            }
            Err(e) => Err(git_error_to_py_err(e)),
        }
    }

    #[pyo3(signature = (command, args, timeout=None, operation=None))]
    fn run_command_with_details(&self, py: Python<'_>, command: &str, args: Vec<String>, timeout: Option<f64>, operation: Option<String>) -> PyResult<PyObject>
    {
        let repo = unsafe { &(*self.inner).inner };
        let mut cmd = GitCommand::new(repo.location())
            .arg(command);
            
        for arg in args {
            cmd = cmd.arg(arg);
        }
        
        if let Some(op) = operation {
            cmd = cmd.operation(op);
        }
        
        if let Some(t) = timeout {
            cmd = cmd.timeout(Duration::from_secs_f64(t));
        }
        
        match cmd.run() {
            Ok(result) => {
                let dict = PyDict::new(py);
                dict.set_item("stdout", result.raw_output())?;
                if let Some(stderr) = result.stderr() {
                    dict.set_item("stderr", stderr)?;
                }
                if let Some(op) = result.operation_name() {
                    dict.set_item("operation", op)?;
                }
                dict.set_item("args", result.args().iter().map(|arg| arg.to_string_lossy().into_owned()).collect::<Vec<_>>())?;
                
                Ok(dict.into())
            }
            Err(e) => Err(git_error_to_py_err(e)),
        }
    }
}

// Create the Python module
#[pymodule]
fn _gitomator(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<PyRepository>()?;
    m.add("GitError", m.py().get_type::<GitError>())?;
    m.add("GitExecutionError", m.py().get_type::<GitExecutionError>())?;
    m.add("GitTimeoutError", m.py().get_type::<GitTimeoutError>())?;
    m.add("GitInvalidUrlError", m.py().get_type::<GitInvalidUrlError>())?;
    m.add("GitInvalidRefNameError", m.py().get_type::<GitInvalidRefNameError>())?;
    m.add("GitInvalidCommitHashError", m.py().get_type::<GitInvalidCommitHashError>())?;
    m.add("GitProviderError", m.py().get_type::<GitProviderError>())?;
    m.add("GitIOError", m.py().get_type::<GitIOError>())?;
    Ok(())
} 