FROM debian:9

RUN apt-get update -yq \
&& apt-get install python3 -yq \
&& apt-get install python3-pip -yq \
&& pip3 install requests

ADD . /app/
WORKDIR /app

EXPOSE 3000
VOLUME /app/logs

CMD python3 index.py