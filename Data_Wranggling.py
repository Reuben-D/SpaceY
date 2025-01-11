# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 15:10:13 2025

@author: Reuben Dlamini
"""

"""
Author: Reuben Dlamini
Project: SpaceY Falcon 9 First Stage Landing Prediction
Description: Data wrangling and exploratory data analysis to prepare training labels
"""

# Import necessary libraries
import pandas as pd
#import numpy as np

# Main execution block
if __name__ == "__main__":
    # Load SpaceX dataset from the provided URL
    df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")

    # Display first 10 rows of the dataset to get an initial overview
    print(df.head(10))

    # Identify and calculate the percentage of missing values in each attribute
    missing_values = df.isnull().sum() / len(df) * 100  # Compute percentage of missing values
    print(missing_values)

    # Identify numerical and categorical columns
    dtypes = df.dtypes  # Get data types of each column
    print(dtypes)

    # STEP 1: Calculate the number of launches at each site
    launch_counts = df["LaunchSite"].value_counts()  # Count occurrences of each launch site
    print(launch_counts)

    # STEP 2: Calculate the number and occurrence of each orbit
    orbit_counts = df["Orbit"].value_counts()  # Count occurrences of each orbit type
    print(orbit_counts)

    # STEP 3: Calculate the number and occurrence of mission outcomes
    landing_outcomes = df['Outcome'].value_counts()  # Count occurrences of each outcome
    print(landing_outcomes)

    # Display unique mission outcomes with their indices to better understand different categories
    for i, outcome in enumerate(landing_outcomes.keys()):
        print(i, outcome)

    # Define unsuccessful landing outcomes
    # Selecting specific unsuccessful outcomes using index positions
    bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])  
    print(bad_outcomes)

    # STEP 4: Create a landing outcome label from the Outcome column
    # Assign 0 if the outcome is in bad_outcomes, otherwise assign 1
    landing_class = [0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]

    df['Class'] = landing_class  # Add the new classification column
    print(df[['Class']].head(8))  # Display first 8 rows of the new column

    # Display first 5 rows with the new Class column
    print(df.head(5))

    # Calculate and display the success rate of landings
    success_rate = df["Class"].mean()  # Compute the mean of Class column to get success rate
    print(f"Landing Success Rate: {success_rate:.2f}")

    # Export the cleaned dataset for the next stage
    #df.to_csv("dataset_part_2.csv", index=False)  # Save dataframe to a CSV file
