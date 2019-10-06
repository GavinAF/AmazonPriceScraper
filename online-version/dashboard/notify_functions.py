import datetime
import smtplib


# Send email in utf-8
def send_email(subject, content, email):

    for ill in ["\n", "\r"]:
        subject = subject.replace(ill, " ")

    headers = {
        "Content-Type": "text/html; charset=utf-8",
        "Content-Disposition": "inline",
        "Content-Transfer-Encoding": "8bit",
        "From": "Amazon Scraper <scraperamazon81@gmail.com>",
        "To": email,
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


    s = smtplib.SMTP("smtp.gmail.com", "587")
    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login("scraperamazon81@gmail.com", "AbJEQCo6ce8z")

    s.sendmail(headers["From"], headers["To"], msg.encode("utf8"))
    s.quit()

def notify(url, title, alert_amount, difference, email):

    subject = "🚨 The price of {} has fallen! 🚨".format(title)

    body = "It's currently {} dollars cheaper than your price point of {}.\nCheck it out now: {}".format(difference, alert_amount, url)

    send_email(subject, body, email)