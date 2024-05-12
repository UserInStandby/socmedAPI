FROM python:3.12-alpine3.18
LABEL author="Max"

ENV PYTHONUBUFFERED 1
ENV PYTHONDONTWRITEBINARY 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./socmedapi /socmedapi

WORKDIR /socmedapi
EXPOSE 8000

ARG DEBUG=true
RUN python -m venv /myvenv && \
    /myvenv/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /myvenv/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEBUG = "true" ]; \
        then /myvenv/bin/pip install -r /tmp/requirements.dev.txt ;\
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/myvenv/bin:$PATH"

USER django-user

CMD ["run.sh"]