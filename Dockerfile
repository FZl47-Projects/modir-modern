FROM hub.hamdocker.ir/library/python:3.11
WORKDIR /django_app/
ADD ./requirements/production.txt ./
RUN pip install -r ./production.txt
WORKDIR /django_app/src
ADD ./src ./
ENTRYPOINT ["/bin/sh", "-c", "python manage.py migrate && python manage.py qcluster &"]
ENTRYPOINT ["/bin/sh", "-c" , "gunicorn --bind 0.0.0.0:8000 config.wsgi"]