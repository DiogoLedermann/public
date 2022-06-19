from safeScheduler import SafeScheduler
from bots.messenger import Messenger
from bots.farmer import Farmer
from bots.scavenger import Scavenger
from bots.trader import Trader
import itertools
import time
from datetime  import datetime
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Bots:

    def __init__(self):
        self.villages = None
        self.schedule = SafeScheduler(minutes_after_failure=30)

        self.open_browser()

        self.messenger = Messenger(self)

        self.messenger.open_whatsapp()

        answer = input('Farm now? (y/n): ')

        self.open_new_tab()

        self.login()
        self.detect_reCAPTCHA()
        self.get_villages()

        self.farmer = Farmer(self)
        self.scavenger = Scavenger(self)
        self.trader = Trader(self)

        if answer == 'y':
            self.farmer.farm()

        self.scavenger.first_scavenge()

        self.close_tab()

        self.schedule.every().hour.at(':00').do(self.job)
        self.schedule.every().hour.at(':30').do(self.job)

        for j in itertools.cycle([1, 2, 3, 2]):
            self.schedule.run_pending()
            print('.' * j)
            time.sleep(1)

    def ceil_datetime(self, date_time, delta):
        return date_time + (datetime.min - date_time) % delta

    def open_browser(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome('D:\chromedriver.exe', options=options)
    
    def open_new_tab(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window \
            (self.driver.window_handles \
                [-1])

    def close_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def login(self):
        self.driver.get("https://www.tribalwars.com.br/")

        wait = WebDriverWait(self.driver, 1)
        try:
            wait.until(EC.visibility_of_element_located \
                ((By.ID, 'user'))).send_keys('BradleyLedermann')
            wait.until(EC.visibility_of_element_located \
                ((By.ID, 'password'))).send_keys('oLAAa100', Keys.RETURN)
        except TimeoutException:
            pass

        wait = WebDriverWait(self.driver, 2.5)

        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, '[href$="107"] span'))).click()

        try:
            wait.until(EC.element_to_be_clickable \
                ((By.LINK_TEXT, 'Abrir'))).click()
            wait.until(EC.element_to_be_clickable \
                ((By.LINK_TEXT, 'Continue a jogar'))).click()
        except TimeoutException:
            pass

        wait.until(EC.element_to_be_clickable \
            ((By.LINK_TEXT, 'Combinado'))).click()

    def detect_reCAPTCHA(self):
        wait = WebDriverWait(self.driver, 1)

        try:
            frame_name = wait.until(EC.visibility_of_element_located \
                ((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]'))) \
                    .get_attribute('name')

            self.driver.switch_to.frame(frame_name)

        except TimeoutException:
            return

        else:
            self.close_tab()

            try:
                self.messenger.open_chat()

            except TimeoutException:
                print('reCAPTCHA detected and whatsapp unavailable.')
                input('Program paused. Press enter to continue...')

            else:
                self.messenger.type(message='reCAPTCHA detected!')

                time.sleep(2)

                self.messenger.send()
                self.messenger.wait_message('Solved')
                self.messenger.type(message='Ok!')

                time.sleep(2)

                self.messenger.send()

            finally:
                self.open_new_tab()
                self.login()

    def get_villages(self):
        wait = WebDriverWait(self.driver, 1)

        villages = wait.until(EC.visibility_of_all_elements_located \
            ((By.CSS_SELECTOR, '#combined_table [href$="overview"]')))
        
        self.villages = \
            [village.get_attribute('href') for village in villages]

    def job(self):
        self.open_new_tab()
        self.login()
        self.detect_reCAPTCHA()
        self.get_villages()
        self.detect_reCAPTCHA()
        self.trader.check_exchange_rates()
        self.detect_reCAPTCHA()
        self.farmer.farm()
        self.close_tab()
        self.messenger.send_current_info()
