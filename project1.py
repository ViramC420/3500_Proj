import pandas as pd

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


