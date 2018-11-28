# build
FROM python:alpine AS build

RUN apk update && apk add build-base libffi-dev openssl-dev

WORKDIR /tmp
COPY requirements.txt /tmp/
RUN pip wheel -w wheels -r /tmp/requirements.txt

# runtime
FROM python:alpine

COPY --from=build /tmp/wheels /tmp/wheels
RUN pip install /tmp/wheels/* && rm -r /tmp/wheels

RUN adduser -D -h /app catgirl
USER catgirl

WORKDIR /app
COPY meowclock /app/meowclock
RUN mkdir /app/data
VOLUME /app/data

ENTRYPOINT ["/usr/bin/env", "python", "-m", "meowclock", "-s", "/app/data"]
STOPSIGNAL SIGINT
