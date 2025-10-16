# Workflow Documentation

## Overview

This document describes the end-to-end workflow for using the GitHub Organization Repository Indexer to create public-facing documentation.

## Prerequisites

### Phase 1 Requirements
- Python 3.8+ (or your chosen language)
- GitHub Personal Access Token with appropriate permissions:
  - `repo` (for private repos) or `public_repo` (for public repos only)
  - `read:org` (to read organization data)
  - `read:user` (to read user profiles)
- Internet connection to access GitHub API

### Phase 2 Requirements
- Cursor or Windsurf IDE installed
- The generated JSON file from Phase 1

## Detailed Workflow

### Step 1: Setup and Configuration

#### 1.1 Create GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Set appropriate scopes:
   - `public_repo` - Access public repositories
   - `read:org` - Read org and team membership, read org projects
   - `read:user` - Read user profile data
4. Copy the generated token
5. Store securely (never commit to repository)

#### 1.2 Configure Environment

Create a `.env` file (add to `.gitignore`):
```
GITHUB_TOKEN=ghp_your_token_here
GITHUB_ORG=your-org-name
OUTPUT_FILE=repositories.json
```

Or set environment variables:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
export GITHUB_ORG="your-org-name"
```

### Step 2: Phase 1 - Data Collection

#### 2.1 Run Collection Script

```bash
# Example command (syntax will depend on implementation)
python collect_repos.py --org your-org-name --output repositories.json
```

#### 2.2 Monitor Progress

The script should display:
- Total repositories found
- Current repository being processed
- Progress percentage
- Any errors or warnings
- Final summary

Example output:
```
Fetching repositories for organization: your-org-name
Found 42 repositories

Processing repositories:
[1/42] awesome-project ✓
[2/42] another-repo ✓
[3/42] experimental-tool ✓
...
[42/42] legacy-system ✓

Successfully processed: 41
Failed: 1
  - private-repo-no-access (403: Forbidden)

Output written to: repositories.json
```

#### 2.3 Verify Output

Check that `repositories.json` exists and is valid:
```bash
# Validate JSON
python -m json.tool repositories.json > /dev/null && echo "Valid JSON"

# View summary
jq '.metadata' repositories.json

# Count repositories
jq '.repositories | length' repositories.json
```

### Step 3: Phase 2 - Documentation Generation

#### 3.1 Prepare Cursor/Windsurf

1. Open Cursor or Windsurf
2. Open the output directory or create a new workspace
3. Have `repositories.json` accessible

#### 3.2 Use the Prompt Template

Copy the prompt from `PROMPT_TEMPLATE.md` and customize:

1. Replace `{ORGANIZATION_NAME}` with your organization name
2. Replace `{ORGANIZATION_DESCRIPTION}` with a brief description
3. Adjust categorization rules if needed
4. Add any specific requirements

#### 3.3 Submit to AI

1. Paste the customized prompt into Cursor/Windsurf
2. Attach or reference the `repositories.json` file
3. Let the AI analyze and generate the README

#### 3.4 Review and Refine

The AI will generate a draft README. Review for:
- Accuracy of categorization
- Completeness of information
- Clarity of presentation
- Proper linking
- Table of contents structure

Provide feedback to refine:
- "Move project X to the 'Core Infrastructure' section"
- "Add more detail about the licensing section"
- "Create a visual diagram showing project relationships"
- "Highlight archived projects more prominently"

#### 3.5 Finalize

Once satisfied:
1. Save the generated `README.md`
2. Review one final time
3. Commit to repository or publish as needed

### Step 4: Publishing (Optional)

#### 4.1 GitHub Repository

Create a dedicated repository for the index:
```bash
git init
git add README.md repositories.json
git commit -m "Initial repository index"
git remote add origin https://github.com/your-org/repo-index.git
git push -u origin main
```

#### 4.2 GitHub Pages

Enable GitHub Pages to create a website:
1. Go to repository Settings → Pages
2. Select source: main branch, / (root)
3. Optionally customize with a theme
4. Access at `https://your-org.github.io/repo-index/`

#### 4.3 Organization README

If you have an organization README:
1. Link to the full index
2. Include highlights or featured projects
3. Add navigation to the detailed repository index

### Step 5: Maintenance and Updates

#### 5.1 Regular Updates

Schedule regular runs to keep documentation current:

**Manual:**
```bash
# Run monthly or quarterly
python collect_repos.py --org your-org-name
# Then regenerate README with updated JSON
```

**Automated (GitHub Actions):**
```yaml
# .github/workflows/update-index.yml
name: Update Repository Index
on:
  schedule:
    - cron: '0 0 1 * *'  # First day of each month
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Collect repository data
        env:
          GITHUB_TOKEN: ${{ secrets.GH_TOKEN }}
        run: python collect_repos.py --org your-org-name
      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add repositories.json
          git commit -m "Update repository index" || exit 0
          git push
```

#### 5.2 Changelog Tracking

Track changes between runs:
```bash
# Save previous version
cp repositories.json repositories.previous.json

# Run new collection
python collect_repos.py --org your-org-name

# Compare (you could build a diff tool)
# - New repositories added
# - Repositories archived
# - Significant activity changes
# - License changes
```

## Troubleshooting

### Common Issues

#### Rate Limiting
**Problem:** GitHub API rate limit exceeded (5000 requests/hour for authenticated)

**Solution:**
- Use authenticated requests (increases limit)
- Implement caching
- Add delays between requests
- Use conditional requests (ETags)

#### Missing Data
**Problem:** Some fields are null or missing

**Solution:**
- Check token permissions
- Verify repository access
- Some data may legitimately be null (no license, no README)
- Log and continue processing

#### Large Organizations
**Problem:** Organization has 500+ repositories, taking too long

**Solution:**
- Implement parallel processing
- Filter repositories (exclude forks, archived, etc.)
- Process in batches
- Cache partial results

#### AI Context Limits
**Problem:** JSON file too large for Cursor/Windsurf context

**Solution:**
- Split into multiple files by category
- Process in batches (active repos first, then archived)
- Create summary JSON with essential fields only
- Use the full JSON as a reference file

## Best Practices

1. **Version Control**: Track both the script and generated documentation
2. **Documentation**: Keep this workflow updated as you refine the process
3. **Security**: Never commit tokens; use environment variables or secrets
4. **Validation**: Always validate JSON before using in Phase 2
5. **Backup**: Keep previous versions of generated documentation
6. **Transparency**: Include generation timestamp in README
7. **Iteration**: Refine prompt template based on results
8. **Collaboration**: Share findings with team, gather feedback

## Success Checklist

- [ ] GitHub token created with proper scopes
- [ ] Environment configured (token, org name)
- [ ] Phase 1 script runs without critical errors
- [ ] `repositories.json` is valid and complete
- [ ] Prompt template customized for organization
- [ ] README generated via Cursor/Windsurf
- [ ] Documentation reviewed for accuracy
- [ ] Published to appropriate location
- [ ] Update process documented/automated
- [ ] Team members can access and understand documentation

## Next Steps

After completing the initial workflow:

1. **Gather Feedback**: Share with stakeholders and collect input
2. **Iterate**: Refine categorization, add/remove sections
3. **Enhance**: Add visualizations, metrics, trends over time
4. **Automate**: Set up scheduled updates
5. **Expand**: Consider adding dependency graphs, security metrics, etc.
