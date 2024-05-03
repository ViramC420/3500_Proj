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

#//IMPLEMENTED BY JUSTIN
#Clean_data function executes when the user enters 2 for the menu options.
#However, this will not execute if the data has not been loaded yet. 
def clean_data(df):

    start_time = time.time()

    print("\nProcessing input data set:")
    print("************************")
    print(f"{datetime.now()} Performing Data Clean Up")

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

    print(f"{datetime.now()} Total Rows Read after cleaning is: {len(df_cleaned)}")

    clean_time = time.time() - start_time
    print(f"Time to process is: {clean_time:.2f} seconds")
    return df_cleaned, clean_time


# ANSWERING QUESTIONS
def print_answers(df):
    print("\nAnswering questions:")
    print("************************")

    print(f"{datetime.now()} 1. What are the 3 months with the highest amount of accidents reported?")
    try:
        top_months = top_three_accident_months(df)
        print(top_months)
    except Exception as e:
        print(f"Failed to calculate due to: {str(e)}")

    # SPACER
    print("\n" + "-"*50 + "\n")

    print(f"{datetime.now()} 2. What is the year with the highest amount of accidents reported?")
    try:
        max_accidents_year, max_accidents_count = year_with_most_accidents(df)
        print(f"Year: {max_accidents_year}, Accident count: {max_accidents_count}")
    except Exception as e:
        print(f"Failed to calculate due to: {str(e)}")


    # SPACER
    print("\n" + "-"*50 + "\n")

    print(f"{datetime.now()} 3. What is the state that had the most accidents of severity 2?")
    try:
        most_severity_2_accidents = state_with_most_severity_2_accidents(df)
        print(most_severity_2_accidents)
    except Exception as e:
        print(f"Failed to calculate due to: {str(e)}")

    # SPACER
    print("\n" + "-"*50 + "\n")

    print(f"{datetime.now()} 4. What severity is the most common in Virginia, California and Florida")
    try:
        most_common_severity = most_common_severity_in_states(df)
        print(most_common_severity)
    except Exception as e:
        print(f"Failed to calculate due to: {str(e)}")

    # SPACER
    print("\n" + "-"*50 + "\n")

    #Question 5: The 5 cities with the most accidents in California displayed per year
    print(f"{datetime.now()} 5. What are the 5 cities that had the most accidents in California?")
    try:
        california_cities = top_five_cities_in_california(df)
        print(f"{datetime.now()} Results:")
        print(california_cities.to_string())  # Converts DataFrame to string for better readability
    except Exception as e:
        print(f"Failed to calculate due to: {str(e)}")

    # SPACER
    print("\n" + "-"*50 + "\n")
    # Question 6: Average humidity and temperature of accidents of severity 4 in Boston displayed per month
    print(f"{datetime.now()} 6. What was the average humidity and average temperature of all accidents of severity 4 that occurred in the city of Boston?")
    try:
        boston_weather = avg_humidity_temperature_boston(df)
        print(f"{datetime.now()} Results:")
        print(boston_weather.to_string())  # Converts DataFrame to string for better readability
    except Exception as e:
        print(f"Failed to calculate due to: {str(e)}")

    # SPACER
    print("\n" + "-"*50 + "\n")
    print(f"{datetime.now()} 7. What are the 3 most common weather conditions when accidents occurred in New York city?")
    try:
        nyc_weather = common_weather_conditions_ny(df)
        print(f"{datetime.now()} Results:")
        # CONVERTS DF TO STRING
        print(nyc_weather.to_string())
    except Exception as e:
        print(f"Failed to calculate due to: {str(e)}")

    # SPACER
    print("\n" + "-"*50 + "\n")

    print(f"{datetime.now()} What was the maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire?")
    try:
        max_vis_nh = max_visibility_severity_2_nh(df)
        print(f"{datetime.now()} Maximum visibility: {max_vis_nh} miles")
    except Exception as e:
        print(f"Failed to calculate due to: {str(e)}")


##########################################
#                                        #
#       BEG print_answer FUNCTIONS       #
#                                        #
##########################################

# QUESTION 1 // IMPLEMENTED BY JUSTIN
def top_three_accident_months(df):

    #Convert Start_Time to datetime
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])

    #Extract year and month from Start_Time
    df['Year_Month'] = df['Start_Time'].dt.to_period('M')

    #Group by the new Year_Month column and count the number of accidents
    monthly_accidents = df.groupby('Year_Month').size()

    #Sort the counts in descending 
    top_months = monthly_accidents.sort_values(ascending=False).head(3)

    return top_months

# QUESTION 2 //IMPLEMENTED BY JUSTIN
def year_with_most_accidents(df):

    #Convert Start_Time to datetime
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])

    #Extract the year from 'Start_Time'
    df['Year'] = df['Start_Time'].dt.year

    #Group by the 'Year' column, find yr with most accidnets
    accident_counts = df['Year'].value_counts()
    max_accidents_year = accident_counts.idxmax()

    #return the number of accidents in that year
    max_accidents_count = accident_counts.max()

    return max_accidents_year, max_accidents_count

#QUESTION 3 // IMPLEMENTED BY JUSTIN
def state_with_most_severity_2_accidents(df):

    # Properly format 'Start_Time' 'Severity'
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['Year'] = df['Start_Time'].dt.year

    # Filter the DataFrame for only accidents with Severity 2
    severity_2_df = df[df['Severity'] == 2]

    # Group the data by State and Year
    grouped = severity_2_df.groupby(['State', 'Year']).size()

    # Reset the index to make 'State' and 'Year' columns again
    grouped = grouped.reset_index(name='Count')

    # Sort and find the state with the maximum accidents for each year
    # First sort by Year and then by Count in descending order to get the state with most accidents on top for each year
    grouped = grouped.sort_values(by=['Year', 'Count'], ascending=[True, False])

    # Drop duplicate years
    result = grouped.drop_duplicates(subset='Year', keep='first').sort_values(by='Year')

    return result

# QUESTION 4 // IMPLEMENTED BY JUSTIN
def most_common_severity_in_states(df):

    states_of_interest = ['VA', 'CA', 'FL']

    # Filter DataFrame for Virginia, California, and Florida
    filtered_df = df[df['State'].isin(states_of_interest)]

    # Group by State and Severity, then count the occurrences
    grouped = filtered_df.groupby(['State', 'Severity']).size()

    grouped_df = grouped.reset_index(name='Count')

    # Sort the DataFrame by State and Count in descending order to find the most common severity for each state
    grouped_df = grouped_df.sort_values(by=['State', 'Count'], ascending=[True, False])

    # Drop duplicates
    most_common_severity = grouped_df.drop_duplicates(subset='State', keep='first').reset_index(drop=True)

    return most_common_severity

#QUESTION 5 // karla
def top_five_cities_in_california(df):
    ca_accidents = df[df['State'] == 'CA'].copy()
    ca_accidents['Year'] = pd.to_datetime(ca_accidents['Start_Time']).dt.year
    grouped = ca_accidents.groupby(['Year', 'City']).size().reset_index(name='Count')
    top_cities_by_year = grouped.sort_values(['Year', 'Count'], ascending=[True, False])
    top_cities_by_year = top_cities_by_year.groupby('Year').head(5)
    return top_cities_by_year.pivot(index='Year', columns='City', values='Count')

# Question 6 //karla
def avg_humidity_temperature_boston(df):
    boston_accidents = df[(df['Severity'] == 4) & (df['City'] == 'Boston')].copy()
    boston_accidents['Month'] = pd.to_datetime(boston_accidents['Start_Time']).dt.month
    return boston_accidents.groupby('Month').agg({'Humidity(%)': 'mean', 'Temperature(F)': 'mean'}).reset_index()

# QUESTION 7
def common_weather_conditions_ny(df):
    # FILTER FOR NY
    nyc_accidents = df[df['City'] == 'New York'].copy()

    # CONVERT Start_Time
    nyc_accidents['Start_Time'] = pd.to_datetime(nyc_accidents['Start_Time'])
    nyc_accidents['Month'] = nyc_accidents['Start_Time'].dt.month

    # GROUP BY MONTH AND WEATHER CONDITION
    grouped = nyc_accidents.groupby(['Month', 'Weather_Condition']).size().reset_index(name='Count')

    # SORT
    top_conditions_by_month = grouped.sort_values(['Month', 'Count'], ascending=[True, False])

    # GET TOP 3 CONDITIONS
    top_conditions_by_month = top_conditions_by_month.groupby('Month').head(3)

    # RETURN IN READABLE FORMAT
    return top_conditions_by_month.pivot(index='Month', columns='Weather_Condition', values='Count')

# QUESTION 8
def max_visibility_severity_2_nh(df):
    # FILTER FOR NH + VIS 2
    nh_severity_2 = df[(df['State'] == 'NH') & (df['Severity'] == 2)].copy()

    # CONVERT TO NUMERIC + ERROR HANDLING
    nh_severity_2.loc[:, 'Visibility(mi)'] = pd.to_numeric(nh_severity_2['Visibility(mi)'], errors='coerce')

    # FIND MAX VISIBILITY
    max_visibility = nh_severity_2['Visibility(mi)'].max()

    # RETURN VIS FOUND
    return max_visibility

##########################################
#                                        #
#       END print_answer FUNCTIONS       #
#                                        #
##########################################


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

# menu 5 and 6
def search_accidents_by_date(year='', month='', day=''):
    filtered_data = accidents_data
    if year:
        filtered_data = filtered_data[filtered_data['Start_Time'].dt.year == int(year)]
    if month:
        filtered_data = filtered_data[filtered_data['Start_Time'].dt.month == int(month)]
    if day:
        filtered_data = filtered_data[filtered_data['Start_Time'].dt.day == int(day)]
    return len(filtered_data)

def search_accidents_by_temp_vis(min_temp='', max_temp='', min_vis='', max_vis=''):
    filtered_data = accidents_data
    if min_temp:
        filtered_data = filtered_data[filtered_data['Temperature(F)'] >= float(min_temp)]
    if max_temp:
        filtered_data = filtered_data[filtered_data['Temperature(F)'] <= float(max_temp)]
    if min_vis:
        filtered_data = filtered_data[filtered_data['Visibility(mi)'] >= float(min_vis)]
    if max_vis:
        filtered_data = filtered_data[filtered_data['Visibility(mi)'] <= float(max_vis)]
    return len(filtered_data)


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
            df, load_time = clean_data(df) # [PH]
            total_time += load_time
        elif choice == '3' and df is not None:
            print_answers(df)
        elif choice in ['4', '5', '6'] and df is not None:
            search_accidents(df, choice)
        elif choice == '7':
            print(f"Total Running Time (In Minutes): {total_time / 60:.2f}")
            print("Exiting the program.")
            running = False

#if __name__ == "__main__":
