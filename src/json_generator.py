"""JSON output generation and validation."""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class JSONGenerator:
    """Handles JSON generation and validation."""

    def __init__(self, tool_version: str = "0.1.0"):
        """
        Initialize JSON generator.

        Args:
            tool_version: Version of the collection tool
        """
        self.tool_version = tool_version

    def generate_output(
        self,
        org_name: str,
        repositories: List[Dict[str, Any]],
        output_file: str,
        backup_previous: bool = True,
    ) -> None:
        """
        Generate JSON output file.

        Args:
            org_name: Organization name
            repositories: List of repository metadata dictionaries
            output_file: Path to output file
            backup_previous: Whether to backup existing file
        """
        output_path = Path(output_file)

        # Backup existing file if it exists
        if backup_previous and output_path.exists():
            self._backup_file(output_path)

        # Create output structure
        output = {
            "metadata": self._create_metadata(org_name, len(repositories)),
            "repositories": repositories,
        }

        # Write to file
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

            logger.info(f"Output written to: {output_path}")
            logger.info(f"File size: {output_path.stat().st_size / 1024:.2f} KB")

            # Validate the generated JSON
            self._validate_output(output_path)

        except Exception as e:
            logger.error(f"Failed to write output file: {e}")
            raise

    def _create_metadata(self, org_name: str, total_repos: int) -> Dict[str, Any]:
        """Create metadata section for JSON output."""
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "organization": org_name,
            "total_repositories": total_repos,
            "tool_version": self.tool_version,
            "github_api_version": "2022-11-28",
        }

    def _backup_file(self, file_path: Path) -> None:
        """Backup existing file with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = file_path.with_stem(f"{file_path.stem}.{timestamp}")

        try:
            file_path.rename(backup_path)
            logger.info(f"Previous file backed up to: {backup_path}")
        except Exception as e:
            logger.warning(f"Could not backup previous file: {e}")

    def _validate_output(self, file_path: Path) -> None:
        """Validate the generated JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Basic validation
            assert "metadata" in data, "Missing 'metadata' section"
            assert "repositories" in data, "Missing 'repositories' section"
            assert isinstance(data["repositories"], list), "'repositories' must be a list"

            metadata = data["metadata"]
            assert "generated_at" in metadata, "Missing 'generated_at' in metadata"
            assert "organization" in metadata, "Missing 'organization' in metadata"
            assert "total_repositories" in metadata, "Missing 'total_repositories' in metadata"

            # Verify repository count matches
            actual_count = len(data["repositories"])
            expected_count = metadata["total_repositories"]
            assert (
                actual_count == expected_count
            ), f"Repository count mismatch: {actual_count} != {expected_count}"

            logger.info("JSON validation passed")

        except AssertionError as e:
            logger.error(f"JSON validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Error validating JSON: {e}")
            raise

    def create_summary(self, output_file: str) -> Dict[str, Any]:
        """
        Create a summary of the generated JSON file.

        Args:
            output_file: Path to JSON file

        Returns:
            Dictionary with summary statistics
        """
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            repos = data["repositories"]

            # Count by status
            active_count = sum(1 for r in repos if not r["status"]["is_archived"])
            archived_count = sum(1 for r in repos if r["status"]["is_archived"])
            fork_count = sum(1 for r in repos if r["status"]["is_fork"])
            template_count = sum(1 for r in repos if r["status"]["is_template"])

            # Count by language
            languages = {}
            for repo in repos:
                primary_lang = repo["languages"]["primary"]
                if primary_lang:
                    languages[primary_lang] = languages.get(primary_lang, 0) + 1

            # Count by license
            licenses = {}
            for repo in repos:
                license_key = repo["license"]["key"]
                if license_key:
                    licenses[license_key] = licenses.get(license_key, 0) + 1
                else:
                    licenses["unlicensed"] = licenses.get("unlicensed", 0) + 1

            # Top repos by stars
            top_repos = sorted(repos, key=lambda r: r["activity"]["stars"], reverse=True)[:5]

            summary = {
                "total_repositories": len(repos),
                "status_breakdown": {
                    "active": active_count,
                    "archived": archived_count,
                    "forks": fork_count,
                    "templates": template_count,
                },
                "top_languages": dict(
                    sorted(languages.items(), key=lambda x: x[1], reverse=True)[:10]
                ),
                "license_breakdown": licenses,
                "top_starred": [
                    {
                        "name": r["basic_info"]["full_name"],
                        "stars": r["activity"]["stars"],
                        "url": r["basic_info"]["html_url"],
                    }
                    for r in top_repos
                ],
            }

            return summary

        except Exception as e:
            logger.error(f"Error creating summary: {e}")
            raise
