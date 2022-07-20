FROM python:3.9-slim-buster
# set work directory
WORKDIR /app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip install --upgrade pip
COPY ./mysite/requirements.txt .

RUN pip install -r requirements.txt
# copy project
COPY ./mysite .
ENTRYPOINT [ "/app/entrypoint.sh" ]