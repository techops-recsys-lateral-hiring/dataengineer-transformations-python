ARG PYTHON_VERSION=3.9.10
FROM --platform=linux/amd64 python:$PYTHON_VERSION
USER root
WORKDIR /opt
RUN wget https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.11%2B9/OpenJDK11U-jdk_x64_linux_hotspot_11.0.11_9.tar.gz && \
    wget https://downloads.lightbend.com/scala/2.13.5/scala-2.13.5.tgz && \
    wget https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
RUN tar xzf OpenJDK11U-jdk_x64_linux_hotspot_11.0.11_9.tar.gz && \
    tar xvf scala-2.13.5.tgz && \
    tar xvf spark-3.2.1-bin-hadoop3.2.tgz
ENV PATH="/opt/jdk-11.0.11+9/bin:/opt/scala-2.13.5/bin:/opt/spark-3.2.1-bin-hadoop3.2/bin:$PATH"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:${PATH}"
RUN poetry config virtualenvs.in-project false

#TODO : Change the user to non root user
#USER 185
WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml

RUN poetry install