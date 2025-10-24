from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster_docker import DockerRunLauncher
from .assets import assets
from .project import jaffle_shop_project
from .schedules import schedules

launcher = DockerRunLauncher(
    image="dbt_project:latest",
    network="dagster_network",
)

defs = Definitions(
    assets=assets,
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=jaffle_shop_project),
        "run_launcher": launcher,
    },
)
