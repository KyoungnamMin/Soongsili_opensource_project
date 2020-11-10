import urllib.request
from bs4 import BeautifulSoup
import csv



@app.route('/funsystem', methods=['GET', 'POST'])
def funsystem_func():
     req = request.get_json()

    url = "https://soongguri.com/main.php?mkey=2&w=3&l=2"
    res = urllib.request.urlopen(url).read()
    res.raise_for_status()
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
        answer_dodam_launch(dodam)
    for dodam2 in dodam_diner : 
        answer_dodam_diner(dodam2)
    for faculty in faculty_launch  : 
        answer_faculty_launch(faculty)
    for pasta in thekichin_pasta : 
        answer_thekichin_pasta(pasta)
    for pizza in thekichin_pizza : 
        answer_thekichin_pizza(pizza)
    for desert in thekichin_desert : 
        answer_thekichin_desert(desert)
