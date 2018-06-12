from selenium import webdriver
from selenium.common.exceptions import TimeoutException
#引入ActionChains滑鼠操作
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import csv, json, os, time

output=[]
def crawl(target):
	driver=webdriver.PhantomJS(phantomjsPath)
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


	soup=BeautifulSoup(driver.page_source,'html.parser')
	#要用find_all這樣回傳的type(tag)才可繼續用
	contents = soup.find_all('ul', attrs={'class': 'deal16'})

	for item in contents[0].find_all(name='li'):
		out={}
		if item.find('a'):#有連結
			for a in item.find_all('a', href=True):
				out['href']="http://www.gomaji.com/"+str(a['href'])
		if item.find('img'):
			for pic in item.find_all('img', attrs={'class': 'lazy'}):
				out['img']=pic['src']
		if item.find('h2'):
			out['title']=item.find_all('h2')[0].string
		if item.find('h3'):
			out['coupon']=item.find_all('h3')[0].string
		if item.find(name='span'):
			out['prize']=item.find_all(name='span')[0].string#other
			#out['prize']=item.find_all(name='span')[1].string#travel
		if out['coupon']!='':
			driver.get(out['href'])
			soup_detail=BeautifulSoup(driver.page_source,'html.parser')
			#以下是兌換券內容
			if 'Travel' in out['href']:
				store_area=soup_detail.select('h1 .travel-sign')#旅遊的tag不一樣
			else:
				store_area=soup_detail.select('h1 img')[0]['alt']
			if store_area=='日本' or store_area=='公益':# or store_area=='購物':
				continue
			else:
				for certif in soup_detail.select('.important'):
					i=0
					for rules in certif.find_all(name='li'):
						if i==0:
							out['term']=rules.text#deadline截止日期
							i=i+1
				output.append(out)
				#print(out)
		#break
url=['http://www.gomaji.com/index.php?city=Taichung',
'http://www.gomaji.com/index.php?city=Taichung&ch=8',
'http://www.gomaji.com/index.php?city=Taichung&ch=9',
'http://www.gomaji.com/travel.php?region=2&city_id=4&ch=2',
'http://www.gomaji.com/index.php?city=Nantou&ch=7',
'http://www.gomaji.com/index.php?city=Nantou&ch=8',
'http://www.gomaji.com/index.php?city=Nantou&ch=9',
'http://www.gomaji.com/travel.php?region=2&city_id=10&ch=2',
'http://www.gomaji.com/index.php?city=Miaoli&ch=7',
'http://www.gomaji.com/index.php?city=Miaoli&ch=8',
'http://www.gomaji.com/index.php?city=Miaoli&ch=9',
'http://www.gomaji.com/travel.php?region=1&city_id=8&ch=2'
'http://www.gomaji.com/index.php?city=Yunlin&ch=7',
'http://www.gomaji.com/index.php?city=Yunlin&ch=8',
'http://www.gomaji.com/index.php?city=Yunlin&ch=9',
'http://www.gomaji.com/travel.php?region=3&city_id=11&ch=2',
'http://www.gomaji.com/index.php?city=Changhua&ch=7',
'http://www.gomaji.com/index.php?city=Changhua&ch=8',
'http://www.gomaji.com/index.php?city=Changhua&ch=9',
'http://www.gomaji.com/travel.php?region=2&city_id=9&ch=2']

phantomjsPath="./phantomjs.exe" if os.name == 'nt' else './phantomjs'

for each in url:
	crawl(each)
	time.sleep(3)
#remove duplicate dict in list
final_output=[dict(t) for t in set([tuple(d.items()) for d in output])]

#json
with open('coupon.json','w',encoding='utf8') as f:#
	json.dump(final_output,f,ensure_ascii=False)
f.close()

#col_name=['title','coupon','prize','href','img','term']
#save to csv 若要utf8加,encoding='utf8'
#with open('coupon.csv','w',encoding='utf8') as f2:
#	w=csv.DictWriter(f2,fieldnames=col_name)
#	w.writeheader()
#	for i in output:
#		w.writerow(i)