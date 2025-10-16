"""Repository metadata collection and processing."""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from github import Repository, GithubException
import base64

logger = logging.getLogger(__name__)


class MetadataCollector:
    """Collects and structures repository metadata."""

    def __init__(self, max_contributors: int = 5):
        """
        Initialize metadata collector.

        Args:
            max_contributors: Maximum number of top contributors to include
        """
        self.max_contributors = max_contributors

    def collect_repository_metadata(self, repo: Repository.Repository) -> Dict[str, Any]:
        """
        Collect all metadata for a single repository.

        Args:
            repo: PyGithub Repository object

        Returns:
            Dictionary containing structured repository metadata
        """
        logger.info(f"Collecting metadata for: {repo.full_name}")

        try:
            metadata = {
                "basic_info": self._collect_basic_info(repo),
                "status": self._collect_status(repo),
                "activity": self._collect_activity(repo),
                "languages": self._collect_languages(repo),
                "license": self._collect_license(repo),
                "topics": self._collect_topics(repo),
                "readme_preview": self._collect_readme_preview(repo),
                "ownership": self._collect_ownership(repo),
            }

            logger.debug(f"Successfully collected metadata for {repo.full_name}")
            return metadata

        except Exception as e:
            logger.error(f"Error collecting metadata for {repo.full_name}: {e}")
            raise

    def _collect_basic_info(self, repo: Repository.Repository) -> Dict[str, Any]:
        """Collect basic repository information."""
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "url": repo.url,
            "html_url": repo.html_url,
            "homepage": repo.homepage,
            "created_at": repo.created_at.isoformat() if repo.created_at else None,
            "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
            "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
            "size": repo.size,
            "default_branch": repo.default_branch,
            "visibility": "public" if not repo.private else "private",
        }

    def _collect_status(self, repo: Repository.Repository) -> Dict[str, bool]:
        """Collect repository status flags."""
        return {
            "is_archived": repo.archived,
            "is_fork": repo.fork,
            "is_template": repo.is_template if hasattr(repo, "is_template") else False,
            "is_disabled": repo.disabled if hasattr(repo, "disabled") else False,
            "has_issues": repo.has_issues,
            "has_projects": repo.has_projects,
            "has_wiki": repo.has_wiki,
            "has_pages": repo.has_pages,
            "has_downloads": repo.has_downloads,
            "has_discussions": repo.has_discussions if hasattr(repo, "has_discussions") else False,
        }

    def _collect_activity(self, repo: Repository.Repository) -> Dict[str, Any]:
        """Collect repository activity metrics."""
        try:
            # Get commit count for last 30 days
            commits_30d = 0
            try:
                since = datetime.now(timezone.utc).replace(day=1)  # Rough approximation
                commits = repo.get_commits(since=since)
                commits_30d = commits.totalCount
            except GithubException as e:
                logger.warning(f"Could not get commits for {repo.full_name}: {e}")

            # Get contributor count
            contributor_count = 0
            try:
                contributors = repo.get_contributors()
                contributor_count = contributors.totalCount
            except GithubException as e:
                logger.warning(f"Could not get contributors for {repo.full_name}: {e}")

            # Get open PRs count
            open_prs = 0
            try:
                pulls = repo.get_pulls(state="open")
                open_prs = pulls.totalCount
            except GithubException as e:
                logger.warning(f"Could not get PRs for {repo.full_name}: {e}")

            return {
                "stars": repo.stargazers_count,
                "watchers": repo.watchers_count,
                "forks": repo.forks_count,
                "open_issues": repo.open_issues_count,
                "open_pull_requests": open_prs,
                "last_commit_date": repo.pushed_at.isoformat() if repo.pushed_at else None,
                "commit_count_30d": commits_30d,
                "contributor_count": contributor_count,
            }
        except Exception as e:
            logger.error(f"Error collecting activity for {repo.full_name}: {e}")
            return {
                "stars": repo.stargazers_count,
                "watchers": repo.watchers_count,
                "forks": repo.forks_count,
                "open_issues": repo.open_issues_count,
                "open_pull_requests": 0,
                "last_commit_date": repo.pushed_at.isoformat() if repo.pushed_at else None,
                "commit_count_30d": 0,
                "contributor_count": 0,
            }

    def _collect_languages(self, repo: Repository.Repository) -> Dict[str, Any]:
        """Collect repository language information."""
        try:
            languages = repo.get_languages()
            if not languages:
                return {"primary": None, "breakdown": {}}

            # Calculate percentages
            total = sum(languages.values())
            breakdown = {
                lang: round((bytes_count / total) * 100, 1)
                for lang, bytes_count in languages.items()
            }

            # Primary language is the one with most bytes
            primary = max(languages.items(), key=lambda x: x[1])[0] if languages else None

            return {"primary": primary, "breakdown": breakdown}
        except GithubException as e:
            logger.warning(f"Could not get languages for {repo.full_name}: {e}")
            return {"primary": None, "breakdown": {}}

    def _collect_license(self, repo: Repository.Repository) -> Optional[Dict[str, Optional[str]]]:
        """Collect repository license information."""
        try:
            license_info = repo.get_license()
            if license_info and license_info.license:
                return {
                    "key": license_info.license.key,
                    "name": license_info.license.name,
                    "spdx_id": license_info.license.spdx_id,
                    "url": license_info.license.url,
                }
        except GithubException as e:
            logger.debug(f"No license found for {repo.full_name}: {e}")

        return {"key": None, "name": None, "spdx_id": None, "url": None}

    def _collect_topics(self, repo: Repository.Repository) -> List[str]:
        """Collect repository topics/tags."""
        try:
            return repo.get_topics()
        except GithubException as e:
            logger.warning(f"Could not get topics for {repo.full_name}: {e}")
            return []

    def _collect_readme_preview(
        self, repo: Repository.Repository, max_chars: int = 500
    ) -> Optional[str]:
        """Collect preview of README content."""
        try:
            readme = repo.get_readme()
            content = base64.b64decode(readme.content).decode("utf-8")
            # Return first max_chars characters
            preview = content[:max_chars]
            if len(content) > max_chars:
                preview += "..."
            return preview
        except GithubException as e:
            logger.debug(f"No README found for {repo.full_name}: {e}")
            return None

    def _collect_ownership(self, repo: Repository.Repository) -> Dict[str, Any]:
        """Collect repository ownership and contributor information."""
        ownership = {
            "owner": {
                "login": repo.owner.login,
                "type": repo.owner.type,
                "url": repo.owner.html_url,
            },
            "top_contributors": [],
            "teams": [],
            "codeowners": {"exists": False, "owners": []},
        }

        # Get top contributors
        try:
            contributors = repo.get_contributors()
            for i, contributor in enumerate(contributors):
                if i >= self.max_contributors:
                    break
                ownership["top_contributors"].append(
                    {
                        "login": contributor.login,
                        "contributions": contributor.contributions,
                        "profile_url": contributor.html_url,
                    }
                )
        except GithubException as e:
            logger.warning(f"Could not get contributors for {repo.full_name}: {e}")

        # Get teams (if accessible)
        try:
            teams = repo.get_teams()
            for team in teams:
                ownership["teams"].append({"name": team.name, "permission": team.permission})
        except GithubException as e:
            logger.debug(f"Could not get teams for {repo.full_name}: {e}")

        # Check for CODEOWNERS file
        try:
            codeowners = None
            for path in [".github/CODEOWNERS", "CODEOWNERS", "docs/CODEOWNERS"]:
                try:
                    file = repo.get_contents(path)
                    codeowners = base64.b64decode(file.content).decode("utf-8")
                    ownership["codeowners"]["exists"] = True
                    # Extract owners (lines starting with @)
                    owners = []
                    for line in codeowners.split("\n"):
                        line = line.strip()
                        if line and not line.startswith("#"):
                            # Extract @mentions
                            words = line.split()
                            owners.extend([w for w in words if w.startswith("@")])
                    ownership["codeowners"]["owners"] = list(set(owners))
                    break
                except GithubException:
                    continue
        except Exception as e:
            logger.debug(f"Error checking CODEOWNERS for {repo.full_name}: {e}")

        return ownership
