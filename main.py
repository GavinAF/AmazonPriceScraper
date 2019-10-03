# Imports
import requests
from bs4 import BeautifulSoup
import smtplib
import os
import datetime
import time
import config
import bitly_api
from pytextbelt import Textbelt

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
phone = ""

# URL to scrape
URL = ""

# Headers to view page with
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
    }

# Check price of item from product link
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

    # Slice digits between dollar sign & decimal
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
    send_text(phone)

    print("Notification dispatched!")


# Send text alert to user
def send_text(phonenumber):
    global title
    global difference
    global alert_amount

    message = ("The price of {} is currently {} dollars cheaper than your {} price point".format(title, difference, alert_amount))

    recipient = Textbelt.Recipient(phonenumber, "us")
    recipient.send(message)
    print("Sent Successfully!" if recipient.send(message)["success"] else "Sending Failed!")


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

while True:
    to_email = input("Enter your email address: ")

    if to_email and not to_email.isspace():
        if "@" in to_email:
            break
        else:
            continue
    else:
        continue

while True:
    phone = input("What is your phone number? ")

    if phone and not phone.isspace():
        if phone.isnumeric():            
            break
        else:
            continue
    else:
        continue

while True:
    URL = input("Paste the amazon product link: ")

    if URL and not URL.isspace():
        if "amazon.com" in URL:
            break
        else:
            continue    
    else:
        continue

while True:
    alert_amount = input("What is your price threshold? ")

    if alert_amount and not alert_amount.isspace():
        if alert_amount.isnumeric():            
            break
        else:
            continue
    else:
        continue

alert_amount = int(alert_amount)
short_URL = bitly.shorten(uri = URL)
print("Thanks! You'll be notified when the price drops under your threshold.\n")

while True:
    check_price()
    time.sleep(86400)
