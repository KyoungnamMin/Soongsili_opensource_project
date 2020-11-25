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
    dodam_launch_route_1 = dodam_trs.find("table")
    dodam_launch_route_2 = dodam_launch_route_1.find("td", attrs = {"style" : "width:283.33333333333px;text-align:left;padding:3px;border:1px dotted #999999;vertical-align:top;"})
    
    dodam_launch_route_3 = dodam_launch_route_2.find_all("div")
    dodam_launch =' '
    
    for i in range(0,5,1):
        dodam_launch += dodam_launch_route_3[i].get_text()
    
    dodam_dinner_route_1 = dodam_trs.find("table")
    dodam_dinner_route_2 = dodam_dinner_route_1.find_all("td", attrs = {"style" : "width:283.33333333333px;text-align:left;padding:3px;border:1px dotted #999999;vertical-align:top;"})
    dodam_dinner_route_3 = dodam_dinner_route_2[2].find_all("div")
    dodam_dinner = " "
    for i in range(0,4,1):
        dodam_dinner += dodam_dinner_route_3[i].get_text()
    
    
    url = "https://ssudorm.ssu.ac.kr:444/SShostel/mall_main.php?viewform=B0001_foodboard_list&board_no=1"
    res = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(res, "html.parser")
    
    table = soup.find("table", attrs={"class": "boxstyle02"})
    dorm_trs = table.find_all("tr")
    
    
    answer_haksik = []
    answer_dodam_launch = []
    answer_dodam_dinner = []
    answer_dorm = []

    for haksik in haksik_trs.find_all("td"):
        answer_haksik.append(haksik.text)

    for dodam_l in dodam_launch :
        answer_dodam_launch.append(dodam_l.text)
        
    for dodam_d in dodam_dinner :
        answer_dodam_dinner.append(dodam_d.text)

    for index, dorm in enumerate(dorm_trs):
        if index > 0:
            answer_dorm.append(dorm.text)
    
    dorm_today = date.today().weekday()
    
    answer = ""
    if user_menu == "학생 식당":
        answer = answer_haksik[0]
    elif user_menu == "도담 식당(점심)":
        answer = answer_dodam_launch[0]
    elif user_menu == "도담 식당(저녁)":
        answer = answer_dodam_dinner[0]
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

