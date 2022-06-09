FROM python:3.10.5-buster

COPY ./requirements.txt /ptt_webapi/requirements.txt

RUN pip install --no-cache-dir -r /ptt_webapi/requirements.txt && \
    pip install gunicorn && \
    apt-get update && \
    apt-get install net-tools

COPY . /ptt_webapi

WORKDIR /ptt_webapi
EXPOSE 8000

CMD [ "gunicorn" ,"--bind=0.0.0.0:8000" ,"--timeout=600" , "ptt_webapi.wsgi" ]
