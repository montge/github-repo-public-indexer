#!/usr/bin/env python3
"""
GitHub Organization Repository Indexer - Phase 1 Data Collection

Collects metadata for all repositories in a GitHub organization and generates
a structured JSON file for documentation generation.

Copyright 2025

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import logging
from typing import Optional

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table

from src.github_client import GitHubClient
from src.metadata_collector import MetadataCollector
from src.json_generator import JSONGenerator
from src import __version__

# Load environment variables
load_dotenv()

# Setup rich console
console = Console()


def setup_logging(verbose: bool = False):
    """Configure logging with rich handler."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


@click.command()
@click.option("--org", "-o", envvar="GITHUB_ORG", required=True, help="GitHub organization name")
@click.option(
    "--token", "-t", envvar="GITHUB_TOKEN", required=True, help="GitHub personal access token"
)
@click.option(
    "--github-url",
    "-u",
    envvar="GITHUB_URL",
    default=None,
    help="GitHub API base URL (for GitHub Enterprise Server, "
    "e.g., https://github.example.com/api/v3)",
)
@click.option(
    "--output",
    "-f",
    default="repositories.json",
    envvar="OUTPUT_FILE",
    help="Output JSON file path",
)
@click.option(
    "--max-contributors", default=5, type=int, help="Maximum number of top contributors to include"
)
@click.option("--include-forks/--no-forks", default=True, help="Include forked repositories")
@click.option(
    "--include-archived/--no-archived", default=True, help="Include archived repositories"
)
@click.option("--backup/--no-backup", default=True, help="Backup existing output file")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--summary", is_flag=True, help="Show summary after collection")
def main(
    org: str,
    token: str,
    github_url: Optional[str],
    output: str,
    max_contributors: int,
    include_forks: bool,
    include_archived: bool,
    backup: bool,
    verbose: bool,
    summary: bool,
):
    """
    GitHub Organization Repository Indexer - Phase 1

    Collects comprehensive metadata for all repositories in a GitHub organization
    and generates a structured JSON file for documentation generation.

    Examples:
        # GitHub.com
        collect_repos.py --org myorg --token ghp_xxx --output repos.json

        # GitHub Enterprise Server
        collect_repos.py --org myorg --token ghp_xxx --github-url https://github.example.com/api/v3
    """
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    # Display header
    header_text = f"[bold blue]GitHub Organization Repository Indexer[/bold blue]\n"
    header_text += f"Version {__version__}\n"
    header_text += f"Phase 1: Data Collection"
    if github_url:
        header_text += f"\n[yellow]GitHub URL:[/yellow] {github_url}"

    console.print(Panel.fit(header_text, border_style="blue"))

    try:
        # Initialize components
        logger.info("Initializing GitHub client...")
        github_client = GitHubClient(token, base_url=github_url)

        metadata_collector = MetadataCollector(max_contributors=max_contributors)
        json_generator = JSONGenerator(tool_version=__version__)

        # Fetch repositories
        console.print(
            f"\n[yellow]Fetching repositories for organization:[/yellow] [bold]{org}[/bold]"
        )
        repositories = github_client.get_all_repositories(
            org, include_forks=include_forks, include_archived=include_archived
        )

        if not repositories:
            console.print("[red]No repositories found![/red]")
            sys.exit(1)

        console.print(f"[green]Found {len(repositories)} repositories[/green]\n")

        # Collect metadata for each repository
        repository_data = []
        failed_repos = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Collecting metadata...", total=len(repositories))

            for repo in repositories:
                try:
                    progress.update(task, description=f"[cyan]Processing: {repo.full_name}")

                    metadata = metadata_collector.collect_repository_metadata(repo)
                    repository_data.append(metadata)

                    progress.advance(task)

                except Exception as e:
                    logger.error(f"Failed to process {repo.full_name}: {e}")
                    failed_repos.append({"name": repo.full_name, "error": str(e)})
                    progress.advance(task)

        # Generate output
        console.print("\n[yellow]Generating JSON output...[/yellow]")
        json_generator.generate_output(
            org_name=org, repositories=repository_data, output_file=output, backup_previous=backup
        )

        # Display summary
        console.print(f"\n[bold green]✓ Collection complete![/bold green]")

        summary_table = Table(show_header=False, box=None)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")

        summary_table.add_row("Successfully processed", str(len(repository_data)))
        summary_table.add_row("Failed", str(len(failed_repos)))
        summary_table.add_row("Output file", output)

        console.print(summary_table)

        # Show failed repositories if any
        if failed_repos:
            console.print("\n[yellow]Failed repositories:[/yellow]")
            for failed in failed_repos:
                console.print(f"  [red]×[/red] {failed['name']}: {failed['error']}")

        # Show detailed summary if requested
        if summary and repository_data:
            console.print("\n[bold cyan]Repository Summary:[/bold cyan]")
            summary_data = json_generator.create_summary(output)

            # Status breakdown
            console.print("\n[yellow]Status Breakdown:[/yellow]")
            status_table = Table(show_header=False, box=None)
            status_table.add_column("Status", style="cyan")
            status_table.add_column("Count", justify="right", style="green")

            for status, count in summary_data["status_breakdown"].items():
                status_table.add_row(status.title(), str(count))

            console.print(status_table)

            # Top languages
            if summary_data["top_languages"]:
                console.print("\n[yellow]Top Languages:[/yellow]")
                lang_table = Table(show_header=False, box=None)
                lang_table.add_column("Language", style="cyan")
                lang_table.add_column("Count", justify="right", style="green")

                for lang, count in list(summary_data["top_languages"].items())[:5]:
                    lang_table.add_row(lang, str(count))

                console.print(lang_table)

            # Top starred
            if summary_data["top_starred"]:
                console.print("\n[yellow]Top Starred Repositories:[/yellow]")
                for repo in summary_data["top_starred"]:
                    console.print(f"  ⭐ {repo['stars']:>4} - {repo['name']}")

        # Next steps
        console.print(f"\n[bold cyan]Next Steps:[/bold cyan]")
        console.print(f"1. Review the generated file: [green]{output}[/green]")
        console.print(f"2. Use [green]PROMPT_TEMPLATE.md[/green] with Cursor/Windsurf")
        console.print(f"3. Generate your documentation README")

        # Check rate limit
        github_client.check_rate_limit()

        sys.exit(0 if not failed_repos else 1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
