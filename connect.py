import time
from ConfigParser import RawConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
import user
import os

class Connect(object):

    def __init__(self, text):
        self.text = text
        config = RawConfigParser()
        config.read('../config.ini')
        self.email = config.get('main', 'email')
        self.password = config.get('main', 'password')
        self.search_link = config.get('main', 'search_link')
        self.limit = config.getint('main', 'day_limit')

        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--lang=en')
        chrome_options.add_argument("start-maximized")
        #self.chrome = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=chrome_options)
        self.chrome = webdriver.Chrome(executable_path='../chromedriver',
                                       chrome_options=chrome_options)
        self.login()
        self.send_request(self.chrome)

    def login(self):
        self.chrome.get(url='https://www.linkedin.com')
        self.chrome.find_element_by_id('login-email').send_keys(self.email)
        self.chrome.find_element_by_id('login-password').send_keys(self.password)
        self.chrome.find_element_by_id('login-submit').click()

    def send_request(self, chrome):
        counter = user.get_day_counter()
        page_number = 1
        while counter < self.limit:
            chrome.get('{}&page={}'.format(self.search_link, page_number))
            time.sleep(5)
            list = chrome.find_elements(By.XPATH, ".//div[@class='search-results__cluster-content']/ul/li//button")

            if list:
                for item in list:
                    if item.text != "Connect":
                        pass
                    else:
                        # self.chrome.execute_script("window.scrollTo(0, 200)")
                        time.sleep(1)
                        item.click()
                        time.sleep(4)
                        try:
                            chrome.find_element(By.XPATH, './/button[@name="cancel"]').click()
                            # chrome.find_element(By.XPATH, './/button[text()="Send now"]').click()
                            full_name = item.get_attribute('aria-label').split('with ')
                            self.text.insert('end', "{} was ivited.\n".format(full_name[-1]))
                            self.text.see('end')
                            user.create(full_name[-1])
                            counter += 1
                        except Exception as e:
                            self.text.insert('end', "Yonchi joked: {}\n".format(e.message))
                            self.text.see('end')
                        if counter == self.limit:
                            self.text.insert('end', "Yonchi finished work !\n")
                            self.text.see('end')
                            counter += 1000000
                            break
                page_number += 1
                if counter != 0 and counter % 10 == 0 and counter < 1000000:
                    self.text.insert('end', "Current added -> {}\n".format(counter))
                    self.text.see('end')
            else:
                self.text.insert('end', "Yonchi finished work !\n")
                self.text.see('end')
                counter += 1000000
                        # chrome.find_element(By.XPATH, './/button[text()="Send now"]').click()


        # chrome.find_element_by_xpath("//fieldset/ol/li[1]/label/div[text()='1st']").click()
        # time.sleep(5)
        # chrome.find_element_by_xpath("//button/span/span[1]/h3[text()='Keywords']").click()
        # time.sleep(5)
        # chrome.find_element_by_id("advanced-search-title").send_keys('tra-ta-ta-ta')
        # time.sleep(3)
        # chrome.execute_script("window.scrollTo(0, 500)")
        # time.sleep(3)
        # chrome.find_element_by_xpath("//button/span/span[1]/h3[text()='Locations']").click()
        # time.sleep(5)
        # chrome.find_element_by_id("sf-facetGeoRegion-add").click()
        # time.sleep(5)
        # chrome.find_element_by_xpath("//div/div[1]/div/div/input[@placeholder='Type a location name']").send_keys("United States")
        # time.sleep(5)
        # chrome.find_element_by_xpath("//div/ul/li/div/h3").click()
        # time.sleep(5)
        # chrome.execute_script("window.scrollTo(0, 500)")
        # time.sleep(3)
