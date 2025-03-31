# Gitomator

A Rust library for Git operations with Python bindings.

## Features

- Type-safe wrappers for Git operations
- Fluent command-building API
- Support for different Git providers (GitHub, GitLab)
- Comprehensive error handling
- Async support (optional)
- Python bindings

## Project Structure

```
.
├── Cargo.toml                 # Root workspace configuration
├── README.md                  # This file
├── core                       # Core Rust library
│   ├── Cargo.toml             # Core library configuration
│   └── src                    # Core library source code
│       ├── async_impl         # Asynchronous implementation
│       │   └── mod.rs
│       ├── error.rs           # Error types
│       ├── lib.rs             # Library entry point
│       ├── providers          # Git provider implementations
│       │   ├── github.rs
│       │   ├── gitlab.rs
│       │   └── mod.rs
│       ├── repository.rs      # Repository implementation
│       ├── types.rs           # Type definitions
│       └── utils.rs           # Utility functions
├── ffi                        # FFI bindings for Python
│   ├── Cargo.toml             # FFI configuration
│   └── src
│       ├── errors.rs          # FFI error handling
│       ├── lib.rs             # FFI entry point
│       └── wrappers.rs        # FFI wrapper functions
├── gitomator                  # Python package
│   └── gitomator
│       └── __init__.py        # Python module entry point
└── pyproject.toml             # Python project configuration
```

## Usage

### Rust

```rust
use gitomator_core::{self, BranchName, GitUrl, Repository};
use std::str::FromStr;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize a new repository
    let repo = gitomator_core::init("./my_repo")?;
    
    // Create a file and commit it
    // ...
    repo.add(vec!["README.md"])?;
    repo.commit_all("Initial commit")?;
    
    // Create a new branch
    let branch_name = BranchName::from_str("feature-branch")?;
    repo.create_local_branch(&branch_name)?;
    
    // List branches
    let branches = repo.list_branches()?;
    for branch in branches {
        println!("Branch: {}", branch);
    }
    
    Ok(())
}
```

### Python

```python
from gitomator import Repository, BranchName

# Initialize a new repository
repo = Repository.init("./my_repo")

# Create a file and commit it
# ...
repo.add(["README.md"])
repo.commit_all("Initial commit")

# Create a new branch
branch_name = BranchName("feature-branch")
repo.create_local_branch(branch_name)

# List branches
branches = repo.list_branches()
for branch in branches:
    print(f"Branch: {branch}")
```

## Building and Testing

### Rust Library

```bash
# Build the library
cargo build

# Run tests
cargo test

# Run the example
cargo run --example basic_usage
```

### Python Package

```bash
# Build the Python package
maturin develop

# Test the Python package
python -c "import gitomator; print(gitomator.__version__)"
```

## Features

- `serde`: Enables serde serialization/deserialization
- `async`: Enables async support with tokio

## License

MIT OR Apache-2.0