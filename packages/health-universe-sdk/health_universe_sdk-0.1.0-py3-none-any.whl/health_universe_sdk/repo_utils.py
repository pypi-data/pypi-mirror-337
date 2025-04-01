import os
import subprocess
import sys
from typing import List, Optional

import click


def create_repo_from_template(
    repo_name: str,
    private: bool = False,
    description: str = "",
    org: Optional[str] = None,
) -> str:
    """Create a new repository from the Health-Universe tool template using GitHub CLI.

    Args:
        repo_name: Name of the repository to create
        private: Whether the repository should be private (default: False)
        description: Description of the repository (default: "")
        org: Optional organization under which to create the repository (default: None)

    Returns:
        URL of the created repository

    Raises:
        SystemExit: If the repository creation fails
    """
    while True:
        try:
            _check_gh_cli_installed()
            visibility = "--private" if private else "--public"
            desc_arg: List[str] = ["-d", description] if description else []
            full_repo_name = f"{org}/{repo_name}" if org else repo_name

            cmd = [
                "gh",
                "repo",
                "create",
                full_repo_name,
                "--template=Health-Universe/tool-template",
                visibility,
            ] + desc_arg

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if line.startswith("https://"):
                    return line.strip()
            if org:
                return f"https://github.com/{org}/{repo_name}"
            else:
                return f"https://github.com/{os.getenv('GITHUB_USER', '')}/{repo_name}"

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            if "Name already exists on this account" in error_msg:
                click.secho(
                    f"Repository '{repo_name}' already exists on your account.",
                    fg="yellow",
                )
                if click.confirm(
                    "Would you like to try a different name?", default=True
                ):
                    repo_name = click.prompt("Enter a new repository name")
                else:
                    click.secho("Repository creation cancelled.", fg="red")
                    sys.exit(1)
            else:
                click.secho(f"Error creating repository: {error_msg}", fg="red")
                sys.exit(1)

        except Exception as e:
            click.secho(f"Error: {str(e)}", fg="red")
            sys.exit(1)


def _check_gh_cli_installed() -> None:
    """Check if GitHub CLI is installed and exit if not.

    Raises:
        SystemExit: If GitHub CLI is not installed
    """
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True, text=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        click.secho(
            "Error: GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/",
            fg="red",
        )
        sys.exit(1)
