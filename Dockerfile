FROM frolvlad/alpine-python3

WORKDIR /var/www
COPY ./requirements.txt ./requirements.txt
RUN apk add --no-cache --virtual=.build_dependencies gcc musl-dev linux-headers libffi-dev python3-dev && \
    pip install -r ./requirements.txt && \
    pip install uwsgi && \
    rm -rf ~/.cache/pip && \
    apk del .build_dependencies

COPY ./ ./
RUN chown -R nobody: ./
USER nobody
CMD uwsgi --need-app --manage-script-name --mount '/=app:app' --http-socket 0.0.0.0:5000
