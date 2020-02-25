from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import phrases as p
import time
from random import randint
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
        self. base_url = "https://www.bitchute.com/"
        self.login()

    @staticmethod
    def exit_application():
        os.system("python restart.py")

    def login(self):
        print("session id at login: ", self.driver.session_id)

        try:

            self.driver.get(f"{self.base_url}")

            login_element = self.driver.find_element_by_link_text("Login")
            self.driver.implicitly_wait(10)
            login_element.click()

            # fill up the credential fields
            gls.sleep_time()
            self.driver.find_element_by_name('username').send_keys(self.username)
            gls.sleep_time()
            self.driver.find_element_by_name('password').send_keys(self.password)
            gls.sleep_time()
            self.driver.find_element_by_xpath('//*[contains(@id,"auth_submit")]').click()

            print("login success...")
        except Exception as e:
            print("the login issue is: ", e)
            print(traceback.format_exc())
            pass

    def infinite_scroll(self):
        print("starting infinite scroll")
        popular_tab_xpath = '//*[contains(@href,"#listing-popular")]'
        gls.sleep_time()
        try:
            print("session id at infinite scroll: ", self.driver.session_id)
            self.driver.get(self.base_url)
            gls.sleep_time()
            self.driver.find_element_by_xpath(popular_tab_xpath).click()

            gls.sleep_time()
            count = 0
            scroll_pause_time = 6

            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            gls.sleep_time()

            random_num = randint(3, 7)
            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(scroll_pause_time)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                gls.sleep_time()

                if new_height == last_height:
                    break
                last_height = new_height

                count += 1
                print(f'number of scrolls', count)
                if count == random_num:
                    break

        except Exception as em:
            print('infinite_scroll Error occurred ' + str(em))
            print(traceback.format_exc())
            pass

        finally:
            print(" infinite_scroll() done")


if __name__ == '__main__':
    bt_bot = BitchuteBot("saber2k", "W4e@qmMkyCrwM%J")

    bt_bot.infinite_scroll()

    n = p.Sentence()
    # final_sentence = f"This is kinda {random.choice(words.ADJECTIVES)}. {n}. Learn more at: {gls.single_lander_source()}"

