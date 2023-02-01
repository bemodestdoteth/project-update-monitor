from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from update import get_update
from config import print_n_log, send_notification, send_error_message
from db import create_coins_db, create_xangle_rebrand_db, create_xangle_swap_db, create_coindar_db, create_proxy_db, reset_proxy
import asyncio
import os

def main():
    os.chdir(os.path.dirname(__file__))
    asyncio.run(send_notification("Initializing..."))

    # Check db existence before beginning
    if not(os.path.isfile("coins.db")):
        print_n_log("No database detected. Creating new before moving on.")
        create_coins_db()
        create_xangle_swap_db()
        create_xangle_rebrand_db()
        create_coindar_db()
        create_proxy_db()

    # Reset previous proxy before moving on
    reset_proxy()
    get_update()
    '''
    scheduler = BlockingScheduler()
    scheduler.add_job(get_update, "interval", minutes=30, next_run_time=datetime.now())
    scheduler.start()    
    '''

if __name__ == "__main__":
    main()