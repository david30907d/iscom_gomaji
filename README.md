# README

## Linux

1. `sudo apt-get install libnss3-dev`
2. `pip3 install -r requirements.txt`
2. run crawler to update results (optional):`python3 go_detail.py`
3. run django api server:`python3 manage.py runserver`

## Windows

1. `pip3 install -r requirements.txt`
2. run crawler to update results (optional):`python3 go_detail.py`
3. run django api server:`python3 manage.py runserver`

## Docker

1. `docker build -t iscomcrawler .`
2. `docker run -itd --name iscomcrawler1 iscomcrawler`
3. `docker exec -it iscomcrawler1 bash`
4. run crawler to update results (optional):`python3 go_detail.py`
5. run django api server:`python3 manage.py runserver`