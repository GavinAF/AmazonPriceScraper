# Imports
import requests
from bs4 import BeautifulSoup
import smtplib
import os
import datetime
import time

# Variables
dsign = "$"
dpoint = "."
alert_amount = 300
title = ""
difference = 0
i_price = 0

# URL to scrape
URL = "https://www.amazon.com/gp/product/B01N2PE8CZ/"

# Headers to view page with
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Cache-Control" : "no-cache",
    "Pragma" : "no-cache"
    }


def check_price():
    # Setting global variables
    global title
    global i_price
    global difference
    global alert_amount

    # Get page contents & prettify them
    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    # Get item name, price
    title = soup2.find(id="productTitle").get_text()
    price = soup2.find(id="priceblock_ourprice").get_text()

    # Strip whitespace off title
    title = (title.strip())

    # Only grab the characters between the dollar sign & decimal point ($123.12 > 123)
    pstart = price.find(dsign)
    pstart_len = (pstart + len(dsign))
    pend = price.find(dpoint)
    new_price = (price[pstart_len:pend])

    i_price = int(new_price)

    if(i_price < alert_amount):
        difference = alert_amount -i_price
        notify()

# Function to send an email to the user
def notify():
    # Global Variables
    global difference
    global alert_amount

    subject = "🚨 The price of {} has fallen! 🚨".format(title)

    body = "It's currently {} dollars cheaper than your price point of {}.\nCheck it out now: {}".format(difference, alert_amount, URL)

    send_email(subject, body)

    print("Notification dispatched!")


# Send email in utf-8
def send_email(subject, content):

    for ill in ["\n", "\r"]:
        subject = subject.replace(ill, " ")

    headers = {
        "Content-Type": "text/html; charset=utf-8",
        "Content-Disposition": "inline",
        "Content-Transfer-Encoding": "8bit",
        "From": "scraperamazon81@gmail.com",
        "To": "gavinafoutz@gmail.com",
        "Date": datetime.datetime.now().strftime("%a, %d %b %Y  %H:%M:%S %Z"),
        "X-Mailer": "python",
        "Subject": subject
    }

    # create the message
    msg = ""
    for key, value in headers.items():
        msg += "%s: %s\n" % (key, value)

    # add contents
    msg += "\n%s\n"  % (content)

    s = smtplib.SMTP("smtp.gmail.com", "587")

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login("scraperamazon81@gmail.com", "AbJEQCo6ce8z")

    s.sendmail(headers["From"], headers["To"], msg.encode("utf8"))
    s.quit()


while True:
    check_price()
    time.sleep(86400)