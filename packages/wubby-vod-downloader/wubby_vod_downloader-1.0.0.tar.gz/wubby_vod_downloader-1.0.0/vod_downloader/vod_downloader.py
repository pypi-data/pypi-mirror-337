# vod_downloader/vod_downloader.py

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm  # Import tqdm

# Base URL of the VOD archive
base_url = "https://archive.wubby.tv/vods/public/"

# Function to get the list of months sorted by timestamp
def get_sorted_months():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all directories (these are links to the month folders)
    month_links = []
    for row in soup.find_all('tr'):
        link = row.find('a', href=True)
        if link and 'title' in link.attrs:
            timestamp = row.find_all('td')[2].text.strip()
            if timestamp:
                # Parse the timestamp into a datetime object
                try:
                    timestamp = datetime.strptime(timestamp, "%Y-%b-%d %H:%M")
                    month_links.append((link['title'], timestamp))
                except ValueError:
                    continue  # Skip any entries that don't have a valid timestamp
    # Sort months by timestamp (descending order)
    sorted_months = sorted(month_links, key=lambda x: x[1], reverse=True)
    
    return sorted_months

# Function to get and sort VODs by timestamp within a month folder
def get_sorted_vods(month_folder):
    month_url = base_url + month_folder + "/"
    response = requests.get(month_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all VOD links and their timestamps
    vod_links = []
    for row in soup.find_all('tr'):
        link = row.find('a', href=True)
        if link and link['href'].endswith('.mp4'):
            # Get the VOD timestamp (the date part) for sorting
            timestamp = row.find_all('td')[2].text.strip()
            if timestamp:
                try:
                    timestamp = datetime.strptime(timestamp, "%Y-%b-%d %H:%M")
                    vod_links.append((link['href'], timestamp))
                except ValueError:
                    continue  # Skip any entries that don't have a valid timestamp

    # Sort VODs by timestamp (descending order)
    sorted_vods = sorted(vod_links, key=lambda x: x[1], reverse=True)
    
    return sorted_vods

# Function to download VODs from the most recent month
def download_vods(month_folder, count=5):
    sorted_vods = get_sorted_vods(month_folder)

    if not sorted_vods:
        print(f"No VODs found in the month folder: {month_folder}")
        return

    # Create a folder for the downloads if it doesn't exist
    download_folder = 'vod_downloads'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Initialize a progress bar with `tqdm`
    for i, (vod_link, _) in enumerate(tqdm(sorted_vods[:count], desc="Downloading VODs", unit="VOD", dynamic_ncols=True)):
        vod_url = base_url + month_folder + "/" + vod_link
        vod_filename = os.path.join(download_folder, vod_link.split('/')[-1])

        # Check if the VOD has already been downloaded
        if os.path.exists(vod_filename):
            print(f"Skipping {vod_filename}, already downloaded.")
            continue  # Skip this VOD if it already exists

        print(f"Downloading VOD {i+1}: {vod_url}")
        response = requests.get(vod_url, stream=True)
        
        # Save the VOD to a file with progress
        with open(vod_filename, 'wb') as f:
            total_length = int(response.headers.get('content-length', 0))
            if total_length == 0:
                f.write(response.content)
            else:
                for chunk in tqdm(response.iter_content(chunk_size=8192), total=total_length // 8192, unit='B', unit_scale=True, leave=False):
                    f.write(chunk)
        print(f"Downloaded {vod_filename}")

# Get sorted months based on timestamp
sorted_months = get_sorted_months()

# If we found any months, proceed with downloading from the most recent one
if sorted_months:
    most_recent_month = sorted_months[0][0]  # Get the folder name of the most recent month
    print(f"Most recent month: {most_recent_month}")
    download_vods(most_recent_month, count=5)
else:
    print("No VOD directories found.")
