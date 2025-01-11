# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 20:09:50 2025

@author: Reuben Dlamini
"""

"""
Author: Reuben Dlamini
Project: SpaceY Falcon 9 First Stage Landing Prediction
Description: Collecting data from the SpaceX API, performing basic data wrangling, and formatting for analysis.
"""

# Import necessary libraries
import requests  # For making API requests
import pandas as pd  # For handling tabular data
#import numpy as np  # For numerical computations
import datetime  # For handling date and time operations

# Setting Pandas display options to show all columns and full column content
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# Function to extract booster version using API
def getBoosterVersion(data):
    BoosterVersion = []
    for x in data['rocket']:
        if x:  # Ensuring the value is not None
            response = requests.get("https://api.spacexdata.com/v4/rockets/" + str(x)).json()
            BoosterVersion.append(response.get('name', None))  # Append booster name or None
    return BoosterVersion

# Function to extract launch site details including name, longitude, and latitude
def getLaunchSite(data):
    LaunchSite, Longitude, Latitude = [], [], []
    for x in data['launchpad']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/" + str(x)).json()
            Longitude.append(response.get('longitude', None))
            Latitude.append(response.get('latitude', None))
            LaunchSite.append(response.get('name', None))
    return LaunchSite, Longitude, Latitude

# Function to extract payload mass and orbit type
def getPayloadData(data):
    PayloadMass, Orbit = [], []
    for load in data['payloads']:
        if load:
            response = requests.get("https://api.spacexdata.com/v4/payloads/" + load).json()
            PayloadMass.append(response.get('mass_kg', None))
            Orbit.append(response.get('orbit', None))
    return PayloadMass, Orbit

# Function to extract core details
def getCoreData(data):
    Outcome, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount, Serial = [], [], [], [], [], [], [], [], []
    for core in data['cores']:
        if core and core.get('core'):
            response = requests.get("https://api.spacexdata.com/v4/cores/" + core['core']).json()
            Block.append(response.get('block', None))
            ReusedCount.append(response.get('reuse_count', None))
            Serial.append(response.get('serial', None))
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core.get('landing_success', 'None')) + ' ' + str(core.get('landing_type', 'None')))
        Flights.append(core.get('flight', None))
        GridFins.append(core.get('gridfins', None))
        Reused.append(core.get('reused', None))
        Legs.append(core.get('legs', None))
        LandingPad.append(core.get('landpad', None))
    return Outcome, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount, Serial

# Define the SpaceX API endpoint for past launches
spacex_url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)

# Check if API request was successful (Status Code 200)
if response.status_code == 200:
    data_j = response.json()
    data = pd.json_normalize(data_j)  # Convert JSON response to Pandas DataFrame
else:
    raise Exception("Failed to retrieve data from SpaceX API")

# Selecting only relevant columns for further analysis
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']].copy()

# Filtering out rows with multiple cores or payloads
data = data[data['cores'].map(len) == 1]
data = data[data['payloads'].map(len) == 1]

# Extract single values from lists in 'cores' and 'payloads' columns
data['cores'] = data['cores'].map(lambda x: x[0])
data['payloads'] = data['payloads'].map(lambda x: x[0])

# Convert date_utc to datetime and extract only the date
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Restrict dataset to launches before a specific date
data = data[data['date'] <= datetime.date(2020, 11, 13)]

# Apply API extraction functions
BoosterVersion = getBoosterVersion(data)
LaunchSite, Longitude, Latitude = getLaunchSite(data)
PayloadMass, Orbit = getPayloadData(data)
Outcome, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount, Serial = getCoreData(data)

# Create a dictionary from extracted data
launch_dict = {
    'FlightNumber': list(data['flight_number']),
    'Date': list(data['date']),
    'BoosterVersion': BoosterVersion,
    'PayloadMass': PayloadMass,
    'Orbit': Orbit,
    'LaunchSite': LaunchSite,
    'Outcome': Outcome,
    'Flights': Flights,
    'GridFins': GridFins,
    'Reused': Reused,
    'Legs': Legs,
    'LandingPad': LandingPad,
    'Block': Block,
    'ReusedCount': ReusedCount,
    'Serial': Serial,
    'Longitude': Longitude,
    'Latitude': Latitude
}

# Convert dictionary to Pandas DataFrame
df = pd.DataFrame(launch_dict)

# Filter only Falcon 9 launches
data_falcon9 = df[df['BoosterVersion'] == "Falcon 9"].copy()

# Reset FlightNumber column
data_falcon9.loc[:, 'FlightNumber'] = list(range(1, data_falcon9.shape[0] + 1))

# Check for missing values
print(data_falcon9.isnull().sum())


# Handle missing values in PayloadMass by replacing NaNs with column mean
payloadmass_mean = data_falcon9['PayloadMass'].mean()
data_falcon9['PayloadMass'].fillna(payloadmass_mean, inplace=True)



# Save cleaned dataset to CSV
#data_falcon9.to_csv('dataset_part_1.csv', index=False)

print('Code successfully ran')