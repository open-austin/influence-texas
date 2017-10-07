FROM python:3.6.1

LABEL maintaner="<Michael Rollins influencetx@gmail.com>"

ENV DATABASE_URL=psql://influencetx:mysecretpassword@localhost:5432/influencetx
ENV OPENSTATES_API_KEY=${OPENSTATES_API_KEY}
ENV TPJ_DB_USER=${TPJ_DB_USER}
ENV TPJ_DB_PASSWORD=${TPJ_DB_PASSWORD}

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
postgresql-client \
unixodbc \
unixodbc-dev \
freetds-bin \
freetds-dev \
tdsodbc && \
apt-get clean

RUN pip install -r requirements/local.txt

EXPOSE 5120

CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:5120
