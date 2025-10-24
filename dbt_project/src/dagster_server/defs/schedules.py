import dagster as dg
import dagster_dbt as dgdbt
from .assets import silver, gold

# my_schedule = ScheduleDefinition(
#     name="all_dbt_assets_daily_schedule",
#     cron_schedule="0 0 * * *",
#     job=define_asset_job(
#         name="all_dbt_assets",
#         selection=DbtManifestAssetSelection.build(
#             manifest=manifest,
#             select="tag:XXX",
#         ),
#     ),
# )


@dg.schedule(
    job=dg.define_asset_job(
        name="datamart_jp_hourly",
        selection=dg.AssetSelection.assets(silver),
    ),
    cron_schedule="0/5 * * * *",
)
def datamart_jp_hourly(context: dg.ScheduleEvaluationContext):
    country = "jp"
    run_date = context.scheduled_execution_time.date().strftime("%Y%m%d%H")

    return [
        dg.RunRequest(
            run_key=f"{country}|{run_date}",
            partition_key=dg.MultiPartitionKey({"country": country, "dt": run_date}),
        )
    ]


datamart_jp_daily = dgdbt.build_schedule_from_dbt_selection(
    [gold],
    job_name="datamart_jp_daily",
    cron_schedule="0 18 * * *",
)

schedules = [
    datamart_jp_hourly,
    datamart_jp_daily,
]
