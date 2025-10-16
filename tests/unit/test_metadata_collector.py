"""Unit tests for src/metadata_collector.py"""

import pytest
import base64
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from github import GithubException
from src.metadata_collector import MetadataCollector


@pytest.mark.unit
class TestMetadataCollector:
    """Test cases for MetadataCollector class."""

    def test_init_default_max_contributors(self):
        """Test MetadataCollector initialization with default max_contributors."""
        collector = MetadataCollector()
        assert collector.max_contributors == 5

    def test_init_custom_max_contributors(self):
        """Test MetadataCollector initialization with custom max_contributors."""
        collector = MetadataCollector(max_contributors=10)
        assert collector.max_contributors == 10

    def test_collect_basic_info(self, mock_github_repo):
        """Test _collect_basic_info collects all basic fields."""
        collector = MetadataCollector()
        basic_info = collector._collect_basic_info(mock_github_repo)

        assert basic_info["name"] == "test-repo"
        assert basic_info["full_name"] == "test-org/test-repo"
        assert basic_info["description"] == "Test repository"
        assert basic_info["url"] == "https://api.github.com/repos/test-org/test-repo"
        assert basic_info["html_url"] == "https://github.com/test-org/test-repo"
        assert basic_info["homepage"] == "https://example.com"
        assert basic_info["size"] == 1024
        assert basic_info["default_branch"] == "main"
        assert basic_info["visibility"] == "public"

    def test_collect_basic_info_private_repo(self):
        """Test _collect_basic_info with private repository."""
        repo = MagicMock()
        repo.name = "private-repo"
        repo.private = True
        repo.created_at = None
        repo.updated_at = None
        repo.pushed_at = None

        collector = MetadataCollector()
        basic_info = collector._collect_basic_info(repo)

        assert basic_info["visibility"] == "private"
        assert basic_info["created_at"] is None
        assert basic_info["updated_at"] is None
        assert basic_info["pushed_at"] is None

    def test_collect_status(self, mock_github_repo):
        """Test _collect_status collects all status flags."""
        collector = MetadataCollector()
        status = collector._collect_status(mock_github_repo)

        assert status["is_archived"] is False
        assert status["is_fork"] is False
        assert status["is_template"] is False
        assert status["is_disabled"] is False
        assert status["has_issues"] is True
        assert status["has_projects"] is True
        assert status["has_wiki"] is True
        assert status["has_pages"] is False
        assert status["has_downloads"] is True

    def test_collect_status_archived_fork(self):
        """Test _collect_status with archived fork repository."""
        repo = MagicMock()
        repo.archived = True
        repo.fork = True
        repo.is_template = True
        repo.disabled = False
        repo.has_issues = False
        repo.has_projects = False
        repo.has_wiki = False
        repo.has_pages = True
        repo.has_downloads = False
        repo.has_discussions = True

        collector = MetadataCollector()
        status = collector._collect_status(repo)

        assert status["is_archived"] is True
        assert status["is_fork"] is True
        assert status["is_template"] is True
        assert status["has_discussions"] is True

    def test_collect_activity(self, mock_github_repo):
        """Test _collect_activity collects all activity metrics."""
        collector = MetadataCollector()
        activity = collector._collect_activity(mock_github_repo)

        assert activity["stars"] == 100
        assert activity["watchers"] == 50
        assert activity["forks"] == 25
        assert activity["open_issues"] == 5
        assert "open_pull_requests" in activity
        assert "last_commit_date" in activity
        assert "commit_count_30d" in activity
        assert "contributor_count" in activity

    def test_collect_activity_with_github_exception(self):
        """Test _collect_activity handles GithubException gracefully."""
        repo = MagicMock()
        repo.stargazers_count = 100
        repo.watchers_count = 50
        repo.forks_count = 25
        repo.open_issues_count = 5
        repo.pushed_at = datetime.now(timezone.utc)
        repo.get_commits.side_effect = GithubException(404, "Not found", None)
        repo.get_contributors.side_effect = GithubException(404, "Not found", None)
        repo.get_pulls.side_effect = GithubException(404, "Not found", None)

        collector = MetadataCollector()
        activity = collector._collect_activity(repo)

        assert activity["stars"] == 100
        assert activity["open_pull_requests"] == 0
        assert activity["commit_count_30d"] == 0
        assert activity["contributor_count"] == 0

    def test_collect_languages(self, mock_github_repo):
        """Test _collect_languages calculates breakdown correctly."""
        collector = MetadataCollector()
        languages = collector._collect_languages(mock_github_repo)

        assert languages["primary"] == "Python"
        assert "Python" in languages["breakdown"]
        assert "JavaScript" in languages["breakdown"]
        assert languages["breakdown"]["Python"] == 80.0
        assert languages["breakdown"]["JavaScript"] == 20.0

    def test_collect_languages_empty(self):
        """Test _collect_languages with no languages."""
        repo = MagicMock()
        repo.full_name = "test-org/empty-repo"
        repo.get_languages.return_value = {}

        collector = MetadataCollector()
        languages = collector._collect_languages(repo)

        assert languages["primary"] is None
        assert languages["breakdown"] == {}

    def test_collect_languages_with_exception(self):
        """Test _collect_languages handles GithubException."""
        repo = MagicMock()
        repo.full_name = "test-org/test-repo"
        repo.get_languages.side_effect = GithubException(404, "Not found", None)

        collector = MetadataCollector()
        languages = collector._collect_languages(repo)

        assert languages["primary"] is None
        assert languages["breakdown"] == {}

    def test_collect_license(self, mock_github_repo):
        """Test _collect_license collects license information."""
        collector = MetadataCollector()
        license_info = collector._collect_license(mock_github_repo)

        assert license_info["key"] == "mit"
        assert license_info["name"] == "MIT License"
        assert license_info["spdx_id"] == "MIT"
        assert "url" in license_info

    def test_collect_license_none(self):
        """Test _collect_license when no license exists."""
        repo = MagicMock()
        repo.full_name = "test-org/no-license"
        repo.get_license.side_effect = GithubException(404, "Not found", None)

        collector = MetadataCollector()
        license_info = collector._collect_license(repo)

        assert license_info["key"] is None
        assert license_info["name"] is None
        assert license_info["spdx_id"] is None
        assert license_info["url"] is None

    def test_collect_topics(self, mock_github_repo):
        """Test _collect_topics collects repository topics."""
        collector = MetadataCollector()
        topics = collector._collect_topics(mock_github_repo)

        assert "python" in topics
        assert "testing" in topics
        assert "automation" in topics
        assert len(topics) == 3

    def test_collect_topics_with_exception(self):
        """Test _collect_topics handles GithubException."""
        repo = MagicMock()
        repo.full_name = "test-org/test-repo"
        repo.get_topics.side_effect = GithubException(404, "Not found", None)

        collector = MetadataCollector()
        topics = collector._collect_topics(repo)

        assert topics == []

    def test_collect_readme_preview(self, mock_github_repo):
        """Test _collect_readme_preview extracts README content."""
        collector = MetadataCollector()
        preview = collector._collect_readme_preview(mock_github_repo)

        assert preview is not None
        assert "# Test Repo" in preview
        assert len(preview) <= 503  # 500 + "..."

    def test_collect_readme_preview_long_content(self):
        """Test _collect_readme_preview truncates long README."""
        repo = MagicMock()
        repo.full_name = "test-org/test-repo"

        long_content = "A" * 1000
        readme = MagicMock()
        readme.content = base64.b64encode(long_content.encode("utf-8")).decode("utf-8")
        repo.get_readme.return_value = readme

        collector = MetadataCollector()
        preview = collector._collect_readme_preview(repo, max_chars=500)

        assert preview is not None
        assert len(preview) == 503  # 500 + "..."
        assert preview.endswith("...")

    def test_collect_readme_preview_none(self):
        """Test _collect_readme_preview when no README exists."""
        repo = MagicMock()
        repo.full_name = "test-org/no-readme"
        repo.get_readme.side_effect = GithubException(404, "Not found", None)

        collector = MetadataCollector()
        preview = collector._collect_readme_preview(repo)

        assert preview is None

    def test_collect_ownership(self, mock_github_repo):
        """Test _collect_ownership collects owner and contributors."""
        collector = MetadataCollector(max_contributors=3)
        ownership = collector._collect_ownership(mock_github_repo)

        assert ownership["owner"]["login"] == "test-org"
        assert ownership["owner"]["type"] == "Organization"
        assert len(ownership["top_contributors"]) == 2
        assert ownership["top_contributors"][0]["login"] == "user1"
        assert ownership["top_contributors"][0]["contributions"] == 100
        assert ownership["top_contributors"][1]["login"] == "user2"

    def test_collect_ownership_codeowners(self):
        """Test _collect_ownership detects CODEOWNERS file."""
        repo = MagicMock()
        repo.full_name = "test-org/test-repo"
        repo.owner.login = "test-org"
        repo.owner.type = "Organization"
        repo.owner.html_url = "https://github.com/test-org"

        # Mock CODEOWNERS file
        codeowners_content = "* @user1 @user2\n/docs/ @doc-team\n# Comment line"
        mock_file = MagicMock()
        mock_file.content = base64.b64encode(codeowners_content.encode("utf-8")).decode("utf-8")
        repo.get_contents.return_value = mock_file

        # Mock contributors
        repo.get_contributors.side_effect = GithubException(403, "Forbidden", None)
        repo.get_teams.side_effect = GithubException(404, "Not found", None)

        collector = MetadataCollector()
        ownership = collector._collect_ownership(repo)

        assert ownership["codeowners"]["exists"] is True
        assert "@user1" in ownership["codeowners"]["owners"]
        assert "@user2" in ownership["codeowners"]["owners"]
        assert "@doc-team" in ownership["codeowners"]["owners"]

    def test_collect_ownership_with_teams(self):
        """Test _collect_ownership includes teams when accessible."""
        repo = MagicMock()
        repo.full_name = "test-org/test-repo"
        repo.owner.login = "test-org"
        repo.owner.type = "Organization"
        repo.owner.html_url = "https://github.com/test-org"

        # Mock teams
        team1 = MagicMock()
        team1.name = "Developers"
        team1.permission = "push"

        team2 = MagicMock()
        team2.name = "Admins"
        team2.permission = "admin"

        repo.get_teams.return_value = [team1, team2]
        repo.get_contributors.side_effect = GithubException(403, "Forbidden", None)
        repo.get_contents.side_effect = GithubException(404, "Not found", None)

        collector = MetadataCollector()
        ownership = collector._collect_ownership(repo)

        assert len(ownership["teams"]) == 2
        assert ownership["teams"][0]["name"] == "Developers"
        assert ownership["teams"][0]["permission"] == "push"
        assert ownership["teams"][1]["name"] == "Admins"

    def test_collect_repository_metadata_complete(self, mock_github_repo):
        """Test collect_repository_metadata returns complete metadata structure."""
        collector = MetadataCollector()
        metadata = collector.collect_repository_metadata(mock_github_repo)

        assert "basic_info" in metadata
        assert "status" in metadata
        assert "activity" in metadata
        assert "languages" in metadata
        assert "license" in metadata
        assert "topics" in metadata
        assert "readme_preview" in metadata
        assert "ownership" in metadata

    def test_collect_repository_metadata_with_exception(self):
        """Test collect_repository_metadata raises exception on error."""
        repo = MagicMock()
        repo.full_name = "test-org/error-repo"
        repo.name = None  # Will cause AttributeError

        collector = MetadataCollector()
        with pytest.raises(Exception):
            collector.collect_repository_metadata(repo)
