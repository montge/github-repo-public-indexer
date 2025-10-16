# Cursor/Windsurf Prompt Template

## Purpose

This template provides a structured prompt to use with Cursor or Windsurf AI assistants for generating the final README documentation from the JSON metadata file.

## How to Use

1. Copy the prompt below
2. Replace all placeholders in `{CURLY_BRACES}` with your specific values:
   - `{ORGANIZATION_NAME}` - Your GitHub organization name
   - `{TARGET_REPO_NAME}` - Name of the repository where README will be stored
   - `{TARGET_REPO_URL}` - Full URL to the target repository
   - `{CREATE_OR_UPDATE}` - Either "create" or "update"
   - `{ORGANIZATION_DESCRIPTION}` - Brief description of your organization
   - `{EXISTING_README_INSTRUCTIONS}` - See "Existing README Scenarios" below
   - `{ADD_ANY_SPECIFIC_REQUIREMENTS}` - Any custom requirements
3. If updating an existing README, attach BOTH the current README.md AND repositories.json
4. Paste into Cursor or Windsurf
5. Review and refine the generated output

### Existing README Scenarios

**Scenario 1: Creating a new README (no existing file)**
```
{EXISTING_README_INSTRUCTIONS} =
"This is a new README. Create it from scratch following the structure below."
```

**Scenario 2: Updating an existing README**
```
{EXISTING_README_INSTRUCTIONS} =
"An existing README.md is attached, along with the previous repositories.json for comparison.

Please:
1. Compare the two JSON files to identify changes (new repos, archived repos, significant activity changes)
2. Update the README while preserving:
   - The introduction and organizational context
   - The 'How to Contribute' section
   - The 'Code of Conduct' link
   - Any other sections that don't contain repository listings
3. Update all repository data, statistics, and the generation timestamp
4. Optionally add a 'Recent Changes' section highlighting major updates since the last generation"
```

**Scenario 3: Major overhaul of existing README**
```
{EXISTING_README_INSTRUCTIONS} =
"An existing README.md is attached but it needs significant restructuring. Review it for any valuable custom content or context, but feel free to reorganize completely based on the new data. Preserve only critical custom sections."
```

---

## PROMPT TEMPLATE

```
I have a JSON file containing metadata about all repositories in the {ORGANIZATION_NAME} GitHub organization. I need you to {CREATE_OR_UPDATE} a comprehensive, public-facing README.md file that documents these repositories in a clear, organized, and easy-to-navigate format.

**Target Repository:** {TARGET_REPO_NAME}
**Repository URL:** {TARGET_REPO_URL}

## About the Organization

{ORGANIZATION_DESCRIPTION}

Example: "We are an open-source community focused on data science tools and educational resources. Our repositories range from production-ready libraries to experimental prototypes and archived legacy projects."

## Existing README Handling

{EXISTING_README_INSTRUCTIONS}

**If creating a NEW README:**
- Start fresh with the structure outlined below
- Use all data from repositories.json

**If UPDATING an existing README:**
- Review the existing README.md carefully
- **If available**, compare the new `repositories.json` with the previous version to identify:
  - New repositories added
  - Repositories that were archived or removed
  - Significant changes in activity (stars, last updated)
  - License changes
- Preserve any manual sections NOT related to repository listings (e.g., "Contributing", "Code of Conduct", "How to Use This Index", custom introductions)
- Update the repository listings based on the new repositories.json
- Update statistics and metadata (generation date, total count)
- Maintain the existing categorization scheme if it's working well, or propose improvements
- Flag any repositories that were in the old README but are missing from the new data
- Preserve any special formatting or customizations that don't conflict with the data
- **Consider adding a "What's New" or "Recent Changes" section** if significant changes occurred

**Important for Updates:**
- Do NOT remove custom sections added manually (look for sections that reference things not in repositories.json)
- Do NOT change the overall tone or voice if a specific style has been established
- DO update all repository-specific information (names, descriptions, stats, URLs)
- DO add new repositories that appear in repositories.json
- DO remove or mark as "No longer available" repositories that are missing from the new data
- DO preserve any hand-crafted introductions or organizational context
- DO note the previous data file timestamp if comparing old vs new JSON

## Input Data

The file `repositories.json` contains structured metadata for each repository including:
- Basic information (name, description, URLs, dates)
- Status (archived, fork, template, etc.)
- Activity metrics (stars, forks, commits, contributors)
- Languages and technology stack
- License information
- Topics/tags
- README previews
- Ownership and POC information (contributors, teams, CODEOWNERS)

## Requirements for the README

### 1. Structure and Organization

Create a well-organized README with:

**Header Section:**
- Title: "{ORGANIZATION_NAME} - Repository Index"
- Brief introduction about the organization
- Badges (optional): ![Last Updated](https://img.shields.io/badge/Last%20Updated-{date}-blue) ![Total Repos](https://img.shields.io/badge/Total%20Repos-{count}-green)
- Last updated timestamp (from metadata.generated_at)
- Total repository count
- Navigation/Table of Contents
- Quick note: "📚 This is an automatically generated index of our public repositories"

**Repository Categories:**
Organize repositories into logical categories. Suggested categories:

- **Active Projects** - Recently updated (within 60 days), not archived
- **Core Infrastructure** - Essential tools and libraries (based on stars/usage)
- **Experimental/Prototypes** - Low activity or marked with experimental topics
- **Archived Projects** - Status: archived
- **Forks** - Repositories that are forks
- **Templates** - Template repositories

You may refine these categories based on the actual data.

**For Each Repository, Include:**
- **Name** (linked to GitHub URL)
- **Description** (from basic_info.description)
- **Status Badges**: Create badge-like indicators for:
  - Archived status
  - License type
  - Primary language
  - Star count (if significant)
- **Key Metrics**: Stars, forks, last activity
- **Topics/Tags**: Display repository topics
- **Point of Contact**: Top contributor(s) or CODEOWNERS
- **Quick Summary**: First 1-2 sentences from README preview

### 2. Visual Design

Use Markdown effectively:
- Tables for structured data
- Emoji/icons for status indicators (⭐ for stars, 📦 for archived, etc.)
- Collapsible sections for detailed information
- Horizontal rules to separate major sections
- Consistent formatting throughout

### 3. Special Sections

**Overview Dashboard:**
Create a high-level summary with:
- Total repositories by status (active/archived)
- Most popular projects (by stars)
- Recently updated projects
- Language distribution summary
- License distribution

**Quick Find:**
- Table of all repositories sorted alphabetically
- Table sorted by activity (stars/recent updates)
- Filter by language or topic

**License Compliance:**
- Group repositories by license
- Highlight unlicensed repositories
- Summary of license types used

**Points of Contact:**
- Index of main contributors across projects
- Team ownership mapping

### 4. Metadata and Transparency

Include at the bottom:

**About This Document Section:**
Create a clear section explaining:
```markdown
## About This Document

This repository index is automatically generated using the [GitHub Organization Repository Indexer](https://github.com/montge/github-repo-public-indexer).

**Generation Details:**
- **Generated:** {metadata.generated_at}
- **Total Repositories:** {metadata.total_repositories}
- **Indexer Version:** {metadata.tool_version}
- **Data Source:** GitHub API v{metadata.github_api_version}

**How It Works:**
1. The indexer collects metadata from all repositories in the {ORGANIZATION_NAME} organization
2. Data is compiled into a structured JSON file
3. This README is generated from that data using AI assistance

**Data Files:**
- [Raw JSON Data](./repositories.json) - Complete repository metadata
- [Indexer Tool](https://github.com/montge/github-repo-public-indexer) - Open source under Apache 2.0
```

**Contributing Section:**
Include guidelines for updating the index:
```markdown
## Contributing

### Updating This Index

This repository index is automatically generated. To update it:

1. **Request an Update:** Open an issue requesting a refresh of the repository index
2. **Report Inaccuracies:** If you notice outdated or incorrect information, please open an issue
3. **Automated Updates:** This index is typically regenerated [monthly/quarterly/as-needed]

### Contributing to Listed Projects

To contribute to any of the repositories listed here:
1. Visit the repository's GitHub page
2. Review the repository's CONTRIBUTING.md (if available)
3. Check open issues or contact the repository maintainers
4. Follow the project's contribution guidelines

### Suggesting Improvements

Have suggestions for how this index could be more useful? We welcome feedback!
- Open an issue with your suggestions
- Describe what information would be helpful
- Suggest new categorizations or organization schemes
```

**Footer/Credits:**
```markdown
---

**Generated with:** [GitHub Organization Repository Indexer](https://github.com/montge/github-repo-public-indexer)
**License:** This index document is provided as-is for informational purposes. Individual repositories maintain their own licenses.
**Maintained by:** {ORGANIZATION_NAME}

See [CONTRIBUTING.md](./CONTRIBUTING.md) for information about updating this index or reporting issues.
```

**CONTRIBUTING.md File:**
Also generate a CONTRIBUTING.md file using the template from:
https://github.com/montge/github-repo-public-indexer/blob/main/CONTRIBUTING_TEMPLATE.md

Customize it with:
- Organization name
- Update frequency
- Link to Code of Conduct (if applicable)
- Contact information

### 5. Navigation and Usability

- Clear table of contents at the top
- Anchor links for easy navigation
- Consistent naming and structure
- Mobile-friendly formatting
- Search-friendly (clear headings, keywords)

## Style Guidelines

- **Tone**: Professional but approachable
- **Clarity**: Prioritize readability over completeness
- **Consistency**: Use the same format for all similar items
- **Brevity**: Summaries should be concise; details in collapsible sections
- **Accuracy**: Use data directly from JSON; don't invent information

## Additional Customization

{ADD_ANY_SPECIFIC_REQUIREMENTS}

Examples:
- "Highlight repositories related to machine learning with a special section"
- "Include a visual chart showing commit activity over time"
- "Create a 'Getting Started' guide for new contributors"
- "Add a section for project dependencies and relationships"

## Output

Generate a complete README.md file following the requirements above. Format it using proper Markdown syntax so it's ready to commit to a GitHub repository.

Please analyze the repositories.json file and create the documentation now.
```

---

## Customization Options

### Option 1: Focus on Specific Repository Types

Add to the prompt:
```
Pay special attention to repositories tagged with {SPECIFIC_TOPIC} and create a dedicated section highlighting these projects.
```

### Option 2: Include Visualizations

Add to the prompt:
```
Create Mermaid diagrams to visualize:
- Repository relationships and dependencies
- Organization structure (teams and ownership)
- Technology stack distribution
```

### Option 3: Comparison and Trends

Add to the prompt:
```
If there's a previous version of repositories.json (as repositories.previous.json), create a "What's Changed" section highlighting:
- New repositories added
- Repositories that were archived
- Significant activity increases
- License changes
```

### Option 4: External Stakeholder Focus

Add to the prompt:
```
This README is intended for external stakeholders and potential contributors. Emphasize:
- How to get involved and contribute
- Beginner-friendly projects
- Projects actively seeking contributors
- Community guidelines and contacts
```

### Option 5: Internal Team Focus

Add to the prompt:
```
This README is for internal team members. Include:
- Deployment status and environments
- Internal documentation links
- Ownership and on-call information
- Maintenance status and tech debt notes
```

## Example Follow-up Prompts

After the initial generation, refine with:

### Reorganization
```
Move the "Experimental Projects" section earlier in the document, right after "Active Projects"
```

### Adding Details
```
For each repository in the "Core Infrastructure" section, add information about:
- Production usage
- Dependent projects
- Deployment frequency
```

### Formatting Changes
```
Convert the "License Compliance" section from a list to a table with columns:
Repository | License | SPDX ID | Link
```

### Visual Enhancements
```
Add emoji indicators for each repository:
- 🟢 Active (updated within 30 days)
- 🟡 Stable (updated within 6 months)
- 🟠 Inactive (updated over 6 months ago)
- ⚫ Archived
```

### Additional Sections
```
Create a new section called "Featured Projects" that highlights the top 5 repositories by stars and includes:
- Detailed description
- Key features from README
- Getting started guide
- Link to documentation
```

## Advanced Usage: Multi-Stage Generation

For very large organizations (100+ repos), consider a multi-stage approach:

### Stage 1: Summary README
```
Create a high-level summary README (no more than 500 lines) that includes:
- Overview and statistics
- Top 20 repositories by activity
- Category summaries (count and brief description)
- Links to detailed category pages
```

### Stage 2: Detailed Category Pages
```
For the "Active Projects" category, create a detailed ACTIVE_PROJECTS.md file with complete information about each repository in this category.
```

### Stage 3: Index and Cross-References
```
Create an alphabetical index (INDEX.md) of all repositories with:
- Repository name
- One-line description
- Link to main README section
- Tags for quick filtering
```

## Validation Checklist

After generation, verify:

- [ ] All repository names are linked correctly
- [ ] No broken internal links
- [ ] Table of contents matches actual sections
- [ ] Dates are formatted consistently
- [ ] License information is accurate
- [ ] POC information is present and accurate
- [ ] No placeholder text remains (TODO, FIXME, etc.)
- [ ] Markdown renders correctly on GitHub
- [ ] Mobile-friendly formatting
- [ ] Statistics in overview match repository count
- [ ] All categories have at least one repository or are marked as empty

## Tips for Best Results

1. **Be Specific**: The more context about your organization, the better the categorization
2. **Iterate**: Generate, review, then refine with follow-up prompts
3. **Examples**: If you have a preferred style, show an example repository section
4. **Constraints**: Specify any size limits (e.g., "keep under 1000 lines")
5. **Audience**: Clearly state who will read this (external users, internal team, investors, etc.)
6. **Updates**: Keep the prompt template updated based on what works well

## Troubleshooting

### AI says file is too large
- Split JSON into category-specific files
- Generate sections separately and combine manually
- Use summary JSON with essential fields only

### Inconsistent formatting
- Provide an example of the exact format desired
- Ask for regeneration with stricter formatting rules
- Use follow-up prompts to fix specific sections

### Missing information
- Verify the JSON contains the data
- Explicitly request the field in the prompt
- Check if the AI has context limits

### Wrong categorization
- Provide explicit categorization rules
- Give examples of which repos belong where
- Use repository topics/tags to guide categorization

## Complete Example: Creating New README

```
I have a JSON file containing metadata about all repositories in the Acme Corp GitHub organization. I need you to create a comprehensive, public-facing README.md file that documents these repositories in a clear, organized, and easy-to-navigate format.

**Target Repository:** acme-public-repos
**Repository URL:** https://github.com/acme/acme-public-repos

## About the Organization

Acme Corp is a technology company building open-source tools for developers. Our repositories include production-ready libraries, command-line tools, and experimental prototypes. We focus on developer experience and automation.

## Existing README Handling

This is a new README. Create it from scratch following the structure below.

**If creating a NEW README:**
- Start fresh with the structure outlined below
- Use all data from repositories.json

[... rest of prompt template ...]
```

## Complete Example: Updating Existing README

```
I have a JSON file containing metadata about all repositories in the Acme Corp GitHub organization. I need you to update a comprehensive, public-facing README.md file that documents these repositories in a clear, organized, and easy-to-navigate format.

**Target Repository:** acme-public-repos
**Repository URL:** https://github.com/acme/acme-public-repos

## About the Organization

Acme Corp is a technology company building open-source tools for developers. Our repositories include production-ready libraries, command-line tools, and experimental prototypes. We focus on developer experience and automation.

## Existing README Handling

An existing README.md is attached. Please review it and update the repository information while preserving:
- The introduction and organizational context
- The "How to Contribute" section
- The "Support" section with contact information
- The "Code of Conduct" link
- Any other sections that don't contain repository listings

Update all repository data (names, descriptions, stars, last updated dates), statistics, and the generation timestamp. If you notice the categorization could be improved, propose changes but ask before making major structural changes.

**If UPDATING an existing README:**
- Review the existing README.md carefully
- Preserve any manual sections NOT related to repository listings
- Update the repository listings based on repositories.json
- Update statistics and metadata (generation date, total count)
- Maintain the existing categorization scheme if it's working well
- Flag any repositories that were in the old README but are missing from the new data
- Preserve any special formatting or customizations

[... rest of prompt template ...]

**Files attached:**
- repositories.json (new data from latest collection)
- repositories.previous.json (previous version for comparison)
- README.md (current version to update)

Note: If you don't have a previous JSON file, just attach the new one and current README.
```
