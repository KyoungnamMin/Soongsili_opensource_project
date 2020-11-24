from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from datetime import date
import urllib.request
import json
import requests

app = Flask(__name__)


@app.route('/food', methods=['GET', 'POST'])
def food_func():
    req = request.get_json()
    user_menu = req['userRequest']
    user_menu = user_menu['block']
    user_menu = user_menu['name']
    
    url = "https://soongguri.com/main.php?mkey=2&w=3&l=1"
    res = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(res, "html.parser")

    data = soup.find("div", attrs={"class": "detail_center"})
    table = data.find("table")
    trs = table.find_all("tr")
    haksik_trs = trs[5]
    dodam_trs = trs[7]
    
    url = "https://ssudorm.ssu.ac.kr:444/SShostel/mall_main.php?viewform=B0001_foodboard_list&board_no=1"
    res = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(res, "html.parser")
    
    table = soup.find("table", attrs={"class": "boxstyle02"})
    dorm_trs = table.find_all("tr")
    
    answer_haksik = []
    answer_dodam = []
    answer_dorm = []

    for haksik in haksik_trs.find_all("td"):
        answer_haksik.append(haksik.text)

    for dodam in dodam_trs.find_all("td"):
        answer_dodam.append(dodam.text)

    for index, dorm in enumerate(dorm_trs):
        if index > 0:
            answer_dorm.append(dorm.text)
    
    dorm_today = date.today().weekday()
    
    answer = ""
    if user_menu == "학생 식당":
        answer = answer_haksik[0]
    elif user_menu == "도담 식당":
        answer = answer_dodam[0]
    elif user_menu == "기숙사 식당":
        answer = "오늘의 기식\n" + answer_dorm[dorm_today]
    else:
        answer = "다시 입력해주세요!"

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }
    return jsonify(res)


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
    # Do not Output Media Room available
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "숭실대 열람실 이용률"
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
                            }
                        ]
                    }
                }
            ],
            'quickReplies': [
                {
                    'label': '🏠',
                    'action': 'message',
                    'messageText': '🏠'
                }
            ]
        }
    }
    return jsonify(res)


@app.route('/funsystem', methods=['GET', 'POST'])
def funsystem_func():
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
        answer_cal.append(calums.text)
        answer_link.append(link)
        img = funsystem.find("div", attrs={"class": "cover"})
        k = img.attrs.get("style")
        s = ""
        c = 0
        for j in k:
            c = c + 1
            if(c > 21 and c < 54):
                s = s + j
        imgs = "https://fun.ssu.ac.kr" + s
        answer_img.append(imgs)

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
                                    "imageUrl": answer_img[0]
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
                                        "webLinkUrl": answer_link[0]
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 가기",
                                        "webLinkUrl": "https://fun.ssu.ac.kr/ko/program/all/list/all/1"
                                    }
                                ]
                            },
                            {
                                "title": answer_cal[1],
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": answer_img[1]
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
                                        "webLinkUrl": "https://fun.ssu.ac.kr/ko/program/all/list/all/1"
                                    }
                                ]
                            },
                            {
                                "title": answer_cal[2],
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": answer_img[2]
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
                                        "webLinkUrl": "https://fun.ssu.ac.kr/ko/program/all/list/all/1"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ],
            'quickReplies': [
                {
                    'label': '🏠',
                    'action': 'message',
                    'messageText': '🏠'
                }
            ]
        }
    }

    return jsonify(res)


@app.route('/notice', methods=['GET', 'POST'])
def notice_func():
    req = request.get_json()

    url = "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/page/1/"
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text)

    notices = soup.find_all("a", attrs={"class": "text-decoration-none d-block text-truncate"})
    answer_cal = []
    answer_link = []
    for n in notices:
        calums = n.find("span", attrs={"class": "d-inline-blcok m-pt-5"})
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
                                    "imageUrl": "https://github.com/KYOUNGNAM-MIN/OpenSource_Project/blob/master/chatbot_icon/noticeicon.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
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
            ],
            'quickReplies': [
                {
                    'label': '🏠',
                    'action': 'message',
                    'messageText': '🏠'
                }
            ]
        }
    }

    return jsonify(res)


# 메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)