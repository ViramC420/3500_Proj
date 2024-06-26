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
import os

# READ DATA INTO DF
def load_data():

    csv_files = [file for file in os.listdir('.') if file.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the directory.")
        return None, None
    
    print("\nAvailabe CSV files:")
    for index, file in enumerate(csv_files):
        print(f"{index + 1}. {file}")

    try:
        file_index = int(input("Select the file number to load: ")) - 1
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None, None
    
    if file_index >= 0 and file_index < len(csv_files):
        file_path = csv_files[file_index]
    else:
        print("Invaled file selection.")
        return None, None

    #Start timing
    start_time = time.time()

    try:
        print("\nLoading input data set:")
        print("************************")
        print(f"{datetime.now()} Starting Script")
        print(f"{datetime.now()} Loading {file_path}")

        # READ FILE INTO DATAFRAME
        df = pd.read_csv(file_path)

        print(f"{datetime.now()} Total Columns Read: {len(df.columns)}")
        print(f"{datetime.now()} Total Rows Read: {len(df)}\n")
    except FileNotFoundError:
        print("The specified file was not found.")
        return None, None  
    except pd.errors.EmptyDataError:
        print("No data: The file is empty.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

    # CALCULATE TIME TAKEN TO LOAD DATA
    load_time = time.time() - start_time

    print(f"Time to load is: {load_time:.2f} seconds")

    # RETURN DATAFRAME AND TIME TAKEN
    return df, load_time

#//IMPLEMENTED BY JUSTIN
#Clean_data function executes when the user enters 2 for the menu options.
def clean_data(df):
    start_time = time.time()
    print("\nProcessing input data set:")
    print("************************")
    print(f"{datetime.now()} Performing Data Clean Up")

    try:
        df['Zipcode'] = df['Zipcode'].astype(str).str.split('-').str[0]
        
        df['Start_Time'] = pd.to_datetime(df['Start_Time'])
        df['End_Time'] = pd.to_datetime(df['End_Time'])
        duration = (df['End_Time'] - df['Start_Time']).dt.total_seconds() / 60
        df = df[duration != 0]

        columns_to_check = ['ID', 'Severity', 'Zipcode', 'Start_Time', 'End_Time', 'Visibility(mi)', 'Weather_Condition', 'Country']
        df_cleaned = df.dropna(subset=columns_to_check)

        min_non_na = len(df.columns) - 2
        df_cleaned = df_cleaned.dropna(thresh=min_non_na)

        df_cleaned = df_cleaned[df_cleaned['Distance(mi)'] != 0]

        print(f"{datetime.now()} Total Rows Read after cleaning is: {len(df_cleaned)}")

        clean_time = time.time() - start_time
        print(f"Time to process is: {clean_time:.2f} seconds")
        return df_cleaned, clean_time
    
    except KeyError as e:
        print(f"Dataframe does not have the specified columns: {e}. Please try again.")
        return None, 0
    except Exception as e:
        print(f"An unexpected error occurured: {e}")
        return None, 0


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

    # SPACER
    print("\n" + "-"*50 + "\n")

    print(f"{datetime.now()} 9. How many accidents of each severity were recorded in Bakersfield?")
    try:
        result = bk(df)
        print(result)
    except Exception as e:
        print(f"Failed to calculate due to: {str(e)}")

    # SPACER 
    print("\n" + "-"*50 + "\n") 
    print(f"{datetime.now()} 10. What was the longest accident (in hours) recorded in Las Vegas in the Spring (March, April, and May)?") 

    try: 
        max_df = ten(df) 
        print(f"{datetime.now()} The longest accident (in hours) was:") 

        # CONVERTS DF TO STRING 
        print(max_df.to_string()) 
    except Exception as e: 
        print(f"Failed to calculate due to: {str(e)}")  
        
##########################################
#                                        #
#       BEG print_answer FUNCTIONS       #
#                                        #
##########################################

# QUESTION 1 // IMPLEMENTED BY JUSTIN
# What are the 3 months with the highest amount of accidents reported?
def top_three_accident_months(df):

    df['Start_Time'] = pd.to_datetime(df['Start_Time'])

    df['Year_Month'] = df['Start_Time'].dt.to_period('M')

    monthly_accidents = df.groupby('Year_Month').size()

    top_months = monthly_accidents.sort_values(ascending=False).head(3)

    return top_months

# QUESTION 2 //IMPLEMENTED BY JUSTIN
# What is the year with the highest amount of accidents reported?
def year_with_most_accidents(df):

    df['Start_Time'] = pd.to_datetime(df['Start_Time'])

    df['Year'] = df['Start_Time'].dt.year

    accident_counts = df['Year'].value_counts()
    max_accidents_year = accident_counts.idxmax()

    max_accidents_count = accident_counts.max()

    return max_accidents_year, max_accidents_count

#QUESTION 3 // IMPLEMENTED BY JUSTIN
#What is the state that had the most accidents of Severity 2?
def state_with_most_severity_2_accidents(df):

    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['Year'] = df['Start_Time'].dt.year

    severity_2_df = df[df['Severity'] == 2]

    grouped = severity_2_df.groupby('State').size()

    grouped = grouped.reset_index(name='Count')

    result = grouped.sort_values(by='Count', ascending=False).head(1)
    return result

# QUESTION 4 // IMPLEMENTED BY JUSTIN
# What Severity is the most common in Virginia, California, and Florida?
def most_common_severity_in_states(df):

    states_of_interest = ['VA', 'CA', 'FL']

    filtered_df = df[df['State'].isin(states_of_interest)]

    grouped = filtered_df.groupby(['State', 'Severity']).size()

    grouped_df = grouped.reset_index(name='Count')

    grouped_df = grouped_df.sort_values(by=['State', 'Count'], ascending=[True, False])

    most_common_severity = grouped_df.drop_duplicates(subset='State', keep='first').reset_index(drop=True)

    return most_common_severity

#QUESTION 5 // karla
# What are the 5 cities that had the most accidents in California?
def top_five_cities_in_california(df):
    # FILTERING
    ca_accidents = df[df['State'] == 'CA'].copy()

    # EXTRACT YEAR AND GROUP BY YEAR AND CITY
    ca_accidents['Year'] = pd.to_datetime(ca_accidents['Start_Time']).dt.year
    grouped = ca_accidents.groupby(['Year', 'City']).size().reset_index(name='Count')

    # GET TOP CITIES OVERALL
    overall_top_cities = grouped.groupby('City')['Count'].sum().nlargest(5).index

    # FILTER TO KEEP TOP 5
    top_cities_by_year = grouped[grouped['City'].isin(overall_top_cities)]

    # FOR BETTER VISIBILITY
    result = top_cities_by_year.pivot(index='Year', columns='City', values='Count').fillna(0)
    result.columns.name = "Top 5 Cities"

    return result

# Question 6 //karla
# What is the average humidity and average temperature of all accidents of 
# severity 4 that occurred in the city of Boston?
def avg_humidity_temperature_boston(df):
    boston_accidents = df[(df['Severity'] == 4) & (df['City'] == 'Boston')].copy()
    boston_accidents['Month'] = pd.to_datetime(boston_accidents['Start_Time']).dt.month
    return boston_accidents.groupby('Month').agg({'Humidity(%)': 'mean', 'Temperature(F)': 'mean'}).reset_index()

# QUESTION 7
# What are the 3 most common weather conditions when accidents occur in New York City?
def common_weather_conditions_ny(df):
    # FILTER FOR NY
    nyc_accidents = df[df['City'] == 'New York'].copy()

    # CONVERT Start_Time
    nyc_accidents['Start_Time'] = pd.to_datetime(nyc_accidents['Start_Time'])
    nyc_accidents['Month'] = nyc_accidents['Start_Time'].dt.month

    # GROUP BY MONTH AND WEATHER CONDITION
    grouped = nyc_accidents.groupby(['Month', 'Weather_Condition']).size().reset_index(name='Count')

    # SORT AND GET TOP 3 CONDITIONS FOR EACH MONTH
    top_conditions_by_month = grouped.sort_values(['Month', 'Count'], ascending=[True, False])
    top_conditions_by_month = top_conditions_by_month.groupby('Month').head(3)

    # READABILITY
    return top_conditions_by_month.pivot(index='Month', columns='Weather_Condition', values='Count').fillna(0)

# QUESTION 8
# What was the max visibility of all accidents of severity 2 that occurred in the state of New Hampshire?
def max_visibility_severity_2_nh(df):
    # FILTER FOR NH + VIS 2
    nh_severity_2 = df[(df['State'] == 'NH') & (df['Severity'] == 2)].copy()

    # CONVERT TO NUMERIC + ERROR HANDLING
    nh_severity_2.loc[:, 'Visibility(mi)'] = pd.to_numeric(nh_severity_2['Visibility(mi)'], errors='coerce')

    # FIND MAX VISIBILITY
    max_visibility = nh_severity_2['Visibility(mi)'].max()

    # RETURN VIS FOUND
    return max_visibility
    
# Question 9
# How many accidents of each severity were recorded in Bakersfield?
def bk(df):

    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['Year'] = df['Start_Time'].dt.year

    filtered_df = df[df['City'] == 'Bakersfield'].copy()

    group = filtered_df.groupby(['Year', 'Severity']).size()

    group_df = group.reset_index(name='Count')

    group_df = group_df.sort_values(by=['Year', 'Severity'], ascending=[True, False])
    result = group_df.drop_duplicates(subset='Year', keep='first').sort_values(by='Year')

    return result
  
# Question 10
# What was the longest accident(in hours) recorded in Las Vegas in the Spring 
# (March, April, and May)?
def ten(df): 

    df['Start_Time'] = pd.to_datetime(df['Start_Time']) 
    df['Month'] = df['Start_Time'].dt.month 
    df['Year'] = df['Start_Time'].dt.year 
    df['Duration (min)'] = df['Start_Time'].dt.minute; 

    spring_df = df[df['Month'].isin([3,4,5])] 
    vegas_accidents = spring_df[spring_df['City'] == 'Las Vegas'].copy() 
    max_df = vegas_accidents.groupby('Year')['Duration (min)'].max() / 60 

    return max_df 
  
##########################################
#                                        #
#       END print_answer FUNCTIONS       #
#                                        #
##########################################
valid_states = {"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"}

# SEARCH CAPACITY
def search_accidents(df, choice):
    month_mapping = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }

    if choice == '4':
        start_time = time.time()
        accident_count = search4(df)
        end_time = time.time()

        if accident_count == 0:
            print("There were no accidents found.")
        else:
            print(f"There were {accident_count} accidents found.") 
        print("Time to perform search is: ", end_time - start_time)

    elif choice == '5':
        while True:
            year = input("Enter a Year (leave blank to include all years): ").strip()
            try:
                if year:
                    year = int(year)
                    if year <= 0:
                        raise ValueError("Year must be a positive integer.")
                    break
                else:
                    year = None
                    break
            except ValueError:
                print("Invalid year entry. Please enter a valid positive integer or leave blank.")

        while True:
            month = input("Enter a Month name or number (leave blank to include all months): ").strip().lower()
            try:
                if month.isdigit():
                    month = int(month)
                    if not 1 <= month <= 12:
                        raise ValueError("Month must be between 1 and 12.")
                    break
                elif month in month_mapping:
                    month = month_mapping[month]
                    break
                elif month == "":
                    month = None
                    break
                else:
                    raise ValueError("Invalid month entry. Please enter a valid month name or number.")
            except ValueError:
                print("Invalid month entry. Please enter a valid month name or number.")

        while True:
            day = input("Enter a Day (leave blank to include all days): ").strip()
            try:
                if day:
                    day = int(day)
                    if not 1 <= day <= 31:
                        raise ValueError("Day must be between 1 and 31.")
                    break
                else:
                    day = None
                    break
            except ValueError:
                print("Invalid day entry. Please enter a valid day between 1 and 31 or leave blank.")

        accidents_count = search_accidents_by_date(df, year=year, month=month, day=day)
        print(f"There are {accidents_count} accidents matching your criteria.")


    elif choice == '6':
        while True:
            try:
                min_temp = input("Enter a Minimum Temperature (F) (leave blank for no minimum): ").strip()
                min_temp = float(min_temp) if min_temp else None
                break
            except ValueError:
                print("Invalid entry for minimum temperature. Please enter a numeric value or leave blank.")

        while True:
            try:
                max_temp = input("Enter a Maximum Temperature (F) (leave blank for no maximum): ").strip()
                max_temp = float(max_temp) if max_temp else None
                break
            except ValueError:
                print("Invalid entry for maximum temperature. Please enter a numeric value or leave blank.")

        while True:
            try:
                min_vis = input("Enter a Minimum Visibility (mi) (leave blank for no minimum): ").strip()
                min_vis = float(min_vis) if min_vis else None
                if min_vis is not None and min_vis < 0:
                    raise ValueError("Visibility cannot be negative.")
                break
            except ValueError:
                print("Invalid entry for minimum visibility. Please enter a non-negative numeric value or leave blank.")

        while True:
            try:
                max_vis = input("Enter a Maximum Visibility (mi) (leave blank for no maximum): ").strip()
                max_vis = float(max_vis) if max_vis else None
                if max_vis is not None and max_vis < 0:
                    raise ValueError("Visibility cannot be negative.")
                break
            except ValueError:
                print("Invalid entry for maximum visibility. Please enter a non-negative numeric value or leave blank.")

        accidents_count = search_accidents_by_temp_vis(df, min_temp, max_temp, min_vis, max_vis)
        print(f"There are {accidents_count} accidents matching your temperature and visibility criteria.")


def valid_state(state):
    return state in valid_states or state == ""

def valid_city(city, df):
    # Assuming df['City'] contains all valid city names
    normalized_cities = df['City'].dropna().unique()
    return city.title() in normalized_cities

def valid_zip(zip_code):
    return zip_code.isdigit() and len(zip_code) == 5

# SEARCH (4) CAPACITY
def search4(df):
    state = ""
    city = ""
    zip_code = ""
    filtered_df = df

    while True:
        state = input("Enter the state (leave blank to search all states): ").upper()
        if valid_state(state):
            break
        else:
            print("ERROR: Invalid state. Please enter a valid 2-letter state abbreviation or leave blank.")

    while True:
        city = input("Enter the city (leave blank to search all cities): ")
        if city == "" or valid_city(city, df):
            break
        else:
            print("ERROR: City not recognized. Please enter a valid city name or leave blank.")

    while True:
        zip_code = input("Enter the zipcode (leave blank to search all zipcodes): ")
        if zip_code == "" or valid_zip(zip_code):
            break
        else:
            print("ERROR: Invalid zipcode. Please enter exactly 5 digits or leave blank.")
    
    if state:
        filtered_df = filtered_df[filtered_df["State"] == state]
    if city:
        filtered_df = filtered_df[filtered_df["City"] == city.title()]
    if zip_code:
        filtered_df = filtered_df[filtered_df["Zipcode"] == zip_code]

    results = len(filtered_df)
    return results
    
# menu 5 and 6
def search_accidents_by_date(df, year=None, month=None, day=None):
    filtered_data = df
    if year is not None:
        filtered_data = filtered_data[filtered_data['Start_Time'].dt.year == year]
    if month is not None:
        filtered_data = filtered_data[filtered_data['Start_Time'].dt.month == month]
    if day is not None:
        filtered_data = filtered_data[filtered_data['Start_Time'].dt.day == day]
    return len(filtered_data)

def search_accidents_by_temp_vis(df, min_temp='', max_temp='', min_vis='', max_vis=''):
    filtered_data = df
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

        while True:  # CONTINUOUS LOOP FOR PROMPT INPUT
            choice = input("Select an option: ")
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                break  # BREAK IF VALID
            else:
                print("Invalid option. Please select a valid number from 1 to 7.")

        if choice == '1':
            df, load_time = load_data()
            if df is not None:  
                total_time += load_time
        elif choice in ['2', '3', '4', '5', '6']:
            if df is None:
                print("\nPlease load the data first before selecting this option.")
                time.sleep(2)  # BRIEF PAUSE
            else:
                if choice == '2':
                    df, process_time = clean_data(df)
                    total_time += process_time
                elif choice == '3':
                    print_answers(df)
                elif choice in ['4', '5', '6']:
                    search_accidents(df, choice)
        elif choice == '7':
            print(f"Total Running Time (In Minutes): {total_time / 60:.2f}")
            print("Exiting the program.")
            running = False

if __name__ == "__main__":
    main()
