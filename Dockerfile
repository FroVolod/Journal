FROM frolvlad/alpine-python3

WORKDIR /var/www
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

USER nobody
COPY ./ ./
CMD python manage.py runserver --host 0.0.0.0
