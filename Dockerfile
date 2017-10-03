FROM python:3.6.1

LABEL maintaner="<Michael Rollins influencetx@gmail.com>"

ARG DATABASE_URL=psql://influencetx:mysecretpassword@localhost:5432/influencetx
ARG OPENSTATES_API_KEY=${OPENSTATES_API_KEY}

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements/local.txt

EXPOSE 5120

CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:5120
