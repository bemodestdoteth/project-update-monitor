from datetime import datetime, timedelta
from db import get_all_coins
from dotenv import load_dotenv
from config import print_n_log, send_message, send_error_message
import asyncio
import time

from src.github.github import github_scrape
from src.github_repo.github_repo import github_repo_scrape
from src.github_wiki.github_wiki import github_wiki_scrape
from src.icx_forum.icx_forum import icx_forum_scrape
from src.mintscan.mintscan import mintscan_scrape
from src.snx_blog.snx_blog import snx_blog_scrape
from src.xtz_agora.xtz_agora import xtz_agora_scrape
from src.xangle.xangle import xangle_scrape
from src.xangle.xangle_token_swap import xangle_token_swap_scrape
from src.xangle.xangle_token_rebrand import xangle_token_rebrand_scrape
from src.coindar.coindar import coindar_scrape

load_dotenv()

def scrape_func_selector(coin):
    try:
        if coin['source'] == "github-release":
            return github_scrape(coin)
        elif coin['source'] == "github-repo":
            return github_repo_scrape(coin)
        elif coin['source'] == "icx-forum":
            return icx_forum_scrape(coin)
        elif coin['source'] == "github-wiki":
            return github_wiki_scrape(coin)
        elif coin['source'] == "mintscan":
            return mintscan_scrape(coin)
        elif coin['source'] == "snx-blog":
            return snx_blog_scrape(coin)
        elif coin['source'] == "xangle":
            return xangle_scrape(coin)
        elif coin['source'] == "xtz-agora":
            return xtz_agora_scrape(coin)
        else:
            return "Pass"
    except Exception as e:
        raise Exception(e)
def get_update():
    try:
        while True:
            coins = get_all_coins()
            for coin in coins:
                result = scrape_func_selector(coin)
                if result is None:
                    print_n_log("{} has no further updates".format(coin['name']))
                elif result == "Pass":
                    print_n_log("Scraping {}: Not updated yet.".format(coin['name']))
                elif result == "New":
                    print_n_log("A new data has been inserted into {}".format(coin['name']))                
                else:
                    print_n_log("{} has some update. Sending via telegram message...".format(result['name']))
                    asyncio.run(send_message(result))

            # Look for xangle updates after looking through each token
            result = coindar_scrape({
                "name": "COINDAR HARD FORK DISCLOSURE",
                "link": "https://coindar.org/en/search?page=1&text=&start=2021-12-04&cats=10&im=&rs=0&fav=0&coins=&cap_from=0&cap_to=9999999999999&vol_from=0&vol_to=9999999999999&ex=1312&sort=1&order=1",
                "selector": ".bc-insight-list-item-wrapper"})
            if result is not None:
                asyncio.run(send_message(result))

            result = xangle_token_swap_scrape({
                "name": "TOKEN SWAP DISCLOSURE",
                "link": "https://xangle.io/insight/disclosure?category=token_swap",
                "selector": ".bc-insight-list-item-wrapper"})
            if result is not None:
                asyncio.run(send_message(result))

            result = xangle_token_rebrand_scrape({
                "name": "TOKEN REBRAND DISCLOSURE",
                "link": "https://xangle.io/insight/disclosure?category=token_rebranding",
                "selector": ".bc-insight-list-item-wrapper"})
            if result is not None:
                asyncio.run(send_message(result))

            # 30 min cooldown after a successful scraping.
            print_n_log("Website updating job finished. Next job is projected at {}".format(datetime.strftime(datetime.now() + timedelta(minutes=30), format="%Y/%m/%d %H:%M:%S")))
            time.sleep(1800)
    except Exception as e:
        print_n_log(e)
        asyncio.run(send_error_message(coin["name"], e))

# Test Function
if __name__ == "__main__":
    get_update()