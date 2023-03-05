from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from update import get_update
from config import print_n_log, send_notification
from db import create_coins_db
import asyncio
import os

def main():
    os.chdir(os.path.dirname(__file__))
    asyncio.run(send_notification("Initializing..."))

    # Check db existence before beginning
    if not(os.path.isfile("coins.db")):
        print_n_log("No database detected. Creating new before moving on.")
        create_coins_db()

    # Create a new scheduler
    scheduler = BlockingScheduler()

    # Schedule the function to run every 30 minutes
    scheduler.add_job(get_update, 'interval', minutes=30, next_run_time=datetime.now())

    # Start the scheduler
    scheduler.start()

if __name__ == "__main__":
    main()