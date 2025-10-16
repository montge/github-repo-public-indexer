# GitHub Repository Metadata

This file contains the recommended metadata for the GitHub repository page.

## Repository Description

```
Automated tool to index and document all repositories in a GitHub organization. Two-phase process: collect metadata via API, generate public-facing README with AI.
```

## About Section Topics (Keywords)

Recommended topics for GitHub repository:
- `github-api`
- `repository-indexer`
- `documentation-generator`
- `github-organization`
- `metadata-collection`
- `python`
- `automation`
- `ci-cd`
- `repository-documentation`
- `open-source`

## Website URL

```
https://github.com/montge/github-repo-public-indexer
```

## Setting These on GitHub

### Via Web Interface:
1. Go to repository settings
2. Find "About" section (top right of repository page)
3. Click the gear icon ⚙️
4. Add the description
5. Add website URL
6. Add topics (press Enter after each one)
7. Check "Releases" and "Packages" if applicable
8. Save changes

### Via GitHub CLI:
```bash
# Update description
gh repo edit montge/github-repo-public-indexer \
  --description "Automated tool to index and document all repositories in a GitHub organization. Two-phase process: collect metadata via API, generate public-facing README with AI."

# Add topics
gh repo edit montge/github-repo-public-indexer \
  --add-topic github-api \
  --add-topic repository-indexer \
  --add-topic documentation-generator \
  --add-topic github-organization \
  --add-topic metadata-collection \
  --add-topic python \
  --add-topic automation \
  --add-topic ci-cd \
  --add-topic repository-documentation \
  --add-topic open-source
```

## Social Preview Image (Optional)

Consider creating a custom social preview image (1280x640px) showing:
- Tool name/logo
- Brief description
- Key features or workflow diagram
- Upload in Settings → Social preview
