# src/pilot_rules/main.py
import os
import shutil
import argparse
import sys
from pathlib import Path
from typing import Optional

# Third-party imports
import tomli
from rich.console import Console
from rich.markdown import Markdown

from devpilot import collector

# --- Import the refactored collector entry point ---


# --- Helper Functions for Scaffolding ---

def get_version() -> str:
    """
    Get the current version from pyproject.toml.
    Searches upwards from the current file's location.

    Returns:
        str: The current version number or a fallback.
    """
    try:
        # Start searching from the package directory upwards
        current_dir = Path(__file__).parent
        while current_dir != current_dir.parent: # Stop at root directory '/'
            pyproject_path = current_dir / "pyproject.toml"
            if pyproject_path.exists():
                print(f"DEBUG: Found pyproject.toml at {pyproject_path}") # Debug print
                with open(pyproject_path, "rb") as f:
                    pyproject_data = tomli.load(f)
                version = pyproject_data.get("project", {}).get("version", "0.0.0")
                if version != "0.0.0":
                    return version
                # If version is placeholder, keep searching upwards
            current_dir = current_dir.parent

        # If not found after searching upwards
        print("DEBUG: pyproject.toml with version not found.") # Debug print
        return "0.0.0" # Fallback if not found
    except Exception as e:
        print(f"DEBUG: Error getting version: {e}") # Debug print
        import traceback
        traceback.print_exc() # Print error during dev
        return "0.0.0" # Fallback on error


def display_guide(guide_path: Path) -> None:
    """
    Display the markdown guide using rich formatting.

    Args:
        guide_path: Path to the markdown guide file.
    """
    console = Console()
    if not guide_path.is_file():
        console.print(f"[red]Error: Guide file not found at '{guide_path}'[/red]")
        return

    try:
        with open(guide_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        markdown = Markdown(markdown_content)
        console.print("\n")
        console.rule("[bold blue]Getting Started Guide")
        console.print("\n")
        console.print(markdown)
        console.print("\n")
        console.rule("[bold blue]End of Guide")

    except Exception as e:
        console.print(f"[red]Error displaying guide '{guide_path}': {str(e)}[/red]")


def copy_template(template_type: str, root_dir: Path) -> Optional[Path]:
    """
    Copy template files based on the specified type ('cursor' or 'copilot').

    Args:
        template_type: Either 'cursor' or 'copilot'.
        root_dir: The root directory (usually CWD) where to copy the templates.

    Returns:
        Path to the relevant guide file if successful, None otherwise.
    """
    console = Console()
    package_dir = Path(__file__).parent # Directory where main.py is located
    templates_dir = package_dir / "templates"
    guides_dir = package_dir / "guides"

    source_dir: Optional[Path] = None
    target_dir: Optional[Path] = None
    guide_file: Optional[Path] = None

    if template_type == "cursor":
        source_dir = templates_dir / "cursor"
        target_dir = root_dir / ".cursor" # Target is relative to root_dir (CWD)
        guide_file = guides_dir / "cursor.md"
    elif template_type == "copilot":
        source_dir = templates_dir / "github"
        target_dir = root_dir / ".github" # Target is relative to root_dir (CWD)
        guide_file = guides_dir / "copilot.md"
    else:
        # This case should not be reached due to argparse mutual exclusion
        console.print(f"[red]Internal Error: Unknown template type '{template_type}'[/red]")
        return None

    if not source_dir or not source_dir.is_dir():
        console.print(f"[red]Error: Template source directory not found: '{source_dir}'[/red]")
        return None
    if not guide_file or not guide_file.is_file():
        console.print(f"[red]Error: Guide file not found: '{guide_file}'[/red]")
        # Decide whether to proceed without a guide or stop
        # return None # Stop if guide is essential

    # Create target directory if it doesn't exist
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        console.print(f"[red]Error: Could not create target directory '{target_dir}': {e}[/red]")
        return None

    # Copy the contents
    console.print(f"Copying {template_type} templates to '{target_dir}'...")
    try:
        for item in source_dir.iterdir():
            target_path = target_dir / item.name
            if item.is_file():
                shutil.copy2(item, target_path)
                # console.print(f"  Copied file: {item.name}") # Optional verbose logging
            elif item.is_dir():
                shutil.copytree(item, target_path, dirs_exist_ok=True)
                # console.print(f"  Copied directory: {item.name}") # Optional verbose logging
        console.print(f"[green]Successfully copied {template_type} templates.[/green]")
        return guide_file # Return path to guide file on success
    except Exception as e:
        console.print(f"[red]Error copying templates from '{source_dir}' to '{target_dir}': {e}[/red]")
        return None


# --- Main Application Logic ---

def main():
    """
    Entry point for the pilot-rules CLI application.
    Handles argument parsing and delegates tasks to scaffolding or collection modules.
    """
    console = Console()
    version = get_version()
    console.print(f"[bold blue]Pilot Rules v{version}[/bold blue]")
    console.print("[blue]www.whiteduck.de[/blue]") # Replace or remove if needed
    console.print()

    parser = argparse.ArgumentParser(
        description="Manage Pilot Rules templates or collect code for analysis.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # --- Mutually Exclusive Actions ---
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--cursor", action="store_true", help="Scaffold Cursor templates (.cursor)")
    action_group.add_argument("--copilot", action="store_true", help="Scaffold Copilot templates (.github)")
    action_group.add_argument("--collect", action="store_true", help="Collect code from the repository")

    # --- Options for Code Collection ---
    collect_group = parser.add_argument_group('Code Collection Options (used with --collect)')
    collect_group.add_argument(
        "--include",
        action="append",
        metavar="EXTS:FOLDER",
        help="Specify files to include. Format: 'ext1,ext2:./folder' or '*:.'."
             " Can be used multiple times. Default: 'py:.' if no includes provided."
    )
    collect_group.add_argument(
        "--exclude",
        action="append",
        metavar="EXTS_OR_*:PATTERN",
        help="Specify path patterns to exclude. Format: 'py:temp' or '*:node_modules'."
             " '*' matches any extension. Can be used multiple times."
    )
    collect_group.add_argument(
        "--output",
        default=None, # Default is handled inside the collector logic now
        metavar="FILEPATH",
        help=f"Path to the output Markdown file (default: '{collector.config.DEFAULT_OUTPUT_FILENAME}')"
    )
    collect_group.add_argument(
        "--config",
        metavar="TOML_FILE",
        help="Path to a .toml configuration file for collection settings."
    )

    args = parser.parse_args()

    # Root directory for scaffolding is the current working directory
    scaffold_root_dir = Path.cwd()
    guide_file_to_display: Optional[Path] = None

    try:
        if args.collect:
            console.print("[cyan]Starting code collection process...[/cyan]")
            # --- Call the refactored collector function ---
            # Errors within the collector (ValueError, etc.) will be caught below
            collector.run_collection(
                include_args=args.include,
                exclude_args=args.exclude,
                output_arg=args.output, # Pass CLI arg (can be None)
                config_arg=args.config
            )
            console.print("[green]Code collection process finished.[/green]")

        elif args.cursor:
            guide_file_to_display = copy_template("cursor", scaffold_root_dir)
            # Success/Error messages printed within copy_template

        elif args.copilot:
            guide_file_to_display = copy_template("copilot", scaffold_root_dir)
            # Success/Error messages printed within copy_template

        # Display guide only if scaffolding was successful and returned a guide path
        if guide_file_to_display:
            display_guide(guide_file_to_display)

    except FileNotFoundError as e:
         # Should primarily be caught within helpers now, but keep as fallback
         console.print(f"[red]Error: Required file or directory not found: {str(e)}[/red]", file=sys.stderr)
         exit(1)
    except ValueError as e: # Catch config errors propagated from collector
         console.print(f"[red]Configuration Error: {str(e)}[/red]", file=sys.stderr)
         exit(1)
    except Exception as e:
        # Catch-all for unexpected errors in main logic or propagated from helpers/collector
        console.print(f"[red]An unexpected error occurred: {str(e)}[/red]", file=sys.stderr)
        import traceback
        traceback.print_exc()
        exit(1)

# --- Standard Python entry point check ---
if __name__ == "__main__":
    main()