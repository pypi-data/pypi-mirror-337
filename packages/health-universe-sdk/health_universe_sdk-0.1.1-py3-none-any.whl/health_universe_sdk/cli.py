import sys
from typing import Optional

import click

from health_universe_sdk.repo_utils import create_repo_from_template


@click.group()
def cli() -> None:
    """Health Universe CLI tools for streamlined development."""
    pass


@cli.command()
@click.option(
    "--private/--public", default=None, help="Make the repository private or public"
)
@click.option("--description", help="Description for the repository")
@click.argument("repo_name", required=False)
def init(
    repo_name: Optional[str], private: Optional[bool], description: Optional[str]
) -> None:
    """
    Create a new repository from the Health Universe tool template.

    Interactive prompts will be shown for any required values not provided as arguments.
    For repositories under organizations, use the format 'organization/repo-name'.
    """
    # Get repository name if not provided
    if not repo_name:
        repo_name = click.prompt("Enter name for the new repository")
    org = None
    if "/" in repo_name:
        org, repo_name = repo_name.split("/", 1)
        click.echo(f"Creating repository {repo_name} under organization {org}")
    if org is None and click.confirm(
        "Create repository under an organization?", default=False
    ):
        org = click.prompt("Enter organization name")
    try:
        repo_url = create_repo_from_template(
            repo_name=repo_name, private=private, description=description, org=org
        )

        click.secho(f"Repository created successfully: {repo_url}", fg="green")
        click.echo("You can clone it using:")
        click.secho(f"  git clone {repo_url}", fg="blue")
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg="red", err=True)
        sys.exit(1)


def main() -> None:
    """Entry point for the Health Universe CLI."""
    cli()


if __name__ == "__main__":
    main()
