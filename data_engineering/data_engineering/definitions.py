"""
Definitions for the data engineering project.
Definitions: a collection of assets, jobs, schedules, and sensors.
"""
from dagster import Definitions, load_assets_from_modules

from data_engineering import assets  # noqa: TID252
from data_engineering.schedules import spacex_pipeline_schedule  # noqa: TID252
from data_engineering.jobs import spacex_pipeline_job  
from data_engineering.resources import RESOURCES_DEV # noqa: TID252

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=[*all_assets],
    jobs=[spacex_pipeline_job],
    schedules=[spacex_pipeline_schedule],
    resources={'postgres':RESOURCES_DEV},
)
