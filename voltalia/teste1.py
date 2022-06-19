from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from urllib.request import urlretrieve

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome('D:\chromedriver.exe', options=options)
driver.get("http://clima1.cptec.inpe.br/monitoramentobrasil/pt")

wait = WebDriverWait(driver, 5)

select_element = wait.until(EC.element_to_be_clickable \
    ((By.CSS_SELECTOR, '[title="Variável dados mensais"]')))

select_object = Select(select_element)
select_object.select_by_index(1)

select_element = wait.until(EC.element_to_be_clickable \
    ((By.CSS_SELECTOR, '#ano_mensal')))

select_object = Select(select_element)
select_object.select_by_index(1)

select_element = wait.until(EC.element_to_be_clickable \
    ((By.CSS_SELECTOR, '#dad_men > select:nth-child(5)')))

select_object = Select(select_element)

for i in range(5):
    select_object.select_by_index(i)

    src = wait.until(EC.visibility_of_element_located \
        ((By.CSS_SELECTOR, '#monitoramento_brasil > span > img'))) \
            .get_attribute('src')

    urlretrieve(src, filename=f"voltaliaImgs/Mapa (Mês {i+1}).png")

driver.quit()
