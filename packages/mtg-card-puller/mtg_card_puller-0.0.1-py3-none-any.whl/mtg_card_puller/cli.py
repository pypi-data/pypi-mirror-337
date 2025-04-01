"""Console script for mtg_card_puller."""

import sys
import click
from mtg_card_puller import mtg_card_puller

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-v", "--verbose", is_flag=True, help="Enable verbose output for debugging"
)
@click.option(
    "-f", "--file", type=str, required=True, help="Path to the file containing card names"
)
def main(verbose, file):
    """Console script for mtg_card_puller."""
    mtg_card_puller.main(deck_file=file) 
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
