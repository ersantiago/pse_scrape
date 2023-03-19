#!/home/xinyx/anaconda3/bin/python
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import os
import re
import pygsheets
#import logging
#logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.debug)
#logging.debug('Start of program')

#trcup variant

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup

reppath = '/mnt/share/scripts/admin_scripts/misc'
os.chdir(reppath)

def write(input):
    encode_input = input.encode('ascii', 'ignore')
    with open('/mnt/share/scripts/admin_scripts/misc/filetest.txt', 'wb') as f:
        f.write(encode_input)
        f.close()
# Opening browser


list = '/mnt/share/scripts/admin_scripts/misc/tabpse.txt'
stklist_p = '/mnt/share/scripts/admin_scripts/misc/all_cmpy'
stklist = open(stklist_p, 'r').read().splitlines()
pse_tablefile = open('/mnt/share/scripts/admin_scripts/misc/pse_table.txt', 'w')

# Load pygsheets
path_cred = '/mnt/share/scripts/admin_scripts/api/IT-DA-9a643fc39003.json'
stxd_sheet = 'https://docs.google.com/spreadsheets/d/1au3cvGiRtNvi8SR28yc9p9YK7m15Ad5lZj3-oGtDEVQ/edit#gid=1270897057'

gc = pygsheets.authorize(service_file=path_cred)
wks = gc.open_by_url(stxd_sheet).worksheet_by_title('Raw_Data')

################################################################################################################################################
# Data from investa
inv_dict = {}

header = ['Symbol', 'Last', '%Change', 'Cap', 'Value', '52High', '52Low', 'TTM_PE']
print("".join(word.ljust(11) for word in header))

full_list = []
for cmpy in stklist:
    symb, id1, id2 = cmpy.split()
    inv_url = 'https://www.investagrams.com/Stock/' + symb

    # get requests
    r = requests.get(inv_url)
    insoup = BeautifulSoup(r.text, 'lxml')

    # get chromedriver
    try:
        #parse invstg
        lprice = insoup.select('#lblStockLatestLastPrice')[0].text.strip()
        cap = insoup.select('#lblStockLatestMarketCap')[0].text.strip()
        perc = insoup.select('#lblStockLatestChangePerc')[0].text.strip()
        perc = perc.replace('(', '')
        perc = perc.replace(')', '')
        value = insoup.select('#lblStockLatestValue')[0].text.strip()
        #parse value:
        fundat = insoup.select('#FundamentalAnalysisContent')[0].text.strip()
        rgx52low = re.compile(r'52-Week Low:\s+(.*?)\s+')
        rgx52high = re.compile(r'52-Week High:\s+(.*?)\s+')
        rgxpe = re.compile(r'TTM \(P/E\):\s+(.*?)\s+')
        high52 = rgx52high.findall(fundat)[0]
        low52 = rgx52low.findall(fundat)[0]
        perat = rgxpe.findall(fundat)[0]
        if 'OVERSOLD' in r.text:
            ovs = 'YES'
        else:
            ovs = 'Unchecked'

        if 'B' in cap:
            cap = cap.split('B')[0]
        elif 'T' in cap:
            cap = str(float(cap.split('T')[0]) * 1000)
        elif 'M' in cap:
            cap = str(float(cap.split('M')[0]) / 1000)
        else:
            cap = cap

        if 'K' in value:
            value = float(value.replace('K','').strip())
            value = str(round((value / 1000), 3))
        elif 'M' in value:
            value = str(float(value.replace('M', '').strip()))
        else:
            value = str(round((float(value) / 1000000), 3))
            print('Recheck Units for stock value:' + cmpy)

    except:
        lprice = 'nodata'
        perc = 'nodata'
        cap = 'nodata'
        value = 'nodata'
        high52 = 'nodata'
        low52 = 'nodata'
        perat = 'nodata'
        ovs = 'nodata'
    results = [symb, lprice, perc, cap, value, low52, high52, perat, ovs]
    full_list.append(results)
    print("".join(word.ljust(11) for word in results))
    out_inv = "\t".join(results)
    pse_tablefile.write(out_inv + '\n')
wks.update_values('A2',full_list)
################################################################################################################################################
''''# Data from pse

pse_dict = {}
browser = webdriver.Chrome('C:\\PyEx\\drivers\chromedriver')

for cmpy in stklist:
    symb, id1, id2 = cmpy.split()
    pse_url = 'http://pse.com.ph/stockMarket/companyInfo.html?id=' + id1 + '&security=' + id2 + '&tab=0'
    inv_url = 'https://www.investagrams.com/Stock/' + symb

    # get requests
    #r = requests.get(inv_url)
    #insoup = BeautifulSoup(r.text, 'lxml')

    # get chromedriver
    browser.get(pse_url)
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
                    pse_tablefile.write(symb + '\n')
                    continue
            except TimeoutException:
                print('Timeout')
                pse_tablefile.write(symb + '\n')
                continue
        except TimeoutException:
            print('Timeout')
            pse_tablefile.write(symb + '\n')
            continue
    except TimeoutException:
        print('Timeout')
        pse_tablefile.write(symb + '\n')
        continue

    #parse invstg
    #lprice = insoup.select('#lblStockLatestLastPrice')[0].text.strip()

    #parse webdriver
    lprice = browser.find_element_by_id('ext-gen386').text
    perati = browser.find_element_by_id('headerCurrentPe').text
    value = browser.find_element_by_id('headerTotalValue').text
    high52 = browser.find_element_by_id('headerFiftyTwoWeekHigh').text
    low52 = browser.find_element_by_id('headerFiftyTwoWeekLow').text
    ffloat = browser.find_element_by_id('ext-gen444').text
    cap = browser.find_element_by_id('ext-gen450').text.strip()
    cap = cap.replace(',', '')
    cap = str(round(float(cap)/1000000000, 3))

    results = [perati, low52, high52, ffloat, cap]
    print(symb + ' : ' + perati + ' : ' + low52 + ' : '+ high52 + ' : '+ ffloat + ' : '+ cap)

    pse_out = "\t:\t".join(results)
    pse_dict[symb] = pse_out
    merge_results = symb + '\t:\t' + inv_dict[symb] + '\t:\t' + pse_dict[symb]

    pse_tablefile.write(merge_results + '\n')
'''
pse_tablefile.close()
#browser.close()
