# Contributing to the Repository Index

Thank you for your interest in improving our repository index!

## About This Repository

This repository contains an automatically generated index of all public repositories in the **{ORGANIZATION_NAME}** organization. It serves as a central directory to help people discover and understand our projects.

## How to Contribute

### Reporting Issues

If you notice any problems with the index, please open an issue:

- **Outdated Information:** Repository data is stale or incorrect
- **Missing Repository:** A public repository is not listed
- **Categorization:** A repository is in the wrong category
- **Broken Links:** Links don't work as expected
- **Display Issues:** Formatting or rendering problems

### Requesting an Update

The repository index is generated from live GitHub data. To request a refresh:

1. Open an issue with the title "Request Index Update"
2. Optionally note any specific repositories that need attention
3. A maintainer will regenerate the index from current data

**Note:** Updates are typically performed {UPDATE_FREQUENCY} (e.g., monthly, quarterly, on-demand).

### Suggesting Improvements

We welcome suggestions for making this index more useful:

- **New Sections:** Propose additional information to include
- **Better Organization:** Suggest alternative categorization schemes
- **Additional Metrics:** Request specific data points to track
- **Visualization:** Ideas for charts, diagrams, or other visual aids

Please open an issue describing your suggestion in detail.

## How the Index is Generated

This index is created using the [GitHub Organization Repository Indexer](https://github.com/montge/github-repo-public-indexer):

1. **Phase 1 - Data Collection:**
   - A script queries the GitHub API for all organization repositories
   - Comprehensive metadata is collected (stars, forks, languages, licenses, etc.)
   - Data is saved to `repositories.json`

2. **Phase 2 - Documentation Generation:**
   - The JSON file is processed by an AI assistant (Cursor/Windsurf)
   - A formatted README.md is generated with categorization and organization
   - Manual review and refinement as needed

3. **Publishing:**
   - The updated README.md is committed to this repository
   - Changes are tracked in version control

## Updating the Index Yourself

If you have maintainer access and want to regenerate the index:

### Prerequisites
- Python 3.8+
- GitHub personal access token with `read:org` scope

### Steps

```bash
# Clone the indexer tool
git clone https://github.com/montge/github-repo-public-indexer.git
cd github-repo-public-indexer

# Install dependencies
./setup.sh
source venv/bin/activate

# Run data collection
python collect_repos.py --org {ORGANIZATION_NAME} --token YOUR_TOKEN --summary

# This generates repositories.json
# Copy it to your index repository
cp repositories.json /path/to/{INDEX_REPO_NAME}/

# Follow Phase 2 instructions in PROMPT_TEMPLATE.md to regenerate README
```

See the [full workflow documentation](https://github.com/montge/github-repo-public-indexer/blob/main/WORKFLOW.md) for details.

## Contributing to Listed Projects

If you want to contribute to one of the repositories listed in this index:

1. Visit the repository's page (click the repository name in the index)
2. Check for a CONTRIBUTING.md file in that repository
3. Review open issues and pull requests
4. Follow the repository's specific contribution guidelines
5. Contact the repository maintainers if you have questions

Each repository has its own contribution process, maintainers, and guidelines.

## Code of Conduct

This project follows {ORGANIZATION_NAME}'s Code of Conduct. Please be respectful and constructive in all interactions.

{LINK_TO_CODE_OF_CONDUCT}

## Questions?

For questions about:
- **The index itself:** Open an issue in this repository
- **Specific projects:** Contact that project's maintainers
- **The indexer tool:** Open an issue at https://github.com/montge/github-repo-public-indexer

## License

This index document and associated metadata are provided as-is for informational purposes. Individual repositories maintain their own licenses as indicated in their listings.

The [GitHub Organization Repository Indexer](https://github.com/montge/github-repo-public-indexer) tool is licensed under Apache 2.0.

---

Thank you for helping make our repository index better! 🙏
