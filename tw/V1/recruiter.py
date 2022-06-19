from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json

class Recruiter:

    def __init__(self, bot):
        self.driver = bot.driver
        self.villages = bot.villages
        self.detect_reCAPTCHA = bot.detect_reCAPTCHA

        self.current_resourses = None

        self.villages_models = [
            'attack',
            'defense',
            'defense',
            'defense',
            'defense',
            'defense',
            'attack'
        ]

        self.paused_list = []
    
    def get_current_resourses(self):
        wait = WebDriverWait(self.driver, 1)

        wood = int(wait.until(EC.visibility_of_element_located \
            ((By.ID, 'wood'))).text)
        
        stone = int(wait.until(EC.visibility_of_element_located \
            ((By.ID, 'stone'))).text)
        
        iron = int(wait.until(EC.visibility_of_element_located \
            ((By.ID, 'iron'))).text)
        
        self.current_resourses = [wood, stone, iron]

    def recruit(self):
        wait = WebDriverWait(self.driver, 1)
        
        self.driver.get(self.villages[0])

        wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, '[href$="train"]'))).click()

        for i, model in enumerate(self.models):

            if i not in self.paused_list:

                recruit = wait.until \
                        (EC.visibility_of_element_located \
                            ((By.CSS_SELECTOR, 'value="Recrutar"')))

                if model == 'attack':
                    axe_cost_time = wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'axe_0_cost_time'))).text
                    axe_input = wait.until \
                        (EC.visibility_of_element_located \
                            ((By.CSS_SELECTOR, 'name="axe"')))

                    light_cost_time = wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'light_0_cost_time'))).text
                    light_input = wait.until \
                        (EC.visibility_of_element_located \
                            ((By.CSS_SELECTOR, 'name="light"')))

                    marcher_cost_time = wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'marcher_0_cost_time'))).text
                    marcher_input = wait.until \
                        (EC.visibility_of_element_located \
                            ((By.CSS_SELECTOR, 'name="marcher"')))

                    ram_cost_time = wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'ram_0_cost_time'))).text                        
                    ram_input = wait.until \
                        (EC.visibility_of_element_located \
                            ((By.CSS_SELECTOR, 'name="ram"')))
                    
                    axe_cost_time = axe_cost_time.split(':')
                    hours, minutes, seconds = [int(value) for value in axe_cost_time]

                    minutes += hours * 60
                    seconds += minutes * 60

                    axes = 7200 // seconds

                    axe_input.send_keys(axes)

                    axe_cost_wood = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'axe_0_cost_wood'))).text)
                    axe_cost_stone = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'axe_cost_stone'))).text)
                    axe_cost_iron = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'axe_cost_iron'))).text)
                    axe_cost_population = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'axe_0_cost_pop'))).text)
                    
                    self.get_current_resourses()

                    wood, stone, iron = self.current_resourses

                    current_population = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'pop_current_label'))).text)
                    max_population = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'pop_max_label'))).text)
                    
                    population_available = max_population - current_population

                    if axe_cost_wood < wood:
                        if axe_cost_stone < stone:
                            if axe_cost_iron < iron:
                                if axe_cost_population < population_available:
                                    recruit.click()
                    
                    light_cost_time = light_cost_time.split(':')
                    hours, minutes, seconds = [int(value) for value in light_cost_time]

                    minutes += hours * 60
                    seconds += minutes * 60

                    lights = 7200 // seconds

                    light_input.send_keys(lights)

                    light_cost_wood = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'light_0_cost_wood'))).text)
                    light_cost_stone = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'light_cost_stone'))).text)
                    light_cost_iron = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'light_cost_iron'))).text)
                    light_cost_population = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'light_0_cost_pop'))).text)
                    
                    self.get_current_resourses()

                    wood, stone, iron = self.current_resourses

                    current_population = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'pop_current_label'))).text)
                    max_population = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'pop_max_label'))).text)
                    
                    population_available = max_population - current_population

                    if light_cost_wood < wood:
                        if light_cost_stone < stone:
                            if light_cost_iron < iron:
                                if light_cost_population < population_available:
                                    recruit.click()
                    
                    ram_cost_time = ram_cost_time.split(':')
                    hours, minutes, seconds = [int(value) for value in ram_cost_time]

                    minutes += hours * 60
                    seconds += minutes * 60

                    rams = 7200 // seconds

                    ram_input.send_keys(rams)

                    ram_cost_wood = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'ram_0_cost_wood'))).text)
                    ram_cost_stone = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'ram_cost_stone'))).text)
                    ram_cost_iron = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'ram_cost_iron'))).text)
                    ram_cost_population = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'ram_0_cost_pop'))).text)
                    
                    self.get_current_resourses()

                    wood, stone, iron = self.current_resourses

                    current_population = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'pop_current_label'))).text)
                    max_population = int(wait.until \
                        (EC.visibility_of_element_located \
                            ((By.ID, 'pop_max_label'))).text)
                    
                    population_available = max_population - current_population

                    if ram_cost_wood < wood:
                        if ram_cost_stone < stone:
                            if ram_cost_iron < iron:
                                if ram_cost_population < population_available:
                                    recruit.click()

                elif model == 'defense':
                    pass

                wait.until(EC.element_to_be_clickable \
                ((By.CSS_SELECTOR, '.arrowRight'))).click()
