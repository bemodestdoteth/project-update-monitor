from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Import file from parent directory
from pathlib import Path
import os
import sys
os.chdir(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))
sys.path.append(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))

from db import get_coin, update_post
from config import prior_setup_playwright
import json

class icx_forum:
    def __init__(self) -> None:
        pass

    @prior_setup_playwright
    def scrape(coin, user_agent):
        # Storing post
        base_url = "https://mintscan.io"

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(user_agent=user_agent)
            page.set_viewport_size({"width": 750, "height": 1334})

            page.goto(coin['link'])
            page.wait_for_selector('span.topic-title')

            # Topmost Proposal
            latest_proposal = {
                'title' : page.query_selector('span.topic-title').inner_text(),
                'link': base_url + page.query_selector('a.search-link').get_attribute('href')
            }
            print(latest_proposal)

        # First time scraping
        if coin["post"] == "":
            update_post(latest_proposal, coin['name'])
            return "New"
        elif json.loads(coin["post"]) == latest_proposal:
            return None
        else:
            update_post(latest_proposal, coin['name'])

            # Return post to send telegram message
            latest_proposal['name'] = coin['name']
            return latest_proposal

# Testing code
if __name__ == "__main__":
    icx_forum.scrape(icx_forum, get_coin("ICX"))