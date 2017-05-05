import random
import time
from selenium.webdriver.common.by import By
import user
from base import BaseMethod


class Connect(BaseMethod):

    def __init__(self, text):
        BaseMethod.__init__(self)
        self.text = text

        self.login()
        self.send_request()

    def send_request(self):
        counter = user.get_day_counter()
        page_number = 1
        while counter < self.limit:
            self.chrome.get('{}&page={}'.format(self.search_link, page_number))
            time.sleep(5)
            list = self.chrome.find_elements(By.XPATH, ".//div[@class='search-results__cluster-content']/ul/li//button")
            if list:
                for item in list:
                    if item.text != "Connect":
                        pass
                    else:
                        # self.chrome.execute_script("window.scrollTo(0, 200)")
                        time.sleep(1)
                        item.click()
                        time.sleep(1)
                        try:
                            # chrome.find_element(By.XPATH, './/button[@name="cancel"]').click()
                            if not self.chrome.find_element(By.XPATH, './/button[text()="Send now"]').is_enabled():
                                self.text.insert('end', "Requires email\n")
                                self.text.see('end')
                                self.chrome.find_element(By.XPATH, './/button[@name="cancel"]').click()
                                continue
                            # self.chrome.find_element(By.XPATH, './/button[@name="cancel"]').click()
                            self.chrome.find_element(By.XPATH, './/button[text()="Send now"]').click()
                            full_name = item.get_attribute('aria-label').split('with ')
                            self.text.insert('end', "%s was invited.\n" % full_name[-1])
                            self.text.see('end')
                            user.create(full_name[-1])
                            time.sleep(random.randrange(20, 40))
                            counter += 1
                        except Exception as e:
                            self.text.insert('end', "Yonchi joked: {}\n".format(e))
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
        self.text.insert('end', "Yonchi used all limit !\n")
        self.text.see('end')
