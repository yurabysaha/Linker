import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from base import BaseMethod
from user import User


class Accept(BaseMethod):

    def __init__(self, text, view):
        BaseMethod.__init__(self)
        self.text = text
        self.view = view
        self.WORK = True
        self.blocks_count = 0
        self.count_for_stop = 0

        self.login()
        self.find_accepted()

    def find_accepted(self):
        self.chrome.get(url='https://www.linkedin.com/mynetwork/invite-connect/connections')
        while self.WORK:
            blocks = self.chrome.find_elements_by_xpath("//div[@class='core-rail']/div/ul/li")
            for u in blocks[self.blocks_count:]:
                name = u.find_element_by_xpath('./div/div/a/span[2]').text
                accept = User().accept(name)
                if accept == 3:
                    self.count_for_stop += 1
                    if self.count_for_stop >= 30:
                        self.WORK = False
                    pass
                if accept == 1:
                    self.view.counts_update()
                    self.count_for_stop = 0
                self.text.insert('end', "Yonchi verify -> %s \n" % name)
                self.text.see('end')
            if self.WORK:
                self.blocks_count = len(blocks)
                self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
            else:
                self.text.insert('end', "Yonchi think that nobody accepted you more")
                self.text.see('end')
                self.chrome.close()

    # def find_accepted(self):
    #     people = User().candidate_for_review()
    #     if people:
    #         users = []
    #         for name in people:
    #             if len(users) < 50:
    #                 users.append(name[0].decode('utf8'))
    #                 if name != people[-1]:
    #                     continue
    #             self.chrome.get(url='https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22F%22%5D&keywords=&origin=GLOBAL_SEARCH_HEADER')
    #             time.sleep(5)
    #             search_field = self.chrome.find_element_by_xpath(".//input[@placeholder='Search']")
    #             search_field.send_keys('firstname:(')
    #             for i in users:
    #                 search_field.send_keys(i)
    #                 if i != users[-1]:
    #                     search_field.send_keys(' OR ')
    #             search_field.send_keys(')')
    #             time.sleep(1)
    #             search_field.send_keys(Keys.ENTER)
    #             time.sleep(5)
    #             self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #             time.sleep(1)
    #             list = self.chrome.find_elements(By.XPATH, ".//div[@class='search-results__cluster-content']/ul/*")
    #             for i in list:
    #                 try:
    #                     user_name = i.find_element_by_xpath(".//h3/span[1]/span").text
    #                     if user_name in users:
    #                         User().accept(user_name)
    #                         self.text.insert('end', "%s -> accept us :)\n" % user_name)
    #                 except Exception as e:
    #                     self.text.insert('end', "%s -> not accept us yet (:\n" % user_name)
    #                     self.text.see('end')
    #             users = []
    #         self.text.insert('end', "Yonchi review all candidate, Yonchi free?\n")
    #         self.text.see('end')
    #         self.chrome.close()
    #     else:
    #         self.text.insert('end', "Nobody to review accept, hahahahhahah!\n")
    #         self.text.see('end')
    #         self.chrome.close()
