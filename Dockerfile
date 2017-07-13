FROM python:3.6.1
LABEL maintainer='Open Austin <info@open-austin.org>'
ARG PORT=5120
COPY . /app
WORKDIR /app
RUN pip install -r requirements/local.txt
CMD python3 manage.py runserver 0.0.0.0:$PORT
