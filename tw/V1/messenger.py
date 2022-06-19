from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from os.path import dirname, realpath
from PIL import Image
from io import BytesIO
import win32clipboard

class Messenger:

    def __init__(self, bot):
        self.driver = bot.driver

    def open_whatsapp(self):
        self.driver.get('https://web.whatsapp.com/')
    
    def open_chat(self):
        wait = WebDriverWait(self.driver, 1)

        wait.until(EC.element_to_be_clickable \
            ((By.CSS_SELECTOR, 'span[title="Eu"]'))).click()

    def type(self, message):
        wait = WebDriverWait(self.driver, 1)

        wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, 'div[class="_2A8P4"]'))) \
                .send_keys(message)

    def send(self):
        wait = WebDriverWait(self.driver, 2)

        wait.until(EC.visibility_of_element_located \
            ((By.CSS_SELECTOR, '[data-icon="send"]'))).click()

    def wait_message(self, message):
        last_message = None

        while last_message != message:

            last_messages = self.driver \
                .find_elements_by_css_selector('span[dir="ltr"]')

            last_message = last_messages[-1].text

            sleep(2)

    def send_image_to_clipboard(self):
        filepath = f'{dirname(realpath(__file__))}/exchangeRates.png'

        image = Image.open(filepath)

        output = BytesIO()

        image.convert("RGB").save(output, "BMP")

        data = output.getvalue()[14:]

        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def send_graph(self):
        self.send_image_to_clipboard()

        try:
            self.open_chat()

        except TimeoutException:
            return
        
        else:
            ActionChains(self.driver) \
                .key_down(Keys.CONTROL) \
                    .send_keys('v') \
                        .key_up(Keys.CONTROL) \
                            .perform()

            self.send()
