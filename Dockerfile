FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /hype
WORKDIR /hype
COPY requirements.txt /hype/
RUN pip install -r requirements.txt
COPY . /hype/

