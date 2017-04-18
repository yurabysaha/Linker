import time
import user
from ConfigParser import SafeConfigParser
from selenium import webdriver
WORK = True


class Accept(object):
    def __init__(self):
        config = SafeConfigParser()
        config.read('config.ini')
        self.email = config.get('main', 'email')
        self.password = config.get('main', 'password')

        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--lang=en')
        self.chrome = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
        self.login()
        self.find_accepted()

    def login(self):
        self.chrome.get(url='https://www.linkedin.com')
        self.chrome.find_element_by_id('login-email').send_keys(self.email)
        self.chrome.find_element_by_id('login-password').send_keys(self.password)
        self.chrome.find_element_by_id('login-submit').click()

    def find_accepted(self):
        self.chrome.get(url='https://www.linkedin.com/mynetwork/invite-connect/connections')
        while WORK:
            blocks = self.chrome.find_elements_by_xpath("//div[@class='core-rail']/div/ul/li")
            for u in blocks:
                name = u.find_element_by_xpath('./div/div/a/span[2]').text
                if user.accept(name) == 3:
                    WORK = False
                    break
            if WORK:
                self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)

if __name__ == '__main__':
    Accept()
