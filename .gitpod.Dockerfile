# You could use `gitpod/workspace-full` as well.
FROM gitpod/workspace-python

RUN pyenv install 3.10.6 \
    && pyenv global 3.10.6 \
    && pyenv shell 3.10.6