from safeScheduler import SafeScheduler
from trader import Trader
import itertools
import time
from datetime import datetime
import json
import matplotlib.pyplot as plt
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Bot:

    def __init__(self):
        self.villages = None
        self.schedule = SafeScheduler(minutes_after_failure=30)

        self.open_browser()

        self.trader = Trader(self)
        self.trader.get_exchange_rates()

        self.schedule.every().hour.at(':00').do \
            (self.trader.get_exchange_rates)
        self.schedule.every().hour.at(':30').do \
            (self.trader.get_exchange_rates)

        for j in itertools.cycle([1, 2, 3, 2]):
            self.schedule.run_pending()
            print('.' * j)
            time.sleep(1)

    def open_browser(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome('D:\chromedriver.exe', options=options)
    
    def open_new_tab(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

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

        input('Press enter to continue...')
        
        wait = WebDriverWait(self.driver, 2.5)

        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, '[href$="112"] span'))).click()

        try:
            wait.until(EC.element_to_be_clickable \
                ((By.LINK_TEXT, 'Abrir'))).click()
            wait.until(EC.element_to_be_clickable \
                ((By.LINK_TEXT, 'Continue a jogar'))).click()
        except TimeoutException:
            pass

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
                self.messenger.type('reCAPTCHA detected!')

                time.sleep(2)

                self.messenger.send()
                self.messenger.wait_message('Solved')
                self.messenger.type('Ok!')

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

class Trader:

    def __init__(self, bot):
        self.bot = bot

        self.current_rates = None
    
    def go_to_exchange_market(self):
        wait = WebDriverWait(self.bot.driver, 2)

        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, 'area[href$="market"]'))).click()
        
        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, '[href$="exchange"]'))).click()

    def save_exchange_rates(self):
        wait = WebDriverWait(self.bot.driver, 1)

        wood_rate = int(wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, '#premium_exchange_rate_wood div'))).text)
        
        stone_rate = int(wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, '#premium_exchange_rate_stone div'))).text)
        
        iron_rate = int(wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, '#premium_exchange_rate_iron div'))).text)
        
        with open(f'exchangeRates.json') as file:
            data = json.load(file)

        date_times, wood_rates, stone_rates, iron_rates = data.values()

        current_date_time = datetime.now()

        date_times.append([
            current_date_time.year, 
            current_date_time.month, 
            current_date_time.day, 
            current_date_time.hour, 
            current_date_time.minute
        ])
        
        wood_rates.append(wood_rate)
        stone_rates.append(stone_rate)
        iron_rates.append(iron_rate)

        data = {
            "date_times" : date_times,
            "wood_rates" : wood_rates,
            "stone_rates" : stone_rates,
            "iron_rates" : iron_rates
        }

        with open(f'exchangeRates.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def plot_graph(self):
        with open(f'exchangeRates.json') as file:
            data = json.load(file)
        
        date_times, wood_rates, stone_rates, iron_rates = data.values()

        for i, date_time in enumerate(date_times):
            year, month, day, hour, minute = date_time

            date_times[i] = datetime(
                year=year, 
                month=month, 
                day=day, 
                hour=hour, 
                minute=minute
            )

        i = -24

        plt.subplots(figsize=(14, 10), constrained_layout=True)
        plt.title('Exchange Rates X Datetime', fontsize=20)
        plt.xlabel('Datetime', fontsize=18)
        plt.ylabel('Exchange Rates', fontsize=18)
        plt.tick_params(labelright=True)
        plt.grid()

        plt.plot_date(date_times[i:], wood_rates[i:], '-o', \
            label='wood', color='brown')
        plt.plot_date(date_times[i:], stone_rates[i:], '-o', \
            label='stone', color='orange')
        plt.plot_date(date_times[i:], iron_rates[i:], '-o', \
            label='iron', color='grey')

        plt.legend()
        
    def save_graph(self):
        plt.savefig(f'exchangeRates.png')

    def get_exchange_rates(self):
        print(f'Checking exchange rates at '\
            + f'{datetime.now().replace(microsecond=0)}')

        self.bot.open_new_tab()
        self.bot.login()
        # self.bot.detect_reCAPTCHA()
        # self.bot.get_villages()
        # for i in [0, 3]:
            # self.bot.driver.get(self.bot.villages[i])
        self.go_to_exchange_market()
        self.save_exchange_rates()
        self.plot_graph()
        self.save_graph()
        self.bot.close_tab()

        # self.messenger.send_graph()

        print(f'Done checking exchange rates at ' \
            + f'{datetime.now().replace(microsecond=0)}')

bot = Bot()
