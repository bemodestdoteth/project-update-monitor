from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from update import get_update, send_error_message
from config import print_n_log
from db import create_coins_db, create_xangle_rebrand_db, create_xangle_swap_db, create_coindar_db, create_noti_db, create_proxy_db
import os

def main():
    # Check db existence before beginning
    if not(os.path.isfile("coins.db")):
        print_n_log("No database detected. Creating new before moving on.")
        create_coins_db()
        create_xangle_swap_db()
        create_xangle_rebrand_db()
        create_coindar_db()
        create_proxy_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(get_update, "interval", minutes=30, next_run_time=datetime.now())
    scheduler.start()

if __name__ == "__main__":
    main()