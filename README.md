# README

## Linux Dependency

1. `sudo apt-get install libnss3-dev`
2. `pip3 install -r requirements.txt`

## Windows

## Docker

1. `docker build -t iscomcrawler .`
2. `docker run -itd --name iscomcrawler1 iscomcrawler`
3. `docker exec -it iscomcrawler1 bash`
4. `python3 go_detail.py`