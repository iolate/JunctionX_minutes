FROM python:3.6

ADD . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y libasound2

RUN pip install -r /app/requirements.txt

CMD ["python", "cron.py"]
