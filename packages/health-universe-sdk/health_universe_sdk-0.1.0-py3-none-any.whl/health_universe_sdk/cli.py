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
@click.option(
    "--org", help="Optional organization under which to create the repository"
)
@click.argument("repo_name", required=False)
def init(
    repo_name: Optional[str],
    private: Optional[bool],
    description: Optional[str],
    org: Optional[str] = None,
) -> None:
    """Create a new repository from the Health Universe tool template.

    Interactive prompts will be shown for any required values not provided as arguments.
    """
    if not repo_name:
        repo_name = click.prompt("Enter name for the new repository")

    if private is None:
        private = click.confirm("Make repository private?", default=False)

    if description is None:
        description = click.prompt(
            "Enter repository description", default="", show_default=False
        )

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
