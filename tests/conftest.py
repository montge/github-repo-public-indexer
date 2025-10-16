"""Pytest configuration and shared fixtures."""

import pytest
import json
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import Mock, MagicMock


@pytest.fixture
def sample_repo_data():
    """Sample repository data for testing."""
    return {
        "basic_info": {
            "name": "test-repo",
            "full_name": "test-org/test-repo",
            "description": "A test repository",
            "url": "https://api.github.com/repos/test-org/test-repo",
            "html_url": "https://github.com/test-org/test-repo",
            "homepage": "https://test-repo.example.com",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-12-31T23:59:59Z",
            "pushed_at": "2023-12-31T20:00:00Z",
            "size": 1024,
            "default_branch": "main",
            "visibility": "public",
        },
        "status": {
            "is_archived": False,
            "is_fork": False,
            "is_template": False,
            "is_disabled": False,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True,
            "has_pages": False,
            "has_downloads": True,
            "has_discussions": False,
        },
        "activity": {
            "stars": 42,
            "watchers": 42,
            "forks": 5,
            "open_issues": 3,
            "open_pull_requests": 1,
            "last_commit_date": "2023-12-31T20:00:00Z",
            "commit_count_30d": 15,
            "contributor_count": 3,
        },
        "languages": {
            "primary": "Python",
            "breakdown": {"Python": 85.5, "Shell": 10.2, "Dockerfile": 4.3},
        },
        "license": {
            "key": "apache-2.0",
            "name": "Apache License 2.0",
            "spdx_id": "Apache-2.0",
            "url": "https://api.github.com/licenses/apache-2.0",
        },
        "topics": ["python", "automation", "github-api"],
        "readme_preview": "# Test Repository\n\nThis is a test repository for testing purposes.",
        "ownership": {
            "owner": {
                "login": "test-org",
                "type": "Organization",
                "url": "https://github.com/test-org",
            },
            "top_contributors": [
                {
                    "login": "contributor1",
                    "contributions": 50,
                    "profile_url": "https://github.com/contributor1",
                }
            ],
            "teams": [],
            "codeowners": {"exists": False, "owners": []},
        },
    }


@pytest.fixture
def sample_metadata():
    """Sample metadata for JSON output."""
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "organization": "test-org",
        "total_repositories": 1,
        "tool_version": "1.0.0",
        "github_api_version": "2022-11-28",
    }


@pytest.fixture
def mock_github_repo():
    """Mock GitHub repository object."""
    import base64

    repo = MagicMock()
    repo.name = "test-repo"
    repo.full_name = "test-org/test-repo"
    repo.description = "Test repository"
    repo.url = "https://api.github.com/repos/test-org/test-repo"
    repo.html_url = "https://github.com/test-org/test-repo"
    repo.homepage = "https://example.com"
    repo.created_at = datetime(2023, 1, 1, tzinfo=timezone.utc)
    repo.updated_at = datetime(2023, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    repo.pushed_at = datetime(2023, 12, 31, 20, 0, 0, tzinfo=timezone.utc)
    repo.size = 1024
    repo.default_branch = "main"
    repo.private = False
    repo.archived = False
    repo.fork = False
    repo.is_template = False
    repo.disabled = False
    repo.has_issues = True
    repo.has_projects = True
    repo.has_wiki = True
    repo.has_pages = False
    repo.has_downloads = True
    repo.has_discussions = False
    repo.stargazers_count = 100
    repo.watchers_count = 50
    repo.forks_count = 25
    repo.open_issues_count = 5

    # Mock owner
    owner = MagicMock()
    owner.login = "test-org"
    owner.type = "Organization"
    owner.html_url = "https://github.com/test-org"
    repo.owner = owner

    # Mock languages
    repo.get_languages.return_value = {"Python": 8000, "JavaScript": 2000}

    # Mock license
    license_obj = MagicMock()
    license_obj.key = "mit"
    license_obj.name = "MIT License"
    license_obj.spdx_id = "MIT"
    license_obj.url = "https://api.github.com/licenses/mit"
    license_info = MagicMock()
    license_info.license = license_obj
    repo.get_license.return_value = license_info

    # Mock topics
    repo.get_topics.return_value = ["python", "testing", "automation"]

    # Mock README
    readme = MagicMock()
    readme_content = "# Test Repo\n\nThis is a test repository."
    readme.content = base64.b64encode(readme_content.encode("utf-8")).decode("utf-8")
    repo.get_readme.return_value = readme

    # Mock contributors
    contributor1 = MagicMock()
    contributor1.login = "user1"
    contributor1.contributions = 100
    contributor1.html_url = "https://github.com/user1"

    contributor2 = MagicMock()
    contributor2.login = "user2"
    contributor2.contributions = 50
    contributor2.html_url = "https://github.com/user2"

    mock_contributors = MagicMock()
    mock_contributors.__iter__.return_value = [contributor1, contributor2]
    mock_contributors.totalCount = 2
    repo.get_contributors.return_value = mock_contributors

    # Mock commits
    mock_commits = MagicMock()
    mock_commits.totalCount = 10
    repo.get_commits.return_value = mock_commits

    # Mock pull requests
    mock_pulls = MagicMock()
    mock_pulls.totalCount = 2
    repo.get_pulls.return_value = mock_pulls

    # Mock teams
    repo.get_teams.return_value = []

    # Mock get_contents (for CODEOWNERS)
    from github import GithubException

    repo.get_contents.side_effect = GithubException(404, "Not found", None)

    return repo


@pytest.fixture
def mock_github_client(mock_github_repo):
    """Mock GitHub client."""
    client = MagicMock()

    # Mock rate limit
    rate_limit = MagicMock()
    rate_limit.core.remaining = 5000
    rate_limit.core.limit = 5000
    rate_limit.core.reset = datetime.now(timezone.utc)
    client.get_rate_limit.return_value = rate_limit

    # Mock organization
    org = MagicMock()
    org.login = "test-org"
    org.name = "Test Organization"
    org.get_repos.return_value = [mock_github_repo]
    client.get_organization.return_value = org

    return client


@pytest.fixture
def temp_json_file(tmp_path, sample_repo_data, sample_metadata):
    """Create a temporary JSON file for testing."""
    json_file = tmp_path / "test_repositories.json"
    data = {"metadata": sample_metadata, "repositories": [sample_repo_data]}
    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)
    return json_file


@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"
