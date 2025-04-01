"""Main module."""

import re
import tqdm
import requests
import time
from pathlib import Path
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

def extract_card_id(mox_full_name: str) -> Tuple[str, str, int]:
    """Extracts the card ID from the full name of a card.

    Args:
        mox_full_name (str): The full name of the card.

    Returns:
        Tuple[str, str, int]: A tuple containing the card name, card series, and card number.
    """
    # Extract the card ID using regex
    card_name = ""
    card_series = ""
    card_number = ""
    match = re.search(r'\d (.*) \(([A-Z0-9]{3})\) (\d{1,3})', mox_full_name)
    if match:
        card_name = match.group(1)
        card_series = match.group(2)
        card_number = int(match.group(3))

        logger.debug(f"Extracted card series: {card_series}, card number: {card_number} from full name: {mox_full_name}")
    else:
        raise ValueError("Problem matching card ID from full name: " + mox_full_name)

    return card_name, card_series, card_number

def execute_request(card_name: str, card_series: str, card_number: int) -> None:
    """Executes a request to the MTG API to fetch card details.

    Args:
        card_name (str): The name of the card.
        card_series (str): The card series.
        card_number (int): The card number.
    """
    normalized_name = card_name.strip(".'").replace(" ", "_")
    headers = {'User-Agent': 'mtg_card_puller', 'Accept': '*/*'}

    # Check if the image already exists
    img_path = Path(f"{normalized_name}.png")
    if img_path.is_file():
        logger.info(f"Image for {card_name} already exists, skipping download.")
        return

    time.sleep(0.1) # Avoid hitting the API too fast
    r = requests.get(f"https://api.scryfall.com/cards/{card_series}/{card_number}", headers=headers)
    if r.status_code != 200:
        logger.error(f"Failed to fetch card details for {card_name} ({card_series} {card_number})")
        return

    img_url = r.json().get('image_uris', {}).get('png')

    time.sleep(0.1) # Avoid hitting the API too fast
    r = requests.get(img_url, stream=True, headers=headers)
    if r.status_code != 200:
        logger.error(f"Failed to fetch image for {card_name} ({card_series} {card_number})")
        return

    # Save the image to a file
    with open(f"{normalized_name}.png", 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)


def main(deck_file: str, verbose: bool = False) -> None:
    """Main entrypoint for the script
    
    Args:
        deck_file (str): Path to the file containing card names.
        verbose (bool): Enable verbose output for debugging.
    """
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    with open(deck_file, 'r') as f:
        pbar = tqdm.tqdm(f.readlines(), desc="Processing cards", colour="green", unit="card")
        for line in pbar:
            try:
                card_name, card_series, card_number = extract_card_id(line.strip())
                pbar.set_description(f"Fetching {card_name[:20]:20}")
            except ValueError as e:
                logger.error(e)

            try:
                execute_request(card_name, card_series, card_number)
                # time.sleep(1)

            except Exception as e:
                logger.error(f"Error fetching card details: {e}")
                continue


