import os
import platform
from ConfigParser import RawConfigParser
from selenium import webdriver
os.environ['HEADLESS_DRIVER'] = '../chromedriver.exe'


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

        if self.witch_browser == '0':  # Run without browser gui
            if platform.system() == 'Windows':
                chrome_options = webdriver.ChromeOptions()
                prefs = {"profile.default_content_setting_values.notifications": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                chrome_options.add_argument('--lang=en')
                chrome_options.add_argument("start-maximized")
                self.chrome = webdriver.Chrome('../headless_ie_selenium.exe', chrome_options=chrome_options)
            else:
                chrome_options = webdriver.ChromeOptions()
                prefs = {"profile.default_content_setting_values.notifications": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                chrome_options.add_argument('--lang=en')
                chrome_options.add_argument('--disable-popup-blocking')
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("start-maximized")
                self.chrome = webdriver.Chrome(executable_path='../chromedriver', chrome_options=chrome_options)
        else:
            if platform.system() == 'Windows':
                chrome_options = webdriver.ChromeOptions()
                prefs = {"profile.default_content_setting_values.notifications": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                chrome_options.add_argument('--lang=en')
                chrome_options.add_argument("start-maximized")
                self.chrome = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=chrome_options)
            else:
                chrome_options = webdriver.ChromeOptions()
                prefs = {"profile.default_content_setting_values.notifications": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                chrome_options.add_argument('--lang=en')
                chrome_options.add_argument('--disable-popup-blocking')
                chrome_options.add_argument("start-maximized")
                self.chrome = webdriver.Chrome(executable_path='../chromedriver', chrome_options=chrome_options)

    def login(self):
        self.text.insert('end', "Open Linkedin.com...\n")
        self.chrome.get(url='https://www.linkedin.com')
        try:
            self.text.insert('end', "Try login...\n")
            self.chrome.find_element_by_id('login-email').send_keys(self.email)
            self.chrome.find_element_by_id('login-password').send_keys(self.password)
            self.chrome.find_element_by_id('login-submit').click()
            self.text.insert('end', "Login successful\n")
        except:
            self.text.insert('end', "Ooopppss.. Problem with login\n")
            exit()
