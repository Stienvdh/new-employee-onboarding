FROM python:3.8
# ENV STATIC_INDEX 1
# COPY ./requirements.txt /app/requirements.txt
# COPY ./app /app
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y cron
COPY crontab /etc/cron.d/crontab
COPY cronscript.py /app/cronscript.py
RUN chmod 0644 /etc/cron.d/crontab

RUN apt-get clean
RUN apt-get update -y && apt-get install -y python-pip python-dev git netcat

COPY . .
# WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements_deploy.txt

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "bash" ]
CMD ["entrypoint.sh"]
