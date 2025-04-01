#!/usr/bin/env python

"""Tests for `mtg_card_puller` package."""

from mtg_card_puller import mtg_card_puller
from mtg_card_puller import cli
from click.testing import CliRunner
import pytest


@pytest.fixture
def test_deck_data():
    """Load sample data

    Load the sample data file in the data folder to test with
    """
    with open('tests/data/sample_deck.txt', 'r') as f:
        yield f 

card_id_cases = [
    ("1 Mr. House, President and CEO (PIP) 7 *F*", "PIP", 7),
    ("1 Arcane Signet (M3C) 283", "M3C", 283),
    ("1 Arid Mesa (MH2) 244", "MH2", 244),
    ("1 Attempted Murder (UNF) 66 *F*", "UNF", 66),
    ("1 Automated Artificer (NEO) 239 *F*", "NEO", 239),
    ("1 Bag of Devouring (AFC) 21", "AFC", 21),
    ("1 Barbarian Class (AFR) 131", "AFR", 131),
    ("1 Battlefield Forge (C21) 278", "C21", 278),
    ("1 Bennie Bracks, Zoologist (NCC) 86", "NCC", 86),
    ("1 Berserker's Frenzy (AFC) 29", "AFC", 29),
    ("1 Big Score (SNC) 102 *F*", "SNC", 102),
    ("1 Blood Crypt (RNA) 245", "RNA", 245),
    ("1 Bloodstained Mire (KTK) 230", "KTK", 230),
    ("1 Boros Signet (SLD) 291 *E*", "SLD", 291),
    ("1 Brazen Dwarf (AFR) 134", "AFR", 134),
]

def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2
    assert "Missing option '-f'" in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Console script for mtg_card_puller' in help_result.output

@pytest.mark.parametrize("card_line, expected_series, expected_number", card_id_cases)
def test_extract_card_id(card_line, expected_series, expected_number):
    assert mtg_card_puller.extract_card_id(card_line)[1:] == (expected_series, expected_number)

