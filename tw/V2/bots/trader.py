from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import matplotlib.pyplot as plt
from numpy import amin, amax

class Trader:

    def __init__(self, bot):
        self.driver = bot.driver
        self.villages = bot.villages

        self.current_rates = None
        self.limit = 5000
        self.reserved_per_resourse = 10000
        self.reserved_PPs = 30
    
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
    
    def save_exchange_rates(self):
        with open('exchangeRates.json') as file:
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

        with open('exchangeRates.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def sell(self, resourse_index, rate):
        wait = WebDriverWait(self.driver, 1)

        sell_inputs = wait.until(EC.visibility_of_all_elements_located \
            ((By.CSS_SELECTOR, '[name^="sell"]')))
        
        resourse_input = sell_inputs[resourse_index]

        sell_amount = self.limit - rate

        resourse_input.send_keys(sell_amount)

        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, '[type="submit"]'))).click()
        
        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, '[class$="btn-confirm-yes"]'))).click()  
        
    def buy(self, resourse_index, rate):
        pass

    def try_exchange(self):
        with open('exchangeRates.json') as file:
            data = json.load(file)
        
        date_times, wood_rates, stone_rates, iron_rates = data.values()

        rates_lists = [wood_rates, stone_rates, iron_rates]
        
        recent_rates = [rates_list[-20:] for rates_list in rates_lists]

        minimun_recent_rate = amin(recent_rates)
        maximun_recent_rate = amax(recent_rates)

        delta = maximun_recent_rate - minimun_recent_rate

        sell_value = round(minimun_recent_rate + 0.2 * delta)
        buy_value = round(maximun_recent_rate - 0.2 * delta)

        current_rates = [rates_list[-1] for rates_list in rates_lists]

        for resourse, current_rate in enumerate(current_rates):

            if current_rate < sell_value:
                self.sell(resourse, current_rate)
            
            if current_rate > buy_value:
                self.buy(resourse, current_rate)

    def plot_graph(self):
        with open('exchangeRates.json') as file:
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

        i = -15

        plt.subplots(figsize=(14, 10), constrained_layout=True)
        plt.title('Exchange Rates X Datetime', fontsize=20)
        plt.xlabel('Datetime', fontsize=18)
        plt.ylabel('Exchange Rates', fontsize=18)
        plt.tick_params(labelright=True)
        plt.grid()
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=16)

        plt.plot_date(date_times[i:], wood_rates[i:], '-o', \
            label='wood', color='brown')
        plt.plot_date(date_times[i:], stone_rates[i:], '-o', \
            label='stone', color='orange')
        plt.plot_date(date_times[i:], iron_rates[i:], '-o', \
            label='iron', color='grey')

        plt.legend()

    def save_graph(self):
        plt.savefig(f'exchangeRates.png')

    def check_exchange_rates(self):  # trade
        print(f'Checking exchange rates at '\
            + f'{datetime.now().replace(microsecond=0)}')

        self.driver.get(self.villages[0])
        self.go_to_exchange_market()
        self.get_exchange_rates()
        self.save_exchange_rates()
        # self.try_exchange()
        self.plot_graph()
        self.save_graph()

        print(f'Done checking exchange rates at ' \
            + f'{datetime.now().replace(microsecond=0)}')
