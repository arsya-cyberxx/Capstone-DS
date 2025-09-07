"""
Defines shared resource configurations for development environment.
"""

from dagster import EnvVar, FilesystemIOManager

SHARED_POSTGRES_CONF = {
      "username": EnvVar("_PG_USERNAME"),
      "password": EnvVar("_PG_PASSWORD"),
      "hostname": EnvVar("_PG_HOSTNAME"),
      "db_name": EnvVar("_PG_DATABASE"),
      "port": EnvVar("_PG_PORT")
}


RESOURCES_DEV = {
    "config": SHARED_POSTGRES_CONF,
    "fs_io_manager": FilesystemIOManager(),
}
