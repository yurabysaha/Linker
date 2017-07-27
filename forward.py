#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from user import User
from base import BaseMethod


class Forward(BaseMethod):
    def __init__(self, text, view):
        BaseMethod.__init__(self)
        self.text = text
        self.view = view

        self.login()
        self.resend_message()

    def resend_message(self):
        people = User().candidate_for_forward()
        if not people:
            self.text.insert('end', "Nobody to send final messages :(\n")
            self.text.see('end')
            self.chrome.close()
            return
        self.chrome.get(url='https://www.linkedin.com/messaging/')
        time.sleep(5)
        search_field = self.chrome.find_element_by_xpath(".//input[@id='search-conversations']")
        for name in people:
            search_field.clear()
            search_field.send_keys(name)
            search_field.send_keys(Keys.ENTER)
            # Cкролимо блок меседжів поки всі не загрузимо
            scroll_block = True
            max_scroll = 0 #Баг на лінкедіні, вічний скролл
            while scroll_block:
                time.sleep(5)
                items_list = self.chrome.find_elements_by_xpath(".//div[contains(@class, 'msg-conversations-container')]//li")
                self.chrome.execute_script("arguments[0].scrollIntoView(true);", items_list[0])
                time.sleep(1)
                self.chrome.execute_script("arguments[0].scrollIntoView(false);", items_list[-2])
                time.sleep(5)
                if items_list == self.chrome.find_elements_by_xpath(".//div[contains(@class, 'msg-conversations-container')]//li")\
                        or max_scroll == 5:
                    scroll_block = False
                max_scroll += 1

            try:
                items_list = self.chrome.find_elements_by_xpath(".//div[contains(@class, 'msg-conversations-container')]//li")
                for item in items_list:
                    self.chrome.execute_script("arguments[0].scrollIntoView(false);", item)
                    if item.get_attribute("class") == "msg-premium-mailboxes__mailbox":
                        continue
                    if item.find_element_by_xpath('.//h3').text == name[0]:
                        item.click()
                        break
            except NoSuchElementException:
                self.text.insert('end', "Not found : %s\n" % name[0])
                self.text.see('end')
                continue
            time.sleep(2)
            person_name = self.chrome.find_element_by_xpath(".//dt[@class='truncate']/h2").text
            time.sleep(1)
            linkedin_name = name[0]
            if person_name == linkedin_name:
                count_messages = self.chrome.find_elements_by_xpath(".//div[contains(@class, 'message-bubble')]")
                if len(count_messages) > 1:
                    User().finish(name[0])
                    self.text.insert('end', "%s - already answer you\n" % name[0])
                    self.text.see('end')
                    self.view.update_count()
                else:
                    # Send forward message
                    text_field = self.chrome.find_element_by_xpath(".//textarea")
                    if '%s' in self.forward_message:
                        z = linkedin_name.split(' ')
                        if '.' in z[0]:
                            z[0] = z[0] + ' ' + z[1]
                        text = self.forward_message % z[0].title()
                    else:
                        text = self.forward_message
                    z = text.split('\n')
                    for i in z:
                        text_field.send_keys(i)
                        text_field.send_keys(Keys.SHIFT + Keys.ENTER)
                        time.sleep(1)
                    text_field.submit()
                    self.text.insert('end', "Final message was sent to: %s\n" % name[0])
                    self.text.see('end')
                    User().send_second_message(name[0])
                    self.view.update_count()
                    time.sleep(random.randrange(20, 40))
        self.text.insert('end', "Yonchi send all final messages, Yeeeeee!\n")
        self.text.see('end')
        self.chrome.close()
