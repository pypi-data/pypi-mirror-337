import os
import shutil
from git import Repo
from pathlib import Path
from urllib.parse import urlparse

def is_github_url(source):
    """Check if the source is a GitHub URL."""
    try:
        result = urlparse(source)
        return all([result.scheme in ['http', 'https', 'git', 'ssh'], 'github.com' in result.netloc]) or ('github.com' in source and '@' in source)
    except:
        return False

def extract_repo_name(source):
    """Extract the repository name from GitHub URL or local path."""
    if is_github_url(source):
        return source.split("/")[-1].replace(".git", "")
    return Path(source).name

def validate_local_path(path):
    """Validate that the local path exists and is accessible."""
    path = Path(path)
    if not path.exists():
        raise ValueError(f"Path does not exist: {path}")
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    if not os.access(path, os.R_OK):
        raise ValueError(f"No read permission for path: {path}")
    return path

def clone_repo(repo_url, destination_folder):
    """Clone the GitHub repository to the specified destination folder."""
    try:
        Repo.clone_from(repo_url, destination_folder, depth=1)
        print(f"Cloned repository: {repo_url}")
    except Exception as e:
        print(f"Error during clone: {e}")
        exit(1)

def filter_documentation_files(repo_path):
    """Filter documentation files in the repository or local folder."""
    doc_extensions = {".md", ".mdx", ".rst", ".txt"}
    doc_files = []
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.lower().startswith("readme") or Path(file).suffix.lower() in doc_extensions:
                doc_files.append(os.path.join(root, file))
    return doc_files

def copy_files(files, output_folder, repo_root):
    """Copy filtered documentation files to the output folder, preserving directory structure."""
    for file in files:
        relative_path = os.path.relpath(file, repo_root)
        dest_file_path = os.path.join(output_folder, relative_path)
        dest_dir = os.path.dirname(dest_file_path)
        
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        try:
            shutil.copy(file, dest_file_path)
            print(f"Copied file: {relative_path}")
        except Exception as e:
            print(f"Error copying file {file}: {e}")

def delete_repo(repo_folder):
    """Delete the cloned repository folder."""
    try:
        shutil.rmtree(repo_folder)
        print(f"Deleted repository folder: {repo_folder}")
    except Exception as e:
        print(f"Error deleting repository folder: {e}")

def main(source, output_folder=None):
    """Main function to extract documentation files from GitHub repository or local folder."""
    repo_name = extract_repo_name(source)
    output_folder = output_folder or f"{repo_name}-docs"
    
    if is_github_url(source):
        # Handle GitHub repository
        destination_folder = repo_name
        clone_repo(source, destination_folder)
        repo_root = destination_folder
    else:
        # Handle local folder
        repo_root = validate_local_path(source)
        print(f"Using local folder: {repo_root}")
    
    # Filter documentation files
    doc_files = filter_documentation_files(repo_root)
    
    # Copy documentation files to the output folder
    copy_files(doc_files, output_folder, repo_root)
    
    # Clean up if it was a cloned repository
    if is_github_url(source):
        delete_repo(destination_folder)
    
    print(f"Documentation extraction completed. Files saved to: {output_folder}")