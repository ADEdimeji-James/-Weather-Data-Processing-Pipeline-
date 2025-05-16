import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
sns.set() # this overrides the matplotlib library for improving visualizations




### Pipeline 1: Data Ingestion

# declare a function that loads the dataset 
def load_dataset(file_name): 
    """
    Loads a CSV file into a pandas DataFrame.

    Parameters:
        file_path (a string): The name or path of the CSV file to load.

    Returns:
        DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(file_name)




### Pipeline 2: Data CLeaning and Transformation 

def clean_weather_data(df):
    """
    Cleans and transforms a weather DataFrame.

    Steps performed:
    1. Fill missing temperature, humidity, and wind speed values with the city's average.
    2. Drop rows with missing date or weather_condition column.
    3. Parse inconsistent date formats into a standard datetime format.
    4. Create a new column for temperature in Fahrenheit.
    5. Standardize the weather_condition column by stripping whitespace and capitalizing values.
    6. Remove rows where weather_condition is 'Unknown'.

    Parameters:
        df (pd.DataFrame): Raw weather data.

    Returns:
        pd.DataFrame: Cleaned and transformed weather data.
    """

    # 1. Fill missing values in each column with the mean of the the city's temperature  
    df['temperature_celsius'] = df.groupby('city')['temperature_celsius'].transform(lambda x: x.fillna(round(x.mean()))) # for temperature 
    df['humidity_percent'] = df.groupby('city')['humidity_percent'].transform(lambda x: x.fillna(round(x.mean())))       # for humidity 
    df['wind_speed_kph'] = df.groupby('city')['wind_speed_kph'].transform(lambda x: x.fillna(round(x.mean())))         # for wind speed 

    # 2. Drop rows where 'date' or 'weather_condition' is missing
    df = df.dropna(subset=['date', 'weather_condition'])          # drops missing values in the mentioned column

    # 3. Fix mixed date formats using a custom parser
    def custom_date_parser(date):
        """Attempts to parse a date string using multiple formats."""
        for fmt in ("%d-%m-%Y", "%d.%m.%Y", "%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%m.%d.%Y", "%Y.%m.%d", "%Y/%m/%d"):
            try:
                return pd.to_datetime(date, format=fmt) 
            except ValueError:
                continue
        return pd.NaT  # Return NaT (Not a Time) if no format matches

    # Apply custom parser
    df['date'] = df['date'].apply(custom_date_parser)

    # 4. Create a new column: temperature in Fahrenheit
    df['temperature_fahrenheit'] = df['temperature_celsius'] * 9 / 5 + 32

    # 5. Clean and standardize weather_condition strings
    def convert_to_string_and_capitalize(data):
        return str(data).strip().title()          # strip() to remove whitespaces and title() for capitalization

    # Apply the function 
    df['weather_condition'] = df['weather_condition'].apply(convert_to_string_and_capitalize)

    # 6. Remove rows where weather condition is 'Unknown'
    df = df[df['weather_condition'] != 'Unknown']

    return df




### Pipeline 3: Data Output 

import os

def save_data_and_generate_report(df, csv_filename='transformed_weather_data.csv', 
                                  report_filename='top_5_hottest_cities.txt', folder='outputs'):
    """
    Saves the cleaned DataFrame as a CSV file and generates a text report listing
    the top 5 cities with the highest average temperature in Celsius.

    This function does the following:
    1. Creates the output folder if it doesn't exist.
    2. Saves the DataFrame as a CSV file inside the output folder.
    3. Generates a text report listing the top 5 hottest cities and saves it in the same folder.

    Parameters:
        df (pd.DataFrame): The cleaned and transformed DataFrame.
        csv_filename (string): The name of the CSV file to save. Default is 'transformed_weather_data.csv'.
        report_filename (string): The name of the text report file. Default is 'top_5_hottest_cities.txt'.
        folder (string): The folder where files should be saved. Default is 'outputs'.

    Returns:
        tuple: Paths of the saved CSV file and the text report file.
    """

    # Create the output folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Build full file paths
    csv_path = os.path.join(folder, csv_filename)
    report_path = os.path.join(folder, report_filename)

    # Save DataFrame as CSV without the index
    df.to_csv(csv_path, index=False)

    # Calculate top 5 cities with highest average temperature
    avg_temp = df.groupby('city')['temperature_celsius'].mean().sort_values(ascending=False).head(5)

    # Write the report to a text file
    with open(report_path, 'w', encoding='utf-8') as file:                      #  opens a file for writing
        file.write("Top 5 Cities with Highest Average Temperature (°C):\n\n")   # This writes a header at the top of the file.
        for city, temp in avg_temp.items():                                     #  loops through each city and its average temperature
            file.write(f"{city}: {temp:.2f}°C\n")

    print(f"CSV data saved to: {csv_path}")
    print(f"Temperature report saved to: {report_path}")

    return csv_path, report_path




### Pipeline 4: Bar charts using matplotlib (bonus) 

def create_avg_temperature_chart(df, output_path='outputs/avg_temperature_per_city.png'):
    """
    Generates and saves a horizontal bar chart showing the average temperature per city.

    Parameters:
        df (pd.DataFrame): The cleaned weather DataFrame containing 'city' and 'temperature_celsius'.
        output_path (str): The file path (including filename) where the chart image will be saved.

    Returns:
        str: The full path to the saved chart image.
    """

    # Group by city and calculate average temperature
    avg_temp = df.groupby('city')['temperature_celsius'].mean().sort_values(ascending=True)

    # Confirm the output directory exists
    folder = os.path.dirname(output_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    # Create the bar chart
    plt.figure(figsize=(10, 6))                            # Set the figure size
    avg_temp.plot(kind='barh', color='skyblue')            # Create a horizontal bar chart  
    plt.title('Average Temperature per City (Celcius)')    # title of the bar chart
    plt.xlabel('Temperature (Celcius)')                    # label of the x-axis
    plt.ylabel('City')                                     # label of the y-axis
    plt.tight_layout()

    # Save the chart to the output folder 
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Chart saved to: {output_path}")
    return output_path







