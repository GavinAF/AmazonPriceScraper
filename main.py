# Imports
import requests
from bs4 import BeautifulSoup
import smtplib
import os
import datetime
import time
import config
import bitly_api

# Variables
dsign = "$"
dpoint = "."
alert_amount = 300
title = ""
difference = 0
i_price = 0
to_email = ""
short_URL = ""
bitly = bitly_api.Connection(config.bitly_user, config.bitly_api_key)

# URL to scrape
URL = ""

# Headers to view page with
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
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
        difference = alert_amount - i_price
        notify()


# Function to send an email to the user
def notify():
    # Global Variables
    global difference
    global alert_amount

    subject = "🚨 The price of {} has fallen! 🚨".format(title)

    body = "It's currently {} dollars cheaper than your price point of {}.\nCheck it out now: {}".format(difference, alert_amount, short_URL["url"])

    send_email(subject, body)

    print("Notification dispatched!")


# Send email in utf-8
def send_email(subject, content):

    global to_email

    for ill in ["\n", "\r"]:
        subject = subject.replace(ill, " ")

    headers = {
        "Content-Type": "text/html; charset=utf-8",
        "Content-Disposition": "inline",
        "Content-Transfer-Encoding": "8bit",
        "From": config.sender,
        "To": to_email,
        "Date": datetime.datetime.now().strftime("%a, %d %b %Y  %H:%M:%S %Z"),
        "X-Mailer": "python",
        "Subject": subject
    }

    # create the message
    msg = ""
    for key, value in headers.items():
        msg += "%s: %s\n" % (key, value)

    # add contents
    msg += "\n%s\n" % (content)

    s = smtplib.SMTP(config.host, config.port)

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(config.username, config.password)

    s.sendmail(headers["From"], headers["To"], msg.encode("utf8"))
    s.quit()


to_email = input("Enter your email address: ")
URL = input("Paste the amazon product link: ")
alert_amount = input("What is your price threshold? ")
alert_amount = int(alert_amount)
short_URL = bitly.shorten(uri = URL)
print("Thanks! You'll be notified when the price drops under your threshold.\n")

while True:
    check_price()
    time.sleep(86400)
