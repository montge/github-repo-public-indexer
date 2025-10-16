# Quick Reference Guide

## TL;DR

**Goal**: Create public-facing documentation for all repositories in a GitHub organization

**Approach**: Two-phase process
1. Script collects metadata → generates JSON
2. AI (Cursor/Windsurf) reads JSON → generates README

## Files Overview

| File | Purpose |
|------|---------|
| **SPECIFICATION.md** | Complete project requirements and architecture |
| **JSON_SCHEMA.md** | Structure of the metadata JSON file |
| **WORKFLOW.md** | Step-by-step execution guide |
| **PROMPT_TEMPLATE.md** | Template for AI documentation generation |
| **README.md** | This project's overview and status |

## Phase 1: Data Collection

### Input
- GitHub organization name
- GitHub API token

### Process
Script fetches for each repository:
- Basic info (name, description, dates)
- Status (archived, fork, etc.)
- Activity (stars, commits, contributors)
- Languages, license, topics
- Ownership and POCs

### Output
`repositories.json` - Structured metadata file

## Phase 2: Documentation Generation

### Input
- `repositories.json` from Phase 1
- Customized prompt (from PROMPT_TEMPLATE.md)

### Process
AI assistant analyzes and creates:
- Categorized repository listings
- Overview dashboard
- Quick find tables
- License compliance section
- POC index

### Output
`README.md` - Public-facing documentation

## Key Metadata Fields

```javascript
{
  "metadata": {
    "generated_at": "timestamp",
    "organization": "org-name",
    "total_repositories": 42
  },
  "repositories": [
    {
      "basic_info": {...},      // name, description, URLs
      "status": {...},          // archived, fork, etc.
      "activity": {...},        // stars, commits, contributors
      "languages": {...},       // primary language, breakdown
      "license": {...},         // SPDX ID, name
      "topics": [...],          // tags
      "readme_preview": "...",  // first 500 chars
      "ownership": {...}        // contributors, teams, CODEOWNERS
    }
  ]
}
```

## Quick Commands

### Setup
```bash
# Set environment variables
export GITHUB_TOKEN="ghp_your_token"
export GITHUB_ORG="your-org-name"

# For GitHub Enterprise Server
export GITHUB_URL="https://github.example.com/api/v3"
```

### Phase 1
```bash
# GitHub.com
python collect_repos.py --org your-org-name --output repositories.json

# GitHub Enterprise Server
python collect_repos.py --org your-org-name --github-url https://github.example.com/api/v3
```

### Validation
```bash
# Check JSON is valid
python -m json.tool repositories.json > /dev/null

# View summary
jq '.metadata' repositories.json

# Count repos
jq '.repositories | length' repositories.json
```

### Phase 2
1. Open Cursor/Windsurf
2. Copy prompt from PROMPT_TEMPLATE.md
3. Customize placeholders
4. Attach repositories.json
5. Generate and review README

## Documentation Structure

Recommended README sections:
1. **Header**: Title, intro, TOC
2. **Overview Dashboard**: Stats and highlights
3. **Categories**:
   - Active Projects
   - Core Infrastructure
   - Experimental
   - Archived
   - Forks/Templates
4. **Quick Find**: Tables for searching
5. **License Compliance**: Grouped by license
6. **POCs**: Contributor index
7. **Metadata**: Generation info

## Customization Points

### Categorization Rules
Define in prompt how to categorize repos:
- By activity level
- By topic/technology
- By team/ownership
- By purpose (library, tool, docs, etc.)

### Filtering
Optionally exclude:
- Forks
- Archived repositories
- Private repositories
- Repositories below certain star count

### Presentation Style
Choose format:
- Detailed (all info visible)
- Summary (collapsible details)
- Tabular (compact tables)
- Mixed (important projects detailed, others summarized)

## GitHub API Permissions

Required token scopes:
- `public_repo` - For public repositories
- `read:org` - For organization data
- `read:user` - For user profiles

Optional (for private repos):
- `repo` - Full repository access

## Rate Limits

- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5,000 requests/hour
- **GitHub Apps**: 15,000 requests/hour

For large orgs, use:
- Conditional requests (ETags)
- Caching
- Parallel processing (within limits)

## Security Checklist

- [ ] Token stored in .env (not in code)
- [ ] .gitignore includes .env and *.json
- [ ] Never commit repositories.json (may contain private data)
- [ ] Use minimal token permissions needed
- [ ] Rotate tokens periodically
- [ ] Review generated README before publishing

## Common Workflows

### Initial Setup
1. Read SPECIFICATION.md
2. Implement Phase 1 script using JSON_SCHEMA.md
3. Test with small organization
4. Refine and validate

### Regular Updates
1. Run Phase 1 script
2. Compare with previous version
3. Update Phase 2 prompt if needed
4. Generate new README
5. Publish updates

### Continuous Automation
1. Set up GitHub Actions workflow
2. Schedule monthly runs
3. Auto-commit JSON updates
4. Manually regenerate README as needed

## Tips

- **Start small**: Test with a small organization first
- **Iterate**: Generate, review, refine prompt, repeat
- **Cache**: Save previous versions for comparison
- **Validate**: Always check JSON before Phase 2
- **Customize**: Adapt categories to your organization
- **Update**: Keep documentation current with regular runs

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Rate limit exceeded | Use authenticated requests, add delays |
| JSON too large for AI | Split by category, use summary version |
| Missing data | Check token permissions, verify access |
| Wrong categorization | Refine categorization rules in prompt |
| Slow processing | Implement parallel fetching, caching |

## Next Actions

1. Choose implementation language (Python/Node.js/Go/Rust)
2. Set up development environment
3. Implement Phase 1 script following JSON_SCHEMA.md
4. Test with sample organization
5. Validate with Cursor/Windsurf
6. Refine and iterate

## Resources

- GitHub API Docs: https://docs.github.com/rest
- Python: PyGithub, ghapi
- Node.js: Octokit
- Go: go-github
- Rust: octocrab
