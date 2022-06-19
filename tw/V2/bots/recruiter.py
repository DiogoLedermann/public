from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bots.safeScheduler import SafeScheduler
from datetime import datetime

class Recruiter:

    def __init__(self, schedule):
        super(Recruiter).__init__()

        self.on = True
        self.job = None
        self.driver = None

        self.schedule = schedule
        
        if datetime.now().hour < 8:
            self.start_night_schift()
        else:
            self.start_day_schift()

    def turn_on(self):
        print('turn on')
        self.on = True
    
    def turn_off(self):
        print('turn off')
        self.on = False
    
    def start_night_schift(self):
        print('start night schift')
        if self.job is not None:
            self.schedule.cancel_job(self.job)
        self.job = self.schedule.every(3).seconds.do(self.recruit)

    def start_day_schift(self):
        print('start day schift')
        if self.job is not None:
            self.schedule.cancel_job(self.job)
        self.job = self.schedule.every().second.do(self.recruit)
    
    def recruit(self):
        if self.on:
            print('recruit')
