#! python3
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass

#import logging
#logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.debug)
#logging.debug('Start of program')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


# Opening browser
browser = webdriver.Chrome('C:\\PyEx\\drivers\chromedriver')

list = 'C:\\PyEx\\tabpse.txt'
list_cmp = open(list, 'r')

pse_tablefile = open('pse_table.txt', 'w')

for cmpy in list_cmp.read().splitlines():
    site = cmpy.split()[0]
    sym = cmpy.split()[1]
    browser.get(site)

    delay = 5 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'headerCurrentPe')))
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'headerLastTradePrice')))
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'headerTotalValue')))
                try:
                    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'ext-gen442')))
                except TimeoutException:
                    print('Timeout')
                    pse_tablefile.write(sym + '\n')
                    continue
            except TimeoutException:
                print('Timeout')
                pse_tablefile.write(sym + '\n')
                continue
        except TimeoutException:
            print('Timeout')
            pse_tablefile.write(sym + '\n')
            continue
    except TimeoutException:
        print('Timeout')
        pse_tablefile.write(sym + '\n')
        continue

    perati = browser.find_element_by_id('headerCurrentPe').text
    value = browser.find_element_by_id('headerTotalValue').text
#    cap = browser.find_element_by_id('ext-gen451').text

    lprice = browser.find_element_by_id('ext-gen386').text
#    ffloat = browser.find_element_by_id('ext-gen445').text
    high52 = browser.find_element_by_id('headerFiftyTwoWeekHigh').text
    low52 = browser.find_element_by_id('headerFiftyTwoWeekLow').text

    ffloat = browser.find_element_by_id('ext-gen444').text
    cap = browser.find_element_by_id('ext-gen449').text

    print(sym + ' : ' + perati + ' : ' + lprice + ' : '+ low52 + ' : '+ high52 + ' : '+ cap + ' : '+ ffloat + ' : '+ value)
    pse_info = [sym, perati, lprice, low52, high52, cap, ffloat, value]
    pse_tablefile.write("\t:\t".join(pse_info) + '\n')

pse_tablefile.close()
browser.close()