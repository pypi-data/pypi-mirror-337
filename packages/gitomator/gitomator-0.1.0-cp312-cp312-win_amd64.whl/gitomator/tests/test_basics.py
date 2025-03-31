import os
import tempfile
import pytest
from gitomator import Repository, GitError

def test_init_repository():
    """Test initializing a new git repository"""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo = Repository.init(temp_dir)
        assert os.path.exists(os.path.join(temp_dir, ".git"))
        
def test_add_and_commit():
    """Test adding and committing files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo = Repository.init(temp_dir)
        
        # Create a test file
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Test content")
            
        # Add and commit the file
        repo.add([os.path.basename(test_file)])
        repo.commit_all("Initial commit")
        
        # Verify commit hash is returned
        hash = repo.get_hash()
        assert isinstance(hash, str)
        assert len(hash) > 0
        
def test_branch_operations():
    """Test creating and listing branches"""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo = Repository.init(temp_dir)
        
        # Create a test file and commit it
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Test content")
            
        repo.add([os.path.basename(test_file)])
        repo.commit_all("Initial commit")
        
        # Create a new branch
        branch_name = "test-branch"
        repo.create_branch(branch_name)
        
        # List branches
        branches = repo.list_branches()
        assert isinstance(branches, list)
        assert branch_name in branches
        
def test_error_handling():
    """Test error handling for invalid operations"""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo = Repository.init(temp_dir)
        
        # Try to add a non-existent file
        with pytest.raises(GitError):
            repo.add(["non-existent-file.txt"])
            
if __name__ == "__main__":
    test_init_repository()
    test_add_and_commit()
    test_branch_operations()
    test_error_handling()
    print("All tests passed!") 