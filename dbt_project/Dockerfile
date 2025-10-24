FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -yqq
RUN apt-get install git -y

# Add code location code
WORKDIR /opt/dagster_server

COPY docker-entrypoint.sh .
COPY src/dagster_server/ .
COPY src/jaffle_shop/ ./jaffle_shop/

RUN pip install -U pip && \
    pip install -r reqirements.txt

RUN cd jaffle_shop && \
    dbt deps && \
    dbt parse

# Run dagster code server on port 4000
EXPOSE 4000

# CMD allows this to be overridden from run launchers or executors to execute runs and steps
CMD ["bash", "docker-entrypoint.sh"]