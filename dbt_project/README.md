# Creating dagster code location from existing dbt project
```
mkdir dbt_project

mv jaffle_shop dbt_project/src/jaffle_shop

cd dbt_project

uv init

uv add dagster-dbt dagster-webserver

uv run dagster-dbt project scaffold --project-name dagster_server --dbt-project-dir jaffle_shop

mv dagster_server src/dagster_server

```
