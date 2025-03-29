import hashlib
import random

import requests

from bs4 import BeautifulSoup


def seed(dry_run=False):
    """
    Get or set a random seed.

    Args:
        dry_run (bool): Should we seed the underlying random module, or just get a seed?

    Returns: (str): The sha256 used as the seed.
    """
    resp = requests.get("https://libraryofbabel.info/random.cgi")
    soup = BeautifulSoup(resp.content, features="lxml")
    try:
        blob = soup.css.select("#textblock")[0].get_text().strip()
        seed_hash = hashlib.sha256(blob.encode()).hexdigest()
    except Exception:
        raise ValueError("Failed to get meta seed")

    if not dry_run:
        random.seed(blob)

    return seed_hash


def main():
    print(seed(dry_run=True))


if __name__ == "__main__":
    main()
