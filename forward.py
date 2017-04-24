from ConfigParser import RawConfigParser

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import user


class Forward:
    def __init__(self, text):
        self.text = text
        config = RawConfigParser()
        config.read('../config.ini')
        self.email = config.get('main', 'email')
        self.password = config.get('main', 'password')
        self.forward_message = config.get('main', 'forward_message')

        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--lang=en')
        chrome_options.add_argument("start-maximized")
        self.chrome = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=chrome_options)
        # self.chrome = webdriver.Chrome(executable_path='../chromedriver',
        #                                chrome_options=chrome_options)
        self.login()
        self.resend_message()

    def login(self):
        self.chrome.get(url='https://www.linkedin.com')
        self.chrome.find_element_by_id('login-email').send_keys(self.email)
        self.chrome.find_element_by_id('login-password').send_keys(self.password)
        self.chrome.find_element_by_id('login-submit').click()

    def resend_message(self):
        people = user.candidate_for_message()
        self.chrome.get(url='https://www.linkedin.com/messaging/')
        time.sleep(5)
        search_field = self.chrome.find_element_by_xpath(".//input[@id='search-conversations']")
        for name in people:
            search_field.send_keys(name)
            time.sleep(5)
            try:
                first_item_list = self.chrome.find_element_by_xpath(".//div[@class='msg-conversations-container']//li[1]")
                first_item_list.click()
            except NoSuchElementException:
                self.text.insert('end', "Not found : %s\n" % name)
                self.text.see('end')
                continue
            time.sleep(2)
            person_name = self.chrome.find_element_by_xpath(".//dt[@class='truncate']/h3").text
            time.sleep(1)
            if person_name == name:
                count_messages = len(self.chrome.find_element_by_xpath(".//div[contains(@class, 'message-bubble')]"))
                if count_messages > 1:
                    user.finish(name)
                else:
                    # Send forward message
                    text_field = self.chrome.find_element_by_xpath(".//textarea")
                    text = self.forward_message % name[0]
                    z = text.split('\n')
                    for i in z:
                        text_field.send_keys(i)
                        text_field.send_keys(Keys.SHIFT + Keys.ENTER)
                        time.sleep(1)
                    text_field.submit()
                    self.text.insert('end', "Message was sent to: %s\n" % name[0])
                    self.text.see('end')
                    user.send_second_message(name[0])
                    time.sleep(31)
                    # Push data base


