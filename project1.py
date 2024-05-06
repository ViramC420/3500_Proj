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

#print statement sections 
#needs to be updated to py prints 
# Menu drop down 
1 = "Load data \n" 
2 = "Process data \n"
3 = "Print Answers \n"
4 = "Search Accidents (Use City, State, and Zip Code)\n"
5 = "Search Accidents (Year, Month and Day) \n"
6 = "Search Accidents (Temperature Range and Visibility Range) \n"
7 = "Quit \n"


if 1 
"Loading and cleaning input data set: \n"
"*********************************** \n"
[cur time] "Starting Script \n"
[cur time] "Loading US_Acidents.csv \n"
[cur time] "Total Columns Read: [ans] \n"
[cur time] "Total Rows Read: [ans] \n\n"
"Time to load is: " [ans] " \n"


If 2
"Processing input data set: \n"
"************************** \n"
[cur time] " Performing Data Clean Up \n"
[cur time] " Total Rows Read after cleaning is: " [ans] "\n"

"Time to process is: " [ans] "\n"


If 3
"Answering questions: \n"
"******************** \n"
[cur time] " In what month were there more accidents reported? \n" 
[cur time] [ans] "\n"
[cur time] " What was the longest accident (in hours) recorded in Florida in the Spring (March, April, and May) of 2020? \n"
[curtime] [ans] "\n"


If 4
"Search Accidents: \n"
"***************** \n"
"Enter a State name: " <User Input> "\n"
"Enter a City name: " <User Input> "\n"
"Enter a ZIP Code: " <User Input> "\n"
"There where " <User Input> " accidents. \n"
"Time to perform search is: " [ans] "\n" 


If 5
"Search Accidents: \n"
"***************** \n"
"Enter a Year: "<User Input> "\n"
"Enter a Month name: "<User Input> "\n"
"Enter a Day: "<User Input> "\n"
"There where "<User Input> "accidents. \n"
"Time to perform search is: " [ans] "\n"


If 6
"Search Accidents: \n"
"***************** \n"
"Enter a Minimum Temperature (F): " <User Input> "\n"
"Enter a Maximum Temperature (F): " <User Input> "\n"
"Enter a Minimum Visibility (mi): " <User Input> "\n"
"Enter a Maximum Visibility (mi): " <User Input> \n"
"There where " <User Input> " accidents. \n"
"Time to perform search is: " [ans] "\n"


If 7
"Total Running Time (In Minutes): " [ans] "\n"




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

# Question 10 
def ten(df): 

    df['Start_Time'] = pd.to_datetime(df['Start_Time']) 
    df['Month'] = df['Start_Time'].dt.month 
    df['Year'] = df['Start_Time'].dt.year 
    df['Duration (min)'] = df['Start_Time'].dt.minute; 

    spring_df = df[df['Month'].isin([3,4,5])] 
    vegas_accidents = spring_df[spring_df['City'] == 'Las Vegas'].copy() 
    max_df = vegas_accidents.groupby('Year')['Duration (min)'].max() / 60 

    return max_df  


