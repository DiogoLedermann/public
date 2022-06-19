import itertools
import schedule
from datetime import datetime, timedelta
from numpy import array
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

def open_new_tab():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

def close_tab():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def login(first):
    driver.get("https://www.tribalwars.com.br/")

    wait = WebDriverWait(driver, 1)
    try:
        wait.until(EC.visibility_of_element_located \
            ((By.ID, 'user'))).send_keys('BradleyLedermann')
        wait.until(EC.visibility_of_element_located \
            ((By.ID, 'password'))).send_keys('oLAAa100', Keys.RETURN)
    except TimeoutException:
        pass

    if first:
        input('Press enter to continue...')
        first = False

    wait = WebDriverWait(driver, 2.5)

    wait.until(EC.element_to_be_clickable \
        ((By.CSS_SELECTOR, '[href$="brp6"] span'))).click()

    try:
        wait.until(EC.element_to_be_clickable \
            ((By.LINK_TEXT, 'Abrir'))).click()
        wait.until(EC.element_to_be_clickable \
            ((By.LINK_TEXT, 'Continue a jogar'))).click()
    except TimeoutException:
        pass

    return first

def go_to_scavenging_screen():
    wait = WebDriverWait(driver, 1)

    wait.until(EC.element_to_be_clickable \
        ((By.CSS_SELECTOR, 'area[href$="place"]'))).click()

    wait.until(EC.element_to_be_clickable \
        ((By.CSS_SELECTOR, 'a[href$="scavenge"]'))).click()

def get_unit_values(scavenging_units):
    return [
        array(scavenging_units) * (15 / 24) * 1,
        array(scavenging_units) * (6 / 24) * 1,
        array(scavenging_units) * (3 / 24) * 1,
        array(scavenging_units) * (2 / 26) * 0
    ]

def find_start_button(option):
    button_css_selector = 'a[class="btn btn-default free_send_button"]'
    start_button = \
        option.find_element_by_css_selector(button_css_selector)
    
    return start_button

def send_keys(inputs, units):
    spear_input, sword_input, axe_input, arrow_input,\
        light_cavalry_input, marcher_input, heavy_cavalry_input \
            = inputs
    spears, swords, axes, arrows, light_cavalry, marchers, heavy_cavalry \
        = [int(value) for value in units]

    spear_input.send_keys(spears)
    sword_input.send_keys(swords)
    axe_input.send_keys(axes)
    arrow_input.send_keys(arrows)
    light_cavalry_input.send_keys(light_cavalry)
    marcher_input.send_keys(marchers)
    heavy_cavalry_input.send_keys(heavy_cavalry)

def clear_inputs(inputs):
    spear_input, sword_input, axe_input, arrow_input, \
        light_cavalry_input, marchers_input, heavy_cavalry_input \
            = inputs

    spear_input.clear()
    sword_input.clear()
    axe_input.clear()
    arrow_input.clear()
    light_cavalry_input.clear()
    marchers_input.clear()
    heavy_cavalry_input.clear()

def scavenge():
    wait = WebDriverWait(driver, 1)

    inputs =  wait.until(EC.visibility_of_all_elements_located \
        ((By.CSS_SELECTOR, 'input[class^="unitsInput"]')))[:-1]

    scavenging_units = [int(element.text.strip('()')) \
        for element in wait.until(EC.visibility_of_all_elements_located \
            ((By.CSS_SELECTOR, 'a[class^="units-entry-all"]')))][:-1]
    
    units_values = get_unit_values(scavenging_units)

    scavenging_options =  wait.until \
        (EC.visibility_of_all_elements_located \
            ((By.CSS_SELECTOR, 'div[class^="scavenge-option"]')))

    for units, option in zip(units_values, scavenging_options):
        try:
            start_button = find_start_button(option)
            send_keys(inputs, units)
            # start_button.click()

            sleep(0.5)

            clear_inputs(inputs)
        except NoSuchElementException:
            pass

def schedule_scavenging(scavenging_jobs, first):
    return_countdown_css_selector = \
        'div[class="options-container"] span[class="return-countdown"]'

    wait = WebDriverWait(driver, 1)

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

    if scavenging_jobs[0] is not None:
        schedule.cancel_job(scavenging_jobs[0])

    next_job = schedule.every().day.at(next_time).do \
        (routine, scavenging_jobs, first)
    
    scavenging_jobs[0] = next_job

    print(f'Next scavenging at {next_time}.')
    
def routine(scavenging_jobs, first):
    open_new_tab()
    first = login(first)
    go_to_scavenging_screen()
    scavenge()
    schedule_scavenging(scavenging_jobs, first)
    close_tab()

scavenging_jobs = [None]

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome('D:\chromedriver.exe', options=options)

first = True
routine(scavenging_jobs, first)

for j in itertools.cycle([1, 2, 3, 2]):
    schedule.run_pending()
    print('.' * j)
    sleep(1)
