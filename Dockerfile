FROM python:3.11-slim

ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"

ENV FLASK_ENV=production

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG API_KEY

ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION
ENV API_KEY $API_KEY

ADD ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . /app/
WORKDIR /app

CMD [ "gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=2" ]