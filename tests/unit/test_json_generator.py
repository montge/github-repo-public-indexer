"""Unit tests for src/json_generator.py"""

import pytest
import json
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch
from src.json_generator import JSONGenerator


@pytest.mark.unit
class TestJSONGenerator:
    """Test cases for JSONGenerator class."""

    def test_init_default_version(self):
        """Test JSONGenerator initialization with default version."""
        generator = JSONGenerator()
        assert generator.tool_version == "0.1.0"

    def test_init_custom_version(self):
        """Test JSONGenerator initialization with custom version."""
        generator = JSONGenerator(tool_version="2.0.0")
        assert generator.tool_version == "2.0.0"

    def test_generate_output_creates_file(self, tmp_path, sample_repo_data):
        """Test that generate_output creates a JSON file."""
        output_file = tmp_path / "output.json"
        generator = JSONGenerator()

        generator.generate_output(
            org_name="test-org",
            repositories=[sample_repo_data],
            output_file=str(output_file),
            backup_previous=False,
        )

        assert output_file.exists()

    def test_generate_output_valid_json_structure(self, tmp_path, sample_repo_data):
        """Test that generated JSON has correct structure."""
        output_file = tmp_path / "output.json"
        generator = JSONGenerator()

        generator.generate_output(
            org_name="test-org",
            repositories=[sample_repo_data],
            output_file=str(output_file),
            backup_previous=False,
        )

        with open(output_file, "r") as f:
            data = json.load(f)

        assert "metadata" in data
        assert "repositories" in data
        assert isinstance(data["repositories"], list)
        assert len(data["repositories"]) == 1

    def test_generate_output_metadata_fields(self, tmp_path, sample_repo_data):
        """Test that metadata contains required fields."""
        output_file = tmp_path / "output.json"
        generator = JSONGenerator(tool_version="1.0.0")

        generator.generate_output(
            org_name="test-org",
            repositories=[sample_repo_data],
            output_file=str(output_file),
            backup_previous=False,
        )

        with open(output_file, "r") as f:
            data = json.load(f)

        metadata = data["metadata"]
        assert metadata["organization"] == "test-org"
        assert metadata["total_repositories"] == 1
        assert metadata["tool_version"] == "1.0.0"
        assert metadata["github_api_version"] == "2022-11-28"
        assert "generated_at" in metadata

    def test_generate_output_backup_previous(self, tmp_path, sample_repo_data):
        """Test that existing file is backed up."""
        output_file = tmp_path / "output.json"
        generator = JSONGenerator()

        # Create initial file
        generator.generate_output(
            org_name="test-org",
            repositories=[sample_repo_data],
            output_file=str(output_file),
            backup_previous=False,
        )

        # Generate again with backup
        generator.generate_output(
            org_name="test-org",
            repositories=[sample_repo_data],
            output_file=str(output_file),
            backup_previous=True,
        )

        # Check that backup was created
        backups = list(tmp_path.glob("output.*.json"))
        assert len(backups) == 1

    def test_create_summary_counts_correctly(self, temp_json_file):
        """Test that create_summary computes correct statistics."""
        generator = JSONGenerator()
        summary = generator.create_summary(str(temp_json_file))

        assert summary["total_repositories"] == 1
        assert "status_breakdown" in summary
        assert "top_languages" in summary
        assert "license_breakdown" in summary
        assert "top_starred" in summary

    def test_create_summary_status_breakdown(self, temp_json_file):
        """Test status breakdown in summary."""
        generator = JSONGenerator()
        summary = generator.create_summary(str(temp_json_file))

        status = summary["status_breakdown"]
        assert status["active"] == 1
        assert status["archived"] == 0
        assert status["forks"] == 0

    def test_create_summary_top_languages(self, temp_json_file):
        """Test top languages in summary."""
        generator = JSONGenerator()
        summary = generator.create_summary(str(temp_json_file))

        assert "Python" in summary["top_languages"]
        assert summary["top_languages"]["Python"] == 1

    def test_validate_output_success(self, temp_json_file):
        """Test that validation passes for valid JSON."""
        generator = JSONGenerator()
        # Should not raise
        generator._validate_output(Path(temp_json_file))

    def test_validate_output_missing_metadata(self, tmp_path):
        """Test that validation fails for missing metadata."""
        bad_file = tmp_path / "bad.json"
        with open(bad_file, "w") as f:
            json.dump({"repositories": []}, f)

        generator = JSONGenerator()
        with pytest.raises(AssertionError, match="Missing 'metadata' section"):
            generator._validate_output(bad_file)

    def test_validate_output_repository_count_mismatch(self, tmp_path):
        """Test that validation fails when repository count doesn't match."""
        bad_file = tmp_path / "bad.json"
        data = {
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "organization": "test-org",
                "total_repositories": 10,  # Wrong count
                "tool_version": "1.0.0",
            },
            "repositories": [],  # Empty
        }
        with open(bad_file, "w") as f:
            json.dump(data, f)

        generator = JSONGenerator()
        with pytest.raises(AssertionError, match="Repository count mismatch"):
            generator._validate_output(bad_file)

    def test_generate_output_write_failure(self, tmp_path):
        """Test exception handling when writing output fails."""
        # Create a read-only directory to cause write failure
        output_dir = tmp_path / "readonly"
        output_dir.mkdir()
        output_file = output_dir / "output.json"
        output_dir.chmod(0o444)  # Make read-only

        generator = JSONGenerator()
        sample_repo = {
            "basic_info": {"name": "test"},
            "status": {"is_archived": False},
            "activity": {"stars": 0},
            "languages": {"primary": None},
            "license": {"key": None},
        }

        try:
            with pytest.raises(Exception):
                generator.generate_output(
                    org_name="test-org",
                    repositories=[sample_repo],
                    output_file=str(output_file),
                    backup_previous=False,
                )
        finally:
            # Clean up: restore permissions
            output_dir.chmod(0o755)

    @patch("src.json_generator.Path.rename")
    def test_backup_file_failure(self, mock_rename, tmp_path):
        """Test backup failure handling."""
        output_file = tmp_path / "output.json"
        sample_repo = {
            "basic_info": {"name": "test"},
            "status": {"is_archived": False},
            "activity": {"stars": 0},
            "languages": {"primary": None},
            "license": {"key": None},
        }

        # Create initial file
        generator = JSONGenerator()
        generator.generate_output(
            org_name="test-org",
            repositories=[sample_repo],
            output_file=str(output_file),
            backup_previous=False,
        )

        # Mock rename to raise exception
        mock_rename.side_effect = OSError("Permission denied")

        # Should log warning but not fail
        generator.generate_output(
            org_name="test-org",
            repositories=[sample_repo],
            output_file=str(output_file),
            backup_previous=True,
        )

        assert output_file.exists()

    def test_validate_output_file_read_error(self, tmp_path):
        """Test validation with file read error."""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not valid json")

        generator = JSONGenerator()
        with pytest.raises(Exception):
            generator._validate_output(bad_file)

    def test_create_summary_unlicensed_repos(self, tmp_path):
        """Test summary with unlicensed repositories."""
        # Create JSON with unlicensed repos
        data = {
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "organization": "test-org",
                "total_repositories": 2,
                "tool_version": "0.1.0",
            },
            "repositories": [
                {
                    "basic_info": {
                        "full_name": "test-org/repo1",
                        "html_url": "https://github.com/test-org/repo1",
                    },
                    "status": {"is_archived": False, "is_fork": False, "is_template": False},
                    "activity": {"stars": 10},
                    "languages": {"primary": "Python"},
                    "license": {"key": None},  # Unlicensed
                },
                {
                    "basic_info": {
                        "full_name": "test-org/repo2",
                        "html_url": "https://github.com/test-org/repo2",
                    },
                    "status": {"is_archived": False, "is_fork": False, "is_template": False},
                    "activity": {"stars": 5},
                    "languages": {"primary": "Python"},
                    "license": {"key": "mit"},  # Licensed
                },
            ],
        }

        json_file = tmp_path / "test.json"
        with open(json_file, "w") as f:
            json.dump(data, f)

        generator = JSONGenerator()
        summary = generator.create_summary(str(json_file))

        assert "unlicensed" in summary["license_breakdown"]
        assert summary["license_breakdown"]["unlicensed"] == 1
        assert summary["license_breakdown"]["mit"] == 1

    def test_create_summary_invalid_json(self, tmp_path):
        """Test summary creation with invalid JSON file."""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not json")

        generator = JSONGenerator()
        with pytest.raises(Exception):
            generator.create_summary(str(bad_file))
