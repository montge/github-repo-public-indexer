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

### Step 3: Prepare Target Repository

The target repository is where your generated README.md will be published.

#### Option A: Existing Repository

```bash
# Clone your existing public-facing repository
cd /path/to/your/workspace
git clone git@github.com:yourorg/your-public-repos-index.git
cd your-public-repos-index

# Copy the generated JSON file here
cp /path/to/github-repo-public-indexer/repositories.json .
```

#### Option B: New Repository

```bash
# Create new repository on GitHub first, then:
cd /path/to/your/workspace
mkdir my-org-public-repos
cd my-org-public-repos
git init
git remote add origin git@github.com:yourorg/my-org-public-repos.git

# Copy the generated JSON file here
cp /path/to/github-repo-public-indexer/repositories.json .

# Create initial commit structure
echo "# Organization Repository Index" > README.md
git add README.md repositories.json
git commit -m "Initial setup"
git branch -M main
git push -u origin main
```

**Important:** The indexer tool does NOT clone the repositories it's indexing. It uses the GitHub API to fetch metadata, so you don't need local copies of all your org's repos.

### Step 4: Phase 2 - Documentation Generation

#### 4.1 Prepare Cursor/Windsurf

1. Open Cursor or Windsurf
2. **Open the target repository directory** (where README will be published)
3. Ensure `repositories.json` is in this directory

#### 4.2 Use the Prompt Template

Copy the prompt from `PROMPT_TEMPLATE.md` and customize:

1. Replace `{ORGANIZATION_NAME}` with your organization name
2. Replace `{TARGET_REPO_NAME}` with your target repository name
3. Replace `{TARGET_REPO_URL}` with the target repository URL
4. Replace `{CREATE_OR_UPDATE}` with "create" or "update"
5. Replace `{ORGANIZATION_DESCRIPTION}` with a brief description
6. Replace `{EXISTING_README_INSTRUCTIONS}` based on your scenario:
   - **New README**: "This is a new README. Create it from scratch."
   - **Updating existing**: List sections to preserve
7. Adjust categorization rules if needed
8. Add any specific requirements

#### 4.3 Submit to AI

**For a NEW README:**
1. Paste the customized prompt into Cursor/Windsurf
2. Attach or reference the `repositories.json` file
3. Let the AI analyze and generate the README

**For UPDATING an existing README:**
1. Paste the customized prompt into Cursor/Windsurf
2. Attach BOTH files:
   - `repositories.json` (new data)
   - `README.md` (existing file to update)
3. Let the AI analyze and update the README

#### 4.4 Review and Refine

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

#### 4.5 Finalize and Commit

After reviewing the generated/updated README:

```bash
# In your target repository directory
git add README.md

# If you're also publishing the JSON file
git add repositories.json

# Commit the changes
git commit -m "Update repository index - $(date +%Y-%m-%d)"

# Push to GitHub
git push
```

#### 4.6 Verify on GitHub

Visit your repository URL to see the published README:
```
https://github.com/yourorg/your-public-repos-index
```

Once satisfied:
1. Save the generated `README.md`
2. Review one final time
3. Commit to repository or publish as needed

### Step 5: Publishing Options (Optional)

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

## Recommended Directory Structure

Here's how to organize your workspace:

```
/your-workspace/
├── github-repo-public-indexer/          # This tool (cloned from GitHub)
│   ├── collect_repos.py
│   ├── src/
│   ├── .env                             # Your credentials (git-ignored)
│   ├── repositories.json                # Generated here (git-ignored)
│   └── ...
│
└── my-org-public-repos/                 # Your public-facing index repo
    ├── README.md                        # Generated/updated by Cursor/Windsurf
    ├── repositories.json                # Copied from indexer (optional to publish)
    └── .github/
        └── workflows/
            └── update-index.yml         # Optional: automation
```

**Workflow:**
1. Run `collect_repos.py` in the indexer tool directory
2. Copy `repositories.json` to your public repo
3. Use Cursor/Windsurf in the public repo to generate/update README
4. Commit and push the public repo

### Step 6: Maintenance and Updates

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
