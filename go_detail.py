# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
#引入ActionChains滑鼠操作
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import csv
import re
import json
import urllib
from urllib.request import urlopen
st=time.time()
#鄉鎮市代碼
code={}
with open('district_code.csv','r') as f:
	spamreader=csv.reader(f,delimiter=',')
	for row in spamreader:
		code[row[1].strip('\"')]=row[0]
def County_code_transfer(addr,item):
	#轉縣市代碼
	if '台中' in addr:
		item['縣市代碼']=66
	elif '苗栗' in addr:
		item['縣市代碼']=10005
	elif '彰化' in addr:
		item['縣市代碼']=10007
	elif '南投' in addr:
		item['縣市代碼']=10008
	elif '雲林' in addr:
		item['縣市代碼']=10009

def Lon_lat_transfer(addr,item):
	#轉經緯度
	addressUrl = "http://maps.googleapis.com/maps/api/geocode/json?address=" + addr
	#中文須轉碼
	addressUrlQuote = urllib.parse.quote(addressUrl,':?=/')
	time.sleep(1)
	response = urlopen(addressUrlQuote).read().decode('utf-8')
	responseJson = json.loads(response)  
	#type of response is string
	#type of responseJson is dict
	#print(responseJson.get("status"))
	if len(responseJson.get('results'))!=0:
		item['經度']=responseJson.get('results')[0]['geometry']['location']['lng']
		item['緯度']=responseJson.get('results')[0]['geometry']['location']['lat']
def Office_hour_transfer(office_hour,item):
	#轉格式
	office={}
	day={'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'日':7}
#{"Week":1,"OpenTime":1000,"CloseTime":1800,"OpenTime_String":"10:00","CloseTime_String":"18:00"}
#營業時間：週一至週五 11:00~15:00 17:00~22:00 週六至週日及國定例假日 11:00~22:00
	sub=office_hour
	#print('-'*30)
	#print(sub)
	#print('-'*30)
	closeday=0
	if '不定期' in sub or '公告' in sub or '不定時' in sub:
		#print('無效時間')
		return
	if '公休' in sub:
		#print('公休')
		#print(sub[sub.rfind(' ')+1:sub.find('公')])#day
		for d in day:
			if d==sub[sub.find('公')-1]:
				closeday=day[d]
		#		print(closeday)
		sub=sub[:sub.rfind(' ')]
	if '(' in sub:
		for i in range(0,2):
			if '(' in sub:
				par=sub[sub.find('('):sub.find(')')+1]
				sub=sub.replace(par,'')
			else:
				break
	for i in range(0, 3):
		#print('now i='+str(i))
		#print(sub)
		if sub.find('至')!=-1:	
			#print(sub.find('至'))
			#print('1st office hour')
			#print(sub[:sub.find('至')])#第一個day
			for d in day:
				if d==sub[sub.find('至')-1]:
					office[day[d]]={'Week':day[d]}
					startday=day[d]
					#print(startday)
			#print(sub[sub.find('至')+1:sub.find('至')+3])#第二個day
			for d in day:
				if d==sub[sub.find('至')+2]:
					office[day[d]]={'Week':day[d]}
					endday=day[d]
					#print(endday)
			#以下適用旅行---週一至週日 24hrs
			if 'hrs' in sub or '24H' in sub or '24h' in sub:
				for i in range(startday,endday+1):
					if i not in office:
						office[i]={'Week':i}
					office[i].update({'OpenTime_String':'00:00'})
					office[i].update({'OpenTime':0000})
					office[i].update({'CloseTime_String':'24:00'})
					office[i].update({'CloseTime':2400})
				item['營業時間']=office
				return
			#以下適用餐券
			#print(sub[sub.find(' ')+1:sub.find('~')])#1st start hour
			for i in range(startday,endday+1):
				if i not in office:
					office[i]={'Week':i}
				#print(office)
				if (sub[sub.find(':')-2:sub.find(':')+3].replace(':','')).isdigit():
					office[i].update({'OpenTime_String':sub[sub.find(':')-2:sub.find('~')]})
					#transfer to int
					#st=sub[sub.find(' ')+1:sub.find(':')+3].replace(':','')
					office[i].update({'OpenTime':int(sub[sub.find(':')-2:sub.find(':')+3].replace(':',''))})
			#print(sub[sub.find('~')+1:sub.find('~')+6])#1st end hour
			for i in range(startday,endday+1):
				if (sub[sub.find('~')+1:sub.find('~')+6].replace(':','')).isdigit():
					office[i].update({'CloseTime_String':sub[sub.find('~')+1:sub.find('~')+6]})
				#transfer to int
				#et=int(sub[sub.find('~')+1:sub.find('~')+6].replace(':',''))
				#print(et)
					office[i].update({'CloseTime':int(sub[sub.find('~')+1:sub.find('~')+6].replace(':',''))})
			sub=sub[sub.find('~')+7:]
			for j in range(0, 2):
				if sub!='' and sub[0].isdigit():#same day 2nd start
					#print('same day 2nd office hour')
					for i in range(startday,endday+1):
						orig=office[i]
						office[i]=[]
						office[i].append(orig)
						new={}
						new[i]={'Week':i}
						new[i].update({'OpenTime_String':sub[sub.find('~')-5:sub.find('~')]})
						#transfer to int					
						
						if sub[sub.find('~')-5:sub.find('~')].replace(':','')!='':
							temp_str=sub[sub.find('~')-5:sub.find('~')]
							if '～' in sub[sub.find('~')-5:sub.find('~')]:
								temp_str=sub[sub.find('~')-5:sub.find('~')].replace('～','')
							new[i].update({'OpenTime':int(temp_str.replace(':',''))})
						new[i].update({'CloseTime_String':sub[sub.find('~')+1:sub.find('~')+6]})
						#transfer to int
						if sub[sub.find('~')+1:sub.find('~')+6].replace(':','')!='':
							temp_str2=sub[sub.find('~')+1:sub.find('~')+6]
							if '～' in sub[sub.find('~')+1:sub.find('~')+6]:
								temp_str2=sub[sub.find('~')+1:sub.find('~')+6].replace('～','')
							new[i].update({'CloseTime':int(temp_str2.replace(':',''))})
						office[i].append(new)
					#print('same day 2nd office hour')
					#print(sub[:sub.find('~')])#2nd start hour
					#print(sub[sub.find('~')+1:sub.find('~')+6])#2nd end hour
					sub=sub[sub.find('~')+7:]
				else:#diff day
					break
			#sub=sub[:sub.rfind(' ')]
		else:
			break
	if closeday!=0:
		office[closeday]=''
	#print(office)
	item['營業時間']=office
	#print('-------------------------------------')

def Gomaji_cate(href,item):
	#gomaji分類
	if 'travel' in href:
		item['Gomaji類別']='旅行'
		item['景點型態']='景點'
	elif 'ch=8' in href:
		item['Gomaji類別']='美容舒壓'
		item['景點型態']='其他'
	elif 'ch=9' in href:
		item['Gomaji類別']='生活娛樂'
		item['景點型態']='景點'
	elif 'Taiwan' in href:
		item['Gomaji類別']='購物'
	else:
		item['Gomaji類別']='餐券'
		item['景點型態']='美食'

def Site_type(name,item):
	#景點型態	
	hotel=['飯店','民宿','旅','酒店','行館','會館']
	for each in hotel:
		if each in name:
			item['景點型態']='住宿'
			break
def District_code_transfer(addr,item):
	#轉鄉鎮市代碼
	for dist in code:
		if dist in addr:
			item['鄉鎮市區代碼']=code[dist]
def Food_cate(food_name,item):
	#美食類別 夜市小吃;甜點冰品;火烤料理;中式美食;異國料理;伴手禮;地方特產;素食;其他
	dessert=['甜點','蛋糕','咖啡','下午茶','冰','鬆餅']
	foreign=['日式','韓式','美式','泰','日本','義式','牛排']
	item['美食類別']=['其他']
	if '素' in food_name:
		item['美食類別'].append('素食')
	if '烤' in food_name:
		item['美食類別'].append('火烤料理')
	if '特產' in food_name:
		item['美食類別'].append('特產')
	if '伴手禮' in food_name:
		item['美食類別'].append('伴手禮')
	if '夜市' in food_name or '小吃' in food_name:
		item['美食類別'].append('夜市小吃')
	for sweet in dessert:
		if sweet in food_name:
			item['美食類別'].append('甜點冰品')
			break
	for dish in foreign:
		if dish in food_name:
			item['美食類別'].append('異國料理')
			break
	if '中式' in food_name or '台式' in food_name or '台味' in food_name:
		item['美食類別'].append('中式美食')
	if len(item['美食類別'])>1:
		item['美食類別'].remove('其他')
def Hotel_cate(hotel,item):
	#住宿類別 Star;TouristHotel;Hotel;Homestay
	if '星級' in hotel:
		item['住宿類別']='Star'
	else:
		item['住宿類別']='Hotel'
def Site_cate(site,item):
	site_cat=[]
	#景點類別 生態類;古蹟類;廟宇類;藝術類;小吃/特產類;國家公園類;國家風景區類;休閒農業類;
	#溫泉類;自然風景類;遊憩類;體育健身類;觀光工廠類;都會公園類;森林遊樂區類;林場類;其他
	if '生態' in site:
		site_cat.append('生態類')
		site_cat.append('自然風景類')
	if '古蹟' in site:
		site_cat.append('古蹟類')
	if '廟' in site:
		site_cat.append('廟宇類')
	art=['藝術','Gallery','美術','展','雕','書法','劇場','表演','舞蹈','音樂','琴']
	for each in art:
		if each in site:
			site_cat.append('藝術類')
			break
	if '國家公園' in site:
		site_cat.append('國家公園類')
		site_cat.append('自然風景類')
	if '國家風景區' in site:
		site_cat.append('國家風景區類')
		site_cat.append('自然風景類')
	if '休閒' in site or '農' in site:
		site_cat.append('休閒農業類')
	if '溫泉' in site:
		site_cat.append('溫泉類')
	if '森林遊樂區' in site:
		site_cat.append('森林遊樂區類')
		site_cat.append('自然風景類')
	if '林場' in site:
		site_cat.append('林場類')
		site_cat.append('自然風景類')
	if '自然風景' in site and '自然風景類' not in site_cat:
		site_cat.append('自然風景類')
	if '遊憩' in site:
		site_cat.append('遊憩類')
	if '體育' in site or '健身' in site or 'GYM' in site or '球' in site:
		site_cat.append('體育健身類')
	if '觀光工廠' in site or '文化館' in site:
		site_cat.append('觀光工廠類')
	if '都會公園' in site:
		site_cat.append('都會公園類')
	else:
		site_cat.append('其他類')
	item['景點類別']=site_cat
def Food_time(office_time,item):
	#美食時段 早餐 中餐 晚餐 宵夜
	i=0
	item['美食適合時段']=[]
	for str_t in re.findall('\d+', office_time):
		t=int(str_t)
		if i%4==0:#開始營業時間
			if t<10 and '早餐' not in item['美食適合時段']:				
				item['美食適合時段'].append('早餐')
			if t>9 and t<13 and '中餐' not in item['美食適合時段']:
				item['美食適合時段'].append('中餐')
			if t>15 and t<18 and '晚餐' not in item['美食適合時段']:
				item['美食適合時段'].append('晚餐')
		if i%4!=0 and i%2==0 and i>0:#結束營業時間
			if t<7 and '宵夜' not in item['美食適合時段']:
				item['美食適合時段'].append('宵夜')
			if t>6 and t<11 and '早餐' not in item['美食適合時段']:
				item['美食適合時段'].append('早餐')
			if t>12 and t<15 and '中餐' not in item['美食適合時段']:
				item['美食適合時段'].append('中餐')
			if t>18 and t<21 and '晚餐' not in item['美食適合時段']:
				item['美食適合時段'].append('晚餐')
		i=i+1

output=[]
#爬蟲
def crawl(target,area):
	#global output
	driver=webdriver.PhantomJS('./phantomjs')
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

	#print('-----------------------')

	soup=BeautifulSoup(driver.page_source,'html.parser')

	for ele in soup.select('.deal16 li a'):
		#print(ele)
	#for ele in soup.select('.class_name h3 a(h3裡)'):	
		if ele.find('h2') and '日本-' in ele.find_all('h2')[0].string:
			#print(ele.find_all('h2')[0].string)
			continue
		else:
		#商品category
			href="http://www.gomaji.com/"+str(ele['href'])
			try:
				driver.get(href)
				soup_detail=BeautifulSoup(driver.page_source,'html.parser')
				out={}
				#景點型態
				Gomaji_cate(target,out)
				if 'Travel' in href:
					out['Gomaji類別']='旅行'
					store_area=soup_detail.select('h1 .travel-sign')#旅遊的tag不一樣
				else:
					store_area=soup_detail.select('h1 img')[0]['alt']
				if store_area=='日本' or store_area=='公益':# or store_area=='購物':
					#soup_detail.select('h1 img')[0]['alt']→商店左上角
					#print(store_area)
					continue
				else:
					#以下為1個店家之store info	
					for h in soup_detail.select('#store_intro h4 a'):
						if '網站' in h.string:
							out['網站連結']=str(h['href'])
						if 'FB' in h.string:
							out['FB連結']=str(h['href'])
					#以下是簡介
					subcribe=""
					for p in soup_detail.select('#store_intro p'):
						order=0
						for child in p.descendants:
							s=child.string
							if child.find('span')==-1 and s.replace('\n','')!='':
								if order>0:#避開店名
									#print(s)
									subcribe+=s.replace('\n','')
								order=order+1
							if order>2 or len(subcribe)>20:
								break
						if len(subcribe)>20:
							break
					#print(subcribe)
					out['簡介']=subcribe
					#以下為圖片
					if soup_detail.select('#store_intro p')[0].find('img'):
						pic=soup_detail.select('#store_intro p')[0].find_all('img')[0]
					elif soup_detail.select('#store_intro p')[1].find('img'):
						pic=soup_detail.select('#store_intro p')[1].find_all('img')[0]
					else:
						pic=soup_detail.select('#store_intro p')[2].find_all('img')[0]
					#print(pic['data-original'])
					if 'data-original' in pic:
						out['圖片']=pic['data-original']
					elif 'scr' in pic:
						out['圖片']=pic['src']
					#以下為適用分店資訊
					for store_info in soup_detail.select('#branch_list'):
						if store_info.find('label'):
							out['景點名稱']=store_info.find_all('label')[0].text
							#景點型態			
							if out['Gomaji類別']=='旅行':
								Site_type(out['景點名稱'],out)
							for store in store_info.find_all('div', attrs={'style': 'display: table-cell;'}):
								for each in store.find_all('p'):		
									if ':' in each.text or '：' in each.text:
										if '電話' in each.text:
											out['連絡電話']=each.text[3:]
										elif '地址' in each.text:
											out['地址資訊']=each.text[3:]
											County_code_transfer(out['地址資訊'],out)
											District_code_transfer(out['地址資訊'],out)
											#以下轉經緯度
											Lon_lat_transfer(out['地址資訊'],out)
										elif '營業時間' in each.text:							
											str_office=each.text[5:]
											Office_hour_transfer(str_office,out)														
										elif '粉絲團' in each.text:
											out['FB連結']=each.text[4:]				
								if '地址資訊' in out:#for多家分店時
									if area in out['地址資訊']:
										break
							#沒有一間分店在area
							if '地址資訊' in out and area in out['地址資訊']:
								pass
							else:
								out={}
								break
							if out['景點型態']=='美食':
								#以下轉美食類別
								out['景點類別']=['小吃/特產類']
								Food_cate(str(out['景點名稱']+out['簡介']),out)
								#以下轉美食時段
								if '營業時間' in out:
									Food_time(str_office,out)
							if out['景點型態']=='住宿':
								#轉住宿類別
								Hotel_cate(str(out['景點名稱']+out['簡介']),out)
							if out['景點型態']=='景點':
								#轉景點類別
								Site_cate(str(out['景點名稱']+out['簡介']),out)
					if out!={} and '地址資訊' in out:
						output.append(out)
						#print(out)	
						#break
			except TimeoutException:
				continue
	driver.close()

url=['http://www.gomaji.com/index.php?city=Taichung&ch=7',
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
#台中,南投,苗栗,雲林,彰化
#target = 'http://www.gomaji.com/index.php?city=Taichung'#票券
#target='http://www.gomaji.com/index.php?city=Taichung&ch=8'#美容舒壓
#target='http://www.gomaji.com/index.php?city=Taichung&ch=9'#生活娛樂
#target="http://www.gomaji.com/travel.php?region=2&city_id=4&ch=2"#travel

chromepath="./chromedriver"
for each in url:
	if 'Taichung' or 'region=2&city_id=4&ch=2' in each:
		area='台中'
	elif 'Nantou' or 'region=2&city_id=10&ch=2' in each:
		area='南投'
	elif 'Miaoli' or 'region=1&city_id=8&ch=2' in each:
		area='苗栗'
	elif 'Yunlin' or 'region=3&city_id=11&ch=2' in each:
		area='雲林'
	elif 'Changhua' or 'region=2&city_id=9&ch=2' in each:
		area='彰化'
	print(each, area)
	crawl(each,area)
	time.sleep(3)
#print(output)
#final_output=list(set(output))
#json
with open('store_to_sites.json','w',encoding='utf8') as f:#
	json.dump(output,f,ensure_ascii=False)
f.close()
#csv
#col_name=['縣市代碼','鄉鎮市區代碼','地址資訊','景點名稱','景點型態','景點類別','美食類別','住宿類別','美食適合時段','經度','緯度','連絡電話','網站連結','營業時間','圖片','Gomaji類別','FB連結','簡介']
#with open('store_to_sites.csv','w',encoding='utf8') as f1:#
#	w=csv.DictWriter(f1,fieldnames=col_name)
#	w.writeheader()
#	for shop in output:
#		w.writerow(shop)
#f1.close()
	
et=time.time()
#print(et-st)