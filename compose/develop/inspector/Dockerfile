FROM python:3.8

ENV PYTHONUNBUFFERED 1
ARG EXTRA_REQUIREMENTS
ARG EXTRA_PACKAGES


# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/master/inspector/entrypoint /entrypoint
COPY ./compose/master/inspector/extras /extras
COPY ./compose/develop/inspector/start /start
COPY ./compose/develop/inspector/celery/worker/start /start-celeryworker
COPY ./compose/develop/inspector/celery/beat/start /start-celerybeat
COPY ./compose/develop/inspector/celery/flower/start /start-flower

RUN /extras

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
