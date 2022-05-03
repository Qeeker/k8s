FROM docker.ops.iszn.cz/baseimage/debian-python3:bullseye

ENV FILE_COMMON=dockerfile-common
ENV DEPLOYMENT_ENV=dockerfile-deployment-env

RUN mkdir /config; echo "dockerfile" > /config/cfg

COPY script.py /script.py
ENTRYPOINT ["python3", "/script.py"]
