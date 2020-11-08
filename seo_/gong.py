import requests
from bs4 import BeautifulSoup
from gensim.summarization.summarizer import summarize
import bs4.element
import datetime


def get_top3():
    
    #가져올 링크 주소 지정
    base_url = "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad"
    
    # 담아낼 dictionary
    ssu_dic = dict()
    
    sections = ["hak","zag"]
    section_ids = ["%ED%95%99%EC%82%AC","%EC%9E%A5%ED%95%99"]
    for sec, sid in zip(sections, section_ids):
        # 해당 분야 상위 목록 주소
        ssu_link = base_url + "/?category=" + sid + "&keyword"
        #print(news_link)
        
        # 해당 분야 상위 HTML 가져오기
        res = requests.get(ssu_link)
        soup = BeautifulSoup(res.text,'lxml')
        
        # 해당 분야 상위 3개 가져오기
        lis3 = soup.find_all('li', class_='start', limit=1)
        
        # 가져온 데이터 정제하기
        ssu_list3 = []
        default_img = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=naver#"
        for li in lis3:
            ssu_link = li.a.attrs.get('href')
            print(ssu_link)
            
            res = requests.get(ssu_link)
            soup = BeautifulSoup(res.text,'lxml')
            body = soup.find('div', class_="col-12 col-lg-9 col-xl-10")
            k = body.find_all('span', style='font-family: arial, helvetica, sans-serif')
            #print(k)
            
            # 본문 가져오기
            ssu_body = ''
            for content in k:
                #print(content.string)
                #if content.string:
                    # content.strip() : whitepace 제거 (참고 : https://www.tutorialspoint.com/python3/string_strip.htm)
                ssu_body += content.string.strip() + ' '
               # print(news_body)
                    # news_body += content.strip()
                   
            
            #print(news_body)
            # title : 제목
            # link : URL
            # news_body : 내용
            # image_url : 이미지 URL
            title = soup.find('h2', class_="font-weight-light mb-3")
            print(title.string)
            print(ssu_body)
            #print(body)
            ssu_info = {
                "title" : title.string,
                "link" : ssu_link,
                "news_body" : ssu_body,
                "image_url" : li.img.attrs.get('src') if li.img else default_img
            }
            
            ssu_list3.append(ssu_info)

        ssu_dic[sec] = ssu_list3
    
    return ssu_dic


ssu_dic = get_top3()

ssu_dic['hak'][0].keys()




