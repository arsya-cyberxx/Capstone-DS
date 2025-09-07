"""
Schedules for the data engineering project.
Schedules: define when and how often jobs should be executed.
"""

from dagster import ScheduleDefinition

from data_engineering.jobs import spacex_pipeline_job

spacex_pipeline_schedule = ScheduleDefinition(
    job=spacex_pipeline_job, cron_schedule="@daily"
)
