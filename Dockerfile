FROM python:3.10-alpine

ENV TZ=GMT \
  ENV=development

RUN apk update \
  && apk add \
  gcc

WORKDIR /app
COPY . /app

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["server.py"]
