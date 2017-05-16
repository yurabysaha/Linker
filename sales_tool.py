import random
import time
import urlparse
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from user import User
from base import BaseMethod


class Sales(BaseMethod):

    def __init__(self, text):
        BaseMethod.__init__(self)
        self.text = text

        self.login()
        self.send_request()

    def send_request(self):
        counter = User().get_day_counter()
        page_number = 0
        while counter < self.limit:
            # Parse filter url
            par = urlparse.parse_qs(urlparse.urlparse(self.sales_url).query)
            change_param_url = self.sales_url.replace('count=' + par['count'][0], 'count=' + str(50))
            filter_url = change_param_url.replace('start=' + par['start'][0], 'start=' + str(page_number))
            # -----------------
            self.chrome.get(filter_url)
            time.sleep(5)
            list = self.chrome.find_elements(By.XPATH, ".//ul[@id='results-list']/li//div[@class='content-wrapper']")
            if list:
                for item in list:
                    verify_connect = item.find_elements(By.XPATH, ".//div[@class='secondary-actions-container']"
                                                                 "//ul[@class='dropdown']/li/button")
                    buttons_name = []
                    for v in verify_connect:
                        buttons_name.append(v.get_attribute('class'))
                    if "action connect" not in buttons_name:
                        continue

                    element = item.find_element(By.XPATH, ".//div[@class='secondary-actions-container']")
                    hov = ActionChains(self.chrome).move_to_element(element)
                    hov.perform()
                    time.sleep(1)
                    item.find_element(By.XPATH, ".//button[@class='action connect']").click()
                    time.sleep(3)
                    try:
                        # Cancel if need enter required email address
                        try:
                            self.chrome.find_element(By.XPATH, './/input[@id="connect-email-input"]')
                            self.text.insert('end', "Requires email\n")
                            self.text.see('end')
                            time.sleep(2)
                            self.chrome.find_element(By.XPATH, './/button[@class="dialog-close"]').click()
                            time.sleep(2)
                            continue
                        except:
                            pass
                        # --------------------------------------------
                        full_name = self.chrome.find_element(By.CLASS_NAME, 'fullname').text
                        # Send message
                        text_field = self.chrome.find_element(By.XPATH, ".//textarea[@id='connect-message-content']")
                        text_field.clear()
                        time.sleep(2)
                        # Get First Name
                        if '%s' in self.sales_message_text:
                            z = full_name.split(' ')
                            if '.' in z[0]:
                                z[0] = z[0] + ' ' + z[1]
                            text = self.sales_message_text % z[0].title()
                        else:
                            text = self.sales_message_text
                        z = text.split('\n')
                        for i in z:
                            text_field.send_keys(i)
                            text_field.send_keys(Keys.SHIFT + Keys.ENTER)
                            time.sleep(1)
                        # -------------
                        time.sleep(2)
                        # ------------
                        # self.chrome.find_element(By.XPATH, './/button[@class="dialog-close"]').click()
                        self.chrome.find_element(By.XPATH, './/button[text()="Send Invitation"]').click()
                        self.text.insert('end', "%s was invited.\n" % full_name)
                        self.text.see('end')
                        User().create(full_name)
                        time.sleep(random.randrange(20, 40))
                        counter += 1
                    except Exception as e:
                        self.text.insert('end', "Yonchi joked: {}\n".format(e))
                        self.text.see('end')
                        continue
                    if counter == self.limit:
                        self.text.insert('end', "Yonchi finished work !\n")
                        self.text.see('end')
                        counter += 1000000
                        break
                page_number += 50
                if counter != 0 and counter % 10 == 0 and counter < 1000000:
                    self.text.insert('end', "Current added -> {}\n".format(counter))
                    self.text.see('end')
            else:
                self.text.insert('end', "Yonchi finished work !\n")
                self.text.see('end')
                counter += 1000000
        self.text.insert('end', "Yonchi used all limit !\n")
        self.text.see('end')
        self.chrome.close()
