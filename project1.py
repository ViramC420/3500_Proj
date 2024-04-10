# Course: cmps3500
# CLASS PROJECT 
# PYTHON IMPLEMENTATION: BASIC DATA ANALYSIS 
# Date: 4.9.24 
# Student 1: Justin Alejo 
# Student 2: Karla Medrano   
# Student 3: Christian Viramontes 
# Student 4: Delaney Welch  
# Description: Implementation Basic Data Analysis Routines 

import pandas as pd
import numpy as np
from datetime import datetime
import time

file_path = 'US_Accidents_data.csv'

def print_csv_contents(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # only consider the first 5 digits of the zip code
    df['Zipcode'] = df['Zipcode'].astype(str).str.split('-').str[0]

    #convert Start_time and End_time to datetime
    #calculate the durations and filter our rows where duration is zero
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['End_Time'] = pd.to_datetime(df['End_Time'])
    duration = (df['End_Time'] - df['Start_Time']).dt.total_seconds() / 60
    df = df[duration != 0]

    # Drop the rows where data is missing from any one of these column names
    columns_to_check = ['ID', 'Severity', 'Zipcode', 'Start_Time', 'End_Time', 'Visibility(mi)', 'Weather_Condition', 'Country']
    df_cleaned = df.dropna(subset=columns_to_check)

    # Drop the rows where data is missing from more than 3 columns
    min_non_na = len(df.columns) - 2;
    df_cleaned = df_cleaned.dropna(thresh=min_non_na)

    #Eliminate all rows with distance equal to zero
    df_cleaned = df_cleaned[df_cleaned['Distance(mi)'] != 0] 
    
    # Print the contents of the DataFrame
    print(df_cleaned)


print_csv_contents(file_path)


# What would happen I get a file that is corrupted?
# What if 2 of the columns don't have the same number of rows?
# What if the programs takes too much to long to process the data set?
# What if you divide by zero?
# What if there is an error in one of the formulas?


# READ DATA INTO DF
def load_data(file_path):
    # START TIMING 
    start_time = time.time()
    
    print("\nLoading input data set:")
    print("************************")
    print(f"{datetime.now()} Starting Script")
    print(f"{datetime.now()} Loading {file_path}")

    # READ FILE
    df = pd.read_csv(file_path)

    print(f"{datetime.now()} Total Columns Read: {len(df.columns)}")
    print(f"{datetime.now()} Total Rows Read: {len(df)}")

    # CALCULATE TIME TAKEN TO LOAD DATA
    load_time = time.time() - start_time

    print(f"Time to load is: {load_time:.2f} seconds")

    # RETURN DATAFRAME AND TIME TAKEN
    return df, load_time


# SEARCH CAPACITY
def search_accidents(df, choice):
    if choice == '4':
        state = input("Enter a State name: ")
        city = input("Enter a City name: ")
        zipcode = input("Enter a ZIP Code: ")
        # [PH]

    elif choice == '5':
        year = input("Enter a Year: ")
        month = input("Enter a Month name: ")
        day = input("Enter a Day: ")
        # [PH]

    elif choice == '6':
        min_temp = input("Enter a Minimum Temperature (F): ")
        max_temp = input("Enter a Maximum Temperature (F): ")
        min_vis = input("Enter a Minimum Visibility (mi): ")
        max_vis = input("Enter a Maximum Visibility (mi): ")
        # [PH]


# MAIN MENU DROP-DOWN
def main():
    running = True
    df = None
    total_time = 0

    while running:
        print("\nMenu:")
        print("(1) Load data")
        print("(2) Process data")
        print("(3) Print Answers")
        print("(4) Search Accidents (Use City, State, and Zip Code)")
        print("(5) Search Accidents (Year, Month and Day)")
        print("(6) Search Accidents (Temperature Range and Visibility Range)")
        print("(7) Quit")

        choice = input("Select an option: ")

        if choice == '1':
            df, load_time = load_data(file_path)
            total_time += load_time
        elif choice == '2' and df is not None:
            clean_data(df) # [PH]
        elif choice == '3' and df is not None:
            print_answers(df) # [PH]
        elif choice in ['4', '5', '6'] and df is not None:
            search_accidents(df, choice)
        elif choice == '7':
            print(f"Total Running Time (In Minutes): {total_time / 60:.2f}")
            print("Exiting the program.")
            running = False

if __name__ == "__main__":
    main()
