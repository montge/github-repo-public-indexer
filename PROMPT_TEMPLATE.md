# Cursor/Windsurf Prompt Template

## Purpose

This template provides a structured prompt to use with Cursor or Windsurf AI assistants for generating the final README documentation from the JSON metadata file.

## How to Use

1. Copy the prompt below
2. Replace all placeholders in `{CURLY_BRACES}` with your specific values
3. Paste into Cursor or Windsurf
4. Attach or reference the `repositories.json` file
5. Review and refine the generated output

---

## PROMPT TEMPLATE

```
I have a JSON file containing metadata about all repositories in the {ORGANIZATION_NAME} GitHub organization. I need you to create a comprehensive, public-facing README.md file that documents these repositories in a clear, organized, and easy-to-navigate format.

## About the Organization

{ORGANIZATION_DESCRIPTION}

Example: "We are an open-source community focused on data science tools and educational resources. Our repositories range from production-ready libraries to experimental prototypes and archived legacy projects."

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
- Last updated timestamp (from metadata.generated_at)
- Total repository count
- Navigation/Table of Contents

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
- Generation date and time
- Data collection method
- Link to the raw JSON file (if published)
- How to request updates or corrections
- Tool version used

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
