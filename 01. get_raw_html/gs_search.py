from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from openpyxl import Workbook, load_workbook
import os, urllib, re, time, random, winsound, sys

Freq = 1500 # Set Frequency To 2500 Hertz
Dur = 500 # Set Duration To 1000 ms == 1 second
def solve_captcha():
    winsound.Beep(Freq,Dur)
    raw_input('Please, solve the CAPTCHA and press ENTER: ')
# Detects captcha
def checkload(url, element_id):
    loaded_correctly = False
    attempt = 1
    while loaded_correctly == False:
        try:
            print(url)
            br.get(url)
            html = br.find_element_by_xpath('//html').get_attribute('innerHTML').encode('utf-8')
            if html.find("Please show you're not a robot") > 0:
                solve_captcha()
            elif html.find("your computer or network may be sending automated queries") > 0:
                solve_captcha()
            elif html.find("Demuestra que no eres un robot") > 0:
                solve_captcha()
            elif html.find("inusual procedente de tu red de ordenadores") > 0:
                solve_captcha()
            elif html.find("Our systems have detected unusual traffic from your computer") > 0:
                solve_captcha()
            doc_list = br.find_element_by_class_name(element_id)
            loaded_correctly = True
        except:
            if attempt == 3:
                print('THE FOLLOWING URL COULDN\'T BE DOWNLOADED:')
                print(url)
                break
            loaded_correctly = False
            print('Trying again ' + url)
            attempt += 1
            time.sleep(2)

# Open Firefox instance
br = webdriver.Firefox()

br.get('http://scholar.google.com')

# Reads the list of URLs
f = open(sys.argv[1], 'r')
url_list = f.readlines()
del url_list[-1]
f.close()

# Path of this script
c_dir = os.path.dirname(os.path.abspath(__file__))

# Checks if the articles_html directory exists, 
# and creates it if it doesn't.
art_dir = 'articles_html'
if not os.path.exists(art_dir):
    os.makedirs(art_dir)

# Main loop. It iterates through the list of URLs,
# and downloads all the content in HTML format.
# It also checks if there are more than one page
# of results for each journal, and downloads all the
# pages.
i = 1
for c_url in url_list:
    more_results = True
    c_url = c_url.strip()
    sleep_seconds = random.randint(5, 15)
    checkload(c_url, 'gs_rt')
    while more_results == True:
        html = br.find_element_by_xpath('//html').get_attribute('innerHTML').encode('utf-8')
        try:
            br.find_element_by_class_name('gs_rt')
        except:
            more_results = False
            continue # continues to next query if no results are shown in the page
        html = br.find_element_by_xpath('//html').get_attribute('innerHTML').encode('utf-8')
        c_url = br.current_url
        if c_url.find('start=') == -1:
            start_page = '0'
        else:
            start_page = c_url[c_url.find('start=')+6:c_url.find('&', c_url.find('start=')+6)]
        write_path = art_dir + '/' + str(i) + '.' + start_page + '.html'
        w = open(write_path, 'w')
        w.write(html)
        w.close()
        try:
            next_page = br.find_element_by_xpath('//span[contains(@class, "gs_ico_nav_next")]/..').get_attribute('href')
            time.sleep(sleep_seconds)
            checkload(next_page, 'gs_rt')
        except:
            more_results = False
            time.sleep(sleep_seconds)
        i += 1
br.close()
