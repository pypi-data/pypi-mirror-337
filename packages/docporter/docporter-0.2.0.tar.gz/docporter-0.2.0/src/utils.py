import re

def validate_github_url(url):
    """Validate that the URL is a valid GitHub repository URL."""
    github_https_regex = re.compile(r"^https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(\.git)?$")
    github_ssh_regex = re.compile(r"^git@github\.com:[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(\.git)?$")

    if not (github_https_regex.match(url) or github_ssh_regex.match(url)):
        raise ValueError(f"Invalid GitHub URL: {url}")
    return True