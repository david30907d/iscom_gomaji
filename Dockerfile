# Base python 3.5 build, inspired by 
# https://github.com/crosbymichael/python-docker/blob/master/Dockerfile 
FROM sgoblin/python3.5
MAINTAINER davidtnfsh <davidtnfsh@gmail.com> 

# install ifconfig
RUN apt-get install -y net-tools vim wget libnss3-dev
RUN git clone https://github.com/david30907d/iscom_gomaji.git

# solve encoding error for chinese
RUN sudo locale-gen zh_TW zh_TW.UTF-8
RUN echo "LC_CTYPE=zh_TW.UTF-8" | sudo tee -a /etc/environment
ENV LANG=C.UTF-8

# add ll in alias
RUN export alias ll='ls -al'

CMD [] 

ENTRYPOINT ["/bin/bash"]

EXPOSE 8000
