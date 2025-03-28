import re

def validate_github_url(url):
    """Validate that the URL is a valid GitHub repository URL."""
    github_regex = re.compile(r"^https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(\.git)?$")
    if not github_regex.match(url):
        raise ValueError(f"Invalid GitHub URL: {url}")
    return True