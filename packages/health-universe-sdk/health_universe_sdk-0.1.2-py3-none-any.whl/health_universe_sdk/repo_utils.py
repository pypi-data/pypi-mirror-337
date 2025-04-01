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
    """
    Create a new repository from the Health-Universe tool template using GitHub CLI.

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
    while True:  # Loop until successful creation or user cancellation
        try:
            # Get GitHub CLI version
            gh_version = _get_gh_version()

            # Create the repository using GitHub CLI
            visibility = "--private" if private else "--public"
            desc_arg: List[str] = ["-d", description] if description else []

            # Version-specific handling
            if gh_version >= (2, 69, 0):
                # New format: use org/repo-name syntax
                full_repo_name = f"{org}/{repo_name}" if org else repo_name
                cmd = [
                    "gh",
                    "repo",
                    "create",
                    full_repo_name,
                    "--template=Health-Universe/tool-template",
                    visibility,
                ] + desc_arg
            else:
                # Legacy format: use --org flag
                cmd = [
                    "gh",
                    "repo",
                    "create",
                    repo_name,
                    "--template=Health-Universe/tool-template",
                    visibility,
                ] + desc_arg

                # Add org flag if needed
                if org:
                    cmd.extend(["--org", org])

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            # Extract the repository URL from the output
            for line in result.stdout.splitlines():
                if line.startswith("https://"):
                    return line.strip()

            # Fallback if URL not found in output
            if org:
                return f"https://github.com/{org}/{repo_name}"
            else:
                return f"https://github.com/{os.getenv('GITHUB_USER', '')}/{repo_name}"

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)

            # Check if the error is due to a repository name that already exists
            if "Name already exists on this account" in error_msg:
                click.secho(
                    f"Repository '{repo_name}' already exists on your account.",
                    fg="yellow",
                )
                if click.confirm(
                    "Would you like to try a different name?", default=True
                ):
                    repo_name = click.prompt("Enter a new repository name")
                    # Continue the loop with the new name
                else:
                    # User chose not to try again, exit
                    click.secho("Repository creation cancelled.", fg="red")
                    sys.exit(1)
            else:
                # Different error, show it and exit
                click.secho(f"Error creating repository: {error_msg}", fg="red")
                sys.exit(1)

        except Exception as e:
            click.secho(f"Error: {str(e)}", fg="red")
            sys.exit(1)


def _get_gh_version() -> tuple:
    """Get the installed GitHub CLI version.

    Returns:
        A tuple of version components (major, minor, patch)

    Raises:
        SystemExit: If GitHub CLI is not installed or version cannot be determined
    """
    try:
        result = subprocess.run(
            ["gh", "--version"], check=True, capture_output=True, text=True
        )

        # Parse version from output (typically "gh version X.Y.Z")
        for line in result.stdout.splitlines():
            if line.startswith("gh version"):
                version_str = line.split("version")[1].strip()
                # Parse version into components
                components = version_str.split(".")
                if len(components) >= 3:
                    return tuple(int(x) for x in components[:3])

        # If we couldn't parse the version properly, return a safe default
        click.secho(
            "Warning: Could not determine GitHub CLI version. Using legacy command format.",
            fg="yellow",
        )
        return 0, 0, 0

    except (subprocess.SubprocessError, FileNotFoundError):
        click.secho(
            "Error: GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/",
            fg="red",
        )
        sys.exit(1)
