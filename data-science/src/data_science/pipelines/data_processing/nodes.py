"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.0.0
"""
import pandas as pd

from data_science.postgres_fn.postgres_io import PGStorageHandler

def get_data_from_postgres() -> pd.DataFrame:
    """
    Function to get data from Postgres database
    """
    pg_handler = PGStorageHandler()
    df = pg_handler.execute_query("select * from falcon9_api_data")
    return df

def labelling_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Labelling the data for binary classification
    """
    landing_outcomes = df['Outcome'].value_counts()
    bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])

    landing_class = []

    for _, value in df['Outcome'].items():
        if value in bad_outcomes:
            landing_class.append(0)
        else:
            landing_class.append(1)

    df['Class']=landing_class
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature Engineering
    """
    features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
    features_one_hot = pd.get_dummies(features, drop_first=True)
    features_one_hot =  features_one_hot.astype(float)
    return features_one_hot
