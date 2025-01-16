# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:21:26 2025

@author: Reuben Dlamini
"""
import requests
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd

# Author: Reuben Dlamini

# Helper functions
def date_time(table_cells):
    """
    Step 1: Extracts the date and time from the HTML table cell
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    Step 2: Extracts the booster version from the HTML table cell
    """
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out

def landing_status(table_cells):
    """
    Step 3: Extracts the landing status from the HTML table cell
    """
    return [i for i in table_cells.strings][0]

def get_mass(table_cells):
    """
    Step 4: Extracts the payload mass from the HTML table cell
    """
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass

def extract_column_from_header(row):
    """
    Step 5: Extracts the column name from the header row
    """
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
    column_name = ' '.join(row.contents)
    if not(column_name.strip().isdigit()):
        return column_name.strip()

# Step 6: Request the webpage
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
response = requests.get(static_url)

# Check if the request was successful
print(response.status_code)  # 200 means OK

# Step 7: Parse the content of the response with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Print page title to ensure it's loaded correctly
print(soup.title.string)

# Step 8: Extract column names from the header
html_tables = soup.find_all('table')

# Print the third table to ensure it contains the correct launch data
first_launch_table = html_tables[2]

# Extract the column names from the <th> elements in the table header
column_names = []
th_result = first_launch_table.find_all('th')

for th in th_result:
    col_name = extract_column_from_header(th)
    if col_name and len(col_name) > 1:
        column_names.append(col_name)

print(column_names)

# Step 9: Prepare dictionary for storing the data
launch_dict = dict.fromkeys(column_names)

# Remove irrelevant column
del launch_dict['Date and time ( )']

# Initialize the dictionary with empty lists
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []

# Additional columns
launch_dict['Version Booster'] = []
launch_dict['Booster landing'] = []
launch_dict['Date'] = []
launch_dict['Time'] = []

# Step 10: Extract data and populate the dictionary
extracted_row = 0

for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    for rows in table.find_all("tr"):
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
        
        row = rows.find_all('td')
        
        if flag:  # Only process rows with valid flight number
            extracted_row += 1
            
            # Extract and append Flight Number
            launch_dict["Flight No."].append(flight_number)
            print(flight_number)
            
            datatimelist = date_time(row[0])
            # Date and Time
            launch_dict["Date"].append(datatimelist[0].strip(','))
            print(datatimelist[0])
            launch_dict["Time"].append(datatimelist[1])
            print(datatimelist[1])
            
            # Booster version
            bv = booster_version(row[1])
            if not(bv):
                bv = row[1].a.string
            launch_dict["Version Booster"].append(bv)
            print(bv)
            
            # Launch Site
            launch_site = row[2].a.string
            launch_dict["Launch site"].append(launch_site)
            print(launch_site)
            
            # Payload
            payload = row[3].a.string
            launch_dict["Payload"].append(payload)
            print(payload)
            
            # Payload Mass
            payload_mass = get_mass(row[4])
            launch_dict["Payload mass"].append(payload_mass)
            print(payload_mass)
            
            # Orbit
            orbit = row[5].a.string
            launch_dict["Orbit"].append(orbit)
            print(orbit)
            
            # Customer
            if row[6]:
                customer = row[6].a.string if row[6].a else row[6].string.strip()
            else:
                customer = ''
            launch_dict["Customer"].append(customer)
            print(customer)
            
            # Launch outcome
            launch_outcome = list(row[7].strings)[0]
            launch_dict["Launch outcome"].append(launch_outcome)
            print(launch_outcome)
            
            # Booster landing
            booster_landing = landing_status(row[8])
            launch_dict["Booster landing"].append(booster_landing)
            print(booster_landing)

# Step 11: Create a DataFrame from the dictionary
df = pd.DataFrame({key: pd.Series(value) for key, value in launch_dict.items()})

# Step 12: Save the DataFrame to a CSV file
df.to_csv('spacex_web_scraped.csv', index=False)

print("Data saved to spacex_web_scraped.csv")

