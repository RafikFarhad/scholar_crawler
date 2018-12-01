from Scraper import Scraper, Browser
import getpass
import sys
import time
import json
import random


# import Helper

def scraping():
    # username = 'adhare.opsora.58'
    # username = input('Your Username: [Press ENTER for default]\n')
    # if username=='':
    #     username = 'adhare.opsora.58'

    # password = input('Your Password:\n')
    # if password=='':
    #     password = 'hola22hola'

    report('Digging in for: ' + '6F3Kj_8AAAAJ')

    browser = Browser()
    browser.firstPage('6F3Kj_8AAAAJ')
    print(browser.driver.page_source)
    report('Loaded')
    time.sleep(5)
    scraper = Scraper()
    publications = scraper.getPublications()
    print(publications)
    report('Done Publication Scraping...')
    # browser.driver.get('https://mbasic.facebook.com/friends/center/requests/')
    # while True:
    #     try:
    #         confirmButton = browser.driver.find_elements_by_link_text('Confirm')
    #     except Exception as e:
    #         print(e.message)
    #         break
    #     if len(confirmButton)==0:
    #         report('All Friend Request Accepted')
    #         break
    #     time.sleep(2)
    #     confirmButton[random.randrange(0, len(confirmButton))].click()
    time.sleep(5000)
    return 1


def report(stri):

    print('################## ' + stri + ' ########################')


def main():

    print('Main Function Started')
    scraping()
    print('Main Function Ends')


if __name__ != 'main':
    main()
