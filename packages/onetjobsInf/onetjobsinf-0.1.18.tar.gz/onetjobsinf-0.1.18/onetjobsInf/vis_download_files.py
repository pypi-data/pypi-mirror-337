# This code is for downloading a text file from the O*NET website without the API
import requests
import pandas as pd

def download_occups(local_filename='onetjobsInf/src_data/Occupation Data.txt'):
    # Send a GET request to the URL
    url = 'https://www.onetcenter.org/dl_files/database/db_25_1_text/Occupation Data.txt'
    response = requests.get(url, stream=True)
    print(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open the local file in write-binary mode
        with open(local_filename, 'wb') as f:
            # Write the content of the response to the local file
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File downloaded successfully: {local_filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

if __name__ == "__main__":
    download_occups()

def download_txtfile_aspd(url):
    # Send a GET request to the URL
    response = requests.get(url, stream=True)
    print(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Read the content of the response into a pandas DataFrame
        df = pd.read_csv(response.raw, delimiter='\t', encoding='utf-8')
        print(f"File downloaded and read into DataFrame successfully")
        
        # Select only the 'Element Name' and 'Element ID' columns
        df = df[['O*NET-SOC Code', 'Element Name', 'Element ID', 'Scale ID', 'Data Value', 'Lower CI Bound', 'Upper CI Bound']]
        
        return df
        
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return None

