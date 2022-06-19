from datetime import datetime
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import matplotlib.pyplot as plt

class Trader:

    def __init__(self, bot):
        self.driver = bot.driver
        self.villages = bot.villages

        self.sell_price = 700
        
        self.current_rates = None
        self.current_resourses = None
    
    def go_to_exchange_market(self):
        wait = WebDriverWait(self.driver, 2)

        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, 'area[href$="market"]'))).click()
        
        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, '[href$="exchange"]'))).click()

    def get_exchange_rates(self):
        wait = WebDriverWait(self.driver, 1)

        wood_rate = int(wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, '#premium_exchange_rate_wood div'))).text)
        
        stone_rate = int(wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, '#premium_exchange_rate_stone div'))).text)
        
        iron_rate = int(wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, '#premium_exchange_rate_iron div'))).text)
        
        self.current_rates = [wood_rate, stone_rate, iron_rate]
    
    def get_current_resourses(self):
        wait = WebDriverWait(self.driver, 1)

        wood = int(wait.until(EC.visibility_of_element_located \
            ((By.ID, 'wood'))).text)
        
        stone = int(wait.until(EC.visibility_of_element_located \
            ((By.ID, 'stone'))).text)
        
        iron = int(wait.until(EC.visibility_of_element_located \
            ((By.ID, 'iron'))).text)
        
        self.current_resourses = [wood, stone, iron]

    def save_exchange_rates(self, village):
        with open(f'exchangeRates{village}.json') as file:
            data = json.load(file)

        date_times, wood_rates, stone_rates, iron_rates = data.values()

        current_time = datetime.now()

        date_times.append([
            current_time.year, 
            current_time.month, 
            current_time.day, 
            current_time.hour, 
            current_time.minute
        ])
        
        wood_rate, stone_rate, iron_rate = self.current_rates
        
        wood_rates.append(wood_rate)
        stone_rates.append(stone_rate)
        iron_rates.append(iron_rate)

        data = {
            "date_times" : date_times,
            "wood_rates" : wood_rates,
            "stone_rates" : stone_rates,
            "iron_rates" : iron_rates
        }

        with open(f'exchangeRates{village}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def plot_graph(self, village):
        with open(f'exchangeRates{village}.json') as file:
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
        
    def save_graph(self, village):
        plt.savefig(f'exchangeRates{village}.png')

    def track_prices(self):
        wait = WebDriverWait(self.driver, 1)

        sell_inputs = wait.until(EC.visibility_of_all_elements_located \
            ((By.CSS_SELECTOR, '[name^="sell"]')))

        submit = wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, '[type="submit"]')))

        while True:
            self.get_exchange_rates()
            self.get_current_resourses()

            for i, rate in enumerate(self.current_rates):
                if rate < self.sell_price and rate < self.current_resourses[i]:
                    sell_inputs[i].send_keys(1)

                    submit.click()

                    confirm = wait.until \
                        (EC.element_to_be_clickable \
                            ((By.CSS_SELECTOR, '[class$="yes"]')))
                    confirm.click()

                    sleep(5)

            sleep(1)

    def check_exchange_rates(self):
        print(f'Checking exchange rates at '\
            + f'{datetime.now().replace(microsecond=0)}')

        for i in [3, 0]:
            self.driver.get(self.villages[i])
            self.go_to_exchange_market()
            self.get_exchange_rates()
            self.save_exchange_rates(i)
            self.plot_graph(i)
            self.save_graph(i)

        # self.messenger.send_graph()

        print(f'Done checking exchange rates at ' \
            + f'{datetime.now().replace(microsecond=0)}')

    def trade(self):
        self.driver.get(self.villages[0])
        self.go_to_exchange_market()
        self.track_prices()

