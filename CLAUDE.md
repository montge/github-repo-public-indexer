# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GitHub Organization Repository Indexer - A two-phase tool that:
1. **Phase 1 (Python)**: Collects repository metadata via GitHub API and generates JSON
2. **Phase 2 (AI-assisted)**: Uses the JSON with Cursor/Windsurf to generate documentation

The codebase currently implements Phase 1.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Tool
```bash
# Basic usage with environment variables from .env
python collect_repos.py

# With explicit parameters (GitHub.com)
python collect_repos.py --org myorg --token ghp_xxx --output repos.json

# GitHub Enterprise Server
python collect_repos.py --org myorg --token ghp_xxx --github-url https://github.example.com/api/v3

# With verbose logging and summary
python collect_repos.py --org myorg --verbose --summary

# Exclude forks and archived repos
python collect_repos.py --org myorg --no-forks --no-archived
```

### Validation and Testing
```bash
# Validate generated JSON
python -m json.tool repositories.json > /dev/null

# View metadata
jq '.metadata' repositories.json

# Count repositories
jq '.repositories | length' repositories.json
```

## Architecture

### Module Structure

**src/github_client.py** - GitHub API interaction
- `GitHubClient`: Wraps PyGithub for authenticated API access
- Supports both github.com and GitHub Enterprise Server (via `base_url` parameter)
- Handles rate limiting automatically (waits until reset)
- Methods: `get_organization()`, `get_all_repositories()`, `check_rate_limit()`

**src/metadata_collector.py** - Repository data extraction
- `MetadataCollector`: Collects structured metadata for each repo
- Main method: `collect_repository_metadata()` returns dict matching JSON schema
- Gracefully handles missing data (README, CODEOWNERS, teams, etc.)
- Collects: basic info, status flags, activity metrics, languages, license, topics, README preview, ownership

**src/json_generator.py** - Output generation
- `JSONGenerator`: Creates and validates JSON output
- Automatically backs up previous files with timestamp
- Validates structure after generation
- Method `create_summary()` generates statistics

**collect_repos.py** - CLI entry point
- Built with Click for argument parsing
- Uses Rich for beautiful console output with progress bars
- Environment variables from .env via python-dotenv
- Comprehensive error handling and logging

### Data Flow

```
User → CLI (collect_repos.py)
  ↓
GitHubClient (authenticate, fetch repos)
  ↓
MetadataCollector (collect metadata for each repo)
  ↓
JSONGenerator (create JSON, validate, backup)
  ↓
repositories.json → (Phase 2: Cursor/Windsurf + PROMPT_TEMPLATE.md → README)
```

### JSON Schema

Output follows structure defined in `JSON_SCHEMA.md`:
- `metadata`: Collection info (timestamp, org name, count, version)
- `repositories[]`: Array of repository objects with sections:
  - `basic_info`: name, description, URLs, dates
  - `status`: archived, fork, template, etc.
  - `activity`: stars, forks, commits, contributors
  - `languages`: primary language and breakdown
  - `license`: SPDX information
  - `topics`: repository tags
  - `readme_preview`: first 500 chars
  - `ownership`: owner, top contributors, teams, CODEOWNERS

## Key Implementation Details

### Error Handling Philosophy
- **Graceful degradation**: If optional data fails to fetch (contributors, teams, CODEOWNERS), log warning and continue with null/empty values
- **Fatal errors**: Only fail on critical issues (authentication, org not found, JSON write failure)
- **Per-repository errors**: Collected in `failed_repos` list and reported at end, but don't stop processing

### Rate Limiting
- GitHub API limits: 5000 requests/hour (authenticated)
- `GitHubClient._handle_rate_limit()` automatically waits until reset + 10 seconds
- Use `check_rate_limit()` to monitor remaining requests

### Performance Considerations
- For large orgs (100+ repos), consider `--no-forks` to reduce count
- Most expensive operations: contributor lists, commit counts
- PyGithub handles pagination automatically

### Security
- Never commit `.env` or `repositories.json` (may contain private data)
- `.gitignore` configured to exclude tokens and output files
- Token requires minimal scopes: `public_repo`, `read:org`, `read:user`

## Common Development Tasks

### Adding New Metadata Fields

1. Update `JSON_SCHEMA.md` with new field definition
2. Add collection logic in `src/metadata_collector.py`:
   ```python
   def _collect_new_field(self, repo: Repository.Repository) -> Any:
       try:
           # Fetch data from repo object
           return data
       except GithubException as e:
           logger.warning(f"Could not get new_field for {repo.full_name}: {e}")
           return None
   ```
3. Add to `collect_repository_metadata()` return dict
4. Update validation in `src/json_generator.py` if needed

### Debugging API Issues

Enable verbose logging:
```bash
python collect_repos.py --org myorg --verbose
```

Check specific repository manually:
```python
from src.github_client import GitHubClient
from src.metadata_collector import MetadataCollector

client = GitHubClient("ghp_token")
org = client.get_organization("myorg")
repo = org.get_repo("repo-name")

collector = MetadataCollector()
metadata = collector.collect_repository_metadata(repo)
```

### Testing with Small Organization

Use a test org with few repos first:
```bash
python collect_repos.py --org small-test-org --verbose --summary
```

## Working with Generated JSON

### Quick Queries

```bash
# Active repos only
jq '.repositories[] | select(.status.is_archived == false)' repositories.json

# Python projects
jq '.repositories[] | select(.languages.primary == "Python")' repositories.json

# Unlicensed repos
jq '.repositories[] | select(.license.key == null)' repositories.json

# Top 10 by stars
jq '.repositories | sort_by(.activity.stars) | reverse | .[0:10]' repositories.json
```

### Phase 2 Workflow

1. Generate JSON: `python collect_repos.py --org myorg`
2. Open `PROMPT_TEMPLATE.md` and customize
3. In Cursor/Windsurf: Paste prompt + attach `repositories.json`
4. AI generates `README.md` with categorized repos
5. Review and refine with follow-up prompts

## Configuration Files

- `.env` - Secrets and configuration (never commit)
- `.env.example` - Template with all available options
- `requirements.txt` - Python dependencies (pin versions)
- `.gitignore` - Configured to exclude tokens, output, caches

## Dependencies

Key libraries:
- **PyGithub**: GitHub API client
- **click**: CLI framework
- **rich**: Beautiful console output
- **python-dotenv**: Environment variable management

## Documentation Files

- `SPECIFICATION.md` - Complete requirements and design
- `JSON_SCHEMA.md` - Detailed output schema
- `WORKFLOW.md` - End-to-end process guide
- `PROMPT_TEMPLATE.md` - Template for Phase 2 AI generation
- `CONTRIBUTING_TEMPLATE.md` - Template for index repository CONTRIBUTING.md
- `USAGE.md` - Practical usage examples
- `QUICK_REFERENCE.md` - One-page summary

## Future Enhancements

Potential additions (not yet implemented):
- Parallel processing for large orgs
- Caching of API responses
- Diff/comparison between runs
- GitHub Actions automation
- Direct README generation (skip Phase 2)
- Support for multiple organizations
- Web dashboard/UI
