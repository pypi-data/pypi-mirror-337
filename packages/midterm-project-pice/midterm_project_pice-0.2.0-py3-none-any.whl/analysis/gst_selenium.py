from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random

# Configure Chrome options
options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": os.path.expanduser("~/Downloads"),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Add user agent to appear more like a regular browser
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# Implement retry logic with exponential backoff
max_retries = 3
retry_count = 0
backoff_time = 5  # Start with 5 seconds

while retry_count < max_retries:
    try:
        # Initialize driver
        print(f"Starting Chrome... (Attempt {retry_count + 1}/{max_retries})")
        service = Service("/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        
        # Add random delays to simulate human behavior
        time.sleep(random.uniform(1, 3))
        
        # Open the Google Trends page
        print("Opening Google Trends page...")
        url = "https://trends.google.com/trends/explore?geo=US&q=Sneeze,Vomiting,Sore%20throat,Headache,%22pregnant%22"
        driver.get(url)
        
        # Wait for page to load completely with random delay
        wait_time = random.uniform(8, 12)
        print(f"Waiting {wait_time:.1f} seconds for page to load...")
        time.sleep(wait_time)
        
        # Check for 429 error
        if "429" in driver.page_source or "too many requests" in driver.page_source.lower():
            raise Exception("Received 429 error - Too Many Requests")
            
        # Check if CAPTCHA appears and wait for manual intervention
        print("CHECKING FOR CAPTCHA: If a CAPTCHA appears, please solve it manually now.")
        print("The script will wait for you to complete it.")
        captcha_input = input("Press Enter after solving the CAPTCHA (or type 'skip' to continue without waiting): ")

        if captcha_input.lower() != 'skip':
            # Give additional time to finish CAPTCHA if needed
            print("Continuing after CAPTCHA...")
            time.sleep(3)
        
        # Success - break out of retry loop
        break
        
    except Exception as e:
        print(f"Error: {e}")
        retry_count += 1
        
        if retry_count < max_retries:
            # Exponential backoff
            wait_time = backoff_time * (2 ** (retry_count - 1)) + random.uniform(1, 5)
            print(f"Retrying in {wait_time:.1f} seconds...")
            time.sleep(wait_time)
            
            # Close driver before retrying
            try:
                driver.quit()
            except:
                pass
        else:
            print("Maximum retry attempts reached. Exiting.")
            
if retry_count < max_retries:
    try:
        # Continue with the rest of your script
        print(f"Page title: {driver.title}")
        
        # Try multiple methods to find download buttons
        print("Looking for download buttons...")
        # Remainder of your script...
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Always quit the driver
        print("Closing Chrome...")
        driver.quit()