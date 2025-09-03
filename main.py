from src.data_ingestion.spacex_api import get_data

spacex_url="https://api.spacexdata.com/v4/launches/past"
get_data(spacex_url)