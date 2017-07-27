import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from user import User
from base import BaseMethod


class ConnectWithNote(BaseMethod):

    def __init__(self, text, view):
        BaseMethod.__init__(self)
        self.text = text
        self.view = view

        self.login()
        self.send_request()

    def send_request(self):
        counter = User().get_day_counter()
        page_number = 1
        while counter < self.limit:
            self.chrome.get('{}&page={}'.format(self.search_link, page_number))
            time.sleep(5)
            # Scroll page down for loading all list
            self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            list = self.chrome.find_elements(By.XPATH, ".//div[@class='search-results__cluster-content']/ul/li//button")
            self.chrome.execute_script("window.scrollTo(0, 0);")
            if list:
                for item in list:
                    if item.text != "Connect":
                        pass
                    else:
                        # self.chrome.execute_script("window.scrollTo(0, 200)")
                        time.sleep(1)
                        get_url_id = item.find_element_by_xpath("../../../div[contains(@class, 'search-result__info')]/a")
                        link = get_url_id.get_attribute("href")
                        time.sleep(1)
                        item.click()
                        time.sleep(1)
                        try:
                            # chrome.find_element(By.XPATH, './/button[@name="cancel"]').click()
                            if not self.chrome.find_element(By.XPATH, './/button[text()="Send now"]').is_enabled():
                                self.text.insert('end', "Requires email\n")
                                self.text.see('end')
                                time.sleep(2)
                                self.chrome.find_element(By.XPATH, './/button[@name="cancel"]').click()
                                time.sleep(2)
                                continue
                            # self.chrome.find_element(By.XPATH, './/button[@name="cancel"]').click()
                            full_name = item.get_attribute('aria-label').split('with ')[-1]
                            # self.chrome.find_element(By.XPATH, './/button[text()="Send now"]').click()
                            self.chrome.find_element(By.XPATH, './/button[text()="Add a note"]').click()

                            text_field = self.chrome.find_element(By.XPATH, ".//textarea[@id='custom-message']")
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

                            added = User().create(full_name, link)
                            if added == 1:
                                self.text.insert('end', "%s was invited.\n" % full_name)
                                self.text.see('end')
                                counter += 1
                                self.view.counts_update()
                            else:
                                self.text.insert('end', "%s was invited early!\n" % full_name)
                                self.text.see('end')

                            if counter != 0 and counter % 10 == 0 and counter < 1000000:
                                self.text.insert('end', "Current added -> {}\n".format(counter))
                                self.text.see('end')

                            time.sleep(random.randrange(20, 40))
                        except Exception as e:
                            self.text.insert('end', "Yonchi joked: {}\n".format(e))
                            self.text.see('end')
                        if counter == self.limit:
                            self.text.insert('end', "Yonchi finished work !\n")
                            self.text.see('end')
                            counter += 1000000
                            break
                page_number += 1
                self.text.insert('end', "Yonchi still search candidates!\n")
                self.text.see('end')
            else:
                self.text.insert('end', "Yonchi finished work !\n")
                self.text.see('end')
                counter += 1000000
        self.text.insert('end', "Yonchi used all limit !\n")
        self.text.see('end')
        self.chrome.close()
