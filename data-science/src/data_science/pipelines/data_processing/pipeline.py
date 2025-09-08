"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Node, Pipeline, node  # noqa
from .nodes import get_data_from_postgres, labelling_data, feature_engineering

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=get_data_from_postgres,
            inputs=None,
            outputs="raw_falcon9_data",
            name="get_data_from_postgres",
            tags=["data_extraction"]
        ),
        node(
            func=labelling_data,
            inputs="raw_falcon9_data",
            outputs="labeled_data",
            name="labelling_data",
            tags=["data_transformation"]
        ),
        node(
            func=feature_engineering,
            inputs="labeled_data",
            outputs="feature_engineered_data",
            name="feature_engineering",
            tags=["data_transformation_advanced"]
        )
    ])
