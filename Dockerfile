FROM python:3.12-slim

RUN \
    set -eux; \
    apt-get update; \
    apt-get install curl; \
    apt-get update && apt-get install -y locales \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    rm -rf /var/lib/apt/lists/* 

WORKDIR /app
COPY . .

EXPOSE 8555
CMD ["./dist/adventskalender-web"]

ENV LANG en_US.utf8

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://127.0.0.1:8555/ || exit 1