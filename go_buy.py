from selenium import webdriver
from selenium.common.exceptions import TimeoutException
#引入ActionChains滑鼠操作
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import csv

target = 'http://www.gomaji.com/Taiwan'
chromepath="C:/Users/USER/Downloads/chromedriver_win32/chromedriver.exe"
driver=webdriver.Chrome(chromepath)
driver.get(target)

#一直往下scroll
SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
	# Scroll down to bottom
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	# Wait to load page
	time.sleep(SCROLL_PAUSE_TIME)
	# Calculate new scroll height and compare with last scroll height
	new_height = driver.execute_script("return document.body.scrollHeight")
	if new_height == last_height:
		break
	last_height = new_height


print('*********')
soup=BeautifulSoup(driver.page_source,'html.parser')
#要用find_all這樣回傳的type(tag)才可繼續用
contents = soup.find_all('ul', attrs={'id': 'taiwan-deals2'})

output=[]
for item in contents[0].find_all(name='li'):
	out={}
	if item.find('a'):#有連結
		out['href']="http://www.gomaji.com/"+str(item.find_all('a', href=True)[0]['href'])
	if item.find('img'):
		for pic in item.find_all('img', attrs={'class': 'pic lazy'}):
			out['img']=pic['src']
	if item.find('div',attrs={'class':'seo-alternative'}):
		out['title']=item.find_all('div',attrs={'class':'seo-alternative'})[0].string
	if item.find('h3'):
		for child in item.find_all('h3')[0].descendants:
			out['prize']=child.string.replace(' ','').replace('\n','')
			break
		
	output.append(out)
	#break
col_name=['title','prize','href','img']
#save to csv 若要utf8加,encoding='utf8'
with open('Taichung_buy.csv','w',encoding='utf8') as f:
	w=csv.DictWriter(f,fieldnames=col_name)
	w.writeheader()
	for i in output:
		w.writerow(i)