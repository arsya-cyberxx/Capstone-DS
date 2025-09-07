"""
This module contains the asset definitions for the data engineering pipeline.
Assets: represent a piece of data or a dataset that is produced or consumed by a job.
"""
from dagster import asset, MetadataValue
import pandas as pd

from data_engineering.functions.postgresql_io import PGStorageHandler
from data_engineering.functions.functions import get_data

@asset(compute_kind="python")
def falcon9_data():
    """
    Retrieves past launches from the SpaceX API and stores the data in Postgres
    
    : return :pd.DataFrame with the data
    """
    df = get_data("https://api.spacexdata.com/v4/launches/past")

    pg_handler = PGStorageHandler()
    pg_handler.df_to_table(df, "falcon9_api_data")

    preview_df = pg_handler.execute_query("select * from falcon9_api_data limit 10")
    metadata = {
        "preview_stage_data": MetadataValue.md(
            preview_df.to_markdown(disable_numparse=True)
        ),
    }
    return {"value": preview_df, "metadata": metadata}

@asset(compute_kind="python")
def spacex_launch_data():
    """
    This asset will download the spacex launch data and store it in the database with the table name spacex_launch_data.

    The data is downloaded from the following URL: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv

    The data is then stored in the database using the PGStorageHandler class.

    The preview data is then queried from the database and returned as part of the asset's metadata.

    :return: A dictionary containing the value of the asset and its metadata.
    """
    df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
    
    pg_handler = PGStorageHandler()
    pg_handler.df_to_table(df, "spacex_launch_data")

    preview_df = pg_handler.execute_query("select * from spacex_launch_data limit 10")

    metadata = {
        "preview_stage_data": MetadataValue.md(
            preview_df.to_markdown(disable_numparse=True)
        ),
    }
    return {"value": preview_df, "metadata": metadata}
