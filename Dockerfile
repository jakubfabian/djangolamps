FROM resin/rpi-raspbian
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update  && apt-get install -y  python-dev python-pip python-psycopg2 python-numpy build-essential netcat
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD docker-compose.yml /code/
ADD Dockerfile /code/
RUN apt-get update  && apt-get install -y  python-matplotlib python-tk
