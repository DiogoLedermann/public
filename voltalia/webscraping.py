import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('D:\chromedriver.exe')

driver.get("https://www.google.com.br/")

wait = WebDriverWait(driver, 1)

wait.until(EC.visibility_of_element_located \
    ((By.CSS_SELECTOR, 'input[title=Pesquisar]'))) \
        .send_keys('web scraping wiki', Keys.RETURN)

wait.until(EC.element_to_be_clickable \
    ((By.PARTIAL_LINK_TEXT, 'Coleta de dados web'))).click()

tableElement = wait.until(EC.visibility_of_element_located \
    ((By.CSS_SELECTOR, 'table[class=wikitable]')))

table_data = tableElement.find_elements_by_tag_name('td')

my_table = [data.text for data in table_data]

my_table = np.reshape(my_table, (4, 4))

df = pd.DataFrame(my_table)
print(df)

df.to_excel("output.xlsx")
