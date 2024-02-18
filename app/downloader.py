#downloader.py
import requests

# Function for fetching data from the URL
def fetch_json_feed(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        # Check if the response was successful
        # If not, raise an HTTPError exception
        response.raise_for_status()
        # If the request was successful, parse the response as JSON
        # and return the parsed data
        return response.json()
    except requests.RequestException as e:
        # catch the exception
        print(f"Error fetching JSON feed: {e}")
        # Return None if the fetch was unsuccessful
        return None
