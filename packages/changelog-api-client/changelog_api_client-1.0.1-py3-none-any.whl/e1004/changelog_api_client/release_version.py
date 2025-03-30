import argparse
from datetime import UTC, date, datetime

from .cli_client import create_client
from .errors import handle_error


def run(args: argparse.Namespace) -> None:
    version_number = args.version_number
    released_at = args.released_at
    handle_error(create_client().release_version, version_number, released_at)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "release-version",
        help="Release a version.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("version_number", help="'major.minor.patch'")
    parser.add_argument(
        "--released_at",
        type=date.fromisoformat,
        help="YYYY-MM-DD",
        default=datetime.now(tz=UTC).date(),
    )

    parser.set_defaults(func=run)
