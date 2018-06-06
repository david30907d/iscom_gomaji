# Base python 3.5 build, inspired by 
# https://github.com/crosbymichael/python-docker/blob/master/Dockerfile 
FROM sgoblin/python3.5
MAINTAINER davidtnfsh <davidtnfsh@gmail.com> 

ENV LANG=C.UTF-8

RUN mkdir /code
WORKDIR /code
ADD . /code/

# install ifconfig
RUN apt-get update
RUN apt-get install -y net-tools vim wget libnss3-dev
RUN pip3 install -r requirements.txt

# solve encoding error for chinese
ENV LANG=C.UTF-8

# add ll in alias
RUN export alias ll='ls -al'

# the port on which we will be running app server (django runserver / gunicorn)
EXPOSE 8000

# 建立新容器時要執行的指令
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

ENTRYPOINT [""]