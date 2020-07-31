#A项目
import requests
from bs4 import BeautifulSoup
import pandas as pd
url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
html = requests.get(url,headers=headers,timeout=10)
content = html.text
soup = BeautifulSoup(content,'html.parser')
df = pd.DataFrame(columns = ['名称', '最低至最高价格', '产品图片链接'])#创建Dataframe命名每个字段
list_items = soup.find_all('div',class_='search-result-list-item')#提取每项内容
for i in list_items:
    temp = {}
    name = i.find('p',class_='cx-name text-hover')
    price = i.find('p',class_='cx-price')
    img = i.find('img',class_='img')['src']
    temp['名称'], temp['最低至最高价格'], temp['产品图片链接'] = name.text, price.text, img
    df = df.append(temp,ignore_index=True)

df.to_csv('大众汽车报价数据.csv',index=False)#提取结果保存为csv文件