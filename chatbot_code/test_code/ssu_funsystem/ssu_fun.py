import requests
from bs4 import BeautifulSoup
import csv

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
        k= img.attrs.get("style")
        s = ""
        c = 0
        for j in k:
            c = c+1
            if(c>21 and c<54):
                s = s + j       
        imgs = "https://fun.ssu.ac.kr" + s
        table = calum.get_text(), timetxt, link , imgs
        print(table)