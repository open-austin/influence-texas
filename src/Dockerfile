FROM python:3.7.1

LABEL maintaner="<Michael Rollins michael@influencetx.com>"

ARG APP_ENV=production

WORKDIR /usr/src/app

COPY . .

RUN mkdir logs || true

RUN apt-get update && apt-get install -y \
postgresql-client \
unixodbc \
unixodbc-dev \
freetds-bin \
freetds-dev \
tdsodbc && \
apt-get clean

RUN pip install -r requirements/${APP_ENV}.txt

EXPOSE 5120

#CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:5120
ENTRYPOINT /usr/src/app/entrypoint.sh
