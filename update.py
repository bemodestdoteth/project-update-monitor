from datetime import datetime, timedelta
from db import get_all_coins
from dotenv import load_dotenv
from config import print_n_log, send_message, send_error_message
import asyncio
import time

from src import *
from src.brunch.brunch import brunch
from src.coindar.coindar import coindar
from src.github.github import github
from src.github_repo.github_repo import github_repo
from src.github_wiki.github_wiki import github_wiki
from src.icx_forum.icx_forum import icx_forum
from src.snx_blog.snx_blog import snx_blog
from src.mintscan.mintscan import mintscan
from src.xangle.xangle import xangle
from src.xangle.xangle_swap import xangle_swap
from src.xangle.xangle_rebrand import xangle_rebrand
from src.xtz_agora.xtz_agora import xtz_agora

load_dotenv()

def get_update():
    try:
        coins = get_all_coins()
        for coin in coins:
            print(coin)
            result = getattr(globals()[coin['source']](), "scrape")(coin)
            # result = scrape_func_selector(coin)
            if result is None:
                print_n_log("{} has no further updates".format(coin['name']))
            elif result == "Pass":
                print_n_log("Scraping {}: Not updated yet.".format(coin['name']))
            elif result == "New":
                print_n_log("A new data has been inserted into {}".format(coin['name']))                
            else:
                print_n_log("{} has some update. Sending via telegram message...".format(result['name']))
                asyncio.run(send_message(result))

        # 30 min cooldown after a successful scraping.
        print_n_log("Website updating job finished. Next job is projected at {}".format(datetime.strftime(datetime.now() + timedelta(minutes=30), format="%Y/%m/%d %H:%M:%S")))
    except Exception as e:
        asyncio.run(send_error_message(coin["name"], e))

if __name__ == "__main__":
    get_update()