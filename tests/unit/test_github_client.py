"""Unit tests for src/github_client.py"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from github import GithubException, RateLimitExceededException
from src.github_client import GitHubClient


@pytest.mark.unit
class TestGitHubClient:
    """Test cases for GitHubClient class."""

    @patch("src.github_client.Github")
    def test_init_without_base_url(self, mock_github_class):
        """Test initialization without custom base URL."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Mock user
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        # Mock rate limit
        mock_rate_limit = MagicMock()
        mock_rate_limit.core.remaining = 5000
        mock_rate_limit.core.limit = 5000
        mock_rate_limit.core.reset = datetime.now(timezone.utc)
        mock_client.get_rate_limit.return_value = mock_rate_limit

        client = GitHubClient(token="test_token")

        mock_github_class.assert_called_once_with("test_token")
        assert client.base_url is None

    @patch("src.github_client.Github")
    def test_init_with_base_url(self, mock_github_class):
        """Test initialization with custom base URL."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Mock user
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        # Mock rate limit
        mock_rate_limit = MagicMock()
        mock_rate_limit.core.remaining = 5000
        mock_rate_limit.core.limit = 5000
        mock_rate_limit.core.reset = datetime.now(timezone.utc)
        mock_client.get_rate_limit.return_value = mock_rate_limit

        base_url = "https://github.example.com/api/v3"
        client = GitHubClient(token="test_token", base_url=base_url)

        mock_github_class.assert_called_once_with(base_url=base_url, login_or_token="test_token")
        assert client.base_url == base_url

    @patch("src.github_client.Github")
    def test_get_organization_success(self, mock_github_class):
        """Test successful organization retrieval."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Setup mocks
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        mock_rate_limit = MagicMock()
        mock_rate_limit.core.remaining = 5000
        mock_rate_limit.core.limit = 5000
        mock_rate_limit.core.reset = datetime.now(timezone.utc)
        mock_client.get_rate_limit.return_value = mock_rate_limit

        mock_org = MagicMock()
        mock_org.login = "test-org"
        mock_org.name = "Test Organization"
        mock_client.get_organization.return_value = mock_org

        client = GitHubClient(token="test_token")
        org = client.get_organization("test-org")

        assert org.login == "test-org"
        mock_client.get_organization.assert_called_once_with("test-org")

    @patch("src.github_client.Github")
    def test_get_organization_not_found(self, mock_github_class):
        """Test organization not found error."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Setup mocks
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        mock_rate_limit = MagicMock()
        mock_rate_limit.core.remaining = 5000
        mock_rate_limit.core.limit = 5000
        mock_rate_limit.core.reset = datetime.now(timezone.utc)
        mock_client.get_rate_limit.return_value = mock_rate_limit

        # Mock 404 error
        mock_client.get_organization.side_effect = GithubException(
            status=404, data={"message": "Not Found"}
        )

        client = GitHubClient(token="test_token")

        with pytest.raises(GithubException):
            client.get_organization("nonexistent-org")

    @patch("src.github_client.Github")
    def test_get_all_repositories_success(self, mock_github_class):
        """Test successful repository fetching."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Setup mocks
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        mock_rate_limit = MagicMock()
        mock_rate_limit.core.remaining = 5000
        mock_rate_limit.core.limit = 5000
        mock_rate_limit.core.reset = datetime.now(timezone.utc)
        mock_client.get_rate_limit.return_value = mock_rate_limit

        # Mock repository
        mock_repo = MagicMock()
        mock_repo.name = "test-repo"
        mock_repo.full_name = "test-org/test-repo"
        mock_repo.fork = False
        mock_repo.archived = False

        # Mock organization
        mock_org = MagicMock()
        mock_org.login = "test-org"
        mock_org.name = "Test Organization"
        mock_org.get_repos.return_value = [mock_repo]
        mock_client.get_organization.return_value = mock_org

        client = GitHubClient(token="test_token")
        repos = client.get_all_repositories("test-org")

        assert len(repos) == 1
        assert repos[0].name == "test-repo"

    @patch("src.github_client.Github")
    def test_get_all_repositories_filter_forks(self, mock_github_class):
        """Test filtering out forks."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Setup mocks
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        mock_rate_limit = MagicMock()
        mock_rate_limit.core.remaining = 5000
        mock_rate_limit.core.limit = 5000
        mock_rate_limit.core.reset = datetime.now(timezone.utc)
        mock_client.get_rate_limit.return_value = mock_rate_limit

        # Mock repositories
        mock_repo1 = MagicMock()
        mock_repo1.name = "original-repo"
        mock_repo1.fork = False
        mock_repo1.archived = False

        mock_repo2 = MagicMock()
        mock_repo2.name = "forked-repo"
        mock_repo2.fork = True
        mock_repo2.archived = False

        # Mock organization
        mock_org = MagicMock()
        mock_org.login = "test-org"
        mock_org.get_repos.return_value = [mock_repo1, mock_repo2]
        mock_client.get_organization.return_value = mock_org

        client = GitHubClient(token="test_token")
        repos = client.get_all_repositories("test-org", include_forks=False)

        assert len(repos) == 1
        assert repos[0].name == "original-repo"

    @patch("src.github_client.Github")
    def test_get_all_repositories_filter_archived(self, mock_github_class):
        """Test filtering out archived repositories."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Setup mocks
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        mock_rate_limit = MagicMock()
        mock_rate_limit.core.remaining = 5000
        mock_rate_limit.core.limit = 5000
        mock_rate_limit.core.reset = datetime.now(timezone.utc)
        mock_client.get_rate_limit.return_value = mock_rate_limit

        # Mock repositories
        mock_repo1 = MagicMock()
        mock_repo1.name = "active-repo"
        mock_repo1.fork = False
        mock_repo1.archived = False

        mock_repo2 = MagicMock()
        mock_repo2.name = "archived-repo"
        mock_repo2.fork = False
        mock_repo2.archived = True

        # Mock organization
        mock_org = MagicMock()
        mock_org.login = "test-org"
        mock_org.get_repos.return_value = [mock_repo1, mock_repo2]
        mock_client.get_organization.return_value = mock_org

        client = GitHubClient(token="test_token")
        repos = client.get_all_repositories("test-org", include_archived=False)

        assert len(repos) == 1
        assert repos[0].name == "active-repo"

    @patch("src.github_client.Github")
    @patch("src.github_client.time.sleep")
    def test_rate_limit_handling(self, mock_sleep, mock_github_class):
        """Test automatic rate limit handling."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Setup mocks
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        # First call: low rate limit
        mock_rate_limit_low = MagicMock()
        mock_rate_limit_low.core.remaining = 0
        mock_rate_limit_low.core.limit = 5000
        mock_rate_limit_low.core.reset = datetime.now(timezone.utc) + timedelta(seconds=60)

        # Second call: reset rate limit
        mock_rate_limit_reset = MagicMock()
        mock_rate_limit_reset.core.remaining = 5000
        mock_rate_limit_reset.core.limit = 5000
        mock_rate_limit_reset.core.reset = datetime.now(timezone.utc)

        mock_client.get_rate_limit.side_effect = [
            mock_rate_limit_low,  # Initial check
            mock_rate_limit_low,  # After RateLimitExceededException
            mock_rate_limit_reset,  # After sleep
        ]

        # Mock organization to raise RateLimitExceededException
        mock_org = MagicMock()
        mock_org.login = "test-org"
        mock_org.get_repos.side_effect = [
            RateLimitExceededException(status=403, data={"message": "API rate limit exceeded"}),
            [],  # Success on retry
        ]
        mock_client.get_organization.return_value = mock_org

        client = GitHubClient(token="test_token")
        repos = client.get_all_repositories("test-org")

        # Verify sleep was called
        assert mock_sleep.called
        assert len(repos) == 0

    @patch("src.github_client.Github")
    def test_init_authentication_failure(self, mock_github_class):
        """Test authentication failure during initialization."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Mock authentication failure
        mock_client.get_user.side_effect = GithubException(
            status=401, data={"message": "Bad credentials"}
        )

        with pytest.raises(GithubException):
            GitHubClient(token="invalid_token")

    @patch("src.github_client.Github")
    def test_get_all_repositories_github_exception(self, mock_github_class):
        """Test GithubException when fetching repositories."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Setup mocks
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        mock_rate_limit = MagicMock()
        mock_rate_limit.core.remaining = 5000
        mock_rate_limit.core.limit = 5000
        mock_rate_limit.core.reset = datetime.now(timezone.utc)
        mock_client.get_rate_limit.return_value = mock_rate_limit

        # Mock organization that raises exception when getting repos
        mock_org = MagicMock()
        mock_org.login = "test-org"
        mock_org.get_repos.side_effect = GithubException(
            status=500, data={"message": "Internal Server Error"}
        )
        mock_client.get_organization.return_value = mock_org

        client = GitHubClient(token="test_token")

        with pytest.raises(GithubException):
            client.get_all_repositories("test-org")

    @patch("src.github_client.Github")
    def test_check_rate_limit_low_remaining(self, mock_github_class):
        """Test check_rate_limit with low remaining calls."""
        mock_client = MagicMock()
        mock_github_class.return_value = mock_client

        # Setup mocks
        mock_user = MagicMock()
        mock_user.login = "test-user"
        mock_client.get_user.return_value = mock_user

        # First call for init, second for check_rate_limit
        mock_rate_limit_init = MagicMock()
        mock_rate_limit_init.core.remaining = 5000
        mock_rate_limit_init.core.limit = 5000
        mock_rate_limit_init.core.reset = datetime.now(timezone.utc)

        mock_rate_limit_low = MagicMock()
        mock_rate_limit_low.core.remaining = 50
        mock_rate_limit_low.core.limit = 5000
        mock_rate_limit_low.core.reset = datetime.now(timezone.utc)

        mock_client.get_rate_limit.side_effect = [mock_rate_limit_init, mock_rate_limit_low]

        client = GitHubClient(token="test_token")
        # This should log a warning
        client.check_rate_limit()
