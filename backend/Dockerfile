FROM python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --system

COPY . /app

CMD daphne config.asgi:application
