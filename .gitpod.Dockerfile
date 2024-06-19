# You could use `gitpod/workspace-full` as well.
FROM gitpod/workspace-python

USER root
WORKDIR /opt
RUN if [ "$(arch)" = "aarch64" ] ; then ARCHITECTURE="aarch64" ; else ARCHITECTURE="x64"; fi && \
    wget -O OpenJDK.tar.gz https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.11%2B9/OpenJDK11U-jdk_${ARCHITECTURE}_linux_hotspot_11.0.11_9.tar.gz
RUN tar xzf OpenJDK.tar.gz
ENV JAVA_HOME="/opt/jdk-11.0.11+9" \
    PATH="/opt/jdk-11.0.11+9/bin:$PATH"

#TODO : Change the user to non root user
#USER 185
WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml

RUN pyenv install 3.11.4 && pyenv global 3.11.4 && poetry env use "${HOME}/.pyenv/versions/3.11.4/bin/python3"
