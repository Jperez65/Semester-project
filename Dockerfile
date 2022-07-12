FROM python:3

WORKDIR /app

COPY * ./
RUN apt-get update
RUN apt-get -y install pipenv

RUN pipenv install

EXPOSE 5000

RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]
