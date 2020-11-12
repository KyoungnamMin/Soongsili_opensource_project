# maximal line length when calling readline(). This is to prevent
# reading arbitrary length lines. RFC 1939 limits POP3 line length to
# 512 characters, including CRLF. We have selected 2048 just to be on

# the safe side.


import requests
from bs4 import BeautifulSoup
import csv

filename = "펀시스템.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "공지명","기간","링크", "이미지"
writer.writerow(title)
for i in range(1,3):
    url = "https://fun.ssu.ac.kr/ko/program/all/list/all/{}".format(i)
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    funsystems = soup.find("ul", attrs = {"class": "columns-4"}).find_all("li")
    for funsystem in funsystems:
        calum = funsystem.find("b", attrs = {"class" : "title"})
        link = funsystem.a["href"]
        time = funsystem.find_all("small")
        for item in time:
            timetxt = item.get_text()
        img = funsystem.find("div", attrs={"class" : "cover"})    
        table = calum.get_text(), timetxt, link , img
        writer.writerow(table)
        
        
        
        

