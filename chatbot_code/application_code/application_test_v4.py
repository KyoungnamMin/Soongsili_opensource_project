from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import sys
import time

app = Flask(__name__)

answer_library = []

@app.route('/library', methods=['GET', 'POST'])
def library_func():
    req = request.get_json()
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--no-sandbox')

    driver = Chrome('/usr/local/bin/chromedriver', options=chrome_options)
    driver.get('https://oasis.ssu.ac.kr/#/')

    driver.find_element_by_id('goto-login').click()
    driver.find_element_by_id('userid').send_keys('20162564')
    driver.find_element_by_id('password').send_keys('Go970110go!')
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/form/div[3]/button").click()
    driver.implicitly_wait(3)

    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/ik-static/ul[1]/li[4]/a').click()

    tbody = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/table/tbody")
    rows = tbody.find_elements_by_tag_name('tr')
    
    for index, value in enumerate(rows):
        answer_library.append(value.text)
    driver.quit()
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "type": "basicCard",
                    "items": [
                        {
                            "title": "도서관",
                            "description": answer_library[2],
                            "thumbnail": {
                                "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                            }
                        }
                    ]
                }
            ]
        }
    }
    return jsonify(res)


'''@app.route('/food', methods=['GET', 'POST'])
def food_func():
    req = request.get_json()
    user_menu = req['userRequest']
    user_menu = user_menu['utterance']
    
    url = "https://soongguri.com/main.php?mkey=2&w=3&l=2"
    res = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(res, "html.parser")

    data = soup.find("div", attrs = {"class": "detail_center"})
    table = data.find("table")
    trs = table.find_all("tr")
    dodam_launch = trs[3].find_all("td")
    dodam_diner = trs[5].find_all("td")
    faculty_launch = trs[8].find_all("td")
    thekichin_pasta = trs[11].find_all("td")
    thekichin_pizza = trs[13].find_all("td")
    thekichin_desert = trs[15].find_all("td")
    
    answer_dodam_launch = []
    answer_dodam_diner = []
    answer_faculty_launch = []
    answer_thekichin_pasta = []
    answer_thekichin_pizza=[]
    answer_thekichin_desert=[]

    for dodam in dodam_launch : 
        answer_dodam_launch.append(dodam)
    for dodam2 in dodam_diner : 
        answer_dodam_diner.append(dodam2)
    for faculty in faculty_launch  : 
        answer_faculty_launch.append(faculty)
    for pasta in thekichin_pasta : 
        answer_thekichin_pasta.append(pasta)
    for pizza in thekichin_pizza : 
        answer_thekichin_pizza.append(pizza)
    for desert in thekichin_desert : 
        answer_thekichin_desert.append(desert)
    answer = ""
    if user_menu == u"학식":
        answer = answer_faculty_launch[0]
    elif user_menu == u"도담":
        answer = answer_dodam_launch[0] + answer_dodam_diner
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "type": "basicCard",
                        "items": [
                            {
                                "title": "밥밥",
                                "description": answer,
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                }
                            }
                        ]
                }
            ]
        }
    }
        
        
    return jsonify(res)'''

@app.route('/funsystem', methods=['GET', 'POST'])
def funsystem_func():
    req = request.get_json()
    url = "https://fun.ssu.ac.kr/ko/program/all/list/all/{}"
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    base_url = "https://fun.ssu.ac.kr/"
    
    funsystems = soup.find("ul", attrs={"class": "columns-4"}).find_all("li")
    answer_cal = []
    answer_link = []
    answer_img = []
    
    for funsystem in funsystems:
        calums = funsystem.find("b", attrs={"class": "title"})
        link = base_url + funsystem.a["href"]
        #imgs = funsystem.find("div", attrs={"class": "cover"})
        #img = "{}{}".format(base_url, imgs["style"])
        #answer_img.append(img)
        answer_cal.append(calums.text)
        answer_link.append(link)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": "펀시스템",
                                "description": answer_cal[0],
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
                                        "webLinkUrl": answer_link[0]
                                    }
                                ]
                            },
                            {
                                "title": "펀시스템",
                                "description": answer_cal[1],
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
                                        "webLinkUrl": answer_link[1]
                                    }
                                ]
                            },
                            {
                                "title": "펀시스템",
                                "description": answer_cal[2],
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
                                        "webLinkUrl": answer_link[2]
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }

    return jsonify(res)


#NOTICE
@app.route('/notice', methods=['GET', 'POST'])
def notice_func():
    req = request.get_json()

    url = "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/page/1/"
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text)

    notices = soup.find_all("a", attrs = {"class": "text-decoration-none d-block text-truncate"})
    answer_cal = []
    answer_link = []
    for n in notices:
        calums = n.find("span", attrs = {"class" : "d-inline-blcok m-pt-5"})
        link = "https://scatch.ssu.ac.kr/" + n["href"]
        answer_cal.append(calums.text)
        answer_link.append(link)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": answer_cal[0],
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "바로가기",
                                        "webLinkUrl": answer_link[0]
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 가기",
                                        "webLinkUrl": "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/page/1/"
                                    }
                                ],
                            },
                            {
                                "title": answer_cal[1],
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
                                        "webLinkUrl": answer_link[1]
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 가기",
                                        "webLinkUrl": "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/page/1/"
                                    }
                                ]
                            },
                            {
                                "title": answer_cal[2],
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
                                        "webLinkUrl": answer_link[2]
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 가기",
                                        "webLinkUrl": "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/page/1/"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }

    return jsonify(res)


# 메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)