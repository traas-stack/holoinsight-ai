# syntax=docker/dockerfile:1
FROM python:3.7

RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

WORKDIR /home/admin
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "serving", "run", "--host=0.0.0.0"]
EXPOSE 5000