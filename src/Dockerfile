FROM python:3
USER root

RUN apt-get update
RUN apt-get -y install locales && \
	localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

WORKDIR /root/opt

ADD requirements.txt /root/opt
RUN pip install -r requirements.txt
ADD . /root/opt
	
CMD [ "python", "/root/opt/bot.py" ]