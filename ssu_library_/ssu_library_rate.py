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

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSU")
        self.setGeometry(300, 300, 500, 300)

        self.label = QLabel(' ID ', self)
        self.label.move(320, 20)

        self.label2 = QLabel(' PW ', self)
        self.label2.move(320, 60)

        #self.label3 = QLabel('GmailID ', self)
        #self.label3.move(320, 150)

        #self.label4 = QLabel('NaverID ', self)
        #self.label4.move(320, 200)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(380, 20)
        
        self.code_edit2 = QLineEdit(self)
        self.code_edit2.move(380, 60)

        #self.code_edit3 = QLineEdit(self)
        #self.code_edit3.move(380, 150)

        #self.code_edit4 = QLineEdit(self)
        #self.code_edit4.move(380, 200)

        btn1 = QPushButton("Login", self)
        btn1.move(360, 100)
        btn1.clicked.connect(self.btn1_clicked1)
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 300, 280)
        self.text_edit.setEnabled(False)
    
    def btn1_clicked1(self):
        self.text_edit.append("처리중입니다...잠시만 기다려주세요.")
    def btn1_clicked(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("lang=ko_KR")

        driver = webdriver.Chrome(r'C:\Users\Owner\Desktop\Crawling_Project\sss\chromedriver', chrome_options=options)
        driver.implicitly_wait(3)
        driver.get('https://oasis.ssu.ac.kr/#/')
        driver.implicitly_wait(3)        

        driver.find_element_by_id('goto-login').click()
        driver.find_element_by_id('userid').send_keys(self.code_edit.text())
        driver.find_element_by_id('password').send_keys(self.code_edit2.text())
        driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/form/div[3]/button").click()
        time.sleep(5)
        #driver.get_screenshot_as_file('ScreenShot_SSU_login.png')

        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/ik-static/ul[1]/li[4]/a').click()
        time.sleep(5)
        #driver.switch_to.frame('contentAreaFrame')
        #time.sleep(2)
        #driver.switch_to.frame('isolatedWorkArea')
        #time.sleep(2)
        #driver.get_screenshot_as_file('ScreenShot_SSU_Grade.png')
        
        tbody = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/table/tbody")
        rows = tbody.find_elements_by_tag_name('tr')

        self.text_edit.append("처리중입니다...잠시만 기다려주세요.")
        for index, value in enumerate(rows):
            #print(value.text)
            self.text_edit.append(value.text)
        driver.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()