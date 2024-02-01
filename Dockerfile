FROM python:3.11.7-alpine

RUN apk add --no-cache mariadb-connector-c-dev build-base rust cargo

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8000/tcp

CMD ["sh", "entrypoint.sh"]
