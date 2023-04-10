# Pull base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
# COPY Pipfile Pipfile.lock /code/
# RUN pip install pipenv && pipenv install --system

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN chmod a+rwx /etc
# Copy project
COPY . /code/
RUN mkdir /code/venv/
RUN mkdir /code/venv/logs/
RUN chmod a+rwx /code/venv/logs/
RUN touch /code/venv/logs/gunicorn.log
RUN touch /code/venv/logs/gunicorn-error.log
# RUN chmod a+rwx logs
# RUN touch logs/gunicorn.log