import os
import platform
import time
from ConfigParser import SafeConfigParser
from selenium import webdriver




class Connect(object):

    def __init__(self):
        config = SafeConfigParser()
        config.read('config.ini')
        self.email = config.get('main', 'email')
        self.password = config.get('main', 'password')
        self.search_link = config.get('main', 'search_link')
        self.limit = config.get('main', 'day_limit')

        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--lang=en')
        self.chrome = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
        self.login()

    def login(self):
        self.chrome.get(url='https://www.linkedin.com')
        self.chrome.find_element_by_id('login-email').send_keys(self.email)
        self.chrome.find_element_by_id('login-password').send_keys(self.password)
        self.chrome.find_element_by_id('login-submit').click()


    def search(self, chrome):
        chrome.get('https://www.linkedin.com/search/results/people/?origin=SWITCH_SEARCH_VERTICAL')
        time.sleep(5)
        chrome.find_element_by_xpath("//fieldset/ol/li[1]/label/div[text()='1st']").click()
        time.sleep(5)
        chrome.find_element_by_xpath("//button/span/span[1]/h3[text()='Keywords']").click()
        time.sleep(5)
        chrome.find_element_by_id("advanced-search-title").send_keys('tra-ta-ta-ta')
        time.sleep(3)
        chrome.execute_script("window.scrollTo(0, 500)")
        time.sleep(3)
        chrome.find_element_by_xpath("//button/span/span[1]/h3[text()='Locations']").click()
        time.sleep(5)
        chrome.find_element_by_id("sf-facetGeoRegion-add").click()
        time.sleep(5)
        chrome.find_element_by_xpath("//div/div[1]/div/div/input[@placeholder='Type a location name']").send_keys("United States")
        time.sleep(5)
        chrome.find_element_by_xpath("//div/ul/li/div/h3").click()
        time.sleep(5)
        chrome.execute_script("window.scrollTo(0, 500)")
        time.sleep(3)

if __name__ == '__main__':
    Connect()
