import json
from typing import Optional

import typer

from labtasker.client.cli.task import app
from labtasker.client.core.cli_utils import cli_utils_decorator, parse_filter
from labtasker.client.core.logging import set_verbose, stdout_console, verbose_print

from .impl import get_counts

# For a simpler version, you may refer to 'simple' git branch

# To customize command, you simply register your cmd function using Typer app
# For example, if you wish to implement a sub-command of "task", i.e. labtasker task my-command
# you import sub Typer app from labtasker.client.cli.task and register your command with @app.command()
# The Labtasker automatically loads the module from "project.entry-points" defined in pyproject.toml
# For more information, refer to https://setuptools.pypa.io/en/latest/userguide/entry_point.html
# and https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/


@app.command()
@cli_utils_decorator
def count(
    limit: int = 100,
    extra_filter: Optional[str] = typer.Option(
        None,
        "--extra-filter",
        "-f",
        help='Optional mongodb filter as a dict string (e.g., \'{"$and": [{"metadata.tag": {"$in": ["a", "b"]}}, {"priority": 10}]}\'). '
        'Or a Python expression (e.g. \'metadata.tag in ["a", "b"] and priority == 10\')',
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output.",
        callback=set_verbose,
        is_eager=True,
    ),
):
    """Give a brief summary of the numbers of tasks in each status."""
    extra_filter = parse_filter(extra_filter)
    verbose_print(f"Parsed filter: {json.dumps(extra_filter, indent=4)}")

    result = get_counts(limit=limit, extra_filter=extra_filter)

    fmt_status = {
        "pending": "🟡 Pending",
        "running": "🔵 Running",
        "success": "🟢 Success",
        "failed": "🔴 Failed",
        "cancelled": "⚪ Cancelled",
    }

    for status, cnt in result.items():
        stdout_console.print(f"{fmt_status[status]}: {cnt}")
