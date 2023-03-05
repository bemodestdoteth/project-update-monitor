from bs4 import BeautifulSoup
import requests

# Import file from parent directory
from pathlib import Path
import json
import os
import sys
os.chdir(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))
sys.path.append(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))

from db import get_coin, update_post
from config import prior_setup_bs4, print_n_log

class coindar:
    def __init__(self) -> None:
        pass

    @prior_setup_bs4
    def scrape(coin, user_agent):
        # Storing posts
        base_url = 'https://coindar.org'

        # Make request to site
        s = requests.Session()

        html = s.get(coin["link"], headers={"User-Agent": user_agent}, verify=False, timeout=50)
        soup = BeautifulSoup(html.text, 'html.parser')

        latest_release = {
            'title' : soup.select_one('h2 span').text + ": " + soup.select_one('h3 a').text.strip(),
            'link': base_url + soup.select_one('h3 a')["href"]
        }
        print(latest_release)
        s.close()

        # First time scraping
        if coin["post"] == "":
            update_post(latest_release, coin['name'])
            return "New"
        elif json.loads(coin["post"]) == latest_release:
            return None
        else:
            update_post(latest_release, coin['name'])
            # Return post to send telegram message
            latest_release['name'] = coin['name']
            return latest_release

# Testing code
if __name__ == "__main__":
    coindar.scrape(get_coin("COINDAR HARD FORK DISCLOSURE"))