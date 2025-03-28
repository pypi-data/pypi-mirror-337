import pandas as pd
from pytrends.request import TrendReq
import time
import random
from datetime import datetime
import argparse
import os
import shutil
from typing import Optional

def get_trends_data(keywords, retries=3, timeframe='2023-06-01 2024-05-31', geo='US'):
    """Get Google Trends data with retries and error handling"""
    pytrend = TrendReq(hl='en-US', tz=360)
    
    for attempt in range(retries):
        try:
            # Longer initial delay
            base_delay = random.uniform(10.0, 15.0)
            time.sleep(base_delay)
            
            pytrend.build_payload(keywords, 
                                timeframe=timeframe,
                                geo=geo,
                                gprop='')
            
            data = pytrend.interest_over_time()
            if data is not None and not data.empty:
                return data
            
        except Exception as e:
            wait_time = base_delay * (attempt + 1)
            print(f"Attempt {attempt + 1} failed: {e}. Waiting {wait_time:.1f} seconds...")
            time.sleep(wait_time)
    
    print(f"Failed to get data after {retries} attempts")
    return pd.DataFrame()

def get_trends_in_batches(keywords, batch_size=3, retries=3, timeframe='2023-06-01 2024-05-31', geo='US'):
    """Process keywords in batches to avoid rate limits"""
    # Use keywords as-is without removing duplicates
    print(f"Processing {len(keywords)} keywords in batches of {batch_size}")
    
    all_data = []
    
    # Process in batches
    for i in range(0, len(keywords), batch_size):
        batch = keywords[i:i+batch_size]
        print(f"\nBatch {i//batch_size + 1}/{(len(keywords)-1)//batch_size + 1}: {batch}")
        
        try:
            # Add longer delay between batches
            wait_time = random.uniform(15.0, 20.0)
            print(f"Waiting {wait_time:.1f} seconds before processing batch...")
            time.sleep(wait_time)
            
            batch_data = get_trends_data(batch, retries=retries, timeframe=timeframe, geo=geo)
            
            if not batch_data.empty:
                all_data.append(batch_data)
                print("Batch processed successfully")
            
        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {str(e)}")
    
    # Combine all data
    if all_data:
        final_data = pd.concat(all_data, axis=1)
        final_data = final_data.loc[:,~final_data.columns.duplicated()]
        return final_data
    return pd.DataFrame()

def ensure_data_folder():
    """Create data folder if it doesn't exist"""
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"Created directory: {data_folder}")
    return data_folder

def clean_trends_data(input_file: str, output_file: Optional[str] = None) -> pd.DataFrame:
    """
    Clean Google Trends data by:
    1. Removing rows where is_partial = True
    2. Removing the "soccer" column
    3. Removing the "isPartial" column
    4. Change the date column to Week
    
    Parameters:
    input_file (str): Path to input CSV file
    output_file (str, optional): Path to output CSV file. If None, will create a file with "cleaned_" prefix
    
    Returns:
    pd.DataFrame: Cleaned data
    """
    # Set default output filename if not provided
    if output_file is None:
        file_dir = os.path.dirname(input_file) if os.path.dirname(input_file) else "."
        file_name = os.path.basename(input_file)
        output_file = os.path.join(file_dir, f"cleaned_{file_name}")
    
    # Read the CSV file
    print(f"Reading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Print original shape
    original_shape = df.shape
    print(f"Original data shape: {original_shape}")
    
    # Handle isPartial column
    if 'isPartial' in df.columns:
        # Filter rows where isPartial is True
        df = df[~df['isPartial']]
        # Then remove the isPartial column
        df = df.drop(columns=['isPartial'])
        print("Removed isPartial column")
    
    # Remove the "soccer" column
    if 'soccer' in df.columns:
        df = df.drop(columns=['soccer'])
        print("Removed soccer column")

    if 'date' in df.columns:
        df = df.rename(columns={'date': 'Week'})
        print("Renamed date column to Week")
    
    # Print new shape
    print(f"Cleaned data shape: {df.shape}")
    
    # Save to new CSV file
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
    
    return df

def get_year_data(year):
    """Get data for specified year, first trying to collect from PyTrends API,
    and falling back to existing data files if API collection fails"""
    
    # Ensure data folder exists
    data_folder = ensure_data_folder()
    
    # Define symptom keywords
    keywords = [
        "soccer", "Cough", "Sore Throat", 
        "soccer", "Headache", "Chills",
        "soccer", "Nausea", "Vomiting",
        "soccer", "Diarrhea", "Fatigue"
    ]
    
    # Set timeframe based on specified year
    if year == 2023:
        # For current year, use 'today 12-m'
        timeframe = '2023-06-01 2024-05-31'
        year_suffix = f"{str(year-2000)}_{str(year-1999)}"  # e.g., "23_24"
    else:
        # For specific past years, use date range format
        timeframe = f'{year}-06-01 {year+1}-5-31'
        year_suffix = f"{str(year-2000)}_{str(year-1999)}"  # e.g., "20_21"
    
    print(f"Processing data for year: {year}")
    print(f"Using timeframe: {timeframe}")
    
    # Define the output file in the data folder
    pytrends_data_file = os.path.join(data_folder, "pytrends_data.csv")
    cleaned_output_file = os.path.join(data_folder, "cleaned_pytrends_data.csv")
    
    # FIRST ATTEMPT: Try to collect data from PyTrends API
    print("\n1. ATTEMPTING TO COLLECT DATA FROM GOOGLE TRENDS API...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get the data
    trends_data = get_trends_in_batches(keywords, timeframe=timeframe)
    
    # Check if data collection was successful
    if not trends_data.empty:
        print("Successfully collected data from Google Trends API.")
        # Save to data folder
        trends_data.to_csv(pytrends_data_file)
        print(f"Data saved to {pytrends_data_file}")
        
        # Clean the collected data
        print("\nCleaning the collected data...")
        cleaned_data = clean_trends_data(pytrends_data_file, cleaned_output_file)
        return cleaned_data
    
    # FALLBACK: If PyTrends collection failed, use existing data
    print("\n2. GOOGLE TRENDS API DATA COLLECTION FAILED.")
    print(f"Attempting to use existing data from data_from_gst_website folder for year {year}...")
    
   # Assume the script is in src/analysis/ — go up to src/ and into data_from_gst_website
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data_from_gst_website")
    data_dir = os.path.abspath(data_dir)  # Normalize path

    # Now you can construct file paths relative to data_dir
    filepath = os.path.join(data_dir, f"df_{year_suffix}.csv")
    
    
    print(f"Looking for file: {filepath}")
    
    if os.path.exists(filepath):
        print(f"Found existing data file: {filepath}")
        
        # Copy file to data folder and rename as pytrends_data.csv
        shutil.copy2(filepath, pytrends_data_file)
        print(f"Copied {filepath} to {pytrends_data_file}")
        
        # Clean the copied data
        print("\nCleaning the existing data...")
        cleaned_data = clean_trends_data(pytrends_data_file, cleaned_output_file)

        return cleaned_data
    

    else:
        print(f"Error: No data file found for year {year}. Looked for: {filepath}")
        return None
def main(year=None):
    """
    Main logic of gst_pytrends.
    If `year` is provided, it will override the command-line argument.
    """
    # If no year is provided, use the current year
    if year is None:
        # Set up command-line argument parsing
        parser = argparse.ArgumentParser(description='Collect and clean Google Trends data for symptom keywords')
        parser.add_argument('--year', type=int, default=2023,
                            help='Specify which year to collect data for (e.g., 2020, 2021, 2022, 2023)')
        args = parser.parse_args()
        year = args.year

        # Validate the year
        valid_years = [2020, 2021, 2022, 2023]
        if year not in valid_years:
            raise ValueError(f"Invalid year: {year}. Please specify one of the following years: {valid_years}")


    

    # Get and clean data for the specified year
    cleaned_data = get_year_data(year)

    if cleaned_data is not None:
        print("\nFinal data processing successful!")
        print("Preview of final cleaned data:")
        print(cleaned_data.head())
    else:
        print("\nFAILED: Could not obtain data for the specified year.")
        exit(1)


if __name__ == "__main__":
    # Call the main function without arguments for command-line execution
    main()