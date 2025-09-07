"""
Definitions for the data engineering project.
Definitions: a collection of assets, jobs, schedules, and sensors.
"""

from dagster import define_asset_job

from data_engineering.assets import falcon9_data, spacex_launch_data

spacex_pipeline_job = define_asset_job(
    name="spacex_pipeline_job",
    selection=[
        falcon9_data.key,
        spacex_launch_data.key
    ]
)
