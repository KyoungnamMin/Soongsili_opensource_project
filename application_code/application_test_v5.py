from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib.request
import json
import requests

app = Flask(__name__)


@app.route('/library', methods=['GET', 'POST'])
def library_func():
    url = 'https://oasis.ssu.ac.kr/smufu-api/pc/1/rooms-at-seat'

    res = urllib.request.urlopen(url)
    rec = res.getcode()
    name_ = []
    total_ = []
    occ_ = []
    avail_ = []
    if(rec == 200):
        res_body = res.read()
        data = json.loads(res_body)
        d = data['data']
        d = d['list']
        for i in range(0, 6):
            name_.append(d[i]['name'])
            total_.append(d[i]['activeTotal'])
            occ_.append(d[i]['occupied'])
            avail_.append(d[i]['available'])

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "숭실대 중앙도서관 현재 이용률"
                        },
                        "items": [
                            {
                              "title": name_[0],
                              "description": "잔여 좌석 수: " + str(avail_[0])
                            },
                            {
                              "title": name_[1],
                              "description": "잔여 좌석 수: " + str(avail_[1])
                            },
                            {
                              "title": name_[2],
                              "description": "잔여 좌석 수: " + str(avail_[2])
                            },
                            {
                              "title": name_[3],
                              "description": "잔여 좌석 수: " + str(avail_[3])
                            },
                            {
                              "title": name_[4],
                              "description": "잔여 좌석 수: " + str(avail_[4])
                            },
                            {
                              "title": name_[5],
                              "description": "잔여 좌석 수: " + str(avail_[5])
                            }
                        ]
                    }
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