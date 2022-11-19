import requests
import os
from bs4 import BeautifulSoup
import time
import logging
import telebot

BOT_TOKEN="TBD"
chat_id = TBD

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

URL_TO_MONITOR_MEDIAWORLD = "https://www.mediaworld.it/it/product/_drone-dji-mini-3-pro-con-rc-n1-175181.html"  # change this to the URL you want to monitor
URL_TO_MONITOR_COMET = "https://www.comet.it/dji-dji-mini-3-pro-rc-n1-DJI00063I-prdtt"
URL_TO_MONITOR_UNIEURO = "https://www.unieuro.it/online/Quadricotteri/Mini-3-Pro-RC-N1-pidDJIMINI3PRORCST"
URL_TO_MONITOR_EURONICS = "https://www.euronics.it/foto--video--droni/droni/droni/dji---mini-3-pro-con-rc-n1-grigio/222005251.html"
URL_TO_MONITOR_EXPERT = "https://www.expert.it/it/it/exp/shop/product/mini-3-pro-con-rc-n1/exp785667"
URL_TO_MONITOR_DJISTORE = "https://www.dji-store.it/prodotto/dji-mini-3-pro/"

DELAY_TIME = 300  # seconds

def send_text_alert(alert_str):
    """Sends an SMS text alert."""
    bot.send_message(chat_id,alert_str)

def process_html(string):
    soup = BeautifulSoup(string, features="lxml")

    # make the html look good
    soup.prettify()

    # remove script tags
    for s in soup.select('script'):
        s.extract()

    # remove meta tags
    for s in soup.select('meta'):
        s.extract()

    # convert to a string, remove '\r', and return
    return str(soup).replace('\r', '')

def webpage_was_changed_generic(log, url, prices, c ):
    """Returns true if the webpage was changed, otherwise false."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
    response = requests.get(url, headers=headers)
    processed_response_html = process_html(response.text)
    r = True
    for p in prices:
        if processed_response_html.count(p)==c:
            r= False
    if r:
        log.info("WEBPAGE WAS CHANGED.")
        send_text_alert(f"URGENT! {url} WAS CHANGED!")
    else:
        log.info("Webpage was not changed.")
    return r

def main():
    log = logging.getLogger(__name__)
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')
    log.info("Running Website Monitor")
    while True:
        try:
            webpage_was_changed_generic(log, URL_TO_MONITOR_DJISTORE, ["839,00"], 5)
            webpage_was_changed_generic(log,URL_TO_MONITOR_MEDIAWORLD,["839.–"],2)
            webpage_was_changed_generic(log,URL_TO_MONITOR_COMET,["838,00","839,00"],2)
            #webpage_was_changed_generic(log,URL_TO_MONITOR_UNIEURO,["826.00"],2)
            webpage_was_changed_generic(log,URL_TO_MONITOR_EURONICS,["839,00"],2)
            webpage_was_changed_generic(log,URL_TO_MONITOR_EXPERT,[">839<"],2)
        except:
            log.info("Error checking website.")
        time.sleep(DELAY_TIME)

if __name__ == "__main__":
    main()