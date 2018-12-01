import random
import time

import re
from bs4 import BeautifulSoup
from selenium import webdriver
import json

class Browser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
        self.driver.implicitly_wait(1)

    # self.driver = webdriver.PhantomJS(r'pjs.exe')

    def firstPage(self, user_id):
        self.driver.get("https://scholar.google.com/citations?user=" + user_id)
        time.sleep(random.randrange(1, 3))

    def goTo(self, link):
        self.driver.get(link)

    def getSource(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def close(self):
        self.driver.close()

    def okButton(self):
        return self.driver.find_element_by_css_selector("input[type='submit']")

    def getFriendsPage(self):
        ret = [
            link for link in self.driver.find_elements_by_link_text('See more friends')]
        for l in ret:
            print(l)
        return ret

    def photoCount(self, url):
        # self.driver.get(url + '/photos')
        try:
            if url.find('profile.php') != -1:
                link = url
                self.driver.get(link)
                time.sleep(1)
                self.driver.find_element_by_link_text('Photos').click()
            else:
                link = url + '/photos'
                self.driver.get(link)
        except Exception as e:
            print(e.message)
            return 0
        
        all = self.driver.find_elements_by_link_text('See All')
        # print('Photos Links -------> ',all)
        goto = None
        if (len(all) == 1):
            goto = all[0].click()
        elif (len(all) == 2):
            goto = all[1].click()
        elif (len(all) == 3):
            goto = all[1].click()
        else:
            return 0
        ret = 0
        while True:
            ret += 1
            try:
                goto = self.driver.find_element_by_link_text('See More Photos')
            except Exception as e:
                break
            time.sleep(random.randrange(1, 2))
            goto.click()
        return ret * 12

    def getAllYear(self):
        div_section = self.driver.find_element_by_id('structured_composer_async_container')
        years = div_section.find_elements_by_xpath("div/a")[0:]
        links = []
        for year in years:
            print(year.text)
            print(year.get_attribute('href'))
            links += [year.get_attribute('href')]
        return links

    def getPostStatus(self, url):
        self.goTo(url)
        allYear = self.getAllYear()[1:]
        post = []
        
        for year in allYear:
            html = self.getSource(year)  
            page_count = 1
            while True:
                # html = self.driver.page_source
                # scraper.setHtml(html)
                print("Scrapping page: " + str(page_count))
                page_count += 1
                articles = self.driver.find_elements_by_xpath("//div[@role='article']")
                for i in range(len(articles)):
                    try:
                        if(len(post) >500):
                            return post
                        first_level = articles[i].find_element_by_xpath("div[1]")
                        second_level = first_level.find_element_by_xpath("div[2]")
                        post_text = second_level.text
                        date_div = articles[i].find_element_by_xpath("div[2]/div[1]/abbr")
                        like_comment_meta_data_div = articles[i].find_element_by_xpath("div[2]/div[2]")
                        like_comment_meta_data = like_comment_meta_data_div.text
                        date = date_div.text
                        post += [{
                            'date' : date,
                            'status': post_text,
                            'meta-data': like_comment_meta_data
                        }]
                    except Exception as e:
                        pass
                    
                    # print(post)
                try:
                    self.getNextPage()
                except Exception as e:
                    print(e)
                    break
                    
            time.sleep(random.randrange(1,2))
        return post

    def getNextPage(self):
        try:
            page = self.driver.find_element_by_link_text('See more stories')
            page.click()
            return
        except Exception as e:
            try:
                page = self.driver.find_element_by_link_text('See More Stories')
                page.click()
                return
            except Exception as e:
                try:
                    page = self.driver.find_element_by_link_text('Show More')
                    page.click()
                    return
                except Exception as e:
                    try:
                        page = self.driver.find_element_by_link_text('Show more')
                        page.click()
                        return
                    except Exception as e:
                        raise Exception('Next Page Not Found')
                    pass
                pass
            pass

        


class Scraper():

    def __init__(self):
        print("Hello I'm Scraper()")
        self.host = 'https://scholar.google.com'

    def setHtml(self, html):
        self.bs = BeautifulSoup(html, 'html.parser')

    def getNavLinks(self):
        retVal = []
        links = self.bs.find_all('div', {'class': 'h'})
        for link in links:
            retVal.append((link.a.text, self.host + link.a['href']))
        return retVal

    def scrape(self):
        div = self.bs.find(
            'div', {'id': 'structured_composer_async_container'})
        divs = div.find_all('div', {'role': 'article'})

        retVal = []
        for d in divs:
            tmp = d.find_all('div')
            if len(tmp) >= 3:
                post = tmp[2].text
                retVal.append(post)
        return retVal

    def getElementFromText(self, text):
        return self.bs.findAll(text=re.compile(text))

    
    def getPublications(self):
        print('inside publications...')
        return []

    def extractId(self):
        ids = []
        for link in self.bs.findAll('td', {'class': 'v s'}):
            # print("test:---->  ", link)
            try:
                a = link.a['href'].find('?fref')
                b = link.a['href'].find('&fref')
                c = link.a['href']
                if a is not -1:
                    c = c[0:a]
                if b is not -1:
                    c = c[0:b]
                ids += [
                    [
                        c,
                        link.a.text
                    ]
                ]
            except Exception as e:
                print(e)
                print("Exception for friend : ", c)
        return ids

    def getData(self, name):
        ret = {'name': name}
        try:
            about = self.bs.find('div', {'id': 'bio'}).div.findAll(
                'div', recursive=False)[1].div.text
            ret['about'] = about
        except Exception as e:
            pass

        try:
            all_edu = self.bs.find('div', {'id': 'education'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                              recursive=False)
            edu = []
            for e in all_edu:
                edu += [{
                    'institution': e.div.div.div.div.span.text,
                    'type': e.div.findAll('div', recursive=False)[0].findAll('div', recursive=False)[1].text
                }]
            ret['education'] = edu
        except Exception as e:
            pass

        try:
            all = self.bs.find('div', {'id': 'living'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                       recursive=False)
            data = []
            for d_ in all:
                data += [{
                    d_.div.findAll('td')[0].text: d_.div.findAll('td')[1].text
                }]
            ret['living'] = data
        except Exception as e:
            pass
        try:
            all = self.bs.find('div', {'id': 'contact-info'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                             recursive=False)
            data = []
            for d_ in all:
                data += [{
                    d_.table.findAll('td')[0].text: d_.table.findAll('td')[1].text
                }]
            ret['contact-info'] = data
        except Exception as e:
            pass
        try:
            all = self.bs.find('div', {'id': 'family'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                       recursive=False)
            data = []
            for d_ in all:
                data += [{
                    d_.findAll('h3')[1].text: d_.findAll('h3')[0].text
                }]
            ret['family'] = data
        except Exception as e:
            pass
        try:
            all0 = self.bs.find('div', {'id': 'work'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                     recursive=False)
            data = []
            for d_ in all0:
                p = {}
                i = 0
                info = []
                for dd in d_.div.findAll('div', recursive=True):
                    p[str(i)] = dd.text
                    i += 1
                    info.append(dd.text)
            ret['work'] = info

        except Exception as e:
            # print(e)
            pass
        try:
            all = self.bs.find('div', {'id': 'basic-info'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                           recursive=False)
            data = []
            for d_ in all:
                data += [
                    {d_.table.findAll('td')[0].text: d_.table.findAll('td')[
                        1].text}
                ]
            ret['basic-info'] = data

        except Exception as e:
            pass
        try:
            all = self.bs.find('div', {'id': 'nicknames'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                          recursive=False)
            data = []
            for d_ in all:
                data += [
                    d_.table.findAll('td')[1].text
                ]
            ret['nicknames'] = data
        except Exception as e:
            pass

        return ret
