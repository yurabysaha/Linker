import os
import platform
import time
from selenium import webdriver


def xmlpath():
    if platform.system() == "Linux":
        return '/'
    else:
        return '\\'

ROOT_PATH=os.getcwd() + xmlpath()


def osw():
    if platform.system() == "Linux":
        return ROOT_PATH + 'chromedriver'
    else:
        return ROOT_PATH + 'chromedriver.exe'


def start():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--lang=en')
    #chrome_options.add_argument('-ignore-certificate-errors')
    chrome = webdriver.Chrome(osw(), chrome_options=chrome_options)
    #browserlink = 'https://www.linkedin.com'

    login(chrome)
    time.sleep(5)
    search(chrome)


def login(chrome):
    chrome.get('https://www.linkedin.com')
    chrome.find_element_by_id('login-email').send_keys('tanyabysaha@gmail.com')
    chrome.find_element_by_id('login-password').send_keys('10021993yura')
    chrome.find_element_by_id('login-submit').click()


def search(chrome):
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
    start()
