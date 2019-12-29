FROM python:3.7

ENV PYTHONUNBUFFERED 1
ARG EXTRA_REQUIREMENTS
ARG EXTRA_PACKAGES

RUN addgroup --system django \
    && adduser --system django \
    && adduser django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir --prefer-binary -r /requirements/production.txt

COPY ./compose/master/inspector/entrypoint /entrypoint
COPY ./compose/master/inspector/extras /extras
COPY ./compose/master/inspector/start /start
COPY ./compose/master/inspector/celery/worker/start /start-celeryworker
COPY ./compose/master/inspector/celery/beat/start /start-celerybeat
COPY ./compose/master/inspector/celery/flower/start /start-flower

RUN /extras

RUN chown django /entrypoint /start*

COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE config.settings.production

ENTRYPOINT ["/entrypoint"]
