FROM python:3.12-slim

RUN \
    set -eux; \
    apt-get update; \
    apt-get install -y \
    --no-install-recommends \
    python3-pip \
    curl; \
    apt-get update && apt-get install -y locales \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    rm -rf /var/lib/apt/lists/* 

RUN pip3 install -U pip && pip3 install -U wheel && pip3 install -U setuptools

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir && rm -r requirements.txt

EXPOSE 8555
CMD ["python3", "main.py"]

ENV LANG en_US.utf8

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://0.0.0.0:8555/ || exit 1