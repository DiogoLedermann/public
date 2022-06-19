import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('D:\chromedriver.exe')
driver.maximize_window()
driver.get("https://www.nike.com.br/")

wait = WebDriverWait(driver, 10)

wait.until(EC.element_to_be_clickable \
    ((By.CSS_SELECTOR, '#anchor-acessar-unite-oauth2'))).click()

wait.until(EC.visibility_of_element_located \
    ((By.CSS_SELECTOR, '[placeholder="Endereço de e-mail"]'))) \
        .send_keys('diogoledermannfp@gmail.com')

wait.until(EC.visibility_of_element_located \
    ((By.CSS_SELECTOR, '[placeholder="Senha"]'))) \
        .send_keys('oLAAa100')
