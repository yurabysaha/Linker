import random
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
        people = user.candidate_for_forward()
        if not people:
            self.text.insert('end', "Nobody to send final messages :(\n")
            self.text.see('end')
            self.chrome.close()
            return
        self.chrome.get(url='https://www.linkedin.com/messaging/')
        time.sleep(5)
        search_field = self.chrome.find_element_by_xpath(".//input[@id='search-conversations']")
        for name in people:
            search_field.clear()
            search_field.send_keys(name)
            search_field.send_keys(Keys.ENTER)
            time.sleep(5)
            try:
                items_list = self.chrome.find_elements_by_xpath(".//div[@class='msg-conversations-container']//li")
                for item in items_list:
                    if item.get_attribute("class") == "msg-premium-mailboxes__mailbox":
                        continue
                    if item.find_element_by_xpath('.//h3').text == name[0]:
                        item.click()
                        break
            except NoSuchElementException:
                self.text.insert('end', "Not found : %s\n" % name[0])
                self.text.see('end')
                continue
            time.sleep(2)
            person_name = self.chrome.find_element_by_xpath(".//dt[@class='truncate']/h3").text
            time.sleep(1)
            if person_name == name[0]:
                count_messages = self.chrome.find_elements_by_xpath(".//div[contains(@class, 'message-bubble')]")
                if len(count_messages) > 1:
                    user.finish(name[0])
                else:
                    # Send forward message
                    text_field = self.chrome.find_element_by_xpath(".//textarea")
                    if '%s' in self.forward_message:
                        text = self.forward_message % name[0]
                    else:
                        text = self.forward_message
                    z = text.split('\n')
                    for i in z:
                        text_field.send_keys(i)
                        text_field.send_keys(Keys.SHIFT + Keys.ENTER)
                        time.sleep(1)
                    text_field.submit()
                    self.text.insert('end', "Final message was sent to: %s\n" % name[0])
                    self.text.see('end')
                    user.send_second_message(name[0])
                    time.sleep(random.randrange(20, 40))
        self.text.insert('end', "Yonchi send all final messages, Yeeeeee!\n")
        self.text.see('end')
        self.chrome.close()
