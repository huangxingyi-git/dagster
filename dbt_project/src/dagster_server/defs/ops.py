from dagster import op, In, Out, Output, AssetMaterialization, OpExecutionContext
from dagster_dbt import DbtCliResource
from .project import jaffle_shop_project


@op(
    ins={
        "select": In(str, default_value="fqn:*"),
        "vars": In(str, default_value=""),
    },
    out={"success_dbt_run": Out(str)},
)
def dbt_run(
    context: OpExecutionContext,
    select: str,
    vars: str,
):
    context.log.info(f"Execute: dbt run --cache-selected-only --select {select} --vars {vars}")
    dbt = DbtCliResource(project_dir=jaffle_shop_project)
    dbt_invocation = dbt.cli(
        ["run", "--cache-selected-only", "--select", select, "--vars", vars],
        context=context
    )

    for raw_event in dbt_invocation.stream_raw_events():
        context.log.info(raw_event)
        for asset_event in raw_event.to_default_asset_events(
            manifest=jaffle_shop_project.manifest_path,
            context=context
        ):
            if isinstance(asset_event, AssetMaterialization):
                yield asset_event
    yield Output(value="success_dbt_run", output_name="success_dbt_run")
