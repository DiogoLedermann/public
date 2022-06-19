from datetime import timedelta
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from math import ceil
from datetime  import datetime, timedelta
import json
from numpy import array

class Farmer():

    def __init__(self, bot):
        self.driver = bot.driver
        self.villages = bot.villages
        self.ceil_datetime = bot.ceil_datetime
        self.detect_reCAPTCHA = bot.detect_reCAPTCHA

        self.paused_list = []

        self.minimun_lights = 0
        self.minimun_marchers = 0

        with open('targets.json') as file:
            data = json.load(file)
        
        self.targets = data['targets']
    
    def get_minimun_units(self):
        wait = WebDriverWait(self.driver, 2)

        village_text = wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, '#show_summary h4'))).text
        
        village_points = \
            int(village_text[village_text.find('(')+1:village_text.rfind(' ')])

        minimun_attack = round(0.01 * village_points)

        minimun_lights = ceil(minimun_attack / 4)
        minimun_marchers = ceil(minimun_attack / 5)

        return minimun_lights, minimun_marchers
    
    def farm_players(self, village):
        village_targets = self.targets[village]

        village = int(village)

        self.driver.get(self.villages[village])

        minimun_lights, minimun_marchers = self.get_minimun_units()

        wait = WebDriverWait(self.driver, 1)
        
        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, '[href$="place"]'))).click()

        units_available = wait.until \
            (EC.visibility_of_all_elements_located \
                ((By.CSS_SELECTOR, '[class="units-entry-all"]')))
        
        spies_available, lights_available, marchers_available = \
            [int(units.text.strip('()')) for units in units_available[4:7]]
        
        for target in village_targets:
            self.detect_reCAPTCHA()

            unit_inputs = wait.until \
                (EC.visibility_of_all_elements_located \
                    ((By.CSS_SELECTOR, '[class="unitsInput"]')))

            spy_input, light_input, marcher_input = unit_inputs[4:7]
    
            if spies_available > 1:
                spy_input.send_keys(1)

            if lights_available >= minimun_lights:
                light_input.send_keys(minimun_lights)
                lights_available -= minimun_lights
            
            elif marchers_available >= minimun_marchers:
                marcher_input.send_keys(minimun_marchers)
                marchers_available -= minimun_marchers

            else:
                break

            coordinates = target

            wait.until(EC.visibility_of_element_located \
                ((By.CSS_SELECTOR, '[name="input"]'))) \
                    .send_keys(coordinates)

            wait.until(EC.element_to_be_clickable \
                ((By.ID, 'target_attack'))).click()

            wait.until(EC.element_to_be_clickable \
                ((By.ID, 'troop_confirm_go'))).click()

    def farm_barbarians(self):
        wait = WebDriverWait(self.driver, 3)

        wait.until(EC.element_to_be_clickable \
            ((By.ID, 'manager_icon_farm'))).click()
        
        attacked_checkbox = wait.until(EC.element_to_be_clickable \
            ((By.ID, 'attacked_checkbox')))

        if not attacked_checkbox.is_selected():
            attacked_checkbox.click()

        pages_navigator = wait.until \
            (EC.visibility_of_all_elements_located \
                ((By.ID, 'plunder_list_nav')))[-1]
        
        number_of_pages = len(pages_navigator 
            .find_elements_by_css_selector('strong, a'))

        for i in range(number_of_pages):

            lights_available = int(wait.until \
                (EC.visibility_of_element_located((By.ID, 'light'))).text)

            marchers_available = int(wait.until \
                (EC.visibility_of_element_located((By.ID, 'marcher'))).text)

            self.detect_reCAPTCHA()
            
            buttons = wait.until(EC.visibility_of_all_elements_located \
                ((By.CSS_SELECTOR, 
                    '[class*="farm_icon_a"], [class*="farm_icon_b"]')))
            
            buttons = array(buttons).reshape((int(len(buttons) / 2), 2))

            for j in range(len(buttons)):

                A, B = buttons[j]

                if lights_available > 0:
                    A.click()
                    lights_available -= 1
                
                elif marchers_available > 0:
                    B.click()
                    marchers_available -= 1
                
                else:
                    break

                if j % 8 == 7:
                    self.driver.execute_script("window.scrollBy(0, 240)")

                sleep(0.2)
            
            if lights_available == 0 and marchers_available == 0:
                break

            if i != number_of_pages - 1:
                pages_navigator = wait.until \
                    (EC.visibility_of_all_elements_located \
                        ((By.ID, 'plunder_list_nav')))[-1]

                next_page = pages_navigator \
                    .find_element_by_tag_name('strong + a')

                next_page.click()

    def farm(self):
        print(f'Farming at {datetime.now().replace(microsecond=0)}')

        offensive_villages = self.targets.keys()

        for village in offensive_villages:
            if int(village) not in self.paused_list:
                self.driver.get(self.villages[int(village)])
                # self.farm_players(village)
                self.farm_barbarians()
    
        next_farming = \
            self.ceil_datetime \
                (datetime.now(), timedelta(minutes=30))

        print(f'Done farming farming at ' \
            + f'{datetime.now().replace(microsecond=0)}')

        print(f'Next farming farming at {next_farming}')
