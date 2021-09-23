FROM tiangolo/meinheld-gunicorn-flask:python3.8

WORKDIR /app

RUN pip install youtube-dl

COPY ./ytdl_embed /app