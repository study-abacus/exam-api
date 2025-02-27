FROM python:3.12.1

WORKDIR /app/


RUN addgroup --system app && adduser --system --group app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0
# ENV INSTALL_DEV=true


# Install Poetry
RUN curl -sSLk https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false



# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./server/pyproject.toml ./server/poetry.lock* /app/


# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false

RUN bash -c "poetry install --no-root"


COPY ./server /app
RUN chmod +x run.sh


ENV PYTHONPATH=/app


# chown all the files to the app user
RUN chown -R app:app $HOME


# change to the app user
# Switch to a non-root user, which is recommended by Heroku.
USER app


# And then will start Uvicorn
CMD ["sh","run.sh"]

