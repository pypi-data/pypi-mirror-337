use std::ffi::c_char;

// Python bindings
mod python;

// Wrapper layer between core and FFI
mod wrappers;
pub use wrappers::{GitRepository, GitResultCode};

// Free error message
#[no_mangle]
pub extern "C" fn gitomator_free_error(result: *mut GitResultCode) {
    wrappers::free_error(result);
}

// Initialize a new repository
#[no_mangle]
pub extern "C" fn gitomator_init(path: *const c_char, repo_out: *mut *mut GitRepository) -> GitResultCode {
    if path.is_null() || repo_out.is_null() {
        return wrappers::GitResultCode::error("Null pointer provided");
    }

    match wrappers::init_repository(path) {
        Ok(repo) => {
            unsafe {
                *repo_out = repo;
            }
            wrappers::GitResultCode::success()
        }
        Err(code) => code,
    }
}

// Open an existing repository
#[no_mangle]
pub extern "C" fn gitomator_open(path: *const c_char, repo_out: *mut *mut GitRepository) -> GitResultCode {
    if path.is_null() || repo_out.is_null() {
        return wrappers::GitResultCode::error("Null pointer provided");
    }

    match wrappers::open_repository(path) {
        Ok(repo) => {
            unsafe {
                *repo_out = repo;
            }
            wrappers::GitResultCode::success()
        }
        Err(code) => code,
    }
}

// Clone a repository
#[no_mangle]
pub extern "C" fn gitomator_clone(url: *const c_char, path: *const c_char, repo_out: *mut *mut GitRepository) -> GitResultCode {
    if url.is_null() || path.is_null() || repo_out.is_null() {
        return wrappers::GitResultCode::error("Null pointer provided");
    }

    match wrappers::clone_repository(url, path) {
        Ok(repo) => {
            unsafe {
                *repo_out = repo;
            }
            wrappers::GitResultCode::success()
        }
        Err(code) => code,
    }
}

// Add files to the repository
#[no_mangle]
pub extern "C" fn gitomator_add(repo: *mut GitRepository, paths: *const *const c_char, count: usize) -> GitResultCode {
    wrappers::add_files(repo, paths, count)
}

// Commit all changes
#[no_mangle]
pub extern "C" fn gitomator_commit_all(repo: *mut GitRepository, message: *const c_char) -> GitResultCode {
    wrappers::commit_all(repo, message)
}

// Create a branch
#[no_mangle]
pub extern "C" fn gitomator_create_branch(repo: *mut GitRepository, branch_name: *const c_char) -> GitResultCode {
    wrappers::create_branch(repo, branch_name)
}

// List branches
#[no_mangle]
pub extern "C" fn gitomator_list_branches(
    repo: *mut GitRepository, 
    branches_out: *mut *mut *mut c_char,
    count_out: *mut usize
) -> GitResultCode {
    if repo.is_null() || branches_out.is_null() || count_out.is_null() {
        return wrappers::GitResultCode::error("Null pointer provided");
    }

    match wrappers::list_branches(repo) {
        Ok((branches, _)) => {
            let (c_array, count) = wrappers::branches_to_c_array(branches);
            
            if count > 0 && c_array.is_null() {
                return wrappers::GitResultCode::error("Failed to allocate memory for branch list");
            }
            
            unsafe {
                *branches_out = c_array;
                *count_out = count;
            }
            
            wrappers::GitResultCode::success()
        },
        Err(code) => code,
    }
}

// Free a list of branches
#[no_mangle]
pub extern "C" fn gitomator_free_branch_list(branches: *mut *mut c_char, count: usize) {
    wrappers::free_branch_list(branches, count);
}

// Get current commit hash
#[no_mangle]
pub extern "C" fn gitomator_get_hash(
    repo: *mut GitRepository,
    short: bool,
    hash_out: *mut *mut c_char
) -> GitResultCode {
    if repo.is_null() || hash_out.is_null() {
        return wrappers::GitResultCode::error("Null pointer provided");
    }

    match wrappers::get_hash(repo, short) {
        Ok(hash) => {
            let c_str = wrappers::string_to_c_ptr(hash);
            if c_str.is_null() {
                return wrappers::GitResultCode::error("Failed to convert hash to C string");
            }
            
            unsafe { *hash_out = c_str; }
            wrappers::GitResultCode::success()
        },
        Err(code) => code,
    }
}

// Free a string
#[no_mangle]
pub extern "C" fn gitomator_free_string(string: *mut c_char) {
    wrappers::free_string(string);
}

// Free repository
#[no_mangle]
pub extern "C" fn gitomator_free_repository(repo: *mut GitRepository) {
    wrappers::free_repository(repo);
}
