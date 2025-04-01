import os
import sys
import typer
from ailabel.db.crud import get_all_topics


def print_debug_info():
    """Print debug information about the application configuration."""
    from pathlib import Path
    from ailabel.db.database import data_dir, sqlite_url
    from ailabel.lib.llms import Models

    # Get API key and mask it for security
    api_key = os.environ.get("GEMINI_API_KEY", "")
    masked_key = api_key[:4] + "*" * (len(api_key) - 4) if api_key else "Not set"

    typer.echo("=== AILabel Debug Information ===")
    typer.echo(f"Python version: {sys.version}")
    typer.echo(f"Database location: {data_dir}")
    typer.echo(f"Database URL: {sqlite_url}")
    typer.echo(f"Gemini API Key: {masked_key}")

    # Show configured models
    typer.echo("\nConfigured Gemini models:")
    for model in Models:
        typer.echo(f"  {model.name}: {model.value}")

    # Count existing database records
    try:
        topics_count = len(get_all_topics())
        typer.echo(f"\nDatabase status: {topics_count} topics defined")
    except Exception as e:
        typer.echo(f"\nDatabase status: Error accessing database - {e}")

    # Show environment and file paths
    typer.echo("\nEnvironment:")
    typer.echo(f"  Working directory: {os.getcwd()}")
    typer.echo(f"  Python executable: {sys.executable}")

    # Check for .env file
    env_file = Path(".env.secret")
    env_exists = env_file.exists()
    typer.echo(f"  .env.secret file: {'Found' if env_exists else 'Not found'}")
