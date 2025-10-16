"""GitHub API client wrapper for repository data collection."""

import logging
from typing import List, Optional
from datetime import datetime, timezone
from github import Github, GithubException, Repository, RateLimitExceededException
import time

logger = logging.getLogger(__name__)


class GitHubClient:
    """Wrapper around PyGithub for collecting repository metadata."""

    def __init__(self, token: str, base_url: Optional[str] = None):
        """
        Initialize GitHub client with authentication token.

        Args:
            token: GitHub personal access token
            base_url: Base URL for GitHub API (for GitHub Enterprise Server).
                     Default is https://api.github.com for github.com.
                     For GHE, use https://github.example.com/api/v3
        """
        if base_url:
            # For GitHub Enterprise Server
            logger.info(f"Using custom GitHub URL: {base_url}")
            self.client = Github(base_url=base_url, login_or_token=token)
        else:
            # For github.com
            self.client = Github(token)

        self.user = None
        self.base_url = base_url
        self._validate_token()

    def _validate_token(self):
        """Validate the GitHub token and log rate limit info."""
        try:
            self.user = self.client.get_user()
            rate_limit = self.client.get_rate_limit()
            logger.info(f"Authenticated as: {self.user.login}")
            logger.info(f"Rate limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")
            logger.info(f"Reset at: {rate_limit.core.reset}")
        except GithubException as e:
            logger.error(f"Failed to authenticate: {e}")
            raise

    def get_organization(self, org_name: str):
        """
        Get organization object.

        Args:
            org_name: Name of the GitHub organization

        Returns:
            Organization object
        """
        try:
            org = self.client.get_organization(org_name)
            logger.info(f"Found organization: {org.login} ({org.name})")
            return org
        except GithubException as e:
            logger.error(f"Failed to get organization '{org_name}': {e}")
            raise

    def get_all_repositories(
        self, org_name: str, include_forks: bool = True, include_archived: bool = True
    ) -> List[Repository.Repository]:
        """
        Fetch all repositories for an organization.

        Args:
            org_name: Name of the GitHub organization
            include_forks: Include forked repositories
            include_archived: Include archived repositories

        Returns:
            List of Repository objects
        """
        org = self.get_organization(org_name)
        repositories = []

        try:
            logger.info("Fetching repositories (this may take a while)...")
            all_repos = org.get_repos(type="all")

            for repo in all_repos:
                # Apply filters
                if not include_forks and repo.fork:
                    logger.debug(f"Skipping fork: {repo.name}")
                    continue

                if not include_archived and repo.archived:
                    logger.debug(f"Skipping archived: {repo.name}")
                    continue

                repositories.append(repo)
                logger.debug(f"Added: {repo.full_name}")

            logger.info(f"Found {len(repositories)} repositories")
            return repositories

        except RateLimitExceededException:
            self._handle_rate_limit()
            return self.get_all_repositories(org_name, include_forks, include_archived)
        except GithubException as e:
            logger.error(f"Failed to fetch repositories: {e}")
            raise

    def _handle_rate_limit(self):
        """Handle rate limit by waiting until reset."""
        rate_limit = self.client.get_rate_limit()
        reset_time = rate_limit.core.reset
        sleep_time = (reset_time - datetime.now(timezone.utc)).total_seconds() + 10

        if sleep_time > 0:
            logger.warning(f"Rate limit exceeded. Waiting {sleep_time:.0f} seconds...")
            time.sleep(sleep_time)

    def check_rate_limit(self):
        """Check and log current rate limit status."""
        rate_limit = self.client.get_rate_limit()
        logger.info(f"Rate limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")

        if rate_limit.core.remaining < 100:
            logger.warning(f"Low rate limit! Remaining: {rate_limit.core.remaining}")
