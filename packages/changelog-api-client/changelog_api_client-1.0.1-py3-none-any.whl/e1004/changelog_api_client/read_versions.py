import argparse

from .cli_client import create_client
from .errors import handle_error


def run(args: argparse.Namespace) -> None:
    page_size = args.page_size
    page_token = args.page_token

    handle_error(create_client().read_versions, page_size, page_token)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "read-versions",
        help="Read existing versions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--page_size",
        nargs="?",
        type=int,
        default=4,
        help="number of versions per page",
    )
    parser.add_argument(
        "--page_token", nargs="?", help="Token for pagination", default=None
    )

    parser.set_defaults(func=run)
