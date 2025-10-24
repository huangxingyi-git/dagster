FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -yqq
RUN apt-get install git -y
RUN pip install -U pip && \
    pip install uv

# Set $DAGSTER_HOME and copy dagster.yaml and workspace.yaml there
ENV DAGSTER_HOME=/opt/dagster/

WORKDIR $DAGSTER_HOME

RUN mkdir -p $DAGSTER_HOME

COPY dagster.yaml workspace.yaml pyproject.toml .

RUN uv sync
