# build
FROM python:alpine AS build

RUN apk update && apk add build-base

WORKDIR /tmp
COPY requirements.txt /tmp/
RUN pip wheel -w wheels -r /tmp/requirements.txt

# runtime
FROM python:alpine

COPY --from=build /tmp/wheels /tmp/wheels
RUN pip install /tmp/wheels/* && rm -r /tmp/wheels

RUN useradd -h /app catgirl
USER catgirl

WORKDIR /app
COPY meowclock /app/meowclock

ENTRYPOINT ["python", "-m", "meowclock"]
