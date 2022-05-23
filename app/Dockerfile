FROM python:3.8

COPY . /app

WORKDIR /app

# Install Debian packages.
RUN apt-get clean && apt-get update -y && \
    apt-get install --no-install-recommends -y -q ca-certificates \
    build-essential locales nano

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:${PATH}"
RUN poetry config virtualenvs.in-project true

ENTRYPOINT ["/bin/bash"]