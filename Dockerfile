FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN python install_dependencies.py
RUN python -m spacy download en_core_web_sm

EXPOSE 10000
RUN python manage.py runserver 10000