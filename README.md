# README

## Linux

1. `sudo apt-get install libnss3-dev`
2. `pip3 install -r requirements.txt`
2. run crawler to update results (optional):
    * `python3 go_detail.py`
    * `python3 coupon.py`
3. run django api server:`python3 manage.py runserver`

## Windows

1. `pip3 install -r requirements.txt`
2. run crawler to update results (optional):
    * `python3 go_detail.py`
    * `python3 coupon.py`
3. run django api server:`python3 manage.py runserver`

## Docker

1. `docker build -t iscomgomaji .`
2. `docker run -itd --name iscomgomaji1 iscomgomaji`
3. `docker exec -it iscomgomaji1 bash`
4. run crawler to update results (optional):
    * `python3 go_detail.py`
    * `python3 coupon.py`
5. django api server already start when running the container, so there's no need to execute that cmd again.

## Port Mapping

If you want to access the api server outside container (not in the same network namespace)

you need to run the container with `docker run -itd --name <container name> -p <the port you want to expose>:8000 iscomgomaji`

## Api

* `api/getsite`: return stands of gomaji
  * parameter: `num`, default 10
  * example: `http://ip:port/api/getsite/?num=20`
* `api/getcoupon`: return gomaji coupon
  * parameter: `num`, default 10
  * example: `http://ip:port/api/getcoupon/?num=20`

## Result

* getsite:
```json
[
  {
    "FB連結": "https://www.facebook.com/驖人拉麵食事處-616972351983228/",
    "Gomaji類別": "餐券",
    "連絡電話": "0983-259-057",
    "縣市代碼": 66,
    "景點類別": [
      "小吃/特產類"
    ],
    "美食類別": [
      "素食",
      "異國料理"
    ],
    "景點型態": "美食",
    "簡介": "\t近審計新村、勤美誠品！走進日式餐館，師傅正用心製作道道佳餚，以日式飲饌文化妝點佈置的環境四溢美味香氣，處處盡是味道濃厚的元素，盡情享受一場深度日本之旅！",
    "營業時間": {
      "7": [
        {
          "CloseTime_String": "14:00",
          "OpenTime_String": "11:30",
          "OpenTime": 1130,
          "CloseTime": 1400,
          "Week": 7
        },
        {
          "7": {
            "CloseTime_String": "20:30",
            "OpenTime_String": "17:30",
            "OpenTime": 1730,
            "CloseTime": 2030,
            "Week": 7
          }
        }
      ]
      ...
      ...
      ...
    },
    "景點名稱": "驖人拉麵食事處",
    "鄉鎮市區代碼": "6600400",
    "美食適合時段": [
      "中餐",
      "晚餐"
    ],
    "地址資訊": "台中市西區向上路一段105號(近審計新村、勤美誠品)"
  }
]
```

* getcoupon:
```json
[
  {
    "href": "http://www.gomaji.com/Taichung_p204057.html",
    "coupon": "A.甜美可人150根嫁接 / B.水潤大眼不限根數嫁接 / C.6D唯美輕盈400根嫁接 / D.6D閃耀迷人600...",
    "term": "優惠期間為 2018 年 4 月 21 日 至 2018 年 7 月 21 日，平假日皆可使用，毎週日公休、6/18 公休\n",
    "title": "YES美睫",
    "img": "https://picdn.gomaji.com/products/57/204057/204057_1_3_r.jpg",
    "prize": "299"
  },
  {
    "href": "http://www.gomaji.com/Taichung_p198525.html",
    "coupon": "A.單人炸物飲品吃到飽 / B.單人經典套餐",
    "term": "兌換期為 2018/3/14 至 2018/9/11，平假日皆可使用，公休日依FB粉絲團公告為主\n",
    "title": "快樂小屋桌上遊戲主題餐廳",
    "img": "https://picdn.gomaji.com/products/525/198525/198525_1_r.jpg",
    "prize": "189"
  }
  ...
  ...
  ...
]
```