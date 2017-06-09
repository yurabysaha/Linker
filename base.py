import os
from ConfigParser import RawConfigParser
from selenium import webdriver


class BaseMethod:
    def __init__(self):
        config = RawConfigParser()
        config.read('../config.ini')
        self.email = config.get('main', 'email')
        self.password = config.get('main', 'password')
        self.limit = config.getint('main', 'day_limit')
        self.search_link = config.get('main', 'search_link')
        self.sales_url = config.get('main', 'sales_url')
        self.forward_message = config.get('main', 'forward_message')
        self.message_text = config.get('main', 'message_text')
        self.sales_message_text = config.get('main', 'sales_message_text')
        self.witch_browser = config.get('main', 'browser')

        if self.witch_browser == '1':
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument('--lang=en')
            chrome_options.add_argument("start-maximized")
            self.chrome = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=chrome_options)
        else:
            self.chrome = webdriver.PhantomJS(executable_path='../phantomjs.exe')

    def login(self):
        self.chrome.get(url='https://www.linkedin.com')
        self.chrome.find_element_by_id('login-email').send_keys(self.email)
        self.chrome.find_element_by_id('login-password').send_keys(self.password)
        self.chrome.find_element_by_id('login-submit').click()
