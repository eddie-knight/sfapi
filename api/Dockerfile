FROM alpine:latest
RUN apk add --update \
    python3 \
    python-dev \
    py-pip \
    build-base
COPY code /code
WORKDIR /code
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["run.py"]
