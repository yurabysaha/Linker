import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import user
from base import BaseMethod


class Accept(BaseMethod):

    def __init__(self, text):
        BaseMethod.__init__(self)
        self.text = text
        self.WORK = True
        self.blocks_count = 0

        self.login()
        self.find_accepted()

    # def find_accepted(self):
    #     self.chrome.get(url='https://www.linkedin.com/mynetwork/invite-connect/connections')
    #     while self.WORK:
    #         blocks = self.chrome.find_elements_by_xpath("//div[@class='core-rail']/div/ul/li")
    #         for u in blocks[self.blocks_count:]:
    #             name = u.find_element_by_xpath('./div/div/a/span[2]').text
    #             if user.accept(name) == 3:
    #                 self.WORK = False
    #                 break
    #             self.text.insert('end', "Yonchi verify -> {}\n".format(name))
    #             self.text.see('end')
    #         if self.WORK:
    #             self.blocks_count = len(blocks)
    #             self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #             time.sleep(5)

    def find_accepted(self):
        people = user.candidate_for_review()
        if people:
            users = []
            for name in people:
                if len(users) < 20:
                    users.append(name[0])
                    if name != people[-1]:
                        continue
                self.chrome.get(url='https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22F%22%5D&keywords=&origin=GLOBAL_SEARCH_HEADER')
                time.sleep(5)
                search_field = self.chrome.find_element_by_xpath(".//input[@placeholder='Search']")
                search_field.send_keys('firstname:(')
                for i in users:
                    search_field.send_keys(i)
                    if i != users[-1]:
                        search_field.send_keys(' OR ')
                search_field.send_keys(')')
                time.sleep(1)
                search_field.send_keys(Keys.ENTER)
                time.sleep(5)
                list = self.chrome.find_elements(By.XPATH, ".//div[@class='search-results__cluster-content']/ul/*")
                for i in list:
                    try:
                        user_name = i.find_element_by_xpath(".//h3/span[1]/span").text
                        if user_name in users:
                            user.accept(user_name)
                            self.text.insert('end', "%s -> accept us :)\n" % user_name)
                    except Exception as e:
                        self.text.insert('end', "%s -> not accept us yet (:\n" % user_name)
                        self.text.see('end')
                users = []
            self.text.insert('end', "Yonchi review all candidate, Yonchi free?\n")
            self.text.see('end')
            self.chrome.close()
        else:
            self.text.insert('end', "Nobody to review accept, hahahahhahah!\n")
            self.text.see('end')
            self.chrome.close()
