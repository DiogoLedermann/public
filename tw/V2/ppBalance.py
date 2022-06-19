from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome('D:\chromedriver.exe', options=options)

driver.get("https://www.tribalwars.com.br/")

wait = WebDriverWait(driver, 1)
try:
    wait.until(EC.visibility_of_element_located \
        ((By.ID, 'user'))).send_keys('BradleyLedermann')
    wait.until(EC.visibility_of_element_located \
        ((By.ID, 'password'))).send_keys('oLAAa100', Keys.RETURN)
except TimeoutException:
    pass

input('Press enter to continue...')

wait = WebDriverWait(driver, 2.5)

wait.until(EC.element_to_be_clickable \
    ((By.CSS_SELECTOR, '[href$="107"] span'))).click()

try:
    wait.until(EC.element_to_be_clickable \
        ((By.LINK_TEXT, 'Abrir'))).click()
    wait.until(EC.element_to_be_clickable \
        ((By.LINK_TEXT, 'Continue a jogar'))).click()
except TimeoutException:
    pass

wait.until(EC.element_to_be_clickable \
    ((By.LINK_TEXT, 'Combinado'))).click()

wait.until(EC.element_to_be_clickable \
    ((By.CSS_SELECTOR, '[href$="premium"]'))).click()

wait.until(EC.element_to_be_clickable \
    ((By.LINK_TEXT, 'Histórico de pontos'))).click()

data = []
for i in range(10):
    table = wait.until(EC.element_to_be_clickable \
        ((By.CSS_SELECTOR, '[class="vis"]')))

    rows = table.find_elements_by_tag_name('tr')

    for row in rows[1:]:
        if row.text.split()[5] == 'Utilizado':
            continue
        else:
            data.append(row.text)
    
    pages_navigator = wait.until(EC.element_to_be_clickable \
        ((By.CSS_SELECTOR, '[class="vis_item"]')))
    
    next_page = pages_navigator.find_element_by_css_selector('strong + a')
    next_page.click()
    
date_times = []
PPs = []
Resourses = []
resourse_balance = 0
year = datetime.now().year
for row in data:
    date_time = row.split()[:3]
    date_time = ''.join(date_time)
    date_times.append(date_time)
    
    if len(row.split()) == 13:
        pps = int(row.split()[7])
    elif len(row.split()) == 14:
        pps = int(row.split()[8])

    PPs.append(pps)

    if row.split()[-2] == 'vendido':
        resourse_balance += int(row.split()[-1].strip('()'))
    elif row.split()[-2] == 'comprado':
        resourse_balance -= int(row.split()[-1].strip('()'))

    Resourses.append(resourse_balance)

date_times = date_times[::-1]
PPs = PPs[::-1]
Resourses = Resourses[::-1]

data = {
            "date_times" : date_times,
            "PPs" : PPs,
            "Resourses" : Resourses
        }

with open('ppBalanceData.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

with open('ppBalanceData.json', encoding='utf-8') as file:
    data = json.load(file)

date_times = data['date_times']
PPs = data['PPs']
Resourses = data['Resourses']
Resourses = [value + abs(Resourses[0]) for value in Resourses]

date_times = [datetime.strptime('2021'+date_time, '%Y%b%d,%H:%M') for date_time in date_times]

xticks = []
date_time = date_times[0].replace(minute=0)

while date_time < date_times[-1] + timedelta(hours=1):
    xticks.append(date_time)
    date_time += timedelta(hours=1)

fig, (ax1, ax2) = \
    plt.subplots(figsize=(14, 10), nrows=2, sharex=True)

i = 0
ax1.set_title('Resoures X Datetime', fontsize=20)
ax1.set_xlabel('Datetime', fontsize=18)
ax1.set_ylabel('Resourses', fontsize=18)
ax1.grid()
ax1.plot_date(date_times[i:], Resourses[i:], '-o', label='Resoures')
ax1.legend()

ax2.set_title('PPs X Datetime', fontsize=20)
ax2.set_xlabel('Datetime', fontsize=18)
ax2.set_ylabel('PPs', fontsize=18)
ax2.grid()
ax2.plot_date(date_times[i:], PPs[i:], '-o', label='PPs', color='gold')
ax2.legend()

ax1.set_xticks(xticks)
ax1.tick_params(labelright=True, labelsize=14)

myFmt = mdates.DateFormatter('%b%d - %Hh')
ax1.xaxis.set_major_formatter(myFmt)

fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')

plt.show()
