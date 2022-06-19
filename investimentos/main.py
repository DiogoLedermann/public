from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome('D:\chromedriver.exe', options=options)
driver.maximize_window()
driver.get("https://www.nuinvest.com.br/")

wait = WebDriverWait(driver, 1)

css_selector = 'a.header-button.header-button--login.header-button--v2-purple'

wait.until(EC.element_to_be_clickable \
    ((By.CSS_SELECTOR, css_selector))).click()

wait.until(EC.visibility_of_element_located \
    ((By.ID, 'username'))) \
        .send_keys('13613692724')

wait.until(EC.visibility_of_element_located \
    ((By.ID, 'password'))) \
        .send_keys('oLAAa100!', Keys.RETURN)

input('Pressione Enter para continuar')
