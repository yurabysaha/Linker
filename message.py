import random
import time
from selenium.webdriver.common.keys import Keys
import user
from base import BaseMethod


class Message(BaseMethod):
    def __init__(self, text):
        BaseMethod.__init__(self)
        self.text = text

        self.login()
        self.send_message()

    def send_message(self):
        people = user.candidate_for_message()
        if people:
            for name in people:
                self.chrome.get(url='https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22F%22%5D&keywords=&origin=GLOBAL_SEARCH_HEADER')
                time.sleep(5)
                search_field = self.chrome.find_element_by_xpath(".//input[@placeholder='Search']")
                search_field.send_keys(name)
                time.sleep(1)
                search_field.send_keys(Keys.ENTER)
                time.sleep(5)
                try:
                    user_name = self.chrome.find_element_by_xpath(".//h3/span[1]/span").text
                    if user_name != name[0]:
                        continue
                except Exception as e:
                    print (e)
                    continue
                message_button = self.chrome.find_element_by_xpath(".//button[text()='Message']")
                message_button.click()
                time.sleep(1)
                text_field = self.chrome.find_element_by_xpath(".//textarea")
                if '%s' in self.message_text:
                    text = self.message_text % name[0]
                else:
                    text = self.message_text
                z = text.split('\n')
                for i in z:
                    text_field.send_keys(i)
                    text_field.send_keys(Keys.SHIFT + Keys.ENTER)
                    time.sleep(1)
                text_field.submit()
                self.text.insert('end', "Message was sent to: %s\n" % name[0])
                self.text.see('end')
                user.send_message(name[0])
                time.sleep(random.randrange(20, 40))
            self.text.insert('end', "Yonchi send all messages, Yeeeeee!\n")
            self.text.see('end')
            self.chrome.close()
        else:
            self.text.insert('end', "Nobody to send message, hahahahhahah!\n")
            self.text.see('end')
