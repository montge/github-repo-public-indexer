# GitHub Organization Repository Indexer

A two-phase tool for creating comprehensive, public-facing documentation of all repositories within a GitHub organization.

## Quick Start

```bash
# 1. Setup this indexer tool
./setup.sh
# Edit .env with your credentials

# 2. Collect repository metadata
source venv/bin/activate
python collect_repos.py --summary
# Generates: repositories.json

# 3. Prepare your public-facing repository
cd ../my-org-public-repos  # Your target repo
cp ../github-repo-public-indexer/repositories.json .

# 4. Generate README with Cursor/Windsurf
# - Open Cursor/Windsurf in the target repo directory
# - Use PROMPT_TEMPLATE.md with repositories.json
# - Review and commit the generated README.md
```

**Important:** The tool fetches metadata via GitHub API - no need to clone all your org's repositories.

See **[USAGE.md](USAGE.md)** and **[WORKFLOW.md](WORKFLOW.md)** for detailed instructions.

## Overview

### The Problem
Organizations with multiple GitHub repositories often lack centralized, up-to-date documentation showing:
- What repositories exist and their purposes
- Current status (active, archived, experimental)
- Licensing information
- Points of contact and ownership
- Technology stacks and dependencies

### The Solution
A **two-phase automated approach**:

**Phase 1: Data Collection**
- Script fetches all repository metadata via GitHub API
- Generates structured JSON file with comprehensive information
- Handles pagination, rate limits, and errors gracefully

**Phase 2: Documentation Generation**
- JSON file is provided to Cursor/Windsurf AI assistant
- AI analyzes data and generates human-readable README
- Organized, categorized, and easy-to-navigate documentation

### Why Two Phases?
- **Separation of concerns**: Data collection vs. presentation
- **Reusability**: JSON can be used for multiple outputs
- **Flexibility**: Different documentation styles from same data
- **Context management**: Avoid AI context limits
- **Caching**: Avoid re-fetching data during iteration

## Project Status

- [x] Requirements gathering
- [x] Specification documentation
- [x] JSON schema design
- [x] Workflow documentation
- [x] Prompt template creation
- [x] **Phase 1 script implementation (Python)**
- [ ] Testing with sample organization
- [ ] Phase 2 validation with Cursor/Windsurf
- [ ] Refinement and optimization
- [ ] Production deployment

## Documentation

### Quick References
- **[USAGE.md](USAGE.md)** - Installation and usage guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - One-page summary
- **[CLAUDE.md](CLAUDE.md)** - Guide for Claude Code development

### Design and Architecture
- **[SPECIFICATION.md](SPECIFICATION.md)** - Full project scope and requirements
- **[JSON_SCHEMA.md](JSON_SCHEMA.md)** - Output data structure
- **[WORKFLOW.md](WORKFLOW.md)** - End-to-end process guide

### Phase 2 Documentation Generation
- **[PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md)** - Template for Cursor/Windsurf
- **[CONTRIBUTING_TEMPLATE.md](CONTRIBUTING_TEMPLATE.md)** - Template CONTRIBUTING.md for index repositories

## Implementation Details

### Phase 1 (Implemented)
Python-based data collection tool with:
- **GitHub API Client** (`src/github_client.py`) - Authentication and rate limiting
- **Metadata Collector** (`src/metadata_collector.py`) - Extracts comprehensive repo data
- **JSON Generator** (`src/json_generator.py`) - Creates validated output
- **CLI Interface** (`collect_repos.py`) - User-friendly command-line tool with progress bars

Key features:
- Automatic rate limit handling
- Graceful error recovery
- Rich console output with progress tracking
- Configurable via CLI options or environment variables
- JSON validation and backup
- **GitHub Enterprise Server support** - Works with custom GitHub instances

### Next Steps

1. **Test with Your Organization**
   ```bash
   python collect_repos.py --org your-org-name --summary
   ```

2. **Generate Documentation**
   - Use `PROMPT_TEMPLATE.md` with Cursor/Windsurf
   - Attach the generated `repositories.json`
   - Review and refine the output

3. **Automate Updates**
   - Schedule regular runs (weekly/monthly)
   - Track changes over time
   - Keep documentation current

## Use Cases

- **Open Source Projects**: Share your organization's repositories with the community
- **Internal Teams**: Document internal tools and libraries
- **Compliance**: Track licensing across all repositories
- **Onboarding**: Help new team members discover existing projects
- **Portfolio**: Showcase your organization's work
- **Archival**: Document repository history and evolution

## Technology Stack

- **Python 3.8+**
- **PyGithub** - GitHub API client
- **Click** - CLI framework
- **Rich** - Beautiful terminal output
- **python-dotenv** - Environment management

## Contributing

Contributions welcome! Please:
- Follow the architecture in SPECIFICATION.md
- Ensure JSON output matches JSON_SCHEMA.md
- Add tests for new features
- Update documentation

## Future Enhancements

- Parallel processing for large organizations
- API response caching
- Diff tool to compare runs
- GitHub Actions automation
- Web dashboard interface
- Multi-organization support

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please open an issue.
