from ConfigParser import RawConfigParser

import time
from base import BaseMethod
from results import Results


class Feed(BaseMethod):
    def __init__(self):
        BaseMethod.__init__(self)

        self.login()
        self.feed_news()

    def feed_news(self):
        keys = ['looking for', 'need full-stack developer', 'looking for full-stack developer', 'hiring developers',
                'remote developer', 'need ios', 'need android', 'recommend company']
        find = True
        count = 0
        results = Results()
        results.create_file()
        while find:
            self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            blocks = self.chrome.find_elements_by_xpath('.//*[@class="core-rail"]/div[@class="ember-view"]/div')
            for i in blocks[count:]:
                try:
                    t = i.find_element_by_xpath('.//article//p').text
                    for k in keys:
                        if k in t:
                            print t
                            href = i.find_element_by_xpath('.//article//a').get_attribute('href')
                            print href
                            results.update_file(t, href)
                            break
                except:
                    pass
            if count == len(blocks):
                find = False
            else:
                count = len(blocks)
        self.chrome.close()
