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

class xtz_agora:
    def __init__(self) -> None:
        pass

    @prior_setup_playwright
    def scrape(coin, user_agent):
        # Storing post
        base_url = "https://www.tezosagora.org"

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(user_agent=user_agent)
            page.set_viewport_size({"width": 750, "height": 1334})

            page.goto(coin['link'])
            page.wait_for_selector('div._agoraSelect_95594')

            # Open proposal combobox
            page.locator('div._agoraSelect_95594').click()
            page.wait_for_selector('div._agoraSelect__menu__item_95594')

            current_proposal = page.query_selector('div._agoraSelect__menu__item_95594').inner_text()
            latest_proposal = {
                'title' : current_proposal,
                'link': "{}/period/{}".format(base_url, current_proposal[:2])
            }

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
    xtz_agora.scrape(get_coin("XTZ"))