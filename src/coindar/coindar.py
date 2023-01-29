from bs4 import BeautifulSoup
import requests

# Import file from parent directory
from pathlib import Path
import os
import sys
os.chdir(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))
sys.path.append(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))

from config import prior_setup_bs4, print_n_log
from datetime import datetime
from datetime import timedelta
import calendar
import sqlite3

def empty_database():
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    db_records = cur.execute("SELECT name FROM coindar").fetchall()
    con.close()
    if len(db_records) == 0:
        return True
    else:
        return False
def insert(coins):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    cur.execute("INSERT INTO coindar VALUES (?, ?, ?, ?, ?)", coins)
    con.commit()
    con.close()
@prior_setup_bs4
def coindar_scrape(coin, proxy, user_agent):
    '''
    Scrapes the site change database accordingly
    
    Parameters:
        coin (str) -- Name of the coin
    '''
    # Storing posts[i]
    base_url = 'https://coindar.org'

    # Make request to site
    s = requests.Session()

    html = s.get(coin["link"], proxies={"http": proxy}, headers={"User-Agent": user_agent}, verify=False, timeout=50)
    soup = BeautifulSoup(html.text, 'html.parser')

    # First time scraping
    if empty_database():
        # Get records from the site
        posts = soup.find_all('div', class_='block-day')
        posts.reverse()
        # (name, title, link, date)
        posts_splitted = []
        for i in range(len(posts)):
            date_raw = posts[i].find('div', class_="day").text.replace("\n", "")
            try:
                date = datetime.strptime(date_raw, "%B %d, %Y").strftime("%Y.%m.%d")
            except:
                # To get the last day of the month
                temp_date = (datetime.strptime(date_raw, "%B %Y")).strftime("%Y/%m").split("/")
                ranges = calendar.monthrange(int(temp_date[0]), int(temp_date[1]))
                date = (datetime.strptime(date_raw, "%B %Y") + timedelta(days=ranges[1] - 1)).strftime("%Y.%m.%d")
            posts_splitted.append((
                i + 1,
                posts[i].select_one('div.coin h2 span').text,
                posts[i].select_one('div.caption h3 a').text.replace("\n", "").strip(),
                date,
                base_url + posts[i].select_one('div.caption h3 a')['href']))

        # Connect database and add records
        con = sqlite3.connect('coins.db')
        cur = con.cursor()
        query = "INSERT INTO coindar VALUES (?, ?, ?, ?, ?)"

        for posts[i] in posts_splitted:
            cur.execute(query, posts[i])
            con.commit()
        con.close()

    else:
        # Get records from the database
        con = sqlite3.connect('coins.db')
        cur = con.cursor()
        item_db = cur.execute("SELECT * FROM coindar ORDER BY id DESC").fetchone()
        con.close()

        latest_post = soup.select_one('div.caption h3 a')
        post_name = soup.select_one('div.coin h2 span').text
        post_title = latest_post.text.replace("\n", "").strip()
        date_raw = soup.find('div', class_="day").text.replace("\n", "")
        try:
            post_date = datetime.strptime(date_raw, "%B %d, %Y").strftime("%Y.%m.%d")
        except:
            # To get the last day of the month
            temp_date = (datetime.strptime(date_raw, "%B %Y")).strftime("%Y/%m").split("/")
            ranges = calendar.monthrange(int(temp_date[0]), int(temp_date[1]))
            post_date = (datetime.strptime(date_raw, "%B %Y") + timedelta(days=ranges[1] - 1)).strftime("%Y.%m.%d")
        post_link = base_url + latest_post['href']
        
        s.close()

        if item_db == (item_db[0], post_name, post_title, post_date, post_link):
            print_n_log(msg="No new update on coindary hard fork disclosure.")
            return None
        # Filtered by the website natively
        else:
            print_n_log(msg="New coin swap disclosure detected on xangle.")

            # Return posts[i] to send telegram message
            insert((item_db[0] + 1, post_name, post_title, post_date, post_link))
            return {"name": post_name, "title":post_title, "link": post_link }

if __name__ == "__main__":
    import asyncio
    from update import send_message
    
    result = coindar_scrape({
        "name": "COINDAR HARD FORK DISCLOSURE",
        "link": "https://coindar.org/en/search?page=1&text=&start=2021-12-04&cats=10&im=&rs=0&fav=0&coins=&cap_from=0&cap_to=9999999999999&vol_from=0&vol_to=9999999999999&ex=1312&sort=1&order=1"
        })
    if result is not None:
        asyncio.run(send_message(result))