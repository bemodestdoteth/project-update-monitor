from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

# FreeProxy for preventing IP ban
from fp.fp import FreeProxy

from db import get_working_proxy, write_proxy, delete_proxy
from selenium import webdriver
from datetime import datetime
import logging
import os
import random
import telegram
import time

def print_n_log(msg, is_error = False):
    if not(is_error):
        print("{}  {}".format(datetime.strftime(datetime.now(), format="%Y/%m/%d %H:%M:%S"), msg))
        logging.basicConfig(filename='./scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)
        logging.info(msg)
    else:
        print("{}  Error: {}".format(datetime.strftime(datetime.now(), format="%Y/%m/%d %H:%M:%S"), msg))
        logging.basicConfig(filename='./scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.ERROR)
        logging.error(msg)
def stopwatch(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Elapsed time: {}".format(end - start))
        return result
    return inner
def proxy_agent_rotation():
    # First time setting proxy
    if get_working_proxy() is None:
        proxl = FreeProxy(rand=True).get().replace("http://", "")
        print_n_log("Connected to: {}".format(proxl))
    else:
        proxl = get_working_proxy()
        print_n_log("Connected to: {}".format(proxl))

    with open("user-agents.txt", "r") as file:
        i = random.randint(0, 9999)
        user_agent = file.readlines()[i].replace("\n", "")
    print_n_log("New user-agent: {}".format(user_agent))
    
    return (proxl, user_agent)
def parse_markdown_v2(msg):
    reserved_words = ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!')
    for reserved_word in reserved_words:
        msg = str(msg).replace(reserved_word, "\{}".format(reserved_word))
    return msg
async def send_notification(msg):
    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    msg = '__*🔔Message from {}🔔*__\n{}'.format("Project Update Monitor", parse_markdown_v2(msg))
    await bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='markdownv2')
async def send_message(update_info):
    # Resolve reserved characters
    update_name = parse_markdown_v2(update_info['name'])
    update_title = parse_markdown_v2(update_info['title'])
    update_link = parse_markdown_v2(update_info['link'])

    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    msg = '__*🔔{} has a new update\!🔔*__\n{}\n{}\n'.format(update_name, update_title, update_link)
    await bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='markdownv2')
async def send_error_message(work, msg):
    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    
    msg_2 = "__*🚫An error occurred while working on {}\!\!🚫*__\n\n{}".format(parse_markdown_v2(work), parse_markdown_v2(msg))
    await bot.sendMessage(chat_id=chat_id, text=msg_2, parse_mode='markdownv2')
def prior_setup_bs4(func):
    def inner(coin):
        print("-----------------------------------------")
        print_n_log("NOW WATCHING {}".format(coin['name']))
        print("-----------------------------------------")

        (proxl, user_agent) = proxy_agent_rotation()

        if get_working_proxy() is None:
            write_proxy(proxl)

        return func(coin, proxl, user_agent)
    return inner
def prior_setup_selenium(func):
    def inner(coin, delay = 15):
        print("-----------------------------------------")
        print_n_log("NOW WATCHING {}".format(coin['name']))
        print("-----------------------------------------")

        error_cnt = 0
        driver = ""
        (proxl, user_agent) = proxy_agent_rotation()

        # Open website and handle errors
        while True:
            try:
                driver = os_selection(proxy = proxl, user_agent = user_agent)
                driver.get(coin['link'])
                WebDriverWait(driver, delay).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, coin["selector"])))
                write_proxy(proxl)
                break
            except TimeoutException:
                print_n_log("Connection with proxy failed for TimeoutException. Trying again...")
                if driver != "":
                    driver.quit()
                error_cnt = error_cnt + 1
                if error_cnt >= 2:
                    print_n_log("Changing proxy and user_agents due to concurrent errors...")
                    delete_proxy(proxl)
                    (proxl, user_agent) = proxy_agent_rotation()
                    error_cnt = 0            
            except WebDriverException as e:
                print (e)
                print_n_log("Connection with proxy failed for WebDriverException. Trying again...")
                if driver != "":
                    driver.quit()
                error_cnt = error_cnt + 1
                if error_cnt >= 2:
                    print_n_log("Changing proxy and user_agents due to concurrent errors...")
                    delete_proxy(proxl)
                    (proxl, user_agent) = proxy_agent_rotation()
                    error_cnt = 0            
        
        return func(coin, driver, delay)
    return inner
def os_selection(proxy, user_agent):
    chrome_options = webdriver.ChromeOptions()
    # Selenium on Linux
    if os.name == 'posix':
        # Bypass headless block
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
        chrome_options.page_load_strategy = "eager"
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument('--window-size=1920, 1080')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        chrome_options.add_argument(f'user-agent={user_agent}')
    # Selenium on Windows
    elif os.name == 'nt':
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--window-size=1920, 1080')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument(f'user-agent={user_agent}')
        '''
        Add Extension to Chrome
        t.ly/wxZQ
        Preserve user cookies
        t.ly/uDkv
        '''
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
    driver = webdriver.Chrome(options=chrome_options)
    return driver