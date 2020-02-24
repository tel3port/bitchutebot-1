from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import phrases as p
import random
import words
import globals as gls
import os
import traceback

with open("dictionary/complements.txt") as compfile:

    COMPLEMENTS = [line.strip() for line in compfile]

with open("dictionary/descs.txt") as descfile:

    DESCS = [line.strip() for line in descfile]

with open("dictionary/static_phrase_list.txt") as phrasefile:
    STATIC_PHRASES = [line.strip() for line in phrasefile]


class BitchuteBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--disable-dev-sgm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # chrome_options.add_argument("--headless")
        # self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        self.driver = webdriver.Chrome("./chromedriver", options=chrome_options)
        self. base_url = "https://www.bitchute.com"
        self.login()

    def login(self):
        print("logging me in....")
        print("session id at login: ", self.driver.session_id)

        try:

            self.driver.get(f"{self.base_url}/login/")
            WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable((By.NAME, "id")))

            # fill up the credential fields
            self.driver.find_element_by_name('id').send_keys(self.username)
            self.driver.find_element_by_name('password').send_keys(self.password)

            self.driver.find_element_by_xpath('//*[contains(@type,"submit")]').click()

            print("login success...")
        except Exception as e:
            print("the login issue is: ", e)
            print(traceback.format_exc())
            pass


if __name__ == '__main__':
    n = p.Sentence()
    final_sentence = f"This is kinda {random.choice(words.ADJECTIVES)}. {n}. Learn more at: {gls.single_lander_source()}"
    print(final_sentence)

