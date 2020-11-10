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
    driver.get('https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/')
    driver.implicitly_wait(3)

    ul = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/div[2]/div/ul")
    lis = ul.find_elements_by_tag_name('li')
    count_list = 0
    for index, value in enumerate(lis):
        if(index > 0 and count_list < 3):
            print(value.text)
            count_list += 1

    driver.quit()

__init__()