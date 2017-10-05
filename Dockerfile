FROM python:3.6.1

LABEL maintaner="<Michael Rollins influencetx@gmail.com>"

ENV DATABASE_URL=psql://influencetx:mysecretpassword@localhost:5432/influencetx
ENV OPENSTATES_API_KEY=${OPENSTATES_API_KEY}

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements/local.txt

RUN python3 manage.py makemigrations

EXPOSE 5120

CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:5120 2>&1
