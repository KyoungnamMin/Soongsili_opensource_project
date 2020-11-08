from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import smtplib
from email.mime.text import MIMEText
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *

def __init__():

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(r'C:\Users\Owner\Desktop\Crawling_Project\sss\chromedriver', chrome_options=options)
    driver.implicitly_wait(3)
    driver.get('https://oasis.ssu.ac.kr/#/')
    driver.implicitly_wait(3)

    driver.find_element_by_id('goto-login').click()
    driver.find_element_by_id('userid').send_keys('20162564')
    driver.find_element_by_id('password').send_keys('Go970110go!')
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/form/div[3]/button").click()
    time.sleep(5)
    
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/ik-static/ul[1]/li[4]/a').click()
    time.sleep(5)
            
    tbody = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/table/tbody")
    rows = tbody.find_elements_by_tag_name('tr')
    for index, value in enumerate(rows):
        print(value.text)
    driver.quit()
__init__()