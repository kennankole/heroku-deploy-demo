# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /application

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUBUFFERED 1

# Installing external dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libimage-exiftool-perl \
    && apt-get -y install scribus --no-install-recommends \
    && apt-get -y install inkscape  --no-install-recommends \
    && apt-get -y install ffmpeg  --no-install-recommends \
    && apt-get -y install xvfb  --no-install-recommends \
    && apt-get -y install python3-vtk7  --no-install-recommends \
    && apt-get -y install poppler-utils  --no-install-recommends \
    && apt-get -y install libfile-mimeinfo-perl  --no-install-recommends \
    && apt-get -y install ghostscript  --no-install-recommends \
    && apt-get -y install zlib1g-dev  --no-install-recommends \
    && apt-get -y install libsecret-1-0  --no-install-recommends \
    && apt-get -y install libjpeg-dev  --no-install-recommends \
    && apt-get -y install imagemagick  --no-install-recommends \
    && apt-get -y install libmagic1  --no-install-recommends \
    && apt-get -y install webp  --no-install-recommends \
    && apt-get -y install netcat --no-install-recommends \
    && rm -fr /var/lib/apt/lists/*


RUN apt-get clean all

# Installing pip Dependencies
RUN pip install --upgrade pip && pip install pipenv

COPY ./Pipfile* /application/

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

COPY . /application
# RUN addgroup --system app && adduser --system --group app

# RUN chown -R app:app /application && chmod -R 755 /application
# USER app




# CMD ["gunicorn", "wsgi:app" , "--bind 0.0.0.0:$PORT]
# ENTRYPOINT ["/application/entrypoint.sh"]

