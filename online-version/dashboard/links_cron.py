from django_cron import CronJobBase, Schedule
from .models import Link
import requests
from bs4 import BeautifulSoup
from .notify_functions import notify

class CheckPrices(CronJobBase):
    RUN_EVERY_MINS = 120

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'fire_scraper.check_prices'

    def do(self):

        print("Starting to check prices...")

        links = Link.objects.all().filter(active='True')

        for link in links:
            dsign = "$"
            dpoint = "."
            alert_amount = link.threshold
            title = link.title
            difference = 0
            i_price = 0
            to_email = link.owner.email

            # URL to scrape
            URL = link.url

            # Headers to view page
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "Cache-Control":"no-cache",
                "Pragma":"no-cache"
            }

            page = requests.get(URL, headers=headers)
            soup1 = BeautifulSoup(page.content, 'html.parser')
            soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

            # Get the price (Amazon only currently)
            price = soup2.find(id="priceblock_ourprice").get_text()

            # Slice digits between dollar sign & decimal
            pstart = price.find(dsign)
            pstart_len = (pstart + len(dsign))
            pend = price.find(dpoint)
            new_price = (price[pstart_len:pend])

            i_price = int(new_price)
            alert_amount = int(alert_amount)

            if(i_price < alert_amount):
                difference = alert_amount - i_price
                # url, title, alert_amount, difference, email)
                notify(URL, title, alert_amount, difference, to_email)