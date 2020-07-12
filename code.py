from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import pandas as pd

start_time = time.time()
#Headness Browser
chromeoptions = webdriver.ChromeOptions()
chromeoptions.headless=True

watch_list=["0700","2888","0388",'0005','3690']
raw=[]
for i in range(len(watch_list)):
    url="https://hk.finance.yahoo.com/quote/"+watch_list[i]+".HK"
    driver = webdriver.Chrome(options=chromeoptions)
    driver.get(url)
    html=BeautifulSoup(driver.page_source,'html.parser')
    name=html.find("h1",class_="D(ib) Fz(18px)").get_text()
    price=html.find('span',class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").get_text()
    
    try:
        change=html.find('span',class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)").get_text()
    except:
        change=html.find('span',class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)").get_text()
    percent=re.findall(r'(\W\d+\.\d+\%)',change)
    high_low=html.find_all('td',class_='Ta(end) Fw(600) Lh(14px)')[5].get_text()
    raw.append([name, price,percent[0],high_low])
    driver.close()

data=pd.DataFrame(raw,columns=['Name','Price','Percent','High-low'])
print(data.head())
print('Programs run for {} seconds'.format(int((time.time() - start_time))))