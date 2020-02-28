from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import phrases as p
import time
from random import randint
import words
import globals as gls
import os
import traceback
import random
import heroku3
import requests

with open("dictionary/complements.txt") as compfile:
    global COMPLEMENTS
    COMPLEMENTS = [line.strip() for line in compfile]

with open("dictionary/descs.txt") as descfile:
    global DESCS
    DESCS = [line.strip() for line in descfile]

with open("dictionary/static_phrase_list.txt") as phrasefile:
    global STATIC_PHRASES
    STATIC_PHRASES = [line.strip() for line in phrasefile]


class BitchuteBot:
    def __init__(self, username, password, bot_name):
        self.username = username
        self.password = password
        self.bot_name = bot_name
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--disable-dev-sgm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        # self.driver = webdriver.Chrome("./chromedriver", options=chrome_options)
        self. base_url = "https://www.bitchute.com/"
        self.login()

    def restart_application(self):
        heroku_conn = heroku3.from_key('b477d2e0-d1ba-48b1-a2df-88d87db973e7')
        app = heroku_conn.apps()[self.bot_name]
        app.restart()

    @staticmethod
    def response_generator():
        n = p.Sentence()
        gend_sentence = f"This is kinda {random.choice(words.ADJECTIVES)}. {n}. Learn more at: {gls.single_lander_source()}"
        random_comp = COMPLEMENTS[randint(0, len(COMPLEMENTS) - 1)]
        random_phrase = STATIC_PHRASES[randint(0, len(STATIC_PHRASES) - 1)]
        random_desc = DESCS[randint(0, len(DESCS) - 1)]

        response_list = [gend_sentence, random_comp, f"{random_phrase} {gls.single_lander_source()}", random_desc]

        return response_list[randint(0, len(response_list) - 1)]

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
        tab_xpath = '//*[contains(@href,"#listing-all")]'
        gls.sleep_time()
        try:
            print("session id at infinite scroll: ", self.driver.session_id)
            self.driver.get(self.base_url)
            gls.sleep_time()
            self.driver.find_element_by_xpath(tab_xpath).click()

            gls.sleep_time()
            count = 0
            scroll_pause_time = 6

            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            gls.sleep_time()

            random_num = randint(5, 10)
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

    def link_extractor(self):
        links_set = set()

        global sorted_links_list
        sorted_links_list = []

        results = self.driver.find_elements_by_xpath('//a[@href]')

        print(f"number of video links {len(results)}")

        for res in results:
            final_link = res.get_attribute('href')
            links_set.add(final_link)

        for single_link in list(links_set):
            if '/video/' in single_link:
                print(single_link)
                sorted_links_list.append(single_link)

        return sorted_links_list

    def subscribr(self, video_link):

        try:
            gls.sleep_time()
            self.driver.get(video_link)
            gls.sleep_time()
            button_xpath = "//button[contains(.,'Subscribe')]"
            element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            gls.sleep_time()
            element.click()

        except Exception as em:
            print('subscribr Error occurred ' + str(em))
            print(traceback.format_exc())
            pass

        finally:
            print(" subscribr() done")

    def liker_and_faver(self, video_link):

        try:
            gls.sleep_time()
            self.driver.get(video_link)
            gls.sleep_time()
            like_element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, 'video-like-off')))
            gls.sleep_time()
            like_element.click()

            print("video liked!")
            gls.sleep_time()
            star_xpath = '//*[contains(@data-original-title,"Favorite")]'
            fav_element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, star_xpath)))
            gls.sleep_time()
            fav_element.click()
            print("video faved!")
        except Exception as em:
            print('liker_and_faver Error occurred ' + str(em))
            print(traceback.format_exc())

        finally:
            print("liker_and_faver() done")

    def commentr(self, video_link, single_comment):
        disqus_iframe_xpath = '//*[contains(@title,"Disqus")]'
        btn_xpath = "//button[contains(.,'Post as')]"
        print(f"single comment {single_comment}")

        try:
            gls.sleep_time()
            self.driver.execute_script("window.scrollBy(0,1000)", "")
            self.driver.switch_to.frame(self.driver.find_element_by_xpath(disqus_iframe_xpath))
            placeholder_element = WebDriverWait(self.driver, 25).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, 'placeholder')))
            placeholder_element.click()
            textarea_element = WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located((By.CLASS_NAME, 'textarea')))
            textarea_element.send_keys(single_comment)
            btn_element = self.driver.find_element_by_xpath(btn_xpath)
            gls.sleep_time()
            btn_element.click()

        except Exception as em:
            print('commentr Error occurred ' + str(em))
            print(traceback.format_exc())

        finally:
            print("commentr() done")


if __name__ == '__main__':

    def bitchute_action_sequence():
        count = 0

        bt_bot = BitchuteBot("saber2k", "W4e@qmMkyCrwM%J", 'bitchute-bot-1')

        bt_bot.infinite_scroll()  # to load video urls for extraction

        v_links = bt_bot.link_extractor()

        print(f'number of video links extracted: {len(v_links)}')

        if len(v_links) != 0:

            for _ in range(len(v_links)):
                single_video_link = random.choice(v_links)
                print(f'video being worked on: {single_video_link}')

                bt_bot.subscribr(single_video_link)

                bt_bot.liker_and_faver(single_video_link)

                random_response = bt_bot.response_generator()

                bt_bot.commentr(single_video_link, random_response)

                count += 1

                if count == 400:
                    break

        else:
            print("no video links collected")

        time.sleep(randint(25000, 29000))

        bt_bot.restart_application()

    bitchute_action_sequence()

    # def custom_bitchute_scheduler():
    #     try:
    #         schedule.every().day.at("01:30").do(bitchute_action_sequence)
    #
    #         while True:
    #             schedule.run_pending()
    #             time.sleep(1)
    #
    #     except Exception as e:
    #         print('custom_bitchute_scheduler Error occurred ' + str(e))
    #         print(traceback.format_exc())
    #         pass
    #
    #
    # custom_bitchute_scheduler()
    #
    #
    # def test_locally():
    #     bitchute_action_sequence()

    # test_locally()

