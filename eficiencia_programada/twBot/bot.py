import schedule
from datetime import datetime, timedelta
from numpy import array, around
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

class Bot:

    def __init__(self):
        self.schedule = schedule.Scheduler()
        self.scavenging_job = None

        self.driver = webdriver.Chrome('D:\chromedriver.exe')
        self.driver.set_window_size(560, 1000)
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get("https://www.tribalwars.com.br/")

        self.wait = WebDriverWait(self.driver, 3)
        self.wait.until(EC.visibility_of_element_located \
            ((By.ID, 'user'))).send_keys('BradleyLedermann')
        self.wait.until(EC.visibility_of_element_located \
            ((By.ID, 'password'))).send_keys('oLAAa100', Keys.RETURN)
        self.wait = WebDriverWait(self.driver, 60)
        self.wait.until(EC.presence_of_element_located \
            ((By.CSS_SELECTOR, '[href$="brp6"] span')))
        self.wait = WebDriverWait(self.driver, 3)

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def scavenge(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get("https://www.tribalwars.com.br/")

        self.wait.until(EC.presence_of_element_located \
            ((By.CSS_SELECTOR, '[href$="brp6"] span'))).click()
        self.wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, 'area[href$="place"]'))).click()
        self.wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, 'a[href$="scavenge"]'))).click()
        
        inputs =  self.wait.until(EC.visibility_of_all_elements_located \
            ((By.CSS_SELECTOR, 'input[class^="unitsInput"]')))

        elements = self.wait.until(EC.visibility_of_all_elements_located \
            ((By.CSS_SELECTOR, 'a[class^="units-entry-all"]')))
        
        all_units = array([int(element.text.strip('()')) \
            for element in elements])

        options_units = [
            around(all_units * (15 / 24) * 1),
            around(all_units * (6 / 24) * 1),
            around(all_units * (3 / 24) * 1),
            around(all_units * (2 / 26) * 1)
        ][:-1]

        options = self.wait.until \
            (EC.visibility_of_all_elements_located \
                ((By.CSS_SELECTOR, 'div[class^="scavenge-option"]')))

        for option, option_units in zip(options, options_units):
            for input, units in zip(inputs, option_units):
                input.send_keys(int(units))
            
            start_button = option.find_elements_by_css_selector \
                ('a[class$="free_send_button"]')

            if start_button:
                start_button[0].click()

            sleep(1)

            for input in inputs:
                input.clear()

        return_countdown_css_selector = \
            'div[class="options-container"] span[class="return-countdown"]'

        return_countdowns = self.wait.until \
            (EC.visibility_of_all_elements_located \
                ((By.CSS_SELECTOR, return_countdown_css_selector)))

        return_times = [datetime.strptime(return_countdown.text, '%H:%M:%S') \
            for return_countdown in return_countdowns]

        latest_return = max(return_times)

        hours, minutes, seconds = \
            latest_return.hour, latest_return.minute, latest_return.second

        time_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        next_time = datetime.now() + time_delta
        next_time = next_time.strftime('%H:%M:%S')

        if self.scavenging_job is not None:
            self.schedule.cancel_job(self.scavenging_job)

        self.scavenging_job = self.schedule.every().day.at(next_time).do \
            (self.scavenge)

        print(f'Next scavenging at {next_time}.')

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def loop(self):
        while True:
            self.schedule.run_pending()
            sleep(1)
