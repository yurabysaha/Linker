from ConfigParser import RawConfigParser

import time
from selenium import webdriver

import user


class Message:
    def __init__(self, text):
        self.text = text
        config = RawConfigParser()
        config.read('../config.ini')
        self.email = config.get('main', 'email')
        self.password = config.get('main', 'password')
        self.message_text = config.get('main', 'message_text')

        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--lang=en')
        chrome_options.add_argument("start-maximized")
        # self.chrome = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=chrome_options)
        self.chrome = webdriver.Chrome(executable_path='../chromedriver',
                                       chrome_options=chrome_options)
        self.login()
        self.send_message(self.chrome)

    def login(self):
        self.chrome.get(url='https://www.linkedin.com')
        self.chrome.find_element_by_id('login-email').send_keys(self.email)
        self.chrome.find_element_by_id('login-password').send_keys(self.password)
        self.chrome.find_element_by_id('login-submit').click()

    def send_message(self, chrome):
        people = user.candidate_for_message()
        if people:
            self.chrome.get(url='https://www.linkedin.com/mynetwork/invite-connect/connections')
            time.sleep(5)
            for name in people:
                search_field = chrome.find_element_by_xpath(".//input[@type='search']")
                search_field.send_keys(name[0].encode('utf-8'))
                time.sleep(2)
                message_button = chrome.find_element_by_xpath(".//button/span[text()='Message']")
                message_button.click()
                time.sleep(1)
                text_field = chrome.find_element_by_xpath(".//textarea")
                text_field.send_keys(self.message_text.format(name[0].encode('utf-8')))
                time.sleep(1)
                self.text.insert('end', "Message was sent for: {}\n".format(name[0].encode('utf-8')))
                self.text.see('end')
                self.chrome.get(url='https://www.linkedin.com/mynetwork/invite-connect/connections')
                time.sleep(5)
        else:
            self.text.insert('end', "Nobody to send message, hahahahhahah!\n")
            self.text.see('end')