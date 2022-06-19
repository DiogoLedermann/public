from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from numpy import array
from datetime import datetime, timedelta

class Scavenger:

    def __init__(self, bot):
        self.open_new_tab = bot.open_new_tab
        self.login = bot.login
        self.close_tab = bot.close_tab

        self.villages = bot.villages
        self.schedule = bot.schedule
        self.driver = bot.driver        

        self.scavenging_jobs = [None] * len(self.villages)
        self.start_button = None

    def get_unit_values(self, scavenging_units):
        return [
            array(scavenging_units) * 6 / 11,
            array(scavenging_units) * 3 / 11,
            array(scavenging_units) * 2 / 11,
        ]
    
    def find_start_button(self, option):
        button_css_selector = 'a[class="btn btn-default free_send_button"]'
        self.start_button = \
            option.find_element_by_css_selector(button_css_selector)
    
    def send_keys(self, inputs, units):
        spear_input, sword_input, axe_input, archer_input = inputs
        spears, swords, axes, archers = [int(value) for value in units]

        spear_input.send_keys(spears)
        sword_input.send_keys(swords)
        axe_input.send_keys(axes)
        archer_input.send_keys(archers)
    
    def clear_inputs(self, inputs):
        spear_input, sword_input, axe_input, archer_input = inputs

        spear_input.clear()
        sword_input.clear()
        axe_input.clear()
        archer_input.clear()

    def go_to_scavenging_screen(self):
        wait = WebDriverWait(self.driver, 1)

        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, 'area[href$="place"]'))).click()

        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, 'a[href$="scavenge"]'))).click()

    def scavenge_at_village(self, village):
        print(f'Scavenging village {str(village).zfill(3)} ' \
            + f'at {datetime.now().replace(microsecond=0)}')

        self.open_new_tab()
        self.login()
        self.driver.get(self.villages[village])
        self.go_to_scavenging_screen()
        self.scavenge()

        print(f'Done scavenging village {str(village).zfill(3)} ' \
            + f'at {datetime.now().replace(microsecond=0)}')

        sleep(1)

        self.schedule_scavenging(village)
        self.close_tab()

    def set_scavenging_job(self, job, village):
        self.scavenging_jobs[village] = job

    def schedule_scavenging(self, village):
        return_countdown_css_selector = \
            'div[class="options-container"] span[class="return-countdown"]'

        wait = WebDriverWait(self.driver, 1)

        return_countdowns = wait.until(EC.visibility_of_all_elements_located \
            ((By.CSS_SELECTOR, return_countdown_css_selector)))

        return_times = [datetime.strptime(return_countdown.text, '%H:%M:%S') \
            for return_countdown in return_countdowns]

        latest_return = max(return_times)

        hours, minutes, seconds = \
            latest_return.hour, latest_return.minute, latest_return.second

        time_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        next_time = datetime.now() + time_delta
        next_time = next_time.strftime('%H:%M:%S')

        if self.scavenging_jobs[village] is not None:
            self.schedule.cancel_job(self.scavenging_jobs[village])

        next_job = self.schedule.every().day.at(next_time).do \
            (self.scavenge_at_village, village)
        
        self.set_scavenging_job(next_job, village)

        print(f'Next scavenging at {str(village).zfill(3)} at {next_time}.')

    def scavenge(self):
        wait = WebDriverWait(self.driver, 1)

        inputs =  wait.until(EC.visibility_of_all_elements_located \
            ((By.CSS_SELECTOR, 'input[class^="unitsInput"]')))[:4]

        scavenging_infantry = [int(element.text.strip('()')) \
            for element in wait.until(EC.visibility_of_all_elements_located \
                ((By.CSS_SELECTOR, 'a[class^="units-entry-all"]')))][:4]
        
        heavy_cavalry = [int(element.text.strip('()')) \
            for element in wait.until(EC.visibility_of_all_elements_located \
                ((By.CSS_SELECTOR, 'a[class^="units-entry-all"]')))][-2]
        
        scavenging_units = scavenging_infantry + [heavy_cavalry]

        units_values = self.get_unit_values(scavenging_units)

        scavenging_options =  wait.until \
            (EC.visibility_of_all_elements_located \
                ((By.CSS_SELECTOR, 'div[class^="scavenge-option"]')))[1:]

        for units, option in zip(units_values, scavenging_options):
            try:
                self.find_start_button(option)
                self.send_keys(inputs, units)
                self.start_button.click()

                sleep(0.5)

                self.clear_inputs(inputs)
            except NoSuchElementException:
                pass

    def first_scavenge(self):
        print(f'First scavenging at {datetime.now().replace(microsecond=0)}')

        self.driver.get(self.villages[0])

        wait = WebDriverWait(self.driver, 1)

        self.go_to_scavenging_screen()
        
        for i in range(len(self.villages)):
            self.scavenge()

            sleep(1)

            self.schedule_scavenging(i)
            
            wait.until(EC.element_to_be_clickable \
                ((By.CSS_SELECTOR, '.arrowRight'))).click()

        print(f'Done first scavenging at ' \
            + f'{datetime.now().replace(microsecond=0)}')
