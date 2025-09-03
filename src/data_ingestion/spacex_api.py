"""
This module is do data ingestion from SpaceX API and create a dataset for part 1 of the project.
"""
import datetime

from pandas import DataFrame, json_normalize, to_datetime
import requests
import numpy as np

class SpaceXAPI:
    """Class to interact with SpaceX API and retrieve launch data."""
    def __init__(self):
        self.boosterversion = []
        self.payloadmass = []
        self.orbit = []
        self.launchsite = []
        self.outcome = []
        self.flights = []
        self.gridfins = []
        self.reused = []
        self.legs = []
        self.landingpad = []
        self.block = []
        self.reusedcount = []
        self.serial = []
        self.longitude = []
        self.latitude = []

    def make_data(self, data: DataFrame) -> DataFrame:
        """
        Creates a new dataframe by making API requests to get the booster version, launch site, payload data, and core data from the rocket and core IDs in the dataframe.

        Args:
            data (DataFrame): The dataframe containing the rocket and core IDs.

        Returns:
            DataFrame: The new dataframe with the additional information from the API requests.
        """
        self.getBoosterVersion(data)
        self.getLaunchSite(data)
        self.getPayloadData(data)
        self.getCoreData(data)

        launch_dict = {'FlightNumber': list(data['flight_number']),
            'Date': list(data['date']),
            'BoosterVersion':self.boosterversion,
            'PayloadMass':self.payloadmass,
            'Orbit':self.orbit,
            'LaunchSite':self.launchsite,
            'Outcome':self.outcome,
            'Flights':self.flights,
            'GridFins':self.gridfins,
            'Reused':self.reused,
            'Legs':self.legs,
            'LandingPad':self.landingpad,
            'Block':self.block,
            'ReusedCount':self.reusedcount,
            'Serial':self.serial,
            'Longitude':self.longitude,
            'Latitude':self.latitude}

        return DataFrame(launch_dict)

    def getBoosterVersion(self, data: DataFrame) -> None:
        """
        Makes an API request to get the booster version from the rocket IDs in the dataframe.

        Args:
            data (DataFrame): The dataframe containing the rocket IDs.

        Returns:
            None
        """
        print("Getting Booster Version Data...")
        for x in data['rocket']:
            if x:
                response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
                self.boosterversion.append(response['name'])

    def getLaunchSite(self, data: DataFrame) -> None:
        """
        Makes an API request to get the launch site data from the launchpad IDs in the dataframe.

        Args:
            data (DataFrame): The dataframe containing the launchpad IDs.

        Returns:
            None
        """
        print("Getting Launch Site Data...")
        for x in data['launchpad']:
            if x:
                response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
                self.longitude.append(response['longitude'])
                self.latitude.append(response['latitude'])
                self.launchsite.append(response['name'])

    def getPayloadData(self, data: DataFrame) -> None:
        """
        Makes an API request to get the payload mass and orbit data from the payload IDs in the dataframe.

        Args:
            data (DataFrame): The dataframe containing the payload IDs.

        Returns:
            None
        """
        print("Getting Payload Data...")
        for load in data['payloads']:
            if load:
                response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
                self.payloadmass.append(response['mass_kg'])
                self.orbit.append(response['orbit'])

# Takes the dataset and uses the cores column to call the API and append the data to the lists
    def getCoreData(self, data: DataFrame) -> None:
        """
        Makes an API request to get the core data from the core IDs in the dataframe.

        Args:
            data (DataFrame): The dataframe containing the core IDs.

        Returns:
            None
        """
        print("Getting Core Data...")
        for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                self.block.append(response['block'])
                self.reusedcount.append(response['reuse_count'])
                self.serial.append(response['serial'])
            else:
                self.block.append(None)
                self.reusedcount.append(None)
                self.serial.append(None)
            self.outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            self.flights.append(core['flight'])
            self.gridfins.append(core['gridfins'])
            self.reused.append(core['reused'])
            self.legs.append(core['legs'])
            self.landingpad.append(core['landpad'])

def api_data(spacex_url: str) -> DataFrame:
    """
    Gets the data from the SpaceX API and filters it to only include the rocket, payloads, launchpad, cores, flight number, and date of the launches.

    Args:
        spacex_url (str): The URL of the SpaceX API.

    Returns:
        DataFrame: The filtered dataframe containing the relevant data.
    """
    response = requests.get(spacex_url)
    data= json_normalize(response.json())

    # Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
    data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

    # We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
    data = data[data['cores'].map(len)==1]
    data = data[data['payloads'].map(len)==1]

    # Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
    data['cores'] = data['cores'].apply(lambda x :x[0])
    data['payloads'] = data['payloads'].map(lambda x : x[0])

    # We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
    data['date'] = to_datetime(data['date_utc']).dt.date

    # Using the date we will restrict the dates of the launches
    data = data[data['date'] <= datetime.date(2020, 11, 13)]
    return data

def get_data(spacex_url: str) -> None:
    """
    Gets the data from the SpaceX API and filters it to only include the rocket, payloads, launchpad, cores, flight number, and date of the launches.
    Then, it creates a dataset for part 1 of the project, which includes Falcon 9 launches only, and saves it to a csv file.
    
    Parameters
    ----------
    spacex_url : str
        The URL of the SpaceX API.

    Returns
    -------
    None
    """
    data = api_data(spacex_url)

    api = SpaceXAPI()
    df = api.make_data(data)
    
    # Hint data['BoosterVersion']!='Falcon 1'
    data_falcon9=df[df['BoosterVersion']=='Falcon 9']
    data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))

    # Calculate the mean value of PayloadMass column
    mean=df['PayloadMass'].mean()

    # Replace the np.nan values with its mean value
    df['PayloadMass'].replace(np.nan, mean, inplace=True)
    data_falcon9.to_csv(r'src\data\dataset_part_1.csv', index=False)
