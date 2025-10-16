# GitHub Organization Repository Indexer - Specification

## Project Overview

A two-phase tool designed to create a comprehensive, public-facing documentation of all repositories within a GitHub organization. The tool automates the discovery, analysis, and documentation of repositories to share knowledge about project existence, purpose, status, licensing, and ownership.

## Problem Statement

Organizations often have multiple repositories scattered across GitHub with varying levels of documentation. It's difficult to:
- Understand what repositories exist and their purposes
- Identify repository status (active, archived, experimental)
- Track licensing information
- Determine points of contact (POCs) based on ownership and membership
- Create a unified, accessible view for external stakeholders

## Solution Architecture

### Two-Phase Approach

**Phase 1: Metadata Collection (Automated Script)**
- Fetch all repositories from a GitHub organization using GitHub API
- Collect metadata for each repository
- Generate a structured JSON file containing all repository information

**Phase 2: Documentation Generation (AI-Assisted via Cursor/Windsurf)**
- Use the JSON file as input to a prompt
- AI analyzes the data and generates human-readable README
- Creates organized, easy-to-navigate documentation

### Why Two Phases?

1. **API Rate Limits**: Separating data collection allows for caching and reuse
2. **Scalability**: Large organizations may have hundreds of repos; analyzing separately is more manageable
3. **Flexibility**: JSON intermediate format allows for different documentation outputs
4. **AI Context Limits**: Processing one repo at a time through Cursor/Windsurf is more reliable than bulk analysis

## Requirements

### Functional Requirements

#### Phase 1 - Data Collection Script

1. **GitHub API Integration**
   - Authenticate with GitHub API (personal access token or GitHub App)
   - Fetch all repositories for a specified organization
   - Handle pagination for organizations with many repositories
   - Respect rate limits

2. **Metadata Collection**
   For each repository, collect:
   - **Basic Info**: Name, description, URL, creation date, last updated date
   - **Status**: Is archived, is fork, is template, default branch
   - **Activity**: Star count, fork count, open issues count, last commit date
   - **Languages**: Primary language, language breakdown
   - **License**: License type (SPDX identifier if available)
   - **Topics/Tags**: Repository topics for categorization
   - **README Preview**: First few lines or summary of README.md
   - **Ownership**: Repository owner, contributors (top N), teams with access

3. **POC Identification**
   - Repository owner/creator
   - Top contributors by commit count
   - Teams with admin/maintain access
   - CODEOWNERS file information (if present)

4. **Output Format**
   - Generate well-structured JSON file
   - Include metadata about the collection (timestamp, organization, total repos)
   - Validate JSON schema before writing

5. **Error Handling**
   - Handle API errors gracefully
   - Log repositories that fail to fetch
   - Continue processing remaining repositories on individual failures

#### Phase 2 - Documentation Generation

1. **Input Processing**
   - Read JSON file from Phase 1
   - Validate structure

2. **Prompt Engineering**
   - Provide clear instructions to Cursor/Windsurf
   - Include context about organization and purpose
   - Specify desired README structure

3. **Documentation Output**
   - Organized by category or status
   - Easy navigation (table of contents, links)
   - Clear indication of status (active, archived, experimental)
   - License information prominently displayed
   - POC contact information
   - Quick summary/overview section

### Non-Functional Requirements

1. **Performance**
   - Phase 1 script should handle 100+ repositories efficiently
   - Implement caching where appropriate

2. **Security**
   - Never commit GitHub tokens to repository
   - Use environment variables or secure credential storage
   - Handle private repository data appropriately (if accessing)

3. **Maintainability**
   - Clear code structure and comments
   - Configurable settings (org name, output path, token source)
   - Easy to update when GitHub API changes

4. **Usability**
   - Simple command-line interface
   - Progress indicators during execution
   - Clear error messages

## Data Model

See `JSON_SCHEMA.md` for detailed structure.

## Workflow

### Phase 1 Execution
```
1. Configure script with organization name and credentials
2. Run data collection script
3. Script outputs: repositories.json
4. Review JSON for completeness
```

### Phase 2 Execution
```
1. Open Cursor/Windsurf in the output directory
2. Provide repositories.json to AI
3. Use prompt template (see PROMPT_TEMPLATE.md)
4. AI generates README.md
5. Review and refine as needed
```

## Success Criteria

1. Script successfully retrieves metadata for all repositories in organization
2. JSON output is valid and contains all required fields
3. Generated README is clear, organized, and easy to navigate
4. POC information is accurate and useful
5. License information is correctly identified
6. Tool can be rerun to update documentation as organization evolves

## Future Enhancements

- Automated scheduling (GitHub Actions) to regenerate documentation weekly/monthly
- Integration with organization wikis or GitHub Pages
- Comparison between runs to show changes over time
- Support for multiple organizations
- Export to different formats (Markdown, HTML, PDF)
- Dashboard/web UI for browsing repositories
- Integration with project management tools
