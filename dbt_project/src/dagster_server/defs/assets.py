import json
import dagster as dg
from dagster_dbt import DbtCliResource, dbt_assets

from .project import jaffle_shop_project

partitions_def = dg.MultiPartitionsDefinition(
    {
        "country": dg.StaticPartitionsDefinition(["jp", "cn", "tw", "us", "fr", "au", "vn"]),
        # "country": dg.DynamicPartitionsDefinition(name="country"),
        "dt": dg.HourlyPartitionsDefinition(start_date="2025010100", fmt="%Y%m%d%H"),
    }
)


@dbt_assets(
    manifest=jaffle_shop_project.manifest_path,
    select="tag:bronze",
)
def bronze(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["seed", "--cache-selected-only",], context=context).stream()


@dbt_assets(
    manifest=jaffle_shop_project.manifest_path,
    select="tag:silver",
    partitions_def=partitions_def
)
def silver(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    partition_keys: dg.MultiPartitionKey = context.partition_key.keys_by_dimension
    country = partition_keys["country"]
    run_date = partition_keys["dt"]

    dbt_vars = {
        "country": country,
        "run_date": run_date.replace("-", ""),
    }

    dbt_run_args = [
        "run",
        "--cache-selected-only",
        "--vars",
        json.dumps(dbt_vars),
    ]

    yield from dbt.cli(dbt_run_args, context=context).stream()


@dbt_assets(
    manifest=jaffle_shop_project.manifest_path,
    select="tag:gold",
)
def gold(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    time_window = context.partition_time_window

    dbt_vars = {
        "run_date": time_window.end.strftime("%Y%m%d")
    }
    dbt_build_args = ["run", "--cache-selected-only", "--vars", json.dumps(dbt_vars)]

    yield from dbt.cli(dbt_build_args, context=context).stream()


assets = [
    bronze, silver, gold
]
