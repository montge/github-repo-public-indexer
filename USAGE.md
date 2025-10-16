# Usage Guide

## Installation

### 1. Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your GitHub token
# GITHUB_TOKEN=ghp_your_token_here
# GITHUB_ORG=your-org-name
```

### 3. Get GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - `public_repo` - Access public repositories
   - `read:org` - Read org and team membership
   - `read:user` - Read user profile data
4. Copy the generated token
5. Add to `.env` file

## Basic Usage

### Simple Command (GitHub.com)

```bash
python collect_repos.py --org your-org-name --token ghp_your_token
```

### GitHub Enterprise Server

```bash
python collect_repos.py \
  --org your-org-name \
  --token ghp_your_token \
  --github-url https://github.example.com/api/v3
```

### Using Environment Variables

```bash
# Set in .env file, then simply run:
python collect_repos.py
```

### Common Options

```bash
# Specify output file
python collect_repos.py --org myorg --output my-repos.json

# GitHub Enterprise Server
python collect_repos.py --org myorg --github-url https://github.example.com/api/v3

# Exclude forks
python collect_repos.py --org myorg --no-forks

# Exclude archived repositories
python collect_repos.py --org myorg --no-archived

# Verbose logging
python collect_repos.py --org myorg --verbose

# Show summary after collection
python collect_repos.py --org myorg --summary

# Limit number of contributors per repo
python collect_repos.py --org myorg --max-contributors 10
```

## Making the Script Executable

```bash
# Make executable
chmod +x collect_repos.py

# Run directly
./collect_repos.py --org myorg
```

## Complete Example

```bash
# Activate virtual environment
source venv/bin/activate

# Run with all options
python collect_repos.py \
  --org myorg \
  --token ghp_xxxxxxxxxxxx \
  --output repositories.json \
  --max-contributors 5 \
  --include-forks \
  --include-archived \
  --backup \
  --verbose \
  --summary
```

## Using with gh CLI

If you have `gh` CLI installed, you can get your token:

```bash
# Get current gh token
export GITHUB_TOKEN=$(gh auth token)

# Run script
python collect_repos.py --org myorg
```

## Output

The script generates:
- `repositories.json` - Main output file
- `repositories.YYYYMMDD_HHMMSS.json` - Backup of previous file (if --backup enabled)

### Validating Output

```bash
# Check JSON is valid
python -m json.tool repositories.json > /dev/null && echo "Valid JSON"

# View metadata
jq '.metadata' repositories.json

# Count repositories
jq '.repositories | length' repositories.json

# List repository names
jq '.repositories[].basic_info.name' repositories.json

# Show active (non-archived) repos
jq '.repositories[] | select(.status.is_archived == false) | .basic_info.name' repositories.json

# Show repositories by language
jq '.repositories[] | select(.languages.primary == "Python") | .basic_info.name' repositories.json
```

## Troubleshooting

### Rate Limit Issues

If you hit rate limits:
```bash
# Check current rate limit
gh api rate_limit

# The script will automatically wait if rate limit is exceeded
# Use authenticated requests (always use --token)
```

### Missing Dependencies

```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade
```

### Permission Errors

Ensure your token has the correct scopes:
- `public_repo` or `repo` for repository access
- `read:org` for organization data
- `read:user` for user profiles

### Large Organizations

For organizations with 100+ repositories:
```bash
# Use verbose mode to monitor progress
python collect_repos.py --org myorg --verbose

# Exclude forks and archived to reduce count
python collect_repos.py --org myorg --no-forks --no-archived
```

## Next Steps

After successful collection:

1. **Validate the JSON**:
   ```bash
   python -m json.tool repositories.json > /dev/null
   ```

2. **Review the data**:
   ```bash
   jq '.metadata' repositories.json
   ```

3. **Use with Cursor/Windsurf**:
   - Open `PROMPT_TEMPLATE.md`
   - Customize the prompt
   - Attach `repositories.json`
   - Generate README

## Advanced Usage

### Filtering Results

Edit `collect_repos.py` or create a filter script:

```python
import json

# Load data
with open('repositories.json', 'r') as f:
    data = json.load(f)

# Filter for active Python projects with > 10 stars
filtered = [
    repo for repo in data['repositories']
    if not repo['status']['is_archived']
    and repo['languages']['primary'] == 'Python'
    and repo['activity']['stars'] > 10
]

# Save filtered results
data['repositories'] = filtered
data['metadata']['total_repositories'] = len(filtered)

with open('filtered-repos.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Automated Updates

Create a cron job or GitHub Action to run weekly:

```bash
# crontab -e
# Run every Monday at 9 AM
0 9 * * 1 cd /path/to/project && ./venv/bin/python collect_repos.py --org myorg
```

### Comparing Versions

```bash
# Keep previous version
cp repositories.json repositories-old.json

# Collect new data
python collect_repos.py --org myorg

# Compare
diff <(jq -S '.repositories[].basic_info.name' repositories-old.json) \
     <(jq -S '.repositories[].basic_info.name' repositories.json)
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub personal access token | Yes |
| `GITHUB_ORG` | Organization name | Yes |
| `GITHUB_URL` | GitHub API base URL (for GHE Server) | No (default: api.github.com) |
| `OUTPUT_FILE` | Output file path | No (default: repositories.json) |

## CLI Options Reference

| Option | Short | Environment | Description |
|--------|-------|-------------|-------------|
| `--org` | `-o` | `GITHUB_ORG` | GitHub organization name |
| `--token` | `-t` | `GITHUB_TOKEN` | GitHub personal access token |
| `--github-url` | `-u` | `GITHUB_URL` | GitHub API base URL (for GitHub Enterprise Server) |
| `--output` | `-f` | `OUTPUT_FILE` | Output JSON file path |
| `--max-contributors` | | | Max contributors per repo (default: 5) |
| `--include-forks` | | | Include forked repositories |
| `--no-forks` | | | Exclude forked repositories |
| `--include-archived` | | | Include archived repositories |
| `--no-archived` | | | Exclude archived repositories |
| `--backup` | | | Backup existing output file |
| `--no-backup` | | | Don't backup existing file |
| `--verbose` | `-v` | | Enable verbose logging |
| `--summary` | | | Show summary after collection |

## Help

```bash
# Show help
python collect_repos.py --help
```
