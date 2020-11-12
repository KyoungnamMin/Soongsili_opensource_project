import urllib.request
import json

url = 'https://oasis.ssu.ac.kr/smufu-api/pc/1/rooms-at-seat'

res = urllib.request.urlopen(url)

rec = res.getcode()
if(rec == 200):
    res_body = res.read()
    data = json.loads(res_body)
    d=data['data']
    d=d['list']
    s=[]
    for i in range(0,6):
        s.append([d[i]['name'],d[i]['activeTotal'],d[i]['occupied'],d[i]['available']])
        print(s[i])
else:
    print("Error Code:" + rec)