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

class xangle_swap:
    def __init__(self) -> None:
        pass

    @prior_setup_playwright
    def scrape(coin, user_agent):
        base_url = "https://xangle.io"

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(user_agent=user_agent)
            page.goto(coin['link'])
            page.wait_for_selector('.title.mb3.ellipse', timeout=60000, state="attached")

            # Topmost Proposal
            latest_proposal = {
                'title' : page.query_selector('.title.mb3.ellipse').inner_text(),
                'link': base_url + page.query_selector('.list-content-mobile.mb8').get_attribute('href')
            }

            page.goto(latest_proposal['link'])
            page.wait_for_selector('.project-symbol', timeout=60000, state="attached")
            latest_proposal['title'] = page.query_selector('.project-symbol').inner_text() + ": " + latest_proposal['title']
            print(latest_proposal)
        
        # First time scraping
        if coin["post"] == "":
            update_post(latest_proposal, coin['name'])
            return "New"
        elif json.loads(coin["post"]) == latest_proposal:
            return None
        else:
            # Return post to send telegram message
            update_post(latest_proposal, coin['name'])
            latest_proposal['name'] = coin['name']
            return latest_proposal

# Testing code
if __name__ == "__main__":
    xangle_swap.scrape(get_coin("XANGLE TOKEN SWAP DISCLOSURE"))